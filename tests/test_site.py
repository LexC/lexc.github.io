"""Fast smoke tests for the Python site, generated visual, and static export."""

import re
import struct

from portfolio import create_app
from portfolio.scientific_art import heatmap_svg
from portfolio import content
import pytest


def test_homepage_has_one_page_sections():
    app = create_app(testing=True)
    response = app.test_client().get("/")
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    sections = ["about", "experience", "projects", "research", "expertise", "contact"]
    assert re.findall(r'<section[^>]* id="([^"]+)"', html) == sections
    navigation = html.split('<nav class="site-nav"', 1)[1].split('</nav>', 1)[0]
    assert re.findall(r'href="#([^"]+)"', navigation) == sections
    assert re.findall(r'class="section-index">(\d+)</span>', html) == [
        "01", "02", "03", "04", "05", "06"
    ]
    assert html.count('class="timeline-item"') == 3
    assert "Alex Carvalho" in html
    assert "Lex" in html
    assert (
        "<span>Physicist. Biomedical Researcher.</span> "
        "<span>Software Development Leader.</span>"
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
    monkeypatch.setitem(content.PROJECTS[0], "detail", "<script>project</script>")
    monkeypatch.setitem(content.PUBLICATIONS[0], "title", "<script>publication</script>")
    html = create_app(testing=True).test_client().get("/").get_data(as_text=True)
    assert "&lt;script&gt;" in html
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;project&lt;/script&gt;" in html
    assert "&lt;script&gt;publication&lt;/script&gt;" in html


def test_projects_keep_internal_work_private_and_public_work_linked():
    html = create_app(testing=True).test_client().get("/").get_data(as_text=True)
    internal = html.split('class="project-card project-card-internal"', 1)[1].split('</article>', 1)[0]
    assert "GOTO" in internal
    assert "Internal / Proprietary" in internal
    assert "Initiated and developed the original framework" in internal
    assert "<a " not in internal
    assert "GOTO (Game Outcome Testing Optimizer)" in internal
    assert "<strong>My role</strong>" in internal
    assert "View on GitHub" not in html
    for url in ("https://github.com/LexC/NuFlow", "https://github.com/LexC/Fraud_Classifier"):
        assert f'class="project-access project-access-link" href="{url}"' in html


def test_project_illustrations_are_mapped_accessible_and_served():
    client = create_app(testing=True).test_client()
    html = client.get("/").get_data(as_text=True)
    section = html.split('id="projects"', 1)[1].split('</section>', 1)[0]
    cards = re.findall(r'<article\b.*?</article>', section, re.DOTALL)
    assert len(cards) == 3
    expected = (
        ("GOTO", "goto-platform.png"),
        ("NuFlow", "nuflow-genomics.png"),
        ("Fraud_Classifier", "fraud-classifier-boundary.png"),
    )
    for card, (name, filename) in zip(cards, expected):
        assert f'>{name}</h3>' in card
        source = f'/static/images/projects/{filename}'
        assert f'src="{source}"' in card
        assert len(re.findall(r'<img\b', card)) == 1
        assert re.search(r'alt="Conceptual [^"]+"', card)
        assert 'loading="lazy"' in card
        assert 'decoding="async"' in card
        assert '<figcaption' not in card
        assert 'My contribution' not in card
        if name == "GOTO":
            assert 'class="project-responsibilities"' in card
        else:
            assert 'Independent Project' in card
            assert 'class="project-responsibilities"' not in card
        response = client.get(source)
        assert response.status_code == 200
        assert response.mimetype == "image/png"
        assert response.data.startswith(b'\x89PNG\r\n\x1a\n')
        width, height = struct.unpack('>II', response.data[16:24])
        assert f'width="{width}" height="{height}"' in card


def test_publications_and_direct_contact_links():
    html = create_app(testing=True).test_client().get("/").get_data(as_text=True)
    for url in (
        "https://doi.org/10.1117/1.NPh.10.1.013510",
        "https://doi.org/10.29384/rbfm.2017.v11.n3.p33",
        "mailto:18586901+LexC@users.noreply.github.com",
        "https://www.linkedin.com/in/alexccrv",
        "https://github.com/LexC",
    ):
        assert f'href="{url}"' in html
    assert "Revista Brasileira de Física Médica" in html
    assert "[Conference award name]" in html
    assert "[Conference, year, and recognition details]" in html
    assert "Netherlands" in html
    assert "Open to relocation" in html
