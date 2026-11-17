# Lex · Alex Carvalho

A Python-first, dark-themed, single-page professional portfolio for Alex de Castro Carvalho, developed using **Flask, Jinja2, Tailwind CSS, and Frozen-Flask**.

## Local development (Windows PowerShell)

Install Python 3.12+, Node.js 20+, and Git:

```powershell
git clone https://github.com/LexC/lexc.github.io.git
cd lexc.github.io
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
npm install --no-package-lock
npm run css:build
python app.py
```

Visit **http://127.0.0.1:5000**. For live CSS changes, use `npm run css:watch` in a second terminal. Flask auto-reloads Python and template changes in debug mode.

## Test and export

```powershell
python -m pytest -q
npm run css:build
python freeze.py
```

The generated `dist/` directory contains static files suitable for GitHub Pages, with no continuously running Python backend.

## Architecture

- `app.py`: Flask application factory and route.
- `portfolio_content.py`: professionally relevant copy and editable content models.
- `scientific_art.py`: Python-generated contour-field SVG hero illustration, not scientific measurements.
- `templates/index.html`: one-page Jinja2 template and semantic page sections.
- `static/css/input.css`: Tailwind v4 and the custom charcoal/cyan design system.
- `static/js/site.js`: accessible mobile menu and active-section navigation.
- `freeze.py`: static export for free hosting on GitHub Pages.
- `tests/`: pytest smoke tests.
- `.github/workflows/pages.yml`: tests/build validation only, **no publishing**.

## Publishing status

**GitHub Pages publishing is deliberately disabled.** Merging code will not automatically deploy the website. Restore a deployment step only when the portfolio is ready for a public launch.

## Editorial notes

The current research/project panels are credible *category summaries*, not publication citations or verified public case studies. Add the actual bibliography, detailed case studies, and verified contact links before launch. The abstract heatmap is original decorative artwork, not a representation of measured biomedical data.
