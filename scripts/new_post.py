#!/usr/bin/env python3
"""Start an article on an external post: archive its text privately, write the public record and a draft.

Runs defuddle on the URL (or reads its saved --json output), writes
sources/archive/orig/<slug>.md with the full text, sources/orig/<slug>.md with
the same frontmatter only, and a draft content/posts/<slug>.md. Commits nothing:
commit the private archive first, then this repository.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit

from check_content import PUBLISHED_DATE, public_record


REPO = Path(__file__).resolve().parents[1]
SLUG = re.compile(r"[a-z0-9][a-z0-9-]*")
# Posts and records carry Beijing time, as elsewhere on the site.
LOCAL = timezone(timedelta(hours=8))
DATE_FORMATS = ("%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d %b %Y", "%Y/%m/%d", "%Y.%m.%d")


def run_defuddle(url: str) -> dict:
    command = ["npx", "--yes", "defuddle", "parse", url, "--json", "--md"]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise ValueError(f"defuddle failed: {result.stderr.strip() or result.returncode}")
    return json.loads(result.stdout)


def published_date(value) -> str | None:
    """The page's own publication date as YYYY-MM-DD, or None when defuddle found none."""
    text = str(value or "").strip()
    if match := re.match(r"\d{4}-\d{2}-\d{2}", text):
        return match[0]
    for pattern in DATE_FORMATS:
        try:
            return datetime.strptime(text, pattern).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def author_name(data: dict) -> str | None:
    """defuddle's author, else the page's author meta tag or schema.org author."""
    if isinstance(data.get("author"), str) and data["author"].strip():
        return data["author"].strip()
    for tag in data.get("metaTags") or []:
        if (tag.get("name") or tag.get("property")) in {"author", "article:author", "parsely-author", "dc.creator"}:
            content = (tag.get("content") or "").strip()
            if content and not content.startswith(("http://", "https://")):
                return content
    for item in data.get("schemaOrgData") or []:
        authors = item.get("author") if isinstance(item, dict) else None
        authors = authors if isinstance(authors, list) else [authors]
        names = [entry.get("name") if isinstance(entry, dict) else entry for entry in authors]
        names = [name.strip() for name in names if isinstance(name, str) and name.strip()]
        if names:
            return ", ".join(names)
    return None


def frontmatter(fields: dict) -> str:
    """YAML frontmatter with double-quoted strings, matching the existing records."""
    lines = []
    for key, value in fields.items():
        lines.append(f"{key}: {'null' if value is None else json.dumps(value, ensure_ascii=False)}")
    return "---\n" + "\n".join(lines) + "\n---\n"


def create_post(repo: Path, slug: str, url: str, data: dict, now: datetime,
                published: str | None = None, author: str | None = None) -> list[str]:
    """Write the archive, public record and draft; return notes on fields to check by hand."""
    if not SLUG.fullmatch(slug):
        raise ValueError("slug must use lowercase letters, digits and hyphens")
    archive_dir = repo / "sources/archive/orig"
    if not archive_dir.is_dir():
        raise ValueError("sources/archive/orig is missing; clone blog-sources first: git clone https://github.com/QianKuang8/blog-sources.git sources/archive")
    targets = [archive_dir / f"{slug}.md", repo / "sources/orig" / f"{slug}.md", repo / "content/posts" / f"{slug}.md"]
    if existing := [str(path.relative_to(repo)) for path in targets if path.exists()]:
        raise ValueError(f"already exists: {', '.join(existing)}")
    title = (data.get("title") or "").strip()
    body = (data.get("content") or "").strip()
    if not title or not body:
        raise ValueError("defuddle returned no title or no text; record the URL in sources/failed/failed-sources.md")
    notes = []
    published = published or published_date(data.get("published"))
    if published is None:
        notes.append("published_at is null: confirm the page shows no date, or pass --published YYYY-MM-DD")
    elif not PUBLISHED_DATE.fullmatch(published):
        raise ValueError('--published must be "YYYY-MM-DD", "YYYY-MM" or "YYYY"')
    author = author or author_name(data)
    if author is None:
        notes.append("author is unknown: add the author or publisher to the archive, then rerun scripts/source_record.py")
    description = (data.get("description") or "").strip()
    if not description:
        notes.append("description is empty: summarise the original in the archive frontmatter before publishing")
    domain = (data.get("domain") or "").strip() or urlsplit(url).netloc.removeprefix("www.")
    record = {"title": title, "source_url": url, "domain": domain}
    if author:
        record["author"] = author
    record.update(
        published_at=published, description=description,
        retrieved_at=now.isoformat(timespec="seconds"), extractor="defuddle",
    )
    archived = frontmatter(record) + "\n" + body + "\n"
    stamp = now.isoformat(timespec="seconds")
    draft = (
        f"---\ndate: '{stamp}'\nlastmod: '{stamp}'\ndraft: true\n"
        f"title: {json.dumps(title, ensure_ascii=False)}\n"
        'summary: ""\ndescription: ""\ntags: []\ncategories: ["好文分享"]\n'
        'author: "Qian"\nisCJKLanguage: true\nshowToc: true\n---\n\n'
        f"<!-- 依据 sources/archive/orig/{slug}.md 写解读，标准见 BLOG_PROMPTS.md；发布前删去这行注释和 draft，并换成中文标题。 -->\n\n"
        f"## 原文\n\n- [{title}{f' — {author}' if author else ''}]({url})\n"
    )
    for path, text in zip(targets, (archived, public_record(archived), draft)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="article slug, shared by the post, record and archive")
    parser.add_argument("url", help="original article URL")
    parser.add_argument("--from-json", type=Path, help="read saved `defuddle parse --json --md` output instead of running defuddle")
    parser.add_argument("--published", help="the page's own publication date when defuddle misses it (YYYY-MM-DD, YYYY-MM or YYYY)")
    parser.add_argument("--author", help="author or publisher when defuddle misses it")
    args = parser.parse_args()
    try:
        data = json.loads(args.from_json.read_text(encoding="utf-8")) if args.from_json else run_defuddle(args.url)
        notes = create_post(REPO, args.slug, args.url, data, datetime.now(LOCAL), args.published, args.author)
    except (OSError, ValueError) as exc:
        print(f"new_post: {exc}", file=sys.stderr)
        return 1
    for path in (f"sources/archive/orig/{args.slug}.md", f"sources/orig/{args.slug}.md", f"content/posts/{args.slug}.md"):
        print(f"wrote {path}")
    for note in notes:
        print(f"check: {note}")
    print(f"next: write the draft, run scripts/build_site.py, then commit sources/archive (orig/{args.slug}.md) before this repository")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
