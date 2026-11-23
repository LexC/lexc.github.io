# Site architecture improvement plan

Status: implemented; final desktop/mobile browser verification is pending.

Verification: the original four tests passed before migration. After migration,
all seven rendering/export tests pass, including in a clean virtual environment
with locked Python dependencies and `npm ci`. Flask route discovery succeeds,
and exported HTML matches the saved baseline apart from inter-tag whitespace.
The browser tool could not attach reliably, so screenshots and interactive
desktop/mobile checks remain unverified. Publishing remains disabled.

## Goal

Organize the portfolio so sections are easy to edit, with a small repository root
and room to grow. Preserve the Flask/Jinja static build, design, section anchors,
and publishing-disabled workflow. Add files and dependencies when needed.

## Proposed structure

```text
README.md                    # Setup and common commands
pyproject.toml               # Python package and dependencies
package.json                 # CSS tooling
package-lock.json            # Locked npm dependencies
.gitignore
.github/workflows/pages.yml  # Validation only
docs/architecture-plan.md
requirements/development.lock  # Locked Python dependencies
scripts/build.py             # CSS compilation and static export
src/portfolio/
  __init__.py                # Application factory and homepage route
  content.py                 # Profile and content grouped by section
  scientific_art.py          # Deterministic SVG illustration
  templates/
    base.html                # Document shell, header, and footer
    index.html               # Homepage composition
    components/
      section.html           # Numbered section shell and accessible heading
      keywords.html          # Shared keyword list
    sections/
      hero.html
      about.html
      experience.html
      research.html
      projects.html
      contact.html
  static/
    css/input.css            # Tailwind and authored stylesheet imports
    css/theme.css            # Shared visual tokens and responsive values
    css/shared.css           # Foundations and reusable components
    css/sections.css         # Section-specific layout and artwork
    css/site.css             # Generated bundle; ignored
    js/site.js               # Navigation behavior
tests/
  test_site.py               # Rendering, content, and route checks
  test_export.py             # Exported HTML and local asset checks
dist/                        # Generated static output; ignored
```

The root holds common project manifests, the README, and Git configuration.
Local environments, dependency folders, caches, generated CSS, and `dist/` stay
ignored. Configure package data for templates and static files, and resolve build
paths independently of the working directory.

## Boundaries

- The homepage template includes one template per section in an explicit order.
  Keep shared page structure in `base.html`; extract header or footer partials
  when they become unwieldy or are reused.
- Group editorial content by section in `content.py`. The route passes it to
  templates. Preserve Jinja escaping for content and restrict trusted SVG markup
  to generated artwork.
- Keep colours, typography, spacing, radii, and shared layout dimensions in
  `theme.css`, including responsive token overrides. Keep global foundations and
  reusable components in `shared.css`; keep section layouts and artwork in
  `sections.css`. Import these through `input.css` and compile one CSS bundle.
  Use the section and keyword macros instead of duplicating their markup.
- Keep the factory and single route together. Keep build orchestration separate
  from runtime code and safe to import. Flask serves development; the exported
  static site is the production artifact.
- Keep tests in a conventional, flat `tests/` directory. Cover observable behavior
  and the exported site rather than duplicating implementation details.

## Implementation sequence

1. **Establish a baseline.** Run existing tests and build; capture desktop and
   mobile views. Record current anchors, asset URLs, and commands.
2. **Organize the tree.** Move application code, templates, and static files into
   `src/portfolio/`, and build orchestration into `scripts/`. Add `pyproject.toml`
   package discovery and dependency declarations, generate the development lock,
   and install the package using the commands below in this same step. Update
   imports, Tailwind paths, Flask configuration, package data, documentation,
   `.gitignore`, and CI together. Preserve section anchors and exported `/static/`
   URLs. Run rendering tests and a full export immediately after the move; verify
   asset links before continuing.
