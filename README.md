# Lex · Alex Carvalho

A Python-first, dark-themed, single-page professional portfolio for Alex de Castro Carvalho, developed using **Flask, Jinja2, Tailwind CSS, and Frozen-Flask**.

## Local development (Windows PowerShell)

Use Python 3.12+ and Node.js 22 (CI uses Python 3.12 and Node.js 22), plus Git.
Run commands from the repository root:

```powershell
git clone https://github.com/LexC/lexc.github.io.git
cd lexc.github.io
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements/development.lock
python -m pip install -e . --no-deps
npm.cmd ci
npm.cmd run css:build
python -m flask --app portfolio:create_app run --debug
```

Visit **http://127.0.0.1:5000**. For live CSS changes, use `npm.cmd run css:watch` in a second terminal. Flask auto-reloads Python and template changes in debug mode. On Linux/macOS use `npm` instead of `npm.cmd`; activate the environment with `source .venv/bin/activate`. If PowerShell activation is unavailable, use `.venv/Scripts/python.exe` directly for Python commands.

## Test and export

```powershell
python scripts/build.py
python -m pytest -q
```

The generated `dist/` directory contains static files suitable for GitHub Pages, with no continuously running Python backend.

For a temporary export, use `python scripts/build.py --output path/to/empty-directory`.
Relative destinations resolve from the repository root. Alternative destinations
must be empty or nonexistent; only the default `dist/` permits stale-file cleanup.
The build compiles CSS before freezing and never installs dependencies or publishes.
Tests exercise this same command with a temporary directory and check assets,
anchors, ARIA references, rendering, content validation, and escaping.

Preview the static output with `python -m http.server 8000 --directory dist`, then
open **http://127.0.0.1:8000**. Check desktop/mobile layout, keyboard menu controls,
Escape returning focus, and navigation with JavaScript disabled after visual changes.

## Architecture

- `src/portfolio/__init__.py`: Flask application factory and homepage route.
- `src/portfolio/content.py`: editable copy, grouped content, and validation.
- `assets/`: shared portrait and design references. Flask serves these at `/assets/`; the static build includes the portrait used by the page. The responsive cyan frame is drawn in SVG in the hero template.
- `src/portfolio/scientific_art.py`: retained deterministic decorative SVG illustration.
- `src/portfolio/templates/`: shared shell, homepage composition, and section templates.
- `src/portfolio/static/css/input.css`: Tailwind and labeled shared/section styles.
- `src/portfolio/static/js/site.js`: mobile menu and active-section navigation.
- `scripts/build.py`: import-safe CSS build and static export.
- `tests/`: rendering and real export checks.
- `.github/workflows/pages.yml`: tests/build validation only, **no publishing**.

See [the architecture plan](docs/architecture-plan.md) for boundaries and future growth.

## Refreshing dependencies

Python dependency ranges live in `pyproject.toml`; resolved runtime/test versions
live in `requirements/development.lock`. To refresh, use a disposable clean virtual
environment with the supported Python version:

```powershell
python -m venv .venv-refresh
.venv-refresh/Scripts/python -m pip install --upgrade ".[dev]"
.venv-refresh/Scripts/python -m pip freeze --exclude pip --exclude lex-portfolio | Set-Content -Encoding ascii requirements/development.lock
```

Review the lock diff, install it into the development environment, reinstall the
editable package with `--no-deps`, and run build/tests. Build-backend dependencies
are managed by pip's isolated build environment. For npm, update dependency ranges
deliberately, run `npm.cmd install` to update `package-lock.json`, then verify with
`npm.cmd ci` and the same build/tests. Commit manifests and locks together.

## Publishing status

**GitHub Pages publishing is deliberately disabled.** Merging code will not automatically deploy the website. Restore a deployment step only when the portfolio is ready for a public launch.

## Editorial notes

The current research/project panels are credible *category summaries*, not publication citations or verified public case studies. Add the actual bibliography, detailed case studies, and verified contact links before launch. The abstract heatmap is original decorative artwork, not a representation of measured biomedical data.
