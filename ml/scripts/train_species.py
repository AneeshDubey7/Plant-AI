"""
train_species.py — Train EfficientNet-B3 for plant species identification.

Usage:
    python scripts/train_species.py --epochs 30 --batch-size 32

This script is structurally similar to train_disease.py but targets
the species classification task (14 plant species from PlantVillage).
The same two-phase training strategy is used:
  Phase 1: Freeze EfficientNet backbone, train head only
  Phase 2: Unfreeze all layers for end-to-end fine-tuning
"""

import argparse
import json
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, models, transforms
from sklearn.metrics import classification_report
import numpy as np

# ── Config ────────────────────────────────────────────────────────────────────

NUM_CLASSES    = 14          # Plant species count
IMAGE_SIZE     = 300
DATA_DIR       = Path("data/species")
MODELS_DIR     = Path("../backend/models")
CHECKPOINTS_DIR = Path("models/checkpoints")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_transforms(train: bool):
    if train:
        return transforms.Compose([
            transforms.RandomResizedCrop(IMAGE_SIZE, scale=(0.65, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(p=0.3),
            transforms.RandomRotation(45),
            transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.3, hue=0.15),
            transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.9, 1.1)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            transforms.RandomErasing(p=0.25, scale=(0.02, 0.15)),
        ])
    else:
        return transforms.Compose([
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])


def build_species_model(num_classes: int, freeze_backbone: bool = True) -> nn.Module:
    model = models.efficientnet_b3(weights=models.EfficientNet_B3_Weights.IMAGENET1K_V1)

    if freeze_backbone:
        for param in model.features.parameters():
            param.requires_grad = False

    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.4, inplace=True),
        nn.Linear(in_features, 256),
        nn.SiLU(inplace=True),
        nn.Dropout(p=0.2),
        nn.Linear(256, num_classes),
    )
    return model.to(DEVICE)


def train_epoch(model, loader, criterion, optimizer):
    model.train()
    total_loss, correct, total = 0.0, 0, 0
    for images, labels in loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        total_loss += loss.item() * images.size(0)
        correct += outputs.argmax(1).eq(labels).sum().item()
        total += labels.size(0)
    return total_loss / total, correct / total


@torch.no_grad()
def evaluate(model, loader, criterion):
    model.eval()
    total_loss, correct, total = 0.0, 0, 0
    preds_all, labels_all = [], []
    for images, labels in loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        outputs = model(images)
        total_loss += criterion(outputs, labels).item() * images.size(0)
        pred = outputs.argmax(1)
        correct += pred.eq(labels).sum().item()
        total += labels.size(0)
        preds_all.extend(pred.cpu().numpy())
        labels_all.extend(labels.cpu().numpy())
    return total_loss / total, correct / total, preds_all, labels_all


def export_onnx(model, path):
    model.eval()
    dummy = torch.randn(1, 3, IMAGE_SIZE, IMAGE_SIZE).to(DEVICE)
    torch.onnx.export(
        model, dummy, str(path),
        export_params=True, opset_version=17, do_constant_folding=True,
        input_names=["image"], output_names=["logits"],
        dynamic_axes={"image": {0: "batch"}, "logits": {0: "batch"}},
    )
    print(f"✅ Species ONNX model exported: {path}")