3. **Separate page sections.** Extract the shell and section templates while
   preserving markup, content, and appearance. Group content by section, including
   hardcoded editorial copy. Validate essentials such as required content and
   unique navigation targets, with clear errors. Rerun rendering and export checks
   and compare desktop/mobile output with the baseline before continuing.
4. **Clean up styles and behavior.** Format and label styles, introduce shared
   variables where useful, and name menu and active-section initialization
   functions. Make mobile navigation available without JavaScript and verify
   keyboard behavior with it enabled. Rebuild CSS and compare desktop/mobile
   output; check keyboard and no-JavaScript navigation at this step.
5. **Make builds repeatable.** Commit an npm lock and use `npm ci`. Python
   dependency declarations and the lock introduced in step 2 remain the source
   of truth. Document dependency refresh commands and supported Python/Node
   versions. Verify the complete installation and build from a fresh environment.
6. **Verify the completed migration.** Run pytest and export to a temporary destination.
   Check rendered sections, unique navigation targets, nonempty HTML and referenced
   assets, and fragment links. Check mobile, keyboard, and no-JavaScript navigation
   in a browser. Run applicable automated checks in CI without enabling publishing.

Acceptance: a fresh checkout can install dependencies, run checks, and build a
working static site using documented commands. The site retains its content,
appearance, anchors, and accessibility behavior, with mobile navigation also
available when JavaScript is disabled.

## Planned commands and build contract

These commands describe the intended interface after migration. Run them from
the repository root in an activated virtual environment:

```powershell
python -m pip install -r requirements/development.lock
python -m pip install -e . --no-deps
npm ci
python -m flask --app portfolio:create_app run --debug
```

The lock includes runtime and test dependencies. The editable installation makes
the `src/` package importable without `PYTHONPATH` workarounds; `--no-deps` keeps
runtime dependencies at the versions already installed from the lock. Configure
the package build backend in `pyproject.toml`. Update README and CI to use this
same setup when the package moves, rather than deferring installation changes.

```powershell
python scripts/build.py
python -m pytest -q
python scripts/build.py --output <empty-export-directory>
```

- The default build compiles CSS through `npm run css:build`, then exports into
  the repository's resolved `dist/` directory. Keep `npm run css:watch` available
  for development.
- `--output` selects an alternative destination, with relative paths resolved
  from the repository root. Require an empty or nonexistent alternative directory;
  permit cleanup only of the verified default `dist/` destination. This prevents
  stale output without deleting unrelated files.
- Expose an import-safe `build(output_dir=None)` function in `scripts/build.py`
  and keep CLI execution behind a `main()` guard. Pass the resolved destination
  to Frozen-Flask, rather than freezing into a hardcoded location.
- Run subprocesses from the repository root and propagate CSS/export failures
  as nonzero exit codes. The build must not install dependencies or publish.
- Export tests invoke the script with `--output` pointing to pytest's `tmp_path`,
  then inspect the generated HTML and assets. This exercises the same build path
  used locally and in CI without overwriting a developer's `dist/` directory.
- CI installs locked dependencies and the package, runs the build and pytest,
  and keeps publishing disabled. Verification occurs throughout the migration;
  the final step confirms the complete workflow.

## When the site grows

These are options, not work to implement or empty files to create now:

- Split `content.py` into a package if sections acquire enough records or editing
  logic to make one file difficult to navigate.
- Split `sections.css` further if individual section rules become hard to
  maintain; retain the shared theme and one compiled bundle. Extract template
  components when reused.
- Move routes into their own module if additional pages need them. Add detail
  templates and export checks when verified projects or publications warrant pages.
- Group tests into unit, integration, or browser directories when their number
  makes a flat directory inconvenient. Add browser automation when interaction
  complexity justifies its dependency and maintenance.
- Add canonical URLs, a sitemap, and hosting-specific base-path configuration
  when the public URL and deployment requirements are confirmed. Publishing
  remains a separate decision.

Implement in small reviewable steps and compare rendered output after markup or
style changes. Avoid speculative content fields or infrastructure for the current
portfolio.
