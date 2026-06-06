import json, shutil, torch
import torch.nn as nn
from torchvision import models
from pathlib import Path

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {DEVICE}")

def export(model_name, num_classes):
    ckpt       = Path(f"models/checkpoints/best_{model_name}.pt")
    class_json = Path(f"models/{model_name}_classes.json")
    onnx_out   = Path(f"models/{model_name}_efficientnet_b3.onnx")
    backend    = Path("../backend/models")

    if not ckpt.exists():
        print(f"❌ {ckpt} not found — skipping")
        return

    # Build model
    m = models.efficientnet_b3(weights=None)
    in_f = m.classifier[1].in_features
    m.classifier = nn.Sequential(
        nn.Dropout(p=0.4, inplace=True),
        nn.Linear(in_f, 512),
        nn.ReLU(inplace=True),
        nn.Dropout(p=0.3),
        nn.Linear(512, num_classes),
    )
    m.load_state_dict(torch.load(ckpt, map_location=DEVICE, weights_only=True))
    m.to(DEVICE).eval()
    print(f"✅ {model_name} checkpoint loaded ({num_classes} classes)")

    # Export ONNX
    dummy = torch.randn(1, 3, 300, 300).to(DEVICE)
    torch.onnx.export(
        m, dummy, str(onnx_out),
        export_params=True, opset_version=17,
        do_constant_folding=True,
        input_names=["image"], output_names=["logits"],
        dynamic_axes={"image": {0: "batch"}, "logits": {0: "batch"}},
    )
    print(f"✅ ONNX saved: {onnx_out} ({onnx_out.stat().st_size/1e6:.1f} MB)")

    # Copy to backend
    backend.mkdir(parents=True, exist_ok=True)
    shutil.copy2(onnx_out,   backend / f"{model_name}_efficientnet_b3.onnx")
    shutil.copy2(class_json, backend / f"{model_name}_classes.json")
    print(f"✅ Copied to backend/models/ ✓")

# Disease model — 38 classes
export("disease", 38)

# Species model — 14 classes
export("species", 14)

print("\n🎉 Export complete!")
print("Now restart backend: uvicorn app.main:app --reload")