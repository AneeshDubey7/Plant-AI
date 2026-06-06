# Model Evaluation & Analysis
# Run this as a Jupyter notebook: jupyter notebook notebooks/model_evaluation.ipynb
# Or execute cells manually in any Python environment

# ── Cell 1: Imports ────────────────────────────────────────────────────────────
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from pathlib import Path

# Style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
print("Imports OK")

# ── Cell 2: Load training history ─────────────────────────────────────────────
MODELS_DIR = Path("../backend/models")

def load_history(name):
    path = MODELS_DIR / f"{name}_training_history.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    print(f"⚠️  {path} not found — run training scripts first")
    return None

disease_history = load_history("disease")
species_history = load_history("species")

# ── Cell 3: Plot training curves ──────────────────────────────────────────────
def plot_training_curves(history, title):
    if history is None:
        print(f"No history for {title}")
        return

    epochs = range(1, len(history["train_loss"]) + 1)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(title, fontsize=14, fontweight='bold')

    # Loss
    axes[0].plot(epochs, history["train_loss"], label="Train Loss", lw=2)
    axes[0].plot(epochs, history["val_loss"],   label="Val Loss",   lw=2, linestyle='--')
    axes[0].set_xlabel("Epoch"); axes[0].set_ylabel("Loss")
    axes[0].set_title("Loss Curves"); axes[0].legend()

    # Accuracy
    train_acc = [a * 100 for a in history["train_acc"]]
    val_acc   = [a * 100 for a in history["val_acc"]]
    axes[1].plot(epochs, train_acc, label="Train Acc", lw=2)
    axes[1].plot(epochs, val_acc,   label="Val Acc",   lw=2, linestyle='--')
    axes[1].set_xlabel("Epoch"); axes[1].set_ylabel("Accuracy (%)")
    axes[1].set_title("Accuracy Curves"); axes[1].legend()
    axes[1].set_ylim([0, 100])

    plt.tight_layout()
    plt.savefig(f"../docs/{title.replace(' ', '_').lower()}_curves.png", dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Best val accuracy: {max(val_acc):.2f}%")

plot_training_curves(disease_history, "Disease Classification — EfficientNet-B3")
plot_training_curves(species_history, "Species Classification — EfficientNet-B3")

# ── Cell 4: PlantVillage class distribution ────────────────────────────────────
DATA_DIR = Path("data/plantvillage")

if DATA_DIR.exists():
    from collections import Counter
    classes = [d.name for d in DATA_DIR.iterdir() if d.is_dir()]
    counts  = {c: len(list((DATA_DIR / c).glob("*"))) for c in classes}
    sorted_counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

    fig, ax = plt.subplots(figsize=(16, 7))
    colors = ['#ef4444' if 'healthy' not in k.lower() else '#22c55e' for k in sorted_counts]
    bars = ax.barh(list(sorted_counts.keys()), list(sorted_counts.values()), color=colors)
    ax.set_xlabel("Number of Images")
    ax.set_title("PlantVillage Dataset — Class Distribution", fontsize=13, fontweight='bold')

    legend = [
        mpatches.Patch(color='#22c55e', label='Healthy'),
        mpatches.Patch(color='#ef4444', label='Diseased'),
    ]
    ax.legend(handles=legend)
    plt.tight_layout()
    plt.savefig("../docs/class_distribution.png", dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Total images: {sum(sorted_counts.values()):,}")
    print(f"Total classes: {len(sorted_counts)}")
else:
    print("Dataset not downloaded yet. Run: python scripts/download_dataset.py")

# ── Cell 5: ONNX inference benchmark ──────────────────────────────────────────
try:
    import onnxruntime as ort
    import time
    from PIL import Image
    import io

    def benchmark_model(onnx_path, n_runs=100, batch_size=1):
        if not Path(onnx_path).exists():
            print(f"Model not found: {onnx_path}")
            return

        sess = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
        input_name = sess.get_inputs()[0].name
        dummy = np.random.randn(batch_size, 3, 300, 300).astype(np.float32)

        # Warmup
        for _ in range(10):
            sess.run(None, {input_name: dummy})

        times = []
        for _ in range(n_runs):
            t0 = time.perf_counter()
            sess.run(None, {input_name: dummy})
            times.append((time.perf_counter() - t0) * 1000)

        print(f"\n{Path(onnx_path).name}")
        print(f"  Mean:   {np.mean(times):.1f} ms")
        print(f"  Median: {np.median(times):.1f} ms")
        print(f"  P95:    {np.percentile(times, 95):.1f} ms")
        print(f"  P99:    {np.percentile(times, 99):.1f} ms")
        print(f"  Throughput: {1000/np.mean(times):.1f} images/sec")
        return times

    times_species = benchmark_model(MODELS_DIR / "species_efficientnet_b3.onnx")
    times_disease = benchmark_model(MODELS_DIR / "disease_efficientnet_b3.onnx")

    if times_species and times_disease:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(times_species, bins=30, alpha=0.7, label="Species Model", color='#16a34a')
        ax.hist(times_disease, bins=30, alpha=0.7, label="Disease Model", color='#ea580c')
        ax.set_xlabel("Inference Time (ms)")
        ax.set_ylabel("Frequency")
        ax.set_title("ONNX Inference Time Distribution (CPU, batch=1)", fontweight='bold')
        ax.legend()
        plt.tight_layout()
        plt.savefig("../docs/inference_benchmark.png", dpi=150, bbox_inches='tight')
        plt.show()

except ImportError:
    print("onnxruntime not installed. Run: pip install onnxruntime")

print("\n✅ Evaluation notebook complete!")
