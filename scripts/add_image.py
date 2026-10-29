#!/usr/bin/env python3
"""Add or remove a figure of an external-article post, keeping the record of where it came from.

Adding downloads the image (or copies a local file, such as a chart screenshot
or a redrawn SVG) to static/images/<slug>/<name>.<ext>, taking the extension
from the file's own bytes and leaving the bytes unchanged. It appends an
image_sources entry to the private archive sources/archive/orig/<slug>.md,
regenerates the public record sources/orig/<slug>.md, and prints the Markdown
to paste into the article.

Removing (--remove) deletes the file and its image_sources entry, once no page
uses the figure; --image-note records why the article no longer uses the
original's images. Commits nothing.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys
import textwrap
from urllib.parse import urlsplit
from urllib.request import urlopen

import yaml

from check_content import FRONTMATTER, figures, is_http_url, public_record
from new_post import LOCAL, SLUG


REPO = Path(__file__).resolve().parents[1]
DOWNLOAD_METHOD = "原图文件，未改动"


def image_format(data: bytes) -> str | None:
    """File extension for PNG, JPEG, GIF, WebP or SVG bytes; None for anything else, such as an HTML error page."""
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    if b"<svg" in data[:1024].lower() and data.lstrip(b"\xef\xbb\xbf \t\r\n").startswith((b"<svg", b"<?xml")):
        return "svg"
    return None


def download(url: str) -> bytes:
    with urlopen(url, timeout=60) as response:
        return response.read()


def image_block(lines: list[str]) -> tuple[int, int] | None:
    """Line range of the image_sources key and its block list in the frontmatter lines, or None without one."""
    start = next((index for index, line in enumerate(lines) if re.match(r"image_sources\s*:", line)), None)
    if start is None:
        return None
    value = lines[start].split(":", 1)[1].strip()
    if value and value != "[]":
        raise ValueError("image_sources is not a block list; edit it by hand")
    end = start + 1
    while end < len(lines) and (lines[end][:1] in {" ", "-"} or not lines[end].strip()):
        end += 1
    return start, end


def with_image_source(text: str, entry: dict) -> str:
    """The archive text with entry appended to image_sources, leaving every other line as it was."""
    match = FRONTMATTER.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")
    lines = match[1].split("\n")
    item = [f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in entry.items()]
    block = image_block(lines)
    if block is None:
        lines += ["image_sources:", *(("  - " if index == 0 else "    ") + line for index, line in enumerate(item))]
    else:
        start, end = block
        lines[start] = "image_sources:"
        first = next((line for line in lines[start + 1:end] if line.lstrip().startswith("- ")), "  - ")
        indent = first[:len(first) - len(first.lstrip())]
        lines[end:end] = [(f"{indent}- " if index == 0 else f"{indent}  ") + line for index, line in enumerate(item)]
    updated = text[:match.start(1)] + "\n".join(lines) + text[match.end(1):]
    before, after = yaml.safe_load(match[1]), yaml.safe_load(FRONTMATTER.match(updated)[1])
    if after.pop("image_sources")[-1] != entry or {key: value for key, value in before.items() if key != "image_sources"} != after:
        raise ValueError("could not append to image_sources cleanly; add the entry by hand")
    return updated


def without_image_source(text: str, path: str, note: str | None = None) -> str:
    """The archive text without the image_sources entry for path, with image_note set when given."""
    match = FRONTMATTER.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")
    lines = match[1].split("\n")
    block = image_block(lines)
    starts = [index for index in range(*block) if lines[index].lstrip().startswith("- ")] if block else []
    groups = [range(begin, next((later for later in starts if later > begin), block[1])) for begin in starts]
    matching = [group for group in groups
                if (yaml.safe_load(textwrap.dedent("\n".join(lines[index] for index in group))) or [{}])[0].get("path") == path]
    if len(matching) != 1:
        raise ValueError(f"image_sources has no entry for {path}")
    dropped = set(matching[0]) | ({block[0]} if len(groups) == 1 else set())
    lines = [line for index, line in enumerate(lines) if index not in dropped]
    if note is not None:
        if not note.strip():
            raise ValueError("--image-note must be nonempty")
        lines = [line for line in lines if not line.startswith("image_note:")]
        lines.append(f"image_note: {json.dumps(note.strip(), ensure_ascii=False)}")
    updated = text[:match.start(1)] + "\n".join(lines) + text[match.end(1):]
    before, after = yaml.safe_load(match[1]), yaml.safe_load(FRONTMATTER.match(updated)[1])
    kept = [entry for entry in before["image_sources"] if entry.get("path") != path]
    if note is not None:
        before["image_note"] = note.strip()
    if after.pop("image_sources", []) != kept or {key: value for key, value in before.items() if key != "image_sources"} != after:
        raise ValueError("could not remove the entry cleanly; edit image_sources by hand")
    return updated


def add_image(repo: Path, slug: str, name: str, data: bytes, title: str, source_url: str, method: str, now: datetime) -> tuple[str, dict]:
    """Save the image and record it; return its site path and the archive frontmatter."""
    if not SLUG.fullmatch(slug) or not SLUG.fullmatch(name):
        raise ValueError("slug and name must use lowercase letters, digits and hyphens (name has no extension)")
    if not title.strip() or not method.strip():
        raise ValueError("--title and --method must be nonempty")
    if not is_http_url(source_url):
        raise ValueError("--source-url must be an absolute HTTP(S) URL")
    extension = image_format(data)
    if extension is None:
        raise ValueError("not a PNG, JPEG, GIF, WebP or SVG file (an HTML page or an error?); open the page in a browser, save the image, and pass the file")
    archive = repo / "sources/archive/orig" / f"{slug}.md"
    if not archive.is_file():
        raise ValueError(f"{archive.relative_to(repo)} is missing; run scripts/new_post.py first (book records are edited by hand)")
    target = repo / "static/images" / slug / f"{name}.{extension}"
    if target.exists():
        raise ValueError(f"already exists: {target.relative_to(repo)}")
    path = f"/images/{slug}/{target.name}"
    entry = {"title": title.strip(), "path": path, "source_url": source_url, "method": method.strip(),
             "retrieved_at": now.isoformat(timespec="seconds")}
    text = with_image_source(archive.read_text(encoding="utf-8"), entry)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    archive.write_text(text, encoding="utf-8")
    (repo / "sources/orig" / f"{slug}.md").write_text(public_record(text), encoding="utf-8")
    return path, yaml.safe_load(FRONTMATTER.match(text)[1])


def remove_image(repo: Path, slug: str, name: str, note: str | None = None) -> str:
    """Delete a figure that no page uses, and its image_sources entry; return its site path."""
    archive = repo / "sources/archive/orig" / f"{slug}.md"
    if not archive.is_file():
        raise ValueError(f"{archive.relative_to(repo)} is missing; book records are edited by hand")
    folder = repo / "static/images" / slug
    files = [file for file in folder.glob("*") if name in (file.name, file.stem)] if folder.is_dir() else []
    if len(files) != 1:
        raise ValueError(f"no single image named {name} in static/images/{slug}/")
    path = f"/images/{slug}/{files[0].name}"
    users = [page.relative_to(repo).as_posix() for page in sorted((repo / "content").rglob("*.md"))
             if any(destination == path for _, destination, _ in figures(page.read_text(encoding="utf-8")))]
    if users:
        raise ValueError(f"{path} is still used by {', '.join(users)}; remove the figure and its caption there first, then renumber the remaining captions")
    text = without_image_source(archive.read_text(encoding="utf-8"), path, note)
    archive.write_text(text, encoding="utf-8")
    (repo / "sources/orig" / f"{slug}.md").write_text(public_record(text), encoding="utf-8")
    files[0].unlink()
    if not any(folder.iterdir()):
        folder.rmdir()
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="article slug, shared by the post, record and archive")
    parser.add_argument("name", help="file name without extension, such as mono-before-after (with --remove, the extension may be given)")
    parser.add_argument("source", nargs="?", help="image URL, or a local file such as a chart screenshot or a redrawn SVG")
    parser.add_argument("--title", help="the figure's title in the original, or a short description (required when adding)")
    parser.add_argument("--source-url", help="where the image comes from (default: the image URL; required for a local file)")
    parser.add_argument("--method", help=f"how it was obtained (default for downloads: {DOWNLOAD_METHOD}; required for a local file, e.g. 原页面图表截图)")
    parser.add_argument("--remove", action="store_true", help="delete the figure and its image_sources entry; remove it from the article first")
    parser.add_argument("--image-note", help="with --remove: why the article uses none of the original's images, when that is now the case")
    args = parser.parse_args()
    if args.remove:
        if args.source or args.title or args.source_url or args.method:
            parser.error("--remove takes only the slug, the file name and --image-note")
        try:
            path = remove_image(REPO, args.slug, args.name, args.image_note)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            print(f"add_image: {exc}", file=sys.stderr)
            return 1
        print(f"removed static{path} and its image_sources entry in sources/archive/orig/{args.slug}.md and sources/orig/{args.slug}.md")
        post = REPO / "content/posts" / f"{args.slug}.md"
        if post.is_file() and not figures(post.read_text(encoding="utf-8")) and args.image_note is None:
            print("the article now has no figures: if the original has images, rerun with --image-note or add image_note to the archive")
        return 0
    if not args.source or not args.title:
        parser.error("adding a figure needs the source and --title")
    if args.image_note:
        parser.error("--image-note goes with --remove")
    remote = urlsplit(args.source).scheme in {"http", "https"}
    if not remote and not (args.source_url and args.method):
        parser.error("a local file needs --source-url (the page it comes from) and --method (how it was made)")
    try:
        data = download(args.source) if remote else Path(args.source).read_bytes()
        path, record = add_image(REPO, args.slug, args.name, data, args.title, args.source_url or args.source,
                                 args.method or DOWNLOAD_METHOD, datetime.now(LOCAL))
    except (OSError, ValueError) as exc:
        print(f"add_image: {exc}", file=sys.stderr)
        return 1
    print(f"saved static{path}")
    print(f"recorded image_sources in sources/archive/orig/{args.slug}.md and sources/orig/{args.slug}.md")
    print("paste where the article discusses it; describe the figure in the alt text and number captions in order:\n")
    print(f"![<what the figure shows>]({path})\n")
    link = f"[{record.get('title')}]({record.get('source_url')})"
    origin = f"原图，来源：{link}" if remote else f"<原页面图表截图|局部截取|重绘|本文绘制>，依据 {link} 整理"
    print(f"*图 N：{origin}。<what readers should notice>*")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
