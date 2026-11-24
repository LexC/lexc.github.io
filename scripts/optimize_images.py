"""Regenerate the committed WebP assets from the original PNGs."""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "src/portfolio/static/images"
PROJECTS = ("goto-platform", "nuflow-genomics", "fraud-classifier-boundary")
PUBLICATIONS = ("jal-06-00011-g003", "NPh_10_1_013510_f001")


def optimize(source, destination, max_size=None):
    with Image.open(source) as original:
        image = original.convert("RGBA" if "A" in original.getbands() else "RGB")
    if max_size is not None:
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, "WEBP", lossless=True, exact=True, method=6,
               icc_profile=b"", exif=b"", xmp=b"")
    print(f"{destination.relative_to(ROOT)}: {image.width}x{image.height}, "
          f"{destination.stat().st_size:,} bytes")


def main():
    optimize(ROOT / "assets/IMG-2026117_ed.png", OUTPUT / "portrait.webp")
    for name in PROJECTS:
        optimize(ROOT / f"assets/originals/projects/{name}.png",
                 OUTPUT / f"projects/{name}.webp")
    for name in PUBLICATIONS:
        optimize(ROOT / f"assets/{name}.png", OUTPUT / f"publications/{name}.webp",
                 max_size=(1600, 1600))


if __name__ == "__main__":
    main()
