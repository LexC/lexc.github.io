# Publishing to GitHub Pages

The site exports to static files and can use GitHub Pages with a public repository
on GitHub Free. Use the included `lexc.github.io` address; a purchased domain and
a paid Python server are not required.

See [development](development.md) for local build and preview commands and
[GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
for hosting availability.

The workflow publishes the generated `dist/` directory to **https://lexc.github.io/**.
Pull requests run the build and tests without publishing. Pushes to `main` and
manual runs on `main` deploy only after both the build and tests succeed.

One-time GitHub setup:

1. Open the repository's **Settings → Pages**.
2. Under **Build and deployment → Source**, select **GitHub Actions**.
   Use the workflow already in this repository; no additional template is needed.
3. Commit and push the launch changes to `main`.
4. Open **Actions → Build and deploy portfolio** and wait for the `build` and
   `deploy` jobs to succeed. The deployment summary links to the live site.

If you enabled Pages after the initial push, open **Actions → Build and deploy
portfolio → Run workflow**, choose `main`, and run it again. If the `github-pages`
environment requires approval, approve the pending deployment in that run.

Future pushes to `main` update the live site automatically. Generated CSS and
`dist/` remain ignored; commit the source files, not the export. Deployment uses
GitHub's built-in token and does not require a personal access token or added secrets.

## Before publishing changes

- Review the content, contact links, and any employer or research descriptions.
- Run the build and tests described in [development](development.md).
- If making a private repository public, review the tracked files and history first.
- For image updates, include both original sources and regenerated WebP assets.
