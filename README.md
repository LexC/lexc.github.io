# Lex Portfolio

[![Build and deploy portfolio](https://github.com/LexC/lexc.github.io/actions/workflows/pages.yml/badge.svg?branch=main)](https://github.com/LexC/lexc.github.io/actions/workflows/pages.yml)

Source code for Alex Carvalho's personal website, configured for deployment to
[lexc.github.io](https://lexc.github.io/).

The project uses Flask and Jinja2 for local development and Frozen-Flask to export
a static website. Tailwind compiles the styles, and a small JavaScript layer
handles navigation and publication-card sizing. The deployed site does not require
a Python server.

## Technology

| Component | Tool |
| --- | --- |
| Application and templates | Python, Flask, Jinja2 |
| Styles | Tailwind CSS and custom CSS |
| Static export | Frozen-Flask |
| Image optimization | Pillow and WebP |
| Tests | pytest |
| Build and deployment | GitHub Actions and GitHub Pages |

## Requirements

- Python 3.12 or later
- Node.js 22 and npm
- Git

## Quick start

Run from PowerShell:

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

Open **http://127.0.0.1:5000**. For live stylesheet updates, run
`npm.cmd run css:watch` in a second terminal.

On Linux/macOS, activate with `source .venv/bin/activate` and use `npm` in place
of `npm.cmd`. See the [development guide](docs/development.md) for setup details
and the PowerShell activation fallback.

## Build and test

With the virtual environment activated:

```powershell
python scripts/build.py
python -m pytest -q
```

The build compiles CSS and writes the static site to `dist/`. To preview it:

```powershell
python -m http.server 8000 --directory dist
```

Open **http://127.0.0.1:8000**. Generated CSS and `dist/` are ignored by Git.

## Repository structure

```text
src/portfolio/     Flask application, content, templates, styles, scripts, and web images
assets/            Original portrait, project artwork, and research figures
scripts/           Static build and image optimization commands
tests/             Rendering, image, and static export checks
requirements/      Locked Python dependencies
.github/workflows/ Build, test, and GitHub Pages deployment
docs/              Development, architecture, and publishing guides
```

## Deployment

The GitHub Actions workflow builds and tests pull requests targeting `main`.
Successful pushes and manual workflow runs on `main` deploy `dist/` to GitHub
Pages once hosting is configured. See [Publishing](docs/publishing.md) for setup.

## Documentation

- [Development and maintenance](docs/development.md): local setup, content edits,
  styles, images, and dependency updates.
- [Architecture](docs/architecture.md): file responsibilities and build boundaries.
- [Publishing](docs/publishing.md): GitHub Pages configuration and deployment.
