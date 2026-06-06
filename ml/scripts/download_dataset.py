"""
download_dataset.py — Download the PlantVillage dataset via the Kaggle API.

Prerequisites:
    1. Create a Kaggle account at kaggle.com
    2. Go to Account → API → Create New Token → downloads kaggle.json
    3. Place kaggle.json at ~/.kaggle/kaggle.json (Linux/Mac)
       or %USERPROFILE%\.kaggle\kaggle.json (Windows)
    4. pip install kaggle

Usage:
    python scripts/download_dataset.py

Dataset: https://www.kaggle.com/datasets/emmarex/plantdisease
  - 38 classes (14 plant species × healthy + disease variants)
  - ~87,000 images
  - ~2.5 GB download
"""

import os
import subprocess
import sys
from pathlib import Path

DATA_DIR = Path("data")
DATASET_SLUG = "emmarex/plantdisease"   # Kaggle dataset identifier
EXTRACT_DIR  = DATA_DIR / "plantvillage"


def check_kaggle_credentials():
    cred_path = Path.home() / ".kaggle" / "kaggle.json"
    if not cred_path.exists():
        print("❌ Kaggle API credentials not found!")
        print(f"   Expected: {cred_path}")
        print()
        print("   Steps to fix:")
        print("   1. Go to https://www.kaggle.com → Account → API → Create New Token")
        print("   2. Move the downloaded kaggle.json to:", cred_path)
        print("   3. Run: chmod 600 ~/.kaggle/kaggle.json  (Linux/Mac only)")
        sys.exit(1)


def download():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    check_kaggle_credentials()

    print(f"⬇️  Downloading PlantVillage dataset ({DATASET_SLUG})…")
    print("    This is ~2.5 GB — may take several minutes.\n")

    subprocess.run(
        ["kaggle", "datasets", "download", "-d", DATASET_SLUG,
         "--unzip", "-p", str(DATA_DIR)],
        check=True
    )

    # Rename extracted folder if needed
    candidates = [DATA_DIR / "PlantVillage", DATA_DIR / "plantdisease"]
    for candidate in candidates:
        if candidate.exists() and not EXTRACT_DIR.exists():
            candidate.rename(EXTRACT_DIR)
            break

    if not EXTRACT_DIR.exists():
        print(f"⚠️  Expected folder not found at {EXTRACT_DIR}.")
        print("    Check the contents of", DATA_DIR)
        return

    # Count what we got
    image_files = list(EXTRACT_DIR.rglob("*.jpg")) + list(EXTRACT_DIR.rglob("*.JPG")) + \
                  list(EXTRACT_DIR.rglob("*.png")) + list(EXTRACT_DIR.rglob("*.PNG"))
    classes     = [d.name for d in EXTRACT_DIR.iterdir() if d.is_dir()]

    print(f"\n✅ Download complete!")
    print(f"   📁 Location  : {EXTRACT_DIR.resolve()}")
    print(f"   🗂️  Classes   : {len(classes)}")
    print(f"   🖼️  Images    : {len(image_files):,}")
    print(f"\nNext steps:")
    print("   python scripts/preprocess.py   # validate & clean dataset")
    print("   python scripts/train_disease.py  --epochs 30")
    print("   python scripts/train_species.py  --epochs 30")


if __name__ == "__main__":
    download()
