"""Flask application for Alex Carvalho's single-page professional portfolio."""

from flask import Flask, render_template

from portfolio_content import PROFILE, NAVIGATION, EXPERTISE, EXPERIENCE, PROJECTS
from scientific_art import heatmap_svg


def create_app(testing: bool = False) -> Flask:
    """Create a local-development app that can also be frozen to static HTML."""
    app = Flask(__name__)
    app.config.update(TESTING=testing)

    @app.get("/")
    def home():
        return render_template(
            "index.html",
            profile=PROFILE,
            navigation=NAVIGATION,
            expertise=EXPERTISE,
            experience=EXPERIENCE,
            projects=PROJECTS,
            scientific_visual=heatmap_svg(),
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
