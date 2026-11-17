"""Exercise the production build and inspect real exported links."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.references = []
        self.aria = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for key in ("src", "href"):
            if key in attrs:
                self.references.append(attrs[key])
        for key in ("aria-labelledby", "aria-describedby", "aria-controls"):
            self.aria.extend(attrs.get(key, "").split())


def test_export_resolves_local_links(tmp_path):
    subprocess.run([sys.executable, str(ROOT / "scripts/build.py"), "--output", str(tmp_path)],
                   cwd=tmp_path, check=True)
    index = tmp_path / "index.html"
    document = Document(index.read_text(encoding="utf-8"))
    assert len(document.ids) == len(set(document.ids))
    assert set(document.aria) <= set(document.ids)
    for reference in document.references:
        url = urlsplit(reference)
        if url.scheme or url.netloc:
            continue
        target = tmp_path / unquote(url.path).lstrip("/") if url.path else index
        if target.is_dir():
            target /= "index.html"
        assert target.is_file() and target.stat().st_size, reference
        if url.fragment:
            assert unquote(url.fragment) in Document(target.read_text(encoding="utf-8")).ids


def test_export_rejects_nonempty_destination(tmp_path):
    sentinel = tmp_path / "keep.txt"
    sentinel.write_text("keep")
    result = subprocess.run([sys.executable, str(ROOT / "scripts/build.py"), "--output", str(tmp_path)],
                            capture_output=True)
    assert result.returncode != 0
    assert sentinel.read_text() == "keep"