def main(args):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)

    # ── For species classification, derive from disease dataset:
    # PlantVillage folder structure: Apple___Apple_scab → class "Apple"
    # We remap the 38 disease classes to 14 unique plant species labels
    # by only keeping healthy samples OR using the plant prefix as the label.
    # A simpler approach: use the PlantVillage structure directly with
    # ImageFolder, using a custom label_from_dirname that strips the disease suffix.
    print(f"📂 Loading species dataset from: {DATA_DIR}")

    full_ds = datasets.ImageFolder(DATA_DIR, transform=get_transforms(True))
    n = len(full_ds)
    n_val  = int(0.1 * n)
    n_test = int(0.1 * n)
    n_train = n - n_val - n_test
    train_ds, val_ds, test_ds = random_split(
        full_ds, [n_train, n_val, n_test], generator=torch.Generator().manual_seed(42)
    )
    val_ds.dataset.transform  = get_transforms(False)
    test_ds.dataset.transform = get_transforms(False)

    print(f"Train: {n_train} | Val: {n_val} | Test: {n_test} | Classes: {len(full_ds.classes)}")

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True,  num_workers=4, pin_memory=True)
    val_loader   = DataLoader(val_ds,   batch_size=args.batch_size*2, num_workers=4, pin_memory=True)
    test_loader  = DataLoader(test_ds,  batch_size=args.batch_size*2, num_workers=4, pin_memory=True)

    with open(MODELS_DIR / "species_classes.json", "w") as f:
        json.dump(full_ds.class_to_idx, f, indent=2)

    model = build_species_model(num_classes=len(full_ds.classes), freeze_backbone=True)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

    best_acc = 0.0
    history = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}

    # Phase 1: Head only
    optimizer = optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()), lr=5e-4, weight_decay=1e-4
    )
    scheduler = CosineAnnealingLR(optimizer, T_max=10)
    phase1_epochs = args.epochs // 3

    print(f"\n🚀 Phase 1 — Head only training ({phase1_epochs} epochs)")
    for ep in range(1, phase1_epochs + 1):
        t = time.time()
        tl, ta = train_epoch(model, train_loader, criterion, optimizer)
        vl, va, _, _ = evaluate(model, val_loader, criterion)
        scheduler.step()
        history["train_loss"].append(tl); history["val_loss"].append(vl)
        history["train_acc"].append(ta);  history["val_acc"].append(va)
        print(f"  Ep {ep:3d} | TL={tl:.4f} TA={ta*100:.2f}% | VL={vl:.4f} VA={va*100:.2f}% | {time.time()-t:.1f}s")
        if va > best_acc:
            best_acc = va
            torch.save(model.state_dict(), CHECKPOINTS_DIR / "best_species_model.pt")

    # Phase 2: Full fine-tune
    for p in model.parameters(): p.requires_grad = True
    optimizer = optim.AdamW([
        {"params": model.features.parameters(), "lr": args.lr * 0.05},
        {"params": model.classifier.parameters(), "lr": args.lr},
    ], weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs - phase1_epochs)

    print(f"\n🔥 Phase 2 — Full fine-tuning ({args.epochs - phase1_epochs} epochs)")
    for ep in range(phase1_epochs + 1, args.epochs + 1):
        t = time.time()
        tl, ta = train_epoch(model, train_loader, criterion, optimizer)
        vl, va, _, _ = evaluate(model, val_loader, criterion)
        scheduler.step()
        history["train_loss"].append(tl); history["val_loss"].append(vl)
        history["train_acc"].append(ta);  history["val_acc"].append(va)
        print(f"  Ep {ep:3d} | TL={tl:.4f} TA={ta*100:.2f}% | VL={vl:.4f} VA={va*100:.2f}% | {time.time()-t:.1f}s")
        if va > best_acc:
            best_acc = va
            torch.save(model.state_dict(), CHECKPOINTS_DIR / "best_species_model.pt")

    # Final evaluation
    model.load_state_dict(torch.load(CHECKPOINTS_DIR / "best_species_model.pt"))
    _, test_acc, preds, labels = evaluate(model, test_loader, criterion)
    print(f"\n🎯 Test Accuracy: {test_acc*100:.2f}%")
    print(classification_report(labels, preds, target_names=full_ds.classes, digits=3))

    with open(MODELS_DIR / "species_training_history.json", "w") as f:
        json.dump(history, f, indent=2)

    export_onnx(model, MODELS_DIR / "species_efficientnet_b3.onnx")
    print(f"\n✅ Done! Best val accuracy: {best_acc*100:.2f}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs",     type=int,   default=30)
    parser.add_argument("--batch-size", type=int,   default=32)
    parser.add_argument("--lr",         type=float, default=1e-4)
    main(parser.parse_args())
