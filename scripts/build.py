"""Compile CSS and freeze the portfolio. Run from any working directory."""
import argparse
from pathlib import Path
import shutil
import subprocess

from flask_frozen import Freezer
from portfolio import create_app

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist"


def build(output_dir=None):
    destination = Path(output_dir) if output_dir is not None else DEFAULT_OUTPUT
    if not destination.is_absolute():
        destination = ROOT / destination
    if destination.absolute() == DEFAULT_OUTPUT and (DEFAULT_OUTPUT.is_symlink() or DEFAULT_OUTPUT.is_junction()):
        raise ValueError("dist must not be a symbolic link or junction")
    destination = destination.resolve()
    if destination != DEFAULT_OUTPUT:
        if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
            raise ValueError("Alternative output directory must be empty or nonexistent")
        if destination == ROOT or destination in ROOT.parents:
            raise ValueError("Output must not be the project or an ancestor directory")
    npm = shutil.which("npm.cmd") or shutil.which("npm")
    if not npm:
        raise RuntimeError("npm is required; install Node.js and run npm ci first")
    subprocess.run([npm, "run", "css:build"], cwd=ROOT, check=True)
    app = create_app()
    app.config.update(FREEZER_DESTINATION=str(destination), FREEZER_RELATIVE_URLS=False,
                      FREEZER_REMOVE_EXTRA_FILES=destination == DEFAULT_OUTPUT)
    Freezer(app).freeze()
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Empty export directory (default: project dist/)")
    args = parser.parse_args()
    print(f"Built {build(args.output)}")


if __name__ == "__main__":
    main()
