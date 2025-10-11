import csv
from pathlib import Path
import sys
import numpy as np
from PIL import Image

# --- Existing entropy functions (copy from your script) ---
def shannon_entropy_from_counts(counts: np.ndarray, base: float = 2.0) -> float:
    total = counts.sum()
    if total == 0:
        return 0.0
    p = counts[counts > 0] / total
    log_fn = np.log2 if base == 2 else (np.log if base == math.e else lambda x: np.log(x) / np.log(base))
    return float(-(p * log_fn(p)).sum())

def entropy_grayscale(arr: np.ndarray) -> float:
    counts = np.bincount(arr.ravel(), minlength=256)
    return shannon_entropy_from_counts(counts, base=2)

def load_image(path: Path, mode: str) -> np.ndarray:
    with Image.open(path) as img:
        if mode == "grayscale":
            img = img.convert("L")
        elif mode == "rgb":
            img = img.convert("RGB")
        elif mode == "rgba":
            img = img.convert("RGBA")
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        return np.array(img, dtype=np.uint8)

# --- Configuration ---
IMAGES_DIR = Path("data/input_images")
MODE = "grayscale"  # or "rgb", "rgba"
CSV_IN = Path("C:/Users/alecs/Documents/ML/Image_Preprocessing/data/BIQ2021.csv")
CSV_OUT = Path("C:/Users/alecs/Documents/ML/Image_Preprocessing/data/BIQ2021_with_entropy.csv")

def compute_entropy_for_image(filename: str, mode: str) -> float:
    img_path = IMAGES_DIR / filename
    arr = load_image(img_path, mode)
    if mode == "grayscale":
        return entropy_grayscale(arr)
    else:
        raise NotImplementedError("Only grayscale mode supported in this snippet.")

def main():
    # Read input CSV
    with CSV_IN.open("r", encoding="utf-8", newline='') as fin:
        reader = csv.DictReader(fin)
        rows = list(reader)
        fieldnames = reader.fieldnames + ["entropy"]

    # Compute entropy for each image
    for row in rows:
        filename = row["file"] if "file" in row else row["filename"]
        try:
            entropy = compute_entropy_for_image(filename, MODE)
        except Exception as ex:
            entropy = ""
            print(f"Error processing {filename}: {ex}", file=sys.stderr)
        row["entropy"] = entropy

    # Write output CSV
    with CSV_OUT.open("w", encoding="utf-8", newline='') as fout:
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    main()
