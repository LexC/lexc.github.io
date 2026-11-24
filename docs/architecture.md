# Site architecture

The portfolio uses Flask and Jinja for local development, Tailwind for CSS, and
Frozen-Flask to export the production site. The deployed site is static and does
not need a running Python server.

See [Development](development.md) for setup and maintenance commands and
[Publishing](publishing.md) for the GitHub Pages workflow.

## File responsibilities

| Location | Responsibility |
| --- | --- |
| `src/portfolio/__init__.py` | Flask application factory, homepage, and original-image route. |
| `src/portfolio/content.py` | Profile, career chapters, expertise, projects, publications, contact details, and content validation. |
| `src/portfolio/templates/base.html` | Shared document metadata, navigation, and footer. |
| `src/portfolio/templates/index.html` | Homepage composition and section order. |
| `src/portfolio/templates/sections/` | Hero, About, Experience, Expertise, Projects, Research, and Contact. |
| `src/portfolio/templates/components/` | Section macros, keyword lists, and reusable SVG icons. |
| `src/portfolio/static/css/theme.css` | Shared colour, typography, spacing, and responsive tokens. |
| `src/portfolio/static/css/shared.css` | Global foundations and reusable components. |
| `src/portfolio/static/css/sections.css` | Section layouts and artwork styling. |
| `src/portfolio/static/css/input.css` | Tailwind entry point and stylesheet imports. |
| `src/portfolio/static/css/site.css` | Generated CSS bundle; ignored by Git. |
| `src/portfolio/static/js/site.js` | Mobile navigation, active-section tracking, and publication-card sizing. |
| `assets/` | Original PNGs; referenced research originals are served at `/assets/`. |
| `src/portfolio/static/images/` | Committed WebP portrait, project images, and research previews. |
| `scripts/optimize_images.py` | Regenerates WebP files from PNG originals. |
| `scripts/build_brand_assets.py` | Regenerates the favicon variants and optimized sharing JPEG. |
| `assets/branding/social-card.png` | Editable/replacement source for the sharing image. |
| `scripts/build.py` | Compiles CSS and exports the static site. |
| `scripts/run-site.ps1` | Windows helper to start or reuse the local Flask preview. |
| `tests/test_site.py` | Rendering, escaping, content, image metadata, and lossless image checks. |
| `tests/test_export.py` | Real exports, local assets, anchors, ARIA references, and output-directory protection. |
| `.github/workflows/pages.yml` | Installs dependencies, builds, tests, and deploys successful `main` builds. |
| `pyproject.toml` | Python package configuration and dependency ranges. |
| `requirements/development.lock` | Resolved Python runtime and development dependencies. |
| `package.json` / `package-lock.json` | CSS commands, npm dependency ranges, and resolved versions. |
| `dist/` | Generated static export; ignored by Git. |

## Boundaries to preserve

- Keep editorial content in `content.py`, presentation in templates, and visual
  tokens in `theme.css`. Reuse section and keyword macros rather than duplicating
  shared markup.
- Preserve Jinja escaping and strict handling of missing template values. Keep
  SVG icons and the portrait frame in the templates.
- Keep the Flask factory and routes small. Build orchestration stays separate,
  import-safe, and usable from any working directory.
- Original PNGs remain the image sources. WebP derivatives are committed so
  ordinary builds do not need to regenerate images. Research cards load previews
  and link to full-resolution originals.
- Keep Python environments, dependency folders, caches, generated CSS, and
  `dist/` out of Git. Commit dependency manifests and locks together.

## Build and validation contract

`python scripts/build.py` compiles CSS and freezes the site into `dist/`. It does
not install dependencies or publish. CSS and export failures return nonzero exit
codes.

`--output` can select an alternative empty or nonexistent directory. Relative
paths resolve from the repository root; only the default `dist/` destination
permits stale-file cleanup. Export tests use temporary directories so they do not
overwrite a developer's preview.

CI uses the same build and tests as local development. Pull requests targeting
`main` run validation. Successful pushes and manual runs on `main` upload the
export and deploy it to the `github-pages` environment when Pages is configured.

## Extending the site

Add structure when it is needed: split content into a package if records grow,
extract repeated templates, or add routes and export checks for new pages. Keep
one compiled stylesheet and the static deployment model unless the product
requires something different. Changes to navigation or layout should also be
checked with a keyboard, on a narrow viewport, and with JavaScript disabled.
