"""Fast smoke tests for the Python site, generated visual, and static export."""

from pathlib import Path

from app import create_app
from scientific_art import heatmap_svg


def test_homepage_has_one_page_sections():
    app = create_app(testing=True)
    response = app.test_client().get("/")
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    for anchor in ('id="about"', 'id="experience"', 'id="research"',
                   'id="projects"', 'id="contact"'):
        assert anchor in html
    assert "Alex Carvalho" in html
    assert "Alex de Castro Carvalho" in html
    assert "Lex" in html


def test_no_missing_routes():
    app = create_app(testing=True)
    assert app.test_client().get("/does-not-exist").status_code == 404


def test_heatmap_is_deterministic_and_accessible():
    assert heatmap_svg() == heatmap_svg()
    assert "Scientific heatmap illustration" in heatmap_svg()
    assert "not measured data" in heatmap_svg()


def test_static_build_assets_exist_when_built():
    stylesheet = Path("static/css/site.css")
    if stylesheet.exists():
        assert stylesheet.stat().st_size > 1000
