"""Fast smoke tests for the Python site, generated visual, and static export."""

from pathlib import Path

from portfolio import create_app
from portfolio.scientific_art import heatmap_svg
from portfolio import content
import pytest


def test_homepage_has_one_page_sections():
    app = create_app(testing=True)
    response = app.test_client().get("/")
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    for anchor in ('id="about"', 'id="experience"', 'id="research"',
                   'id="projects"', 'id="contact"'):
        assert anchor in html
    assert "Alex Carvalho" in html
    assert "Lex" in html
    assert (
        "<span>Physicist. Biomedical Researcher.</span> "
        "<span>Software Development Lead.</span>"
    ) in html
    assert (
        "8+ years of Python experience spanning scientific computing, data science, "
        "and software engineering."
    ) in html


def test_no_missing_routes():
    app = create_app(testing=True)
    assert app.test_client().get("/does-not-exist").status_code == 404


def test_heatmap_is_deterministic_and_accessible():
    assert heatmap_svg() == heatmap_svg()
    assert "Scientific heatmap illustration" in heatmap_svg()
    assert "not measured data" in heatmap_svg()


def test_missing_content_fails_clearly(monkeypatch):
    monkeypatch.delitem(content.PROFILE, "name")
    with pytest.raises(ValueError, match="name"):
        create_app(testing=True)


def test_editorial_text_is_escaped(monkeypatch):
    monkeypatch.setitem(content.PROFILE, "name", "<script>alert(1)</script>")
    html = create_app(testing=True).test_client().get("/").get_data(as_text=True)
    assert "&lt;script&gt;" in html
    assert "<script>alert(1)</script>" not in html
