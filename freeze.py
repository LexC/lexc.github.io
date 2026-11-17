"""Build the Flask application as a static GitHub Pages-compatible website."""

from pathlib import Path

from flask_frozen import Freezer

from app import create_app

app = create_app()
app.config.update(
    FREEZER_DESTINATION=str(Path(__file__).resolve().parent / "dist"),
    FREEZER_RELATIVE_URLS=False,
)
freezer = Freezer(app)

if __name__ == "__main__":
    freezer.freeze()
