"""
train_disease.py — Train EfficientNet-B3 on PlantVillage dataset for disease classification.

Usage:
    python scripts/train_disease.py --epochs 30 --batch-size 32 --lr 1e-4

Dataset: PlantVillage (38 classes, ~87,000 images)
Architecture: EfficientNet-B3 with ImageNet pretrained weights, fine-tuned classifier head
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
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# ── Config ────────────────────────────────────────────────────────────────────

NUM_CLASSES    = 38
IMAGE_SIZE     = 300      # EfficientNet-B3 native input size
DATA_DIR       = Path("data/plantvillage")
MODELS_DIR     = Path("../backend/models")
CHECKPOINTS_DIR = Path("models/checkpoints")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Training on: {DEVICE}")


# ── Data Transforms ───────────────────────────────────────────────────────────

def get_transforms(train: bool):
    if train:
        return transforms.Compose([
            transforms.RandomResizedCrop(IMAGE_SIZE, scale=(0.7, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.RandomRotation(30),
            transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1),
            transforms.RandomGrayscale(p=0.05),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            transforms.RandomErasing(p=0.2),
        ])
    else:
        return transforms.Compose([
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])


# ── Model ─────────────────────────────────────────────────────────────────────

def build_model(num_classes: int, freeze_backbone: bool = False) -> nn.Module:
    """
    EfficientNet-B3 with custom classifier head.
    Phase 1: Freeze backbone, train only the classifier head.
    Phase 2: Unfreeze all layers for full fine-tuning.
    """
    model = models.efficientnet_b3(weights=models.EfficientNet_B3_Weights.IMAGENET1K_V1)

    if freeze_backbone:
        for param in model.features.parameters():
            param.requires_grad = False

    # Replace the classifier head
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.4, inplace=True),
        nn.Linear(in_features, 512),
        nn.ReLU(inplace=True),
        nn.Dropout(p=0.3),
        nn.Linear(512, num_classes),
    )

    return model.to(DEVICE)


# ── Training Loop ─────────────────────────────────────────────────────────────

def train_epoch(model, loader, criterion, optimizer, epoch):
    model.train()
    running_loss, correct, total = 0.0, 0, 0

    for batch_idx, (images, labels) in enumerate(loader):
        images, labels = images.to(DEVICE), labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()

        # Gradient clipping prevents exploding gradients
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        running_loss += loss.item() * images.size(0)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

        if batch_idx % 50 == 0:
            print(
                f"  Epoch {epoch} | Batch {batch_idx}/{len(loader)} | "
                f"Loss: {loss.item():.4f} | Acc: {100.*correct/total:.2f}%"
            )

    return running_loss / total, correct / total


@torch.no_grad()
def evaluate(model, loader, criterion):
    model.eval()
    running_loss, correct, total = 0.0, 0, 0
    all_preds, all_labels = [], []

    for images, labels in loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        outputs = model(images)
        loss = criterion(outputs, labels)

        running_loss += loss.item() * images.size(0)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

        all_preds.extend(predicted.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

    return running_loss / total, correct / total, all_preds, all_labels


# ── Export to ONNX ────────────────────────────────────────────────────────────

def export_to_onnx(model: nn.Module, output_path: Path):
    model.eval()
    dummy = torch.randn(1, 3, IMAGE_SIZE, IMAGE_SIZE).to(DEVICE)

    torch.onnx.export(
        model,
        dummy,
        str(output_path),
        export_params=True,
        opset_version=17,
        do_constant_folding=True,
        input_names=["image"],
        output_names=["logits"],
        dynamic_axes={"image": {0: "batch_size"}, "logits": {0: "batch_size"}},
    )
    print(f"✅ ONNX model exported to: {output_path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main(args):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)

    # ── Dataset ────────────────────────────────────────────────────────────
    print(f"\n📂 Loading dataset from: {DATA_DIR}")
    full_dataset = datasets.ImageFolder(root=DATA_DIR, transform=get_transforms(train=True))

    # 80/10/10 split
    n_total = len(full_dataset)
    n_val   = int(0.1 * n_total)
    n_test  = int(0.1 * n_total)
    n_train = n_total - n_val - n_test
    train_ds, val_ds, test_ds = random_split(
        full_dataset, [n_train, n_val, n_test],
        generator=torch.Generator().manual_seed(42)
    )
    val_ds.dataset.transform  = get_transforms(train=False)
    test_ds.dataset.transform = get_transforms(train=False)

    print(f"Train: {n_train} | Val: {n_val} | Test: {n_test}")
    print(f"Classes ({len(full_dataset.classes)}): {full_dataset.classes[:5]}...")

    train_loader = DataLoader(
        train_ds, batch_size=args.batch_size, shuffle=True,
        num_workers=4, pin_memory=True, persistent_workers=True
    )
    val_loader = DataLoader(
        val_ds, batch_size=args.batch_size * 2, num_workers=4, pin_memory=True
    )
    test_loader = DataLoader(
        test_ds, batch_size=args.batch_size * 2, num_workers=4, pin_memory=True
    )

    # Save class → index mapping
    class_to_idx = full_dataset.class_to_idx
    with open(MODELS_DIR / "disease_classes.json", "w") as f:
        json.dump(class_to_idx, f, indent=2)

    # ── Model, Loss, Optimizer ─────────────────────────────────────────────
    model = build_model(num_classes=len(full_dataset.classes), freeze_backbone=True)

    # Class weights for imbalanced dataset
    class_counts = np.bincount([s[1] for s in full_dataset.samples])
    class_weights = torch.FloatTensor(1.0 / (class_counts + 1e-6)).to(DEVICE)
    criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=0.1)

    # Phase 1: Train only head
    optimizer = optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=args.lr * 10, weight_decay=1e-4
    )
    scheduler = CosineAnnealingLR(optimizer, T_max=10, eta_min=1e-6)

    best_val_acc = 0.0
    history = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}

    print(f"\n🚀 Phase 1: Head-only training ({args.epochs // 3} epochs)")
    for epoch in range(1, args.epochs // 3 + 1):
        t0 = time.time()
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, epoch)
        val_loss, val_acc, _, _ = evaluate(model, val_loader, criterion)
        scheduler.step()

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["train_acc"].append(train_acc)
        history["val_acc"].append(val_acc)

        print(
            f"Epoch {epoch:3d} | "
            f"Train Loss: {train_loss:.4f}, Acc: {100*train_acc:.2f}% | "
            f"Val Loss: {val_loss:.4f}, Acc: {100*val_acc:.2f}% | "
            f"Time: {time.time()-t0:.1f}s"
        )

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), CHECKPOINTS_DIR / "best_disease_model.pt")
            print(f"  💾 Saved best model (val_acc={100*val_acc:.2f}%)")

    # Phase 2: Unfreeze all layers, fine-tune with lower LR
    print(f"\n🔥 Phase 2: Full fine-tuning ({args.epochs - args.epochs // 3} epochs)")
    for param in model.parameters():
        param.requires_grad = True

    optimizer = optim.AdamW([
        {"params": model.features.parameters(), "lr": args.lr * 0.1},
        {"params": model.classifier.parameters(), "lr": args.lr},
    ], weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs - args.epochs // 3, eta_min=1e-7)

    for epoch in range(args.epochs // 3 + 1, args.epochs + 1):
        t0 = time.time()
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, epoch)
        val_loss, val_acc, _, _ = evaluate(model, val_loader, criterion)
        scheduler.step()

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["train_acc"].append(train_acc)
        history["val_acc"].append(val_acc)

        print(
            f"Epoch {epoch:3d} | "
            f"Train Loss: {train_loss:.4f}, Acc: {100*train_acc:.2f}% | "
            f"Val Loss: {val_loss:.4f}, Acc: {100*val_acc:.2f}% | "
            f"Time: {time.time()-t0:.1f}s"
        )

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), CHECKPOINTS_DIR / "best_disease_model.pt")
            print(f"  💾 Saved best model (val_acc={100*val_acc:.2f}%)")

    # ── Final Evaluation ───────────────────────────────────────────────────
    model.load_state_dict(torch.load(CHECKPOINTS_DIR / "best_disease_model.pt"))
    _, test_acc, preds, labels = evaluate(model, test_loader, criterion)
    print(f"\n🎯 Test Accuracy: {100*test_acc:.2f}%")
    print("\nClassification Report:")
    print(classification_report(labels, preds, target_names=full_dataset.classes, digits=3))

    # Save training history
    with open(MODELS_DIR / "disease_training_history.json", "w") as f:
        json.dump(history, f, indent=2)

    # ── Export ONNX ────────────────────────────────────────────────────────
    onnx_path = MODELS_DIR / "disease_efficientnet_b3.onnx"
    export_to_onnx(model, onnx_path)

    print(f"\n✅ Training complete! Best validation accuracy: {100*best_val_acc:.2f}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Plant Disease Classifier")
    parser.add_argument("--epochs",     type=int,   default=30,   help="Number of training epochs")
    parser.add_argument("--batch-size", type=int,   default=32,   help="Training batch size")
    parser.add_argument("--lr",         type=float, default=1e-4, help="Base learning rate")
    parser.add_argument("--data-dir",   type=str,   default=str(DATA_DIR))
    args = parser.parse_args()

    if args.data_dir:
        DATA_DIR = Path(args.data_dir)

    main(args)
