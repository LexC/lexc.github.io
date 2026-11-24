# Developing and maintaining the site

Start here to run the portfolio locally, update its content, and prepare changes.
Commands run from the repository root. Use an activated virtual environment after
the initial setup.

For file responsibilities, see [Architecture](architecture.md). For hosting, see
[Publishing](publishing.md).

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

Visit **http://127.0.0.1:5000**. For live CSS changes, use `npm.cmd run css:watch`
in a second terminal. Flask auto-reloads Python and template changes in debug mode.

On Linux/macOS use `npm` instead of `npm.cmd`; activate the environment with
`source .venv/bin/activate`. If PowerShell activation is unavailable, use
`.venv/Scripts/python.exe` directly for Python commands.

## Build, test, and preview

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

## Editing content

The homepage keeps the hero above six sections: About, Experience, Expertise,
Projects, Research, and Contact. Update portfolio content in
`src/portfolio/content.py`:

- `PROFILE` holds the existing hero, About, and section introductions.
- `EXPERIENCE` holds the four career chapters; `EXPERTISE` holds the About icon
  labels. `EXPERTISE_CATEGORIES` holds the separate capability cards.
- `PROJECTS` holds categories, descriptions, keywords, and optional public URLs.
  GOTO is internal/proprietary and has no public source or demo link. Keep its
  description at the approved professional-summary level.
  Its illustrated cards use the supplied artwork in
  `src/portfolio/static/images/projects/`; image paths, dimensions, and alt text
  are editable in each project record.
- `PUBLICATIONS` holds the selected paper titles, journals, years, DOI links,
  preview images, and links to the original figures.
- `EXPERTISE_CATEGORIES` holds the six capability domains, outline icons, and ten
  technical keywords per domain, rendered as a responsive six-card grid.
- `CONTACT` holds email, LinkedIn, location, and relocation information; the
  GitHub profile URL remains in `PROFILE`.

`RESEARCH` holds the research narrative, scientific distinctions, and contribution
metrics. `PUBLICATIONS` also includes author credit and research-topic tags.

## Design and templates

Change visual values in `src/portfolio/static/css/theme.css`. All sections use
the same semantic roles (for example, `--color-accent`, `--font-body`,
`--text-body`, and `--text-section-title`); responsive values are overridden
there too. Use `rem` for text so browser font preferences remain effective.

Reuse `.card-title`, `.body-copy`, `.section-lead`, `.button`, `.text-link`, and
`.keyword-list` from `shared.css` when adding content. Keep section-specific
grids and artwork in `sections.css`, using theme variables for their visual
values instead of introducing local colour or typography constants.

Use the `section` macro in `templates/components/section.html` for each numbered
section. It owns the container, heading, number, and accessible heading reference.
Use `section_body` from the same component for the main column and its optional
introduction. Use `components/keywords.html` for keyword lists. Keep shared header/footer
structure in `base.html`. Rebuild with `npm.cmd run css:build` (or use
`css:watch`); `site.css` is generated and should not be edited directly.

## Updating images

Keep original project illustrations in `assets/originals/projects/`, the original
portrait in `assets/IMG-2026117_ed.png`, and full-resolution research figures in
`assets/`. After changing an original, regenerate the web images:

```powershell
python scripts/optimize_images.py
```

Pillow is included in the development dependencies. The script preserves the
portrait and project pixels with lossless compression and makes research previews
no larger than 1600 pixels on either side. It prints each output's dimensions;
keep the corresponding width and height in `content.py` in sync. Commit both the
originals and regenerated WebP files. A normal site build uses those committed
files and does not run image optimization.

## Branding and sharing

For the favicon and social sharing image, see [Branding assets](branding.md).

## Updating dependencies

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
