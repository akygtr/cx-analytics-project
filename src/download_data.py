"""
Pulls down the three core datasets for the project.
Run from project root:  python src\download_data.py
"""
import subprocess
from pathlib import Path

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = {
    "olist": "olistbr/brazilian-ecommerce",
    "womens_clothing": "nicapotato/womens-ecommerce-clothing-reviews",
    "twitter_support": "thoughtvector/customer-support-on-twitter",
}

def download(name, slug):
    target = RAW_DIR / name
    if target.exists() and any(target.iterdir()):
        print(f"[skip] {name} already downloaded")
        return
    target.mkdir(exist_ok=True)
    print(f"[fetch] {slug} -> {target}")
    subprocess.run(
        ["kaggle", "datasets", "download", "-d", slug, "-p", str(target), "--unzip"],
        check=True,
    )
    print(f"[done] {name}")

if __name__ == "__main__":
    for name, slug in DATASETS.items():
        try:
            download(name, slug)
        except subprocess.CalledProcessError as e:
            print(f"[error] couldn't fetch {name}: {e}")
    print("\nAll done. Check data/raw/")