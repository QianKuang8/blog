#!/usr/bin/env python3
"""Write public metadata records for full-text archives kept in the private source repository."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from check_content import FRONTMATTER


REPO = Path(__file__).resolve().parents[1]


def public_record(text: str) -> str:
    """Keep the frontmatter only; the archived article text stays private."""
    match = FRONTMATTER.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")
    return f"---\n{match[1]}\n---\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slugs", nargs="+", help="article slugs to copy from the private archive")
    parser.add_argument(
        "--archive", type=Path, default=REPO / "sources/archive/orig",
        help="private archive directory (default: sources/archive/orig)",
    )
    args = parser.parse_args()
    for slug in args.slugs:
        source = args.archive / f"{slug}.md"
        try:
            record = public_record(source.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"{source}: {exc}", file=sys.stderr)
            return 1
        (REPO / "sources/orig" / f"{slug}.md").write_text(record, encoding="utf-8")
        print(f"sources/orig/{slug}.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
