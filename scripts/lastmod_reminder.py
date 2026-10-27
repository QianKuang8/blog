#!/usr/bin/env python3
"""Remind, without blocking, when a staged article or topic changes its text but keeps lastmod.

AGENTS.md: editing the summary, description or body updates lastmod; title,
tag, category, learning-status and formatting changes keep it. Title-only and
whitespace-only body changes therefore do not trigger a reminder. Run from the
pre-commit hook in scripts/hooks/ (enable with `git config core.hooksPath scripts/hooks`).
"""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys

import yaml

from check_content import FRONTMATTER


TEXT_FIELDS = ("summary", "description")


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout


def split(text: str) -> tuple[dict, str] | None:
    match = FRONTMATTER.match(text)
    if not match:
        return None
    try:
        metadata = yaml.safe_load(match[1])
    except yaml.YAMLError:
        return None
    return (metadata, match[2]) if isinstance(metadata, dict) else None


def reminders(repo: Path) -> list[str]:
    """Staged modifications of posts and topic pages whose text changed while lastmod did not."""
    staged = git(repo, "diff", "--cached", "--name-only", "--diff-filter=M", "--", "content/posts", "content/topics")
    found = []
    for path in staged.splitlines():
        if not path.endswith(".md") or path.endswith("_index.md"):
            continue
        before, after = split(git(repo, "show", f"HEAD:{path}")), split(git(repo, "show", f":{path}"))
        if before is None or after is None or str(before[0].get("lastmod")) != str(after[0].get("lastmod")):
            continue
        changed = [key for key in TEXT_FIELDS if before[0].get(key) != after[0].get(key)]
        if re.sub(r"\s+", " ", before[1]).strip() != re.sub(r"\s+", " ", after[1]).strip():
            changed.append("body")
        if changed:
            found.append(f"{path}: {', '.join(changed)} changed but lastmod did not")
    return found


def main() -> int:
    repo = Path(git(Path.cwd(), "rev-parse", "--show-toplevel").strip())
    found = reminders(repo)
    if found:
        print("lastmod reminder (not blocking):", file=sys.stderr)
        for line in found:
            print(f"  {line}", file=sys.stderr)
        print("  Update lastmod for text changes; keep it for title, tag, category, status or formatting-only edits.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
