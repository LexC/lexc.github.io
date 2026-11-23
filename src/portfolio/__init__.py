"""Flask application for Alex Carvalho's single-page professional portfolio."""

from pathlib import Path

from flask import Flask, render_template, send_from_directory
from jinja2 import StrictUndefined
from .content import (
    CONTACT, EXPERIENCE, EXPERTISE, EXPERTISE_CATEGORIES, NAVIGATION,
    PROFILE, PROJECTS, PUBLICATIONS, RESEARCH, validate_content,
)


def create_app(testing: bool = False) -> Flask:
    """Create a local-development app that can also be frozen to static HTML."""
    validate_content()
    app = Flask(__name__)
    app.jinja_env.undefined = StrictUndefined
    app.config.update(TESTING=testing)

    @app.get("/assets/<path:filename>")
    def assets(filename):
        """Serve the shared project images in development and static exports."""
        return send_from_directory(Path(__file__).resolve().parents[2] / "assets", filename)

    @app.get("/")
    def home():
        return render_template(
            "index.html",
            profile=PROFILE,
            research=RESEARCH,
            navigation=NAVIGATION,
            expertise=EXPERTISE,
            experience=EXPERIENCE,
            projects=PROJECTS,
            publications=PUBLICATIONS,
            contact=CONTACT,
            expertise_categories=EXPERTISE_CATEGORIES,
        )

    return app

