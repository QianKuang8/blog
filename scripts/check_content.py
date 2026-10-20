#!/usr/bin/env python3
"""Check publishable Markdown, source records, and the local PDF git history."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import filecmp
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

import yaml


FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)(.*)\Z", re.S)
LEARNING_STATUSES = {"pending", "done"}
PDF_REPOSITORY = "https://github.com/QianKuang8/blog-pdfs/blob/"
# Post frontmatter keys that the templates or Hugo read (compared case-insensitively).
POST_KEYS = {
    "date", "lastmod", "title", "summary", "description", "tags", "categories", "author",
    "iscjklanguage", "showtoc", "learning_status", "draft", "slug", "aliases",
    "publishdate", "expirydate", "weight", "hidemeta", "hidesummary", "hideauthor",
    "showreadingtime", "disableanchoredheadings",
    "robotsnoindex", "canonicalurl", "images", "cover", "searchhidden", "hiddeninhomelist",
}


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
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError("missing YAML frontmatter")
    metadata = yaml.load(match[1], Loader=UniqueKeyLoader)
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return metadata, match[2]


def post_paths(repo: Path) -> list[Path]:
    return [path for path in sorted((repo / "content/posts").rglob("*.md")) if path.name != "_index.md"]


def post_slug(path: Path, metadata: dict) -> str:
    return metadata.get("slug") or (path.parent.name if path.stem == "index" else path.stem)


def load_categories(repo: Path) -> dict[str, dict]:
    """Ordered category settings; display labels come from each category's _index.md title."""
    data = json.loads((repo / "data/categories.json").read_text(encoding="utf-8"))
    categories = {}
    for entry in data["categories"]:
        index = repo / "content/categories" / entry["term"] / "_index.md"
        label = read_markdown(index)[0].get("title") if index.is_file() else None
        categories[entry["term"]] = {**entry, "label": label or entry["term"]}
    return categories


def site_prefix(base_url: str) -> str:
    return urlsplit(base_url).path.rstrip("/")


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


def without_code(body: str) -> str:
    """Drop comments, fenced and inline code so examples never count as links."""
    body = re.sub(r"<!--(?:.*?-->|.*\Z)", "", body, flags=re.S)
    body = re.sub(r"(?ms)^ {0,3}(`{3,}|~{3,}).*?^ {0,3}\1[^\n]*(?:\n|$)", "", body)
    body = re.sub(r"<(code|pre|script|style|template)\b[^>]*>.*?</\1\s*>", "", body, flags=re.I | re.S)
    return re.sub(r"(?<!`)(`+)(?!`)(.*?)\1(?!`)", "", body, flags=re.S)


def linked_urls(body: str) -> list[str]:
    # The generated HTML is checked separately after Hugo has applied its full
    # Markdown rules. This pre-build check supports inline and reference links.
    body = without_code(body)
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


class ImageParser(HTMLParser):
    """Collect (alt, src) for <img> tags outside inert HTML content."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.images: list[tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            values = dict(attrs)
            self.images.append((values.get("alt") or "", values.get("src") or ""))


def figures(body: str) -> list[tuple[str, str, bool]]:
    """(alt, destination, captioned) for each image; captioned means the next paragraph is italic."""
    lines = without_code(body).splitlines()
    found = []
    for index, line in enumerate(lines):
        following = next((text.strip() for text in lines[index + 1:] if text.strip()), "")
        captioned = bool(re.fullmatch(r"(\*|_)(?!\1).*\S\1", following))
        for match in re.finditer(r"!\[([^\]\n]*)\]\(\s*<?([^\s)>]+)>?(?:\s+[\"'][^\n]*?[\"'])?\s*\)", line):
            found.append((match[1], match[2], captioned))
        parser = ImageParser()
        parser.feed(line)
        found.extend((alt, src, captioned) for alt, src in parser.images)
    return found


def image_file(repo: Path, destination: str) -> Path:
    return repo / "static" / unquote(urlsplit(destination).path).lstrip("/")


def local_destinations(body: str) -> list[str]:
    """Root-relative link and image destinations written in Markdown or HTML."""
    body = without_code(body)
    return [
        *re.findall(r"\]\(\s*<?(/[^\s)>]*)", body),
        *re.findall(r"""(?:href|src)\s*=\s*["'](/[^"']*)""", body),
    ]


