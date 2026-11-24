# Branding assets

The site's favicon and link-sharing image use the existing navy/cyan palette.
These assets are committed; ordinary builds only export them.

## Files

- `scripts/build_brand_assets.py`: source for the SVG favicon and its raster variants.
- `src/portfolio/static/favicon.svg`: browser favicon using the Lex initial and cyan accent.
- `src/portfolio/static/favicon.ico`: 16, 32, 48, and 64 pixel fallback icons, also served at `/favicon.ico`.
- `src/portfolio/static/apple-touch-icon.png`: 180 pixel touch icon.
- `assets/branding/social-card.png`: original sharing-card artwork.
- `src/portfolio/static/images/social-card.jpg`: optimized 1200 by 628 sharing image.

## Updating the assets

After editing the favicon definitions or replacing the source sharing PNG, run
this from the repository root in the development environment:

```powershell
python scripts/build_brand_assets.py
python scripts/build.py
python -m pytest -q
```

The script preserves the sharing artwork's aspect ratio and exports a JPEG with
a maximum edge of 1200 pixels. If its resulting dimensions change, update
`og:image:width` and `og:image:height` in `templates/base.html` too. The test suite
checks that those dimensions match the served file.

The production address lives in `SITE_URL` in `src/portfolio/__init__.py`.
Canonical and sharing URLs use that value even during local preview. Update it
if the public site address changes. Sharing metadata and favicon links live in
`src/portfolio/templates/base.html`. The README badge points to `pages.yml` on
`main`; it reports the whole build-and-deploy workflow, including deployment.

Sharing platforms retrieve the card only after it is deployed and publicly
accessible. Existing link previews may retain a cached image after an update.

## Sharing-card provenance

Created with the built-in image-generation tool, using
`assets/IMG-2026117_ed.png` as the portrait reference. The generated PNG is kept
as the source; the build-assets script only converts and scales that PNG.
No image-generation API is called by the site, its tests, or its build.

Final generation prompt:

> Create a finished website social-sharing card for Alex Carvalho's portfolio, using the supplied portrait as the reference. Wide landscape composition, approximately 1.91:1 aspect ratio, intended for a 1200 by 630 sharing image. Match the existing site's simple professional branding: solid deep navy #001722, crisp white text and restrained cyan #00edf2 accents. Use the existing portrait naturally on the right with a thin cyan frame; preserve the person's identity, face, glasses, hairstyle, expression, clothing and photographic appearance. On the left, large bold clear sans-serif text reading exactly 'Alex Carvalho'. Under it, two clear lines reading exactly 'Scientific thinking.' and 'Engineering execution.' with the second line cyan. A small 'Lex.' wordmark in the upper left and 'lexc.github.io' near the lower left. Preserve generous outer safe margins, clear hierarchy and high contrast so the card reads well at thumbnail size. Flat clean background. No extra claims, badges, employer names, scientific charts, invented icons, browser chrome or other text. This is a complete polished sharing graphic, not a screenshot or mockup.
