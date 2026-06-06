"""
# 🌿 Plant Disease Prediction System — Training Script
# Fixed for:
#   - RTX 3050 Laptop GPU (CUDA)
#   - Species label remapping bug
#   - PyTorch 2.3 deprecation warnings

# Run:
#     python train.py --mode export    ← export disease model (already trained)
#     python train.py --mode species   ← train species model
#     python train.py --mode all       ← train both + export
# """

import argparse
import json
import os
import time
import shutil
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torch.amp import GradScaler, autocast          # ← fixed deprecation
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import DataLoader, Dataset, random_split
from torchvision import datasets, models, transforms
from sklearn.metrics import classification_report

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════

DATASET_ROOT = Path(r"C:\Users\anees\OneDrive\Desktop\PlantVillageDataset\plantvillage dataset")

def resolve_data_dir(root):
    for sub in ["color", "train", "Color", "Train"]:
        c = root / sub
        if c.exists() and any(c.iterdir()):
            return c
    return root

DATA_DIR        = resolve_data_dir(DATASET_ROOT)
BASE_DIR        = Path(__file__).parent
MODELS_DIR      = BASE_DIR / "models"
CHECKPOINTS_DIR = BASE_DIR / "models" / "checkpoints"
BACKEND_MODELS  = BASE_DIR.parent / "backend" / "models"

for d in [MODELS_DIR, CHECKPOINTS_DIR, BACKEND_MODELS]:
    d.mkdir(parents=True, exist_ok=True)

IMAGE_SIZE  = 300
BATCH_SIZE  = 16
NUM_WORKERS = 4
EPOCHS      = 25
LR          = 1e-4
DEVICE      = torch.device("cuda" if torch.cuda.is_available() else "cpu")
USE_AMP     = DEVICE.type == "cuda"

print("=" * 62)
print("🌿 Plant Disease Prediction System — Training Script")
print("=" * 62)
print(f"  Device     : {DEVICE}")
if DEVICE.type == "cuda":
    print(f"  GPU        : {torch.cuda.get_device_name(0)}")
    print(f"  VRAM       : {torch.cuda.get_device_properties(0).total_memory/1e9:.1f} GB")
    print(f"  Mixed Prec : Enabled ✅")
else:
    print("  ⚠️  Running on CPU — GPU not detected!")
    print("  Check: pip install torch --index-url https://download.pytorch.org/whl/cu128")
print(f"  Dataset    : {DATA_DIR}")
print(f"  Batch size : {BATCH_SIZE}")
print("=" * 62)


# ══════════════════════════════════════════════════════════════════════════════
# TRANSFORMS
# ══════════════════════════════════════════════════════════════════════════════

