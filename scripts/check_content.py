#!/usr/bin/env python3
"""Check publishable Markdown, source records, and the local PDF git history."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import filecmp
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

import yaml


CATEGORIES = {"好文分享", "原创文章", "视频笔记"}
PDF_REPOSITORY = "https://github.com/QianKuang8/blog-pdfs/blob/"


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate keys rather than silently accepting the last value."""


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def read_markdown(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)(.*)\Z", text, re.S)
    if not match:
        raise ValueError("missing YAML frontmatter")
    metadata = yaml.load(match[1], Loader=UniqueKeyLoader)
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return metadata, match[2]


def aware_datetime(value) -> datetime:
    parsed = value if isinstance(value, datetime) else datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("must include a timezone")
    return parsed


def git(path: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def is_http_url(value) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = urlsplit(value)
        return parsed.scheme in {"https", "http"} and bool(parsed.netloc)
    except ValueError:
        return False


class LinkParser(HTMLParser):
    """Collect clickable anchors, excluding examples and inert HTML content."""

    BLOCKED_TAGS = {"code", "pre", "script", "style", "template"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls: list[str] = []
        self.blocked_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.BLOCKED_TAGS:
            self.blocked_depth += 1
        if tag == "a" and not self.blocked_depth:
            href = dict(attrs).get("href")
            if href:
                self.urls.append(href)

    def handle_endtag(self, tag):
        if tag in self.BLOCKED_TAGS and self.blocked_depth:
            self.blocked_depth -= 1


def html_linked_urls(html: str) -> list[str]:
    parser = LinkParser()
    parser.feed(html)
    return parser.urls


def linked_urls(body: str) -> list[str]:
    # The generated HTML is checked separately after Hugo has applied its full
    # Markdown rules. This pre-build check supports inline and reference links.
    body = re.sub(r"<!--(?:.*?-->|.*\Z)", "", body, flags=re.S)
    body = re.sub(r"(?ms)^ {0,3}(`{3,}|~{3,}).*?^ {0,3}\1[^\n]*(?:\n|$)", "", body)
    body = re.sub(r"<(code|pre|script|style|template)\b[^>]*>.*?</\1\s*>", "", body, flags=re.I | re.S)
    body = re.sub(r"(?<!`)(`+)(?!`)(.*?)\1(?!`)", "", body, flags=re.S)
    definitions: dict[str, str] = {}

    def reference_label(label: str) -> str:
        return " ".join(label.split()).casefold()

    def remove_definition(match):
        definitions.setdefault(reference_label(match[1]), match[2])
        return ""

    body = re.sub(
        r"(?m)^ {0,3}\[([^\]\n]+)\]:[ \t]*<?([^\s>]+)>?[^\n]*(?:\n|$)",
        remove_definition, body,
    )
    inline_link = re.compile(r"(?<![\\!])\[[^\]\n]+\]\(\s*<?([^\s)>]+)>?(?:\s+[\"'][^\n]*?[\"'])?\s*\)")
    urls = [*inline_link.findall(body), *html_linked_urls(body), *re.findall(r"<(https?://[^<>\s]+)>", body)]
    references = inline_link.sub("", body)
    for match in re.finditer(r"(?<![\\!])\[([^\]\n]+)\](?:[ \t]*\[([^\]\n]*)\])?", references):
        label = reference_label(match[2] or match[1])
        if label in definitions:
            urls.append(definitions[label])
    return urls


def validate_content(repo: Path, site_dir: Path | None = None) -> list[str]:
    """Return actionable failures; never fetch remote data or modify the checkout.

    Valid YAML drafts (draft: true) may be incomplete. Every other post must
    satisfy publication requirements, including future-dated posts.
    """
    repo = repo.resolve()
    failures: list[str] = []
    pdf_root = repo / "static/pdfs"
    pdf_git_checked = False
    pdf_git_available = False
    try:
        config = yaml.safe_load((repo / "config/_default/config.yaml").read_text())
        site_url = urlsplit(config["baseURL"])
        site_prefix = site_url.path.rstrip("/")
    except (OSError, KeyError, TypeError, yaml.YAMLError) as exc:
        return [f"config/_default/config.yaml: cannot read baseURL: {exc}"]

    def fail(path: Path, message: str) -> None:
        failures.append(f"{path.relative_to(repo)}: {message}")

    def read(path: Path) -> tuple[dict, str] | None:
        try:
            return read_markdown(path)
        except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
            fail(path, str(exc))
            return None

    def required_text(path: Path, data: dict, keys: tuple[str, ...]) -> None:
        for key in keys:
            if not isinstance(data.get(key), str) or not data[key].strip():
                fail(path, f"{key} must be a nonempty string")

    def date_field(path: Path, data: dict, key: str) -> datetime | None:
        try:
            return aware_datetime(data.get(key))
        except (ValueError, TypeError) as exc:
            fail(path, f"{key} must be an ISO 8601 datetime with a timezone ({exc})")
            return None

    def video_links(post: Path, urls: list[str], pdf_path: str, source_url, context: str = "") -> list[str]:
        parsed_urls = []
        for url in urls:
            try:
                parsed_urls.append((url, urlsplit(url)))
            except ValueError:
                fail(post, f"{context}malformed link URL: {url}")
        expected_site_path = f"{site_prefix}/pdfs/{pdf_path}"
        if not any(
            unquote(parsed.path) == expected_site_path
            and parsed.netloc in {"", site_url.netloc}
            and parsed.scheme in {"", "http", "https"}
            for _, parsed in parsed_urls
        ):
            fail(post, f"{context}missing site PDF link: {expected_site_path}")
        # Other PDF links may be useful further reading. Only this article's
        # PDF satisfies its publication contract and undergoes blob comparison.
        github_links = [
            url for url, parsed in parsed_urls
            if url.startswith(PDF_REPOSITORY)
            and unquote(parsed.path).split("/blob/", 1)[1].partition("/")[2] == pdf_path
        ]
        if not github_links:
            fail(post, f"{context}missing fixed GitHub PDF link: {PDF_REPOSITORY}<commit>/{pdf_path}")
        if isinstance(source_url, str) and source_url not in urls:
            fail(post, f"{context}missing original video link matching source_url")
        return github_links

    post_paths = sorted((repo / "content/posts").rglob("*.md"))
    if not post_paths:
        return ["content/posts: no Markdown articles found"]
    for post in post_paths:
        if post.name == "_index.md":
            continue
        result = read(post)
        if result is None:
            continue
        data, body = result
        if "draft" in data and not isinstance(data["draft"], bool):
            fail(post, "draft must be a YAML boolean")
        if data.get("draft") is True:
            continue
        required_text(post, data, ("title", "summary", "description", "author"))
        if not body.strip():
            fail(post, "article body must not be empty")
        published = date_field(post, data, "date")
        modified = date_field(post, data, "lastmod")
        if published and modified and modified < published:
            fail(post, "lastmod must not precede date")
        for key in ("isCJKLanguage", "showToc"):
            if not isinstance(data.get(key), bool):
                fail(post, f"{key} must be a YAML boolean")
        tags = data.get("tags")
        if not isinstance(tags, list) or any(not isinstance(tag, str) or not tag.strip() for tag in tags):
            fail(post, "tags must be a YAML list of nonempty strings (an empty list is allowed)")
        categories = data.get("categories")
        if not isinstance(categories, list) or len(categories) != 1 or not isinstance(categories[0], str) or categories[0] not in CATEGORIES:
            fail(post, "categories must be a list containing exactly one of 好文分享, 原创文章, 视频笔记")
            continue
        category = categories[0]
        if category == "原创文章":
            continue
        slug = data.get("slug", post.parent.name if post.stem == "index" else post.stem)
        if not isinstance(slug, str) or not re.fullmatch(r"[^/\\.][^/\\]*", slug):
            fail(post, "slug must be a single nonempty path segment")
            continue
        source = repo / "sources" / ("video" if category == "视频笔记" else "orig") / f"{slug}.md"
        result = read(source)
        if result is None:
            continue
        record, source_body = result
        required_text(source, record, ("title", "source_url"))
        if not source_body.strip():
            fail(source, "source record body must not be empty")
        retrieved = date_field(source, record, "retrieved_at")
        if retrieved and retrieved > datetime.now(timezone.utc):
            fail(source, "retrieved_at must not be in the future")
        source_url = record.get("source_url")
        if not is_http_url(source_url):
            fail(source, "source_url must be an absolute HTTP(S) URL")
        if category == "好文分享":
            required_text(source, record, ("domain", "description", "extractor"))
            continue
        required_text(source, record, ("channel", "duration", "pdf_path"))
        if record.get("source_type") != "video":
            fail(source, "source_type must be video")
        if not re.fullmatch(r"(?:\d+:)?\d{1,2}:[0-5]\d", str(record.get("duration", ""))):
            fail(source, "duration must use MM:SS or HH:MM:SS")
        pdf_path = record.get("pdf_path")
        if not isinstance(pdf_path, str) or not re.fullmatch(r"(?:standalone|stanford-mse435)/[a-z0-9][a-z0-9-]*\.pdf", pdf_path):
            fail(source, "pdf_path must be standalone/<slug>.pdf or stanford-mse435/<slug>.pdf")
            continue
        pdf = pdf_root / pdf_path
        if not pdf.is_file() or not pdf.resolve().is_relative_to(pdf_root.resolve()):
            fail(source, f"PDF is missing from static/pdfs: {pdf_path}; initialize the PDF submodule")
            continue
        github_links = video_links(post, linked_urls(body), pdf_path, source_url)
        if site_dir is not None:
            output_page = site_dir / "posts" / slug / "index.html"
            if output_page.is_file():
                github_links.extend(video_links(
                    post, html_linked_urls(output_page.read_text(encoding="utf-8")),
                    pdf_path, source_url, "rendered page: ",
                ))
            elif not published or published <= datetime.now(timezone.utc):
                fail(post, f"missing generated video page: posts/{slug}/index.html")
        if not pdf_git_checked:
            pdf_git_checked = True
            try:
                entry = git(repo, "ls-files", "--stage", "static/pdfs")
                if not entry.startswith("160000 ") or Path(git(pdf_root, "rev-parse", "--show-toplevel")).resolve() != pdf_root.resolve():
                    raise ValueError("static/pdfs must be an initialized Git submodule")
                pdf_git_available = True
            except ValueError as exc:
                fail(source, str(exc))
        if pdf_git_available:
            try:
                actual_blob = git(pdf_root, "hash-object", "--", pdf_path)
                if git(pdf_root, "rev-parse", f"HEAD:{pdf_path}") != actual_blob:
                    fail(source, "PDF bytes differ from the PDF submodule HEAD; commit the PDF repository first")
                for url in set(github_links):
                    fixed_path = unquote(urlsplit(url).path).split("/blob/", 1)[1]
                    commit, _, linked_path = fixed_path.partition("/")
                    if linked_path != pdf_path or not re.fullmatch(r"[0-9a-f]{7,40}", commit):
                        fail(post, f"GitHub PDF link must pin a commit and match pdf_path: {url}")
                        continue
                    try:
                        git(pdf_root, "rev-parse", "--verify", f"{commit}^{{commit}}")
                        if git(pdf_root, "rev-parse", f"{commit}:{pdf_path}") != actual_blob:
                            fail(post, f"GitHub PDF link points to different PDF bytes: {url}")
                    except ValueError:
                        fail(post, f"cannot resolve PDF commit/file locally: {commit}:{pdf_path}; if shallow, run git -C static/pdfs fetch --unshallow")
            except ValueError as exc:
                fail(source, str(exc))
        if site_dir is not None:
            output_pdf = site_dir / "pdfs" / pdf_path
            if not output_pdf.is_file() or not filecmp.cmp(pdf, output_pdf, shallow=False):
                fail(source, f"generated PDF is missing or differs from source bytes: pdfs/{pdf_path}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, help="also compare generated PDF bytes")
    args = parser.parse_args()
    failures = validate_content(Path(__file__).resolve().parents[1], args.site_dir)
    if failures:
        print("Content validation failed:\n" + "\n".join(f"- {failure}" for failure in failures))
        return 1
    print("Content validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
