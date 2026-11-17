"""Generate an original scientific heatmap-inspired SVG using pure Python.

The contour field is decorative; it intentionally represents no measured data.
"""

from html import escape
from math import cos, pi, sin


BANDS = (
    "#1534c5", "#126aff", "#10c4f4", "#27dbb0",
    "#9de950", "#f1ee45", "#ffac28", "#f35a22", "#dd221f",
)


def _contour_path(cx: float, cy: float, rx: float, ry: float, phase: float) -> str:
    points = []
    for step in range(97):
        angle = 2 * pi * step / 96
        distortion = (
            1
            + 0.085 * sin(3 * angle + phase)
            + 0.055 * cos(5 * angle - phase * 0.6)
            + 0.029 * sin(7 * angle + 0.9)
        )
        x = cx + rx * distortion * cos(angle)
        y = cy + ry * distortion * sin(angle)
        points.append(f"{x:.1f},{y:.1f}")
    return "M " + " L ".join(points) + " Z"


def heatmap_svg() -> str:
    """Return deterministic, accessible SVG artwork for the homepage hero."""
    bands = []
    for index, color in enumerate(BANDS):
        scale = 1 - index * 0.102
        x = 280 + index * 3
        y = 265 - index * 1.6
        path = _contour_path(x, y, 235 * scale, 226 * scale, 0.48 + index * 0.13)
        bands.append(
            f'<path d="{escape(path)}" fill="{color}" '
            f'stroke="#ffffff" stroke-opacity=".29" stroke-width=".75"/>'
        )

    dots = []
    for x, y in ((107, 180), (178, 130), (377, 145), (415, 220),
                 (140, 328), (362, 371), (259, 406), (306, 107)):
        dots.append(f'<circle cx="{x}" cy="{y}" r="2.3" fill="#101922" opacity=".65"/>')

    return (
        '<svg class="scientific-map" viewBox="0 0 560 530" '
        'role="img" aria-labelledby="map-title map-desc" '
        'xmlns="http://www.w3.org/2000/svg">'
        '<title id="map-title">Scientific heatmap illustration</title>'
        '<desc id="map-desc">An abstract field of colored contour bands, '
        'from deep blue through cyan and green to yellow, orange and red. '
        'Decorative artwork, not measured data.</desc>'
        '<defs>'
        '<clipPath id="map-clip"><circle cx="280" cy="265" r="229"/></clipPath>'
        '<radialGradient id="map-halo"><stop stop-color="#0caad0" stop-opacity=".22"/>'
        '<stop offset="1" stop-color="#0caad0" stop-opacity="0"/></radialGradient>'
        '</defs>'
        '<circle cx="280" cy="265" r="260" fill="url(#map-halo)"/>'
        '<g clip-path="url(#map-clip)">'
        '<circle cx="280" cy="265" r="233" fill="#112e72"/>'
        + "".join(bands)
        + "".join(dots)
        + '</g>'
        '<circle cx="280" cy="265" r="229" fill="none" stroke="#41dbe7" '
        'stroke-opacity=".65" stroke-width="1.2"/>'
        '</svg>'
    )
