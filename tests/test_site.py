"""Rendering, content, and image checks for the portfolio."""

import re
from io import BytesIO
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
from xml.etree import ElementTree

from PIL import Image
from portfolio import create_app
from portfolio import content
import pytest


def test_homepage_has_one_page_sections():
    app = create_app(testing=True)
    response = app.test_client().get("/")
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    sections = ["about", "experience", "expertise", "projects", "research", "contact"]
    assert re.findall(r'<section[^>]* id="([^"]+)"', html) == sections
    navigation = html.split('<nav class="site-nav"', 1)[1].split('</nav>', 1)[0]
    assert re.findall(r'href="#([^"]+)"', navigation) == sections
    assert re.findall(r'class="section-index">(\d+)</span>', html) == [
        "01", "02", "03", "04", "05", "06"
    ]
    experience = html.split('id="experience"', 1)[1].split('</section>', 1)[0]
    assert re.findall(r'<h3[^>]*>([^<]+)</h3>', experience) == [
        "The Scientist", "The Data Scientist", "The Mathematician", "The Engineer"
    ]
    assert experience.count('class="timeline-dot" aria-hidden="true"') == 4
    assert experience.count('class="timeline-current"') == 1
    assert (
        "I see my career as four chapters, each building on the last, "
        "from scientific investigation to engineering leadership."
    ) in experience
    for text in (
        "2014 – 2020", "2021 – 2023", "2026 – Present",
        "Institute of Physics, University of Campinas",
        "Faculty of Medical Sciences, University of Campinas",
        "Gaming Laboratories International",
        "supporting a 60-person department",
    ):
        assert text in experience
    assert "Four chapters" not in experience
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


def test_favicons_and_sharing_metadata_are_served():
    class Head(HTMLParser):
        def __init__(self, html):
            super().__init__()
            self.meta = {}
            self.links = {}
            self.feed(html)

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "meta":
                self.meta[attrs.get("property") or attrs.get("name")] = attrs.get("content")
            elif tag == "link":
                self.links.setdefault(attrs.get("rel"), []).append(attrs)

    client = create_app(testing=True).test_client()
    head = Head(client.get("/").get_data(as_text=True))
    assert head.links["canonical"][0]["href"] == "https://lexc.github.io/"
    assert head.meta["og:url"] == "https://lexc.github.io/"
    assert head.meta["twitter:card"] == "summary_large_image"
    assert head.meta["og:image"] == head.meta["twitter:image"]
    card_url = urlsplit(head.meta["og:image"])
    assert card_url.scheme == "https" and card_url.netloc == "lexc.github.io"
    response = client.get(card_url.path)
    assert response.status_code == 200 and response.mimetype == "image/jpeg"
    with Image.open(BytesIO(response.data)) as card:
        assert card.size == (int(head.meta["og:image:width"]), int(head.meta["og:image:height"]))
        assert card.width > card.height
    assert len(response.data) < 1_000_000
    assert "Alex Carvalho" in head.meta["og:image:alt"]
    for icon in head.links["icon"] + head.links["apple-touch-icon"]:
        response = client.get(icon["href"])
        assert response.status_code == 200
        if icon.get("type") == "image/svg+xml":
            assert response.mimetype == "image/svg+xml"
            assert ElementTree.fromstring(response.data).tag.endswith("svg")
        else:
            with Image.open(BytesIO(response.data)) as image:
                if icon["rel"] == "apple-touch-icon":
                    assert image.size == (180, 180)
                else:
                    assert {(16, 16), (32, 32), (48, 48)} <= image.info["sizes"]


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
        ("GOTO", "goto-platform.webp"),
        ("NuFlow", "nuflow-genomics.webp"),
        ("Fraud_Classifier", "fraud-classifier-boundary.webp"),
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
        assert response.mimetype == "image/webp"
        with Image.open(BytesIO(response.data)) as image:
            assert image.format == "WEBP"
            width, height = image.size
        assert f'width="{width}" height="{height}"' in card


def test_optimized_images_preserve_pixels_and_link_to_original_figures():
    root = Path(__file__).resolve().parents[1]
    client = create_app(testing=True).test_client()
    html = client.get("/").get_data(as_text=True)
    originals = [("images/portrait.webp", root / "assets/IMG-2026117_ed.png")]
    originals.extend((project["image"], root / "assets/originals/projects" /
                      (Path(project["image"]).stem + ".png")) for project in content.PROJECTS)
    for image_path, original_path in originals:
        response = client.get(f"/static/{image_path}")
        assert response.status_code == 200
        assert response.mimetype == "image/webp"
        assert f'/static/{image_path}' in html
        with Image.open(BytesIO(response.data)) as optimized, Image.open(original_path) as original:
            assert optimized.size == original.size
            assert optimized.convert("RGBA").tobytes() == original.convert("RGBA").tobytes()
        assert len(response.data) < original_path.stat().st_size
    for publication in content.PUBLICATIONS:
        preview = f'/static/{publication["image"]}'
        original = f'/assets/{publication["original_image"]}'
        assert f'href="{original}"' in html
        assert f'src="{preview}"' in html
        response = client.get(preview)
        assert response.status_code == 200
        assert response.mimetype == "image/webp"
        with Image.open(BytesIO(response.data)) as image:
            assert image.size == (publication["image_width"], publication["image_height"])
        original_response = client.get(original)
        assert original_response.status_code == 200
        assert original_response.mimetype == "image/png"
        assert len(response.data) < len(original_response.data)


def test_publications_and_direct_contact_links():
    html = create_app(testing=True).test_client().get("/").get_data(as_text=True)
    for url in (
        "https://doi.org/10.1117/1.NPh.10.1.013510",
        "https://doi.org/10.3390/jal6010011",
        "mailto:alexccvl@outlook.com",
        "https://www.linkedin.com/in/alexccrv",
        "https://github.com/LexC",
    ):
        assert f'href="{url}"' in html
    assert "Journal of Ageing and Longevity" in html
    assert "Scientific Distinctions" in html
    assert "First Author &amp; Oral Presenter" in html
    assert "XXIX Brazilian Congress of Neurology · 2021" in html
    assert "8th BRAINN Congress · 2022" in html
    assert "Netherlands" in html
    assert "Open to relocation" in html
