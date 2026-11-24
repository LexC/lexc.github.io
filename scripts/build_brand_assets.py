"""Regenerate committed favicon files and the sharing JPEG. Requires Pillow."""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "src/portfolio/static"
BACKGROUND = "#001722"
ACCENT = "#00edf2"
WHITE = "#f6f8f9"
RECTANGLES = (
    (0, 0, 64, 64, BACKGROUND, 14),
    (10, 17, 12, 47, ACCENT, 1),
    (23, 17, 30, 46, WHITE, 0),
    (23, 39, 43, 46, WHITE, 0),
)


def build_favicon():
    rectangles = "\n".join(
        f'  <rect x="{x}" y="{y}" width="{right-x}" height="{bottom-y}" '
        f'rx="{radius}" fill="{color}"/>'
        for x, y, right, bottom, color, radius in RECTANGLES
    )
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
           '  <title>Lex</title>\n' + rectangles +
           f'\n  <circle cx="51" cy="42" r="4" fill="{ACCENT}"/>\n</svg>\n')
    (STATIC / "favicon.svg").write_text(svg, encoding="utf-8")
    scale = 8
    icon = Image.new("RGBA", (64 * scale, 64 * scale))
    draw = ImageDraw.Draw(icon)
    for x, y, right, bottom, color, radius in RECTANGLES:
        draw.rounded_rectangle((x*scale, y*scale, right*scale-1, bottom*scale-1),
                               radius=radius*scale, fill=color)
    draw.ellipse((47*scale, 38*scale, 55*scale-1, 46*scale-1), fill=ACCENT)
    icon.save(STATIC / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    icon.resize((180, 180), Image.Resampling.LANCZOS).save(STATIC / "apple-touch-icon.png")


def build_sharing_card():
    source = ROOT / "assets/branding/social-card.png"
    with Image.open(source) as original:
        card = original.convert("RGB")
    card.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
    destination = STATIC / "images/social-card.jpg"
    card.save(destination, quality=92, optimize=True)
    print(f"Sharing card: {card.width}x{card.height}, {destination.stat().st_size:,} bytes")


if __name__ == "__main__":
    build_favicon()
    build_sharing_card()
