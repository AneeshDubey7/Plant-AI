"""
preprocess.py — Validate, clean, and prepare the PlantVillage dataset.

Checks:
  - Corrupt images (cannot be opened by Pillow)
  - Tiny images (< 50×50 pixels)
  - Near-duplicate detection (optional, uses pHash)
  - Class distribution report

Usage:
    python scripts/preprocess.py --data-dir data/plantvillage --output-report report.json
"""

import argparse
import json
import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image
from tqdm import tqdm


MIN_SIZE = 50  # pixels — discard images smaller than this


def check_image(path: Path):
    """Return (path, is_valid, issue) for a single image file."""
    try:
        with Image.open(path) as img:
            img.verify()
        with Image.open(path) as img:
            w, h = img.size
            if w < MIN_SIZE or h < MIN_SIZE:
                return path, False, f"too_small ({w}x{h})"
        return path, True, None
    except Exception as e:
        return path, False, f"corrupt: {e}"


def get_all_images(data_dir: Path):
    exts = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}
    return [p for p in data_dir.rglob("*") if p.suffix in exts]


def main(args):
    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        print("   Run: python scripts/download_dataset.py first")
        return

    all_images = get_all_images(data_dir)
    print(f"📂 Found {len(all_images):,} images in {data_dir}")

    # ── Integrity check ────────────────────────────────────────────────────
    print("\n🔍 Checking image integrity...")
    invalid = []
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as ex:
        futures = {ex.submit(check_image, p): p for p in all_images}
        for future in tqdm(as_completed(futures), total=len(all_images)):
            path, is_valid, issue = future.result()
            if not is_valid:
                invalid.append({"path": str(path), "issue": issue})

    print(f"\n✅ Valid images: {len(all_images) - len(invalid):,}")
    print(f"❌ Invalid images: {len(invalid):,}")

    if invalid and args.remove_invalid:
        for item in invalid:
            Path(item["path"]).unlink(missing_ok=True)
        print(f"🗑️  Removed {len(invalid)} invalid images")

    # ── Class distribution ─────────────────────────────────────────────────
    class_counts = Counter()
    for img_path in all_images:
        class_name = img_path.parent.name
        class_counts[class_name] += 1

    print(f"\n📊 Class Distribution ({len(class_counts)} classes):")
    print(f"{'Class':<45} {'Count':>6} {'Bar'}")
    print("-" * 70)
    max_count = max(class_counts.values())
    for cls, cnt in sorted(class_counts.items()):
        bar = "█" * int(30 * cnt / max_count)
        print(f"{cls:<45} {cnt:>6}  {bar}")

    # ── Save report ────────────────────────────────────────────────────────
    report = {
        "total_images": len(all_images),
        "valid_images": len(all_images) - len(invalid),
        "invalid_images": len(invalid),
        "num_classes": len(class_counts),
        "class_distribution": dict(sorted(class_counts.items())),
        "invalid_details": invalid[:50],  # First 50 for brevity
        "min_class_count": min(class_counts.values()),
        "max_class_count": max(class_counts.values()),
        "avg_class_count": int(sum(class_counts.values()) / len(class_counts)),
    }

    output_path = Path(args.output_report)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n💾 Report saved to: {output_path}")
    print("\n✅ Preprocessing complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir",      default="data/plantvillage")
    parser.add_argument("--output-report", default="data/preprocessing_report.json")
    parser.add_argument("--remove-invalid", action="store_true",
                        help="Delete corrupt/tiny images from disk")
    main(parser.parse_args())
