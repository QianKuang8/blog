#!/usr/bin/env python3
"""Build and validate a clean production site, then replace public/."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile

from check_content import validate_content


def build_site(repo: Path, base_url: str | None = None) -> None:
    repo = repo.resolve()
    destination = repo / "public"
    if destination.is_symlink() or (destination.exists() and not destination.is_dir()):
        raise ValueError("public must be a directory, not a symlink or file")
    failures = validate_content(repo)
    if failures:
        raise ValueError("Content validation failed:\n" + "\n".join(f"- {failure}" for failure in failures))
    # Keep staging beside public so renames stay on the same filesystem.
    with tempfile.TemporaryDirectory(prefix=".public-build-", dir=repo) as staging:
        staging_path = Path(staging)
        output = staging_path / "site"
        command = ["hugo", "--gc", "--minify", "--environment", "production", "--destination", str(output)]
        if base_url:
            command.extend(["--baseURL", base_url])
        subprocess.run(command, cwd=repo, check=True)
        failures = validate_content(repo, output)
        if failures:
            raise ValueError("Content validation failed:\n" + "\n".join(f"- {failure}" for failure in failures))
        subprocess.run([sys.executable, str(repo / "scripts/check_site.py"), str(output)], cwd=repo, check=True)
        # Leave the last verified output intact if Hugo or either validator fails.
        previous = staging_path / "previous"
        if destination.exists():
            destination.rename(previous)
        try:
            output.rename(destination)
        except OSError:
            if previous.exists():
                previous.rename(destination)
            raise
    print(f"Clean production build validated and published to {destination}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", help="override Hugo baseURL, as required by GitHub Pages")
    args = parser.parse_args()
    try:
        build_site(Path(__file__).resolve().parents[1], args.base_url)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
