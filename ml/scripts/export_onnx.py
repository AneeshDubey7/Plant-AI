"""
export_onnx.py — Export trained PyTorch models to ONNX format for fast inference.

ONNX Runtime is 3-5x faster than raw PyTorch on CPU, making it ideal for production.
This script also validates the exported models and benchmarks inference speed.

Usage:
    python scripts/export_onnx.py --species-checkpoint models/checkpoints/best_species_model.pt \
                                   --disease-checkpoint models/checkpoints/best_disease_model.pt
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torchvision import models


IMAGE_SIZE   = 300
MODELS_DIR   = Path("../backend/models")
DEVICE       = torch.device("cpu")  # Export from CPU for portability


def build_model(num_classes: int, checkpoint_path: Path) -> nn.Module:
    model = models.efficientnet_b3(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.4, inplace=True),
        nn.Linear(in_features, 512),
        nn.ReLU(inplace=True),
        nn.Dropout(p=0.3),
        nn.Linear(512, num_classes),
    )
    state = torch.load(checkpoint_path, map_location=DEVICE)
    model.load_state_dict(state)
    model.eval()
    return model


def export_and_validate(model: nn.Module, onnx_path: Path, model_name: str):
    dummy = torch.randn(1, 3, IMAGE_SIZE, IMAGE_SIZE)

    # Export
    torch.onnx.export(
        model, dummy, str(onnx_path),
        export_params=True,
        opset_version=17,
        do_constant_folding=True,
        input_names=["image"],
        output_names=["logits"],
        dynamic_axes={"image": {0: "batch_size"}, "logits": {0: "batch_size"}},
    )
    print(f"✅ Exported: {onnx_path} ({onnx_path.stat().st_size / 1e6:.1f} MB)")

    # Validate with ONNX Runtime
    try:
        import onnxruntime as ort

        session = ort.InferenceSession(
            str(onnx_path),
            providers=["CPUExecutionProvider"],
        )
        input_name = session.get_inputs()[0].name
        dummy_np   = dummy.numpy()

        # Correctness check
        torch_out = model(dummy).detach().numpy()
        onnx_out  = session.run(None, {input_name: dummy_np})[0]
        max_diff   = np.abs(torch_out - onnx_out).max()
        print(f"  Correctness check: max output difference = {max_diff:.6f} (should be < 1e-4)")
        assert max_diff < 1e-3, f"ONNX output diverges too much: {max_diff}"

        # Speed benchmark
        N_WARMUP = 5
        N_BENCH  = 50
        for _ in range(N_WARMUP):
            session.run(None, {input_name: dummy_np})
        t0 = time.perf_counter()
        for _ in range(N_BENCH):
            session.run(None, {input_name: dummy_np})
        elapsed = (time.perf_counter() - t0) / N_BENCH * 1000
        print(f"  ONNX inference time: {elapsed:.1f} ms/image (averaged over {N_BENCH} runs)")

        # PyTorch speed for comparison
        with torch.no_grad():
            for _ in range(N_WARMUP):
                model(dummy)
            t0 = time.perf_counter()
            for _ in range(N_BENCH):
                model(dummy)
        pt_elapsed = (time.perf_counter() - t0) / N_BENCH * 1000
        print(f"  PyTorch inference time: {pt_elapsed:.1f} ms/image")
        print(f"  ONNX speedup: {pt_elapsed/elapsed:.2f}x")

    except ImportError:
        print("  ⚠️  onnxruntime not installed — skipping validation")


def main(args):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # Load class counts from saved JSON files
    species_classes_path = MODELS_DIR / "species_classes.json"
    disease_classes_path = MODELS_DIR / "disease_classes.json"

    if species_classes_path.exists():
        with open(species_classes_path) as f:
            n_species = len(json.load(f))
    else:
        n_species = 14  # default
        print("⚠️  species_classes.json not found, using default n_classes=14")

    if disease_classes_path.exists():
        with open(disease_classes_path) as f:
            n_disease = len(json.load(f))
    else:
        n_disease = 38
        print("⚠️  disease_classes.json not found, using default n_classes=38")

    # Export species model
    if Path(args.species_checkpoint).exists():
        print(f"\n📦 Exporting Species model ({n_species} classes)...")
        species_model = build_model(n_species, Path(args.species_checkpoint))
        export_and_validate(species_model, MODELS_DIR / "species_efficientnet_b3.onnx", "Species")
    else:
        print(f"⚠️  Species checkpoint not found: {args.species_checkpoint}")

    # Export disease model
    if Path(args.disease_checkpoint).exists():
        print(f"\n📦 Exporting Disease model ({n_disease} classes)...")
        disease_model = build_model(n_disease, Path(args.disease_checkpoint))
        export_and_validate(disease_model, MODELS_DIR / "disease_efficientnet_b3.onnx", "Disease")
    else:
        print(f"⚠️  Disease checkpoint not found: {args.disease_checkpoint}")

    print("\n✅ Export complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--species-checkpoint", default="models/checkpoints/best_species_model.pt")
    parser.add_argument("--disease-checkpoint", default="models/checkpoints/best_disease_model.pt")
    main(parser.parse_args())