def validate_content(repo: Path, site_dir: Path | None = None, base_url: str | None = None) -> list[str]:
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
        site_url = urlsplit(base_url or config["baseURL"])
        prefix = site_prefix(site_url.geturl())
    except (OSError, KeyError, TypeError, yaml.YAMLError) as exc:
        return [f"config/_default/config.yaml: cannot read baseURL: {exc}"]
    try:
        categories = load_categories(repo)
        tag_groups = json.loads((repo / "data/tag_groups.json").read_text(encoding="utf-8"))
    except (OSError, KeyError, TypeError, ValueError, yaml.YAMLError) as exc:
        return [f"data/: cannot read category or tag settings: {exc}"]
    registered_tags = [*tag_groups.get("sources", []), *tag_groups.get("other", [])]
    for group in tag_groups.get("topics", []):
        registered_tags.extend([*group.get("tags", []), *group.get("details", [])])
    if len(registered_tags) != len(set(registered_tags)):
        failures.append("data/tag_groups.json: a tag is registered in more than one group")
    retired_tags = set(tag_groups.get("retired", []))
    referenced_sources: set[Path] = set()

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

    def check_record(source: Path, record: dict, body: str) -> None:
        required_text(source, record, ("title", "source_url"))
        retrieved = date_field(source, record, "retrieved_at")
        if retrieved and retrieved > datetime.now(timezone.utc):
            fail(source, "retrieved_at must not be in the future")
        if not is_http_url(record.get("source_url")):
            fail(source, "source_url must be an absolute HTTP(S) URL")
        if source.parent.name == "video" or record.get("source_type") == "book":
            if not body.strip():
                fail(source, "source record body must not be empty")
        elif body.strip():
            fail(source, "keep only metadata here; store the article text in the private archive (sources/archive/orig/)")

    def check_image_sources(source: Path, record: dict) -> set[str]:
        """Validate image provenance entries and return the image paths they cover."""
        entries = record.get("image_sources", [])
        if not isinstance(entries, list) or any(not isinstance(entry, dict) for entry in entries):
            fail(source, "image_sources must be a list of mappings")
            return set()
        paths = set()
        for number, entry in enumerate(entries, 1):
            label = f"image_sources[{number}]"
            for key in ("title", "path", "method"):
                if not isinstance(entry.get(key), str) or not entry[key].strip():
                    fail(source, f"{label}.{key} must be a nonempty string")
            if not is_http_url(entry.get("source_url")):
                fail(source, f"{label}.source_url must be an absolute HTTP(S) URL")
            try:
                if aware_datetime(entry.get("retrieved_at")) > datetime.now(timezone.utc):
                    fail(source, f"{label}.retrieved_at must not be in the future")
            except (ValueError, TypeError) as exc:
                fail(source, f"{label}.retrieved_at must be an ISO 8601 datetime with a timezone ({exc})")
            path = entry.get("path")
            if not isinstance(path, str) or not path.strip():
                continue
            if not path.startswith("/images/"):
                fail(source, f"{label}.path must start with /images/")
            elif not image_file(repo, path).is_file():
                fail(source, f"{label}.path does not exist: static{path}")
            paths.add(path)
        return paths

    def video_links(post: Path, urls: list[str], expected_site_path: str, pdf_path: str, source_url, context: str = "") -> list[str]:
        parsed_urls = []
        for url in urls:
            try:
                parsed_urls.append((url, urlsplit(url)))
            except ValueError:
                fail(post, f"{context}malformed link URL: {url}")
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

    posts = post_paths(repo)
    if not posts:
        return ["content/posts: no Markdown articles found"]
    for post in posts:
        result = read(post)
        if result is None:
            continue
        data, body = result
        if "draft" in data and not isinstance(data["draft"], bool):
            fail(post, "draft must be a YAML boolean")
        terms = data.get("categories")
        slug = post_slug(post, data)
        if isinstance(terms, list) and len(terms) == 1 and isinstance(terms[0], str) and categories.get(terms[0], {}).get("source") and isinstance(slug, str):
            referenced_sources.add(repo / "sources" / categories[terms[0]]["source"] / f"{slug}.md")
        if data.get("draft") is True:
            continue
        unknown = sorted(key for key in data if str(key).lower() not in POST_KEYS)
        if unknown:
            fail(post, f"unknown frontmatter keys {unknown}; remove them, or add them to POST_KEYS in scripts/check_content.py when a template reads them")
        if "learning_status" in data and (
            not isinstance(data["learning_status"], str) or data["learning_status"] not in LEARNING_STATUSES
        ):
            fail(post, "learning_status must be pending or done; omit the field for an unmarked article")
        required_text(post, data, ("title", "summary", "description", "author"))
        if not body.strip():
            fail(post, "article body must not be empty")
        if prefix:
            for destination in local_destinations(body):
                if destination == prefix or destination.startswith(f"{prefix}/"):
                    fail(post, f"link {destination} hardcodes the site path {prefix}; write it relative to the site root")
        images = figures(body)
        for alt, destination, _ in images:
            if not alt.strip():
                fail(post, f"image {destination} needs descriptive alt text")
            if not destination.startswith("/images/"):
                fail(post, f"image {destination} must be stored under static/images/ and written as /images/...")
            elif not image_file(repo, destination).is_file():
                fail(post, f"image file is missing: static{unquote(urlsplit(destination).path)}")
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
        else:
            if retired_tags.intersection(tags):
                fail(post, f"retired tags are no longer assigned: {sorted(retired_tags.intersection(tags))}")
            if set(tags) - set(registered_tags):
                fail(post, f"register new tags in data/tag_groups.json: {sorted(set(tags) - set(registered_tags))}")
        if not isinstance(terms, list) or len(terms) != 1 or not isinstance(terms[0], str) or terms[0] not in categories:
            fail(post, f"categories must be a list containing exactly one of {', '.join(categories)}")
            continue
        source_dir = categories[terms[0]].get("source")
        if not source_dir:
            continue
        for _, destination, captioned in images:
            if not captioned:
                fail(post, f"image {destination} needs an italic caption paragraph right after it, stating what it shows and where it comes from")
        if not isinstance(slug, str) or not re.fullmatch(r"[^/\\.][^/\\]*", slug):
            fail(post, "slug must be a single nonempty path segment")
            continue
        source = repo / "sources" / source_dir / f"{slug}.md"
        result = read(source)
        if result is None:
            continue
        record, source_body = result
        check_record(source, record, source_body)
        own_recorded = check_image_sources(source, record)
        recorded = set(own_recorded)
        related = record.get("related_sources", [])
        if not isinstance(related, list) or any(not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name) for name in related):
            fail(source, "related_sources must be a list of source record slugs")
            related = []
        for name in related:
            related_source = source.parent / f"{name}.md"
            referenced_sources.add(related_source)
            related_result = read(related_source)
            if related_result is not None:
                check_record(related_source, *related_result)
                recorded |= check_image_sources(related_source, related_result[0])
        source_url = record.get("source_url")
        if source_dir == "orig":
            required_text(source, record, ("domain", "description", "extractor"))
            used = {destination for _, destination, _ in images if destination.startswith("/images/")}
            for destination in sorted(used - recorded):
                fail(post, f"image {destination} is missing from image_sources in {source.relative_to(repo)}; for articles, record it in the private archive and run scripts/source_record.py")
            for path in sorted(own_recorded - used):
                fail(source, f"image_sources lists {path}, but the article does not use it")
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
        github_links = video_links(post, linked_urls(body), f"/pdfs/{pdf_path}", pdf_path, source_url)
        if site_dir is not None:
            output_page = site_dir / "posts" / slug / "index.html"
            if output_page.is_file():
                github_links.extend(video_links(
                    post, html_linked_urls(output_page.read_text(encoding="utf-8")),
                    f"{prefix}/pdfs/{pdf_path}", pdf_path, source_url, "rendered page: ",
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
    for record_path in list(referenced_sources):
        try:
            related = read_markdown(record_path)[0].get("related_sources") or []
        except (OSError, ValueError, TypeError, yaml.YAMLError):
            continue
        if isinstance(related, list):
            referenced_sources.update(record_path.parent / f"{name}.md" for name in related if isinstance(name, str))
    for source_dir in sorted({entry["source"] for entry in categories.values() if entry.get("source")}):
        for record in sorted((repo / "sources" / source_dir).glob("*.md")):
            if record not in referenced_sources:
                fail(record, "no article uses this source record; delete it or list it in related_sources")
    referenced_images = {
        unquote(urlsplit(destination).path)
        for page in (repo / "content").rglob("*.md")
        for _, destination, _ in figures(page.read_text(encoding="utf-8"))
    }
    for image in sorted((repo / "static/images").rglob("*")):
        if image.is_file() and f"/{image.relative_to(repo / 'static').as_posix()}" not in referenced_images:
            fail(image, "no page uses this image; delete it or reference it from an article")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, help="also compare generated PDF bytes")
    parser.add_argument("--base-url", help="the baseURL the site was built with (default: config baseURL)")
    args = parser.parse_args()
    failures = validate_content(Path(__file__).resolve().parents[1], args.site_dir, args.base_url)
    if failures:
        print("Content validation failed:\n" + "\n".join(f"- {failure}" for failure in failures))
        return 1
    print("Content validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