def get_transforms(train=True):
    mean = [0.485, 0.456, 0.406]
    std  = [0.229, 0.224, 0.225]
    if train:
        return transforms.Compose([
            transforms.RandomResizedCrop(IMAGE_SIZE, scale=(0.7, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.RandomRotation(30),
            transforms.ColorJitter(brightness=0.3, contrast=0.3,
                                   saturation=0.3, hue=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
            transforms.RandomErasing(p=0.2),
        ])
    else:
        return transforms.Compose([
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
        ])


# ══════════════════════════════════════════════════════════════════════════════
# SPECIES DATASET — fixed remapping
# ══════════════════════════════════════════════════════════════════════════════

class SpeciesDataset(Dataset):
    """
    Wraps PlantVillage ImageFolder but remaps labels to plant species only.
    e.g. Tomato___Early_blight (idx=30) → Tomato (idx=13)
    This fixes the 'Target 30 out of bounds' error.
    """
    def __init__(self, imagefolder_dataset, class_to_species_idx):
        self.dataset           = imagefolder_dataset
        self.class_to_species  = class_to_species_idx  # original_idx → species_idx

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        img, original_label = self.dataset[idx]
        species_label = self.class_to_species[original_label]
        return img, species_label


def load_disease_dataset():
    print(f"\n📂 Loading disease dataset: {DATA_DIR}")
    ds = datasets.ImageFolder(root=DATA_DIR, transform=get_transforms(True))
    print(f"   {len(ds.classes)} classes | {len(ds):,} images")

    # Save class mapping
    with open(MODELS_DIR / "disease_classes.json", "w") as f:
        json.dump(ds.class_to_idx, f, indent=2)

    return ds


def load_species_dataset():
    print(f"\n📂 Loading species dataset: {DATA_DIR}")

    # Load full disease dataset first
    base_ds = datasets.ImageFolder(root=DATA_DIR, transform=get_transforms(True))

    # Build species list from class folder names
    # e.g. "Tomato___Early_blight" → "Tomato"
    def get_plant(cls_name):
        return cls_name.split("___")[0].replace("_", " ").strip()

    plant_names = sorted(set(get_plant(c) for c in base_ds.classes))
    plant_to_idx = {name: i for i, name in enumerate(plant_names)}

    # Map original disease class index → species index
    class_to_species = {}
    for cls_name, orig_idx in base_ds.class_to_idx.items():
        plant = get_plant(cls_name)
        class_to_species[orig_idx] = plant_to_idx[plant]

    print(f"   {len(plant_names)} species: {plant_names}")
    print(f"   {len(base_ds):,} images")

    # Verify mapping is correct
    max_species_idx = max(class_to_species.values())
    print(f"   Species idx range: 0 → {max_species_idx} (num_classes={len(plant_names)})")
    assert max_species_idx == len(plant_names) - 1, "Mapping error!"

    # Save mapping
    with open(MODELS_DIR / "species_classes.json", "w") as f:
        json.dump(plant_to_idx, f, indent=2)
    print(f"   Mapping saved → {MODELS_DIR / 'species_classes.json'}")

    # Wrap in SpeciesDataset
    species_ds = SpeciesDataset(base_ds, class_to_species)
    species_ds.classes      = plant_names
    species_ds.class_to_idx = plant_to_idx

    return species_ds, len(plant_names)


# ══════════════════════════════════════════════════════════════════════════════
# MODEL
# ══════════════════════════════════════════════════════════════════════════════

def build_model(num_classes, freeze_backbone=True):
    model = models.efficientnet_b3(
        weights=models.EfficientNet_B3_Weights.IMAGENET1K_V1
    )
    if freeze_backbone:
        for p in model.features.parameters():
            p.requires_grad = False

    in_f = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.4, inplace=True),
        nn.Linear(in_f, 512),
        nn.ReLU(inplace=True),
        nn.Dropout(p=0.3),
        nn.Linear(512, num_classes),
    )
    return model.to(DEVICE)


# ══════════════════════════════════════════════════════════════════════════════
# TRAINING FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def train_one_epoch(model, loader, criterion, optimizer, scaler, ep, total):
    model.train()
    total_loss, correct, n = 0.0, 0, 0
    t0 = time.time()

    for i, (images, labels) in enumerate(loader):
        images = images.to(DEVICE, non_blocking=True)
        labels = labels.to(DEVICE, non_blocking=True)

        optimizer.zero_grad()

        with autocast(device_type=DEVICE.type, enabled=USE_AMP):   # ← fixed
            out  = model(images)
            loss = criterion(out, labels)

        scaler.scale(loss).backward()
        scaler.unscale_(optimizer)
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(optimizer)
        scaler.update()

        total_loss += loss.item() * images.size(0)
        correct    += out.argmax(1).eq(labels).sum().item()
        n          += labels.size(0)

        if (i + 1) % 10 == 0 or (i + 1) == len(loader):
            pct = (i + 1) / len(loader)
            bar = "█" * int(pct * 25) + "░" * (25 - int(pct * 25))
            eta = (time.time() - t0) / pct * (1 - pct)
            print(
                f"\r  Ep {ep:2d}/{total} [{bar}] "
                f"Loss:{total_loss/n:.3f} "
                f"Acc:{100.*correct/n:5.1f}% "
                f"ETA:{eta:4.0f}s",
                end="", flush=True
            )
    print()
    return total_loss / n, correct / n


@torch.no_grad()
def evaluate(model, loader, criterion):
    model.eval()
    total_loss, correct, n = 0.0, 0, 0
    all_preds, all_labels = [], []

    for images, labels in loader:
        images = images.to(DEVICE, non_blocking=True)
        labels = labels.to(DEVICE, non_blocking=True)

        with autocast(device_type=DEVICE.type, enabled=USE_AMP):
            out  = model(images)
            loss = criterion(out, labels)

        total_loss += loss.item() * images.size(0)
        preds       = out.argmax(1)
        correct    += preds.eq(labels).sum().item()
        n          += labels.size(0)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

    return total_loss / n, correct / n, all_preds, all_labels


# ══════════════════════════════════════════════════════════════════════════════
# FULL TRAINING PIPELINE
# ══════════════════════════════════════════════════════════════════════════════

def run_training(model_name, full_ds, num_classes, epochs=EPOCHS):
    print(f"\n{'='*62}")
    print(f"🧠  Training: {model_name.upper()} MODEL  ({num_classes} classes)")
    print(f"{'='*62}")

    # Split 80/10/10
    n       = len(full_ds)
    n_val   = int(0.1 * n)
    n_test  = int(0.1 * n)
    n_train = n - n_val - n_test

    train_ds, val_ds, test_ds = random_split(
        full_ds, [n_train, n_val, n_test],
        generator=torch.Generator().manual_seed(42)
    )
    print(f"   Train:{n_train:,} | Val:{n_val:,} | Test:{n_test:,}")

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,
                              num_workers=NUM_WORKERS, pin_memory=True,
                              persistent_workers=True)
    val_loader   = DataLoader(val_ds,   batch_size=BATCH_SIZE * 2,
                              num_workers=NUM_WORKERS, pin_memory=True,
                              persistent_workers=True)
    test_loader  = DataLoader(test_ds,  batch_size=BATCH_SIZE * 2,
                              num_workers=NUM_WORKERS, pin_memory=True,
                              persistent_workers=True)

    model     = build_model(num_classes, freeze_backbone=True)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    scaler    = GradScaler(device=DEVICE.type, enabled=USE_AMP)   # ← fixed

    best_ckpt    = CHECKPOINTS_DIR / f"best_{model_name}.pt"
    best_val_acc = 0.0
    history      = {"train_loss": [], "val_loss": [],
                    "train_acc":  [], "val_acc":  []}

    # ── Phase 1: Head only ─────────────────────────────────────
    P1 = max(5, epochs // 4)
    P2 = epochs - P1

    optimizer = optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LR * 10, weight_decay=1e-4
    )
    scheduler = CosineAnnealingLR(optimizer, T_max=P1, eta_min=1e-6)

    print(f"\n🚀 Phase 1 — Head only | {P1} epochs | backbone frozen")
    print("-" * 62)

    for ep in range(1, P1 + 1):
        tl, ta = train_one_epoch(model, train_loader, criterion, optimizer, scaler, ep, P1)
        vl, va, _, _ = evaluate(model, val_loader, criterion)
        scheduler.step()
        history["train_loss"].append(tl); history["train_acc"].append(ta)
        history["val_loss"].append(vl);   history["val_acc"].append(va)
        saved = ""
        if va > best_val_acc:
            best_val_acc = va
            torch.save(model.state_dict(), best_ckpt)
            saved = " ← 💾 saved"
        print(f"  → Val Acc: {va*100:.2f}%  Best: {best_val_acc*100:.2f}%{saved}")

    # ── Phase 2: Full fine-tune ────────────────────────────────
    for p in model.parameters():
        p.requires_grad = True

    optimizer = optim.AdamW([
        {"params": model.features.parameters(),   "lr": LR * 0.1},
        {"params": model.classifier.parameters(), "lr": LR},
    ], weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=P2, eta_min=1e-7)

    print(f"\n🔥 Phase 2 — Full fine-tune | {P2} epochs | all layers")
    print("-" * 62)

    for ep in range(1, P2 + 1):
        tl, ta = train_one_epoch(model, train_loader, criterion, optimizer, scaler, ep, P2)
        vl, va, _, _ = evaluate(model, val_loader, criterion)
        scheduler.step()
        history["train_loss"].append(tl); history["train_acc"].append(ta)
        history["val_loss"].append(vl);   history["val_acc"].append(va)
        saved = ""
        if va > best_val_acc:
            best_val_acc = va
            torch.save(model.state_dict(), best_ckpt)
            saved = " ← 💾 saved"
        print(f"  → Val Acc: {va*100:.2f}%  Best: {best_val_acc*100:.2f}%{saved}")

    # ── Test evaluation ────────────────────────────────────────
    model.load_state_dict(torch.load(best_ckpt, map_location=DEVICE))
    _, test_acc, preds, labels_list = evaluate(model, test_loader, criterion)
    print(f"\n🎯 Test Accuracy : {test_acc*100:.2f}%")
    print(f"   Best Val Acc  : {best_val_acc*100:.2f}%\n")
    print(classification_report(
        labels_list, preds,
        target_names=full_ds.classes, digits=3
    ))

    with open(MODELS_DIR / f"{model_name}_history.json", "w") as f:
        json.dump(history, f, indent=2)

    print(f"✅ {model_name} training complete!")
    return num_classes


# ══════════════════════════════════════════════════════════════════════════════
# ONNX EXPORT
# ══════════════════════════════════════════════════════════════════════════════

def export_onnx(model_name):
    print(f"\n📦 Exporting {model_name} → ONNX...")

    class_json = MODELS_DIR / f"{model_name}_classes.json"
    ckpt       = CHECKPOINTS_DIR / f"best_{model_name}.pt"

    if not ckpt.exists():
        print(f"❌ Checkpoint not found: {ckpt}")
        print(f"   Run: python train.py --mode {model_name}")
        return False

    if not class_json.exists():
        print(f"❌ Class mapping not found: {class_json}")
        return False

    with open(class_json) as f:
        num_classes = len(json.load(f))

    model = build_model(num_classes, freeze_backbone=False)
    model.load_state_dict(torch.load(ckpt, map_location=DEVICE))
    model.eval()

    dummy     = torch.randn(1, 3, IMAGE_SIZE, IMAGE_SIZE).to(DEVICE)
    onnx_path = MODELS_DIR / f"{model_name}_efficientnet_b3.onnx"

    torch.onnx.export(
        model, dummy, str(onnx_path),
        export_params=True, opset_version=17,
        do_constant_folding=True,
        input_names=["image"], output_names=["logits"],
        dynamic_axes={"image": {0: "batch"}, "logits": {0: "batch"}},
    )
    print(f"✅ ONNX exported: {onnx_name} ({onnx_path.stat().st_size/1e6:.1f} MB)")

    # Validate
    try:
        import onnxruntime as ort
        sess = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
        out  = sess.run(None, {"image": dummy.cpu().numpy()})[0]
        print(f"✅ Validated — output shape: {out.shape}  ✓")
    except Exception as e:
        print(f"⚠️  Validation skipped: {e}")

    # Copy to backend
    onnx_name = f"{model_name}_efficientnet_b3.onnx"
    shutil.copy2(onnx_path,  BACKEND_MODELS / onnx_name)
    shutil.copy2(class_json, BACKEND_MODELS / f"{model_name}_classes.json")
    print(f"✅ Copied to backend/models/ ✓")
    return True


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode",
                        choices=["disease", "species", "export", "all"],
                        default="all")
    parser.add_argument("--epochs", type=int, default=EPOCHS)
    args = parser.parse_args()

    if not DATA_DIR.exists():
        print(f"❌ Dataset not found: {DATA_DIR}")
        return

    if args.mode == "disease" or args.mode == "all":
        ds = load_disease_dataset()
        run_training("disease", ds, len(ds.classes), args.epochs)
        export_onnx("disease")

    if args.mode == "species" or args.mode == "all":
        ds, n = load_species_dataset()
        run_training("species", ds, n, args.epochs)
        export_onnx("species")

    if args.mode == "export":
        export_onnx("disease")
        export_onnx("species")

    if args.mode in ("disease", "species", "all"):
        print("\n" + "=" * 62)
        print("🎉 DONE! Next steps:")
        print("=" * 62)
        print("  1. cd ../backend")
        print("  2. venv\\Scripts\\activate")
        print("  3. uvicorn app.main:app --reload")
        print('  4. Should show: ✅ Models loaded (not demo mode)')
        print("=" * 62)


if __name__ == "__main__":
    main()