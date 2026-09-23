#!/usr/bin/env python3
"""Validate generated Hugo output for blog-specific SEO and navigation rules."""

from __future__ import annotations

from datetime import date, datetime
from functools import lru_cache
from html.parser import HTMLParser
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlsplit
from xml.etree import ElementTree

import yaml

from check_content import aware_datetime, read_markdown


SITE_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("public")
ARTICLE_CATEGORIES = {
    "好文分享": "categories/好文分享/index.html",
    "原创文章": "categories/原创文章/index.html",
    "视频笔记": "categories/视频笔记/index.html",
}
CATEGORY_LABELS = {
    "好文分享": "阅读与解读",
    "原创文章": "研究与实践",
    "视频笔记": "视频笔记",
}
HOME_CATEGORY_ORDER = ("原创文章", "好文分享", "视频笔记")


def class_names(attributes: dict[str, str | None]) -> set[str]:
    return set((attributes.get("class") or "").split())


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.json_ld_scripts: list[str] = []
        self.links: list[tuple[dict[str, str | None], str]] = []
        self.references: list[tuple[str, str, str]] = []
        self.canonical_url: str | None = None
        self.canonical_urls: list[str] = []
        self.post_meta: list[str] = []
        self.post_meta_fields: set[str] = set()
        self.main_menu_links: list[tuple[dict[str, str | None], str]] = []
        self.meta: list[dict[str, str | None]] = []
        self.headings: list[tuple[str, str]] = []
        self.class_counts: dict[str, int] = {}
        self.post_tag_labels: list[str | None] = []
        self.tag_groups: list[str] = []
        self.post_entries: list[dict[str, object]] = []
        self.learning_groups: list[dict[str, object]] = []
        self.learning_controls: list[dict[str, str | None]] = []
        self._learning_containers: list[dict[str, object] | None] = []
        self._link_learning_containers: list[dict[str, object]] = []
        self._json_ld_parts: list[str] | None = None
        self._link_attrs: dict[str, str | None] | None = None
        self._link_parts: list[str] = []
        self._link_in_main_menu = False
        self._link_post_entry: dict[str, object] | None = None
        self._heading_tag: str | None = None
        self._heading_parts: list[str] = []
        self._main_menu_depth = 0
        self._main_menu_tag: str | None = None
        self._post_meta_depth = 0
        self._post_meta_parts: list[str] = []
        self._article_depth = 0
        self._post_entry_contexts: list[tuple[int, dict[str, object]]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        classes = class_names(attributes)
        if {"data-learning-record", "data-learning-status", "data-learning-edit", "data-learning-back"}.intersection(attributes):
            self.learning_controls.append(attributes)
        for class_name in classes:
            self.class_counts[class_name] = self.class_counts.get(class_name, 0) + 1
        if attributes.get("data-tag-group"):
            self.tag_groups.append(attributes["data-tag-group"])
        if tag == "ul" and "post-tags" in classes:
            self.post_tag_labels.append(attributes.get("aria-label"))

        for attribute in ("href", "src"):
            if attributes.get(attribute) and tag != "base":
                self.references.append((tag, attribute, attributes[attribute]))
        if tag == "link" and "canonical" in (attributes.get("rel") or "").split():
            self.canonical_url = attributes.get("href")
            self.canonical_urls.append(attributes.get("href") or "")
        if tag == "div":
            if self._post_meta_depth:
                self._post_meta_depth += 1
            elif "post-meta" in classes:
                self._post_meta_depth = 1
                self._post_meta_parts = []
        if self._post_meta_depth:
            self.post_meta_fields.update(
                (attributes.get("data-post-meta-fields") or "").split()
            )

        if tag == self._main_menu_tag:
            self._main_menu_depth += 1
        elif tag in {"ul", "nav"} and attributes.get("id") == "menu" and not self._main_menu_depth:
            self._main_menu_tag = tag
            self._main_menu_depth = 1

        if tag in {"section", "details"}:
            container = None
            if "data-learning-group" in attributes:
                container = {"tag": tag, "attrs": attributes, "links": []}
                self.learning_groups.append(container)
            self._learning_containers.append(container)

        if tag == "article":
            self._article_depth += 1
            if "data-post-entry" in attributes:
                entry: dict[str, object] = {
                    "slug": attributes.get("data-post-entry"),
                    "links": [],
                }
                self.post_entries.append(entry)
                self._post_entry_contexts.append((self._article_depth, entry))

        if tag == "script" and attributes.get("type") == "application/ld+json":
            self._json_ld_parts = []
        elif tag == "a":
            self._link_attrs = attributes
            self._link_parts = []
            self._link_in_main_menu = self._main_menu_depth > 0
            self._link_post_entry = self._post_entry_contexts[-1][1] if self._post_entry_contexts else None
            self._link_learning_containers = [item for item in self._learning_containers if item is not None]
        elif tag == "meta":
            self.meta.append(attributes)
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._heading_tag = tag
            self._heading_parts = []

    def handle_data(self, data: str) -> None:
        if self._post_meta_depth:
            self._post_meta_parts.append(data)
        if self._json_ld_parts is not None:
            self._json_ld_parts.append(data)
        if self._link_attrs is not None:
            self._link_parts.append(data)
        if self._heading_tag is not None:
            self._heading_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "div" and self._post_meta_depth:
            self._post_meta_depth -= 1
            if not self._post_meta_depth:
                self.post_meta.append(" ".join("".join(self._post_meta_parts).split()))
        if tag == "script" and self._json_ld_parts is not None:
            self.json_ld_scripts.append("".join(self._json_ld_parts).strip())
            self._json_ld_parts = None
        elif tag == "a" and self._link_attrs is not None:
            link = (self._link_attrs, "".join(self._link_parts).strip())
            self.links.append(link)
            if self._link_in_main_menu:
                self.main_menu_links.append(link)
            if self._link_post_entry is not None and "data-post-link" in self._link_attrs:
                links = self._link_post_entry["links"]
                assert isinstance(links, list)
                links.append(link)
            for container in self._link_learning_containers:
                container["links"].append(link)
            self._link_attrs = None
            self._link_parts = []
            self._link_in_main_menu = False
            self._link_post_entry = None
            self._link_learning_containers = []
        elif tag == self._heading_tag:
            self.headings.append(
                (self._heading_tag, "".join(self._heading_parts).strip())
            )
            self._heading_tag = None
            self._heading_parts = []

        if tag == "article":
            if (
                self._post_entry_contexts
                and self._post_entry_contexts[-1][0] == self._article_depth
            ):
                self._post_entry_contexts.pop()
            self._article_depth = max(0, self._article_depth - 1)
        elif tag == self._main_menu_tag and self._main_menu_depth:
            self._main_menu_depth -= 1
            if not self._main_menu_depth:
                self._main_menu_tag = None
        if tag in {"section", "details"} and self._learning_containers:
            self._learning_containers.pop()


def read_html(relative_path: str) -> str:
    path = SITE_DIR / relative_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


@lru_cache
def parse_html(relative_path: str) -> PageParser:
    parser = PageParser()
    parser.feed(read_html(relative_path))
    return parser


def json_ld(relative_path: str, failures: list[str]) -> list[dict]:
    items = []
    for script in parse_html(relative_path).json_ld_scripts:
        try:
            item = json.loads(script)
        except json.JSONDecodeError as error:
            failures.append(f"{relative_path} should contain valid JSON-LD: {error}")
            continue
        if not isinstance(item, dict):
            failures.append(f"{relative_path} JSON-LD should contain an object")
            continue
        items.append(item)
    return items


def assert_true(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def normalized_url_path(href: str | None) -> str:
    if not href:
        return ""
    return unquote(urlsplit(href).path).rstrip("/")


def url_path_ends_with(href: str | None, suffix: str) -> bool:
    path = normalized_url_path(href)
    normalized_suffix = suffix.strip("/")
    return path == normalized_suffix or path.endswith(f"/{normalized_suffix}")


def source_article_categories(failures: list[str]) -> dict[str, tuple[str, str]]:
    """Keep source taxonomy identity separate from rendered category/type labels."""
    repo = Path(__file__).resolve().parent.parent
    result: dict[str, tuple[str, str]] = {}
    for source in sorted((repo / "content/posts").glob("*.md")):
        if source.stem == "_index":
            continue
        try:
            metadata, _ = read_markdown(source)
            slug = metadata.get("slug") or source.stem
            relative_path = f"posts/{slug}/index.html"
            if not (SITE_DIR / relative_path).is_file():
                continue
            categories = metadata.get("categories")
            if not isinstance(categories, list) or len(categories) != 1 or categories[0] not in ARTICLE_CATEGORIES:
                failures.append(f"{source.name}: should have exactly one supported source category")
                continue
            term = categories[0]
            label = CATEGORY_LABELS[term]
            if term == "好文分享":
                evidence = repo / "sources/orig" / f"{slug}.md"
                evidence_metadata, _ = read_markdown(evidence) if evidence.is_file() else ({}, "")
                label = "书籍导读" if evidence_metadata.get("source_type") == "book" else "文章解读"
            result[relative_path] = (term, label)
        except (OSError, ValueError, TypeError, yaml.YAMLError) as error:
            failures.append(f"{source.name}: cannot validate article category: {error}")
    return result


def validate_article_category(
    relative_path: str,
    page: PageParser,
    categories: dict[str, tuple[str, str]],
    failures: list[str],
) -> None:
    article_types = [
        (attrs, text) for attrs, text in page.links
        if "article-type" in class_names(attrs)
    ]
    assert_true(
        len(article_types) == 1,
        f"{relative_path} should have exactly one article category",
        failures,
    )
    expected = categories.get(relative_path)
    assert_true(expected is not None, f"{relative_path} should identify a source article category", failures)
    if not article_types or expected is None:
        return
    term, label = expected
    attrs, text = article_types[0]
    home_url = parse_html("index.html").canonical_url or ""
    expected_url = urljoin(home_url, f"categories/{quote(term)}/")
    assert_true(
        attrs.get("data-category-term") == term,
        f"{relative_path}: article category identity should match its source ({term})",
        failures,
    )
    assert_true(
        unquote(urljoin(home_url, attrs.get("href") or "")) == unquote(expected_url),
        f"{relative_path}: article category link should target its original category URL",
        failures,
    )
    assert_true(
        text == label,
        f"{relative_path}: article type should be displayed as {label}",
        failures,
    )


def validate_search_category(
    item: dict,
    index: int,
    category_urls: dict[str, str],
    failures: list[str],
) -> None:
    permalink = item.get("permalink")
    expected = category_urls.get(unquote(permalink)) if isinstance(permalink, str) else None
    if expected is not None:
        assert_true(
            item.get("category") == expected,
            f"index.json item {index}: category label should match its source ({expected})",
            failures,
        )
    else:
        assert_true(
            isinstance(permalink, str) and item.get("category") == "专题"
            and "/topics/" in urlsplit(permalink).path,
            f"index.json item {index}: should identify a source article or topic category",
            failures,
        )


def schema_datetime(
    schema: dict, field: str, relative_path: str, failures: list[str]
) -> datetime | None:
    value = schema.get(field)
    try:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("missing date")
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.utcoffset() is None or parsed.year == 1:
            raise ValueError("missing timezone or zero date")
    except ValueError:
        failures.append(
            f"{relative_path} BlogPosting {field} should be a real ISO datetime with timezone"
        )
        return None
    return parsed


def validate_post_meta(
    relative_path: str,
    page: PageParser,
    schema: dict,
    published: datetime | None,
    modified: datetime | None,
    failures: list[str],
) -> None:
    # The article template omits the container when hideMeta is enabled.
    if not page.post_meta:
        return
    text = " ".join(page.post_meta)
    parts = [part.strip() for part in text.split("·")]
    assert_true(
        bool(text) and all(parts),
        f"{relative_path} post-meta should not be empty or contain empty separator items",
        failures,
    )
    fields = page.post_meta_fields
    assert_true(
        bool(fields),
        f"{relative_path} post-meta should declare its enabled data-post-meta-fields",
        failures,
    )
    assert_true(
        fields <= {"date", "updated", "reading-time", "word-count", "author"},
        f"{relative_path} post-meta declares unsupported fields: {sorted(fields)}",
        failures,
    )
    if "date" in fields and published:
        assert_true(
            published.date().isoformat() in parts,
            f"{relative_path} post-meta should show its publication date",
            failures,
        )
    if "updated" in fields and modified:
        assert_true(
            f"更新于 {modified.date().isoformat()}" in parts,
            f"{relative_path} post-meta should show its modification date",
            failures,
        )
    if "reading-time" in fields:
        assert_true(
            any(re.fullmatch(r"\d+\s*(?:分钟|min(?:ute)?s?)", part) for part in parts),
            f"{relative_path} post-meta should show a numeric reading time",
            failures,
        )
    if "word-count" in fields:
        count = str(schema.get("wordCount", ""))
        assert_true(
            count.isdigit()
            and any(
                re.fullmatch(rf"{count}\s*(?:字|words?)", part)
                or (count == "1" and part == "字")
                for part in parts
            ),
            f"{relative_path} post-meta word count should match BlogPosting wordCount",
            failures,
        )
    if "author" in fields:
        authors = schema.get("author", [])
        if isinstance(authors, dict):
            authors = [authors]
        if not isinstance(authors, list):
            authors = []
        names = [
            author.get("name")
            for author in authors
            if isinstance(author, dict) and isinstance(author.get("name"), str)
        ]
        assert_true(
            bool(names) and all(names) and ", ".join(names) in parts,
            f"{relative_path} post-meta should show its BlogPosting author",
            failures,
        )


def validate_local_references(failures: list[str]) -> None:
    home_url = parse_html("index.html").canonical_url or ""
    home = urlsplit(home_url)
    if home.scheme not in {"http", "https"} or not home.netloc:
        failures.append("home page should have an absolute canonical URL for link validation")
        return
    base_path = unquote(home.path).rstrip("/") + "/"
    root = SITE_DIR.resolve()
    for html_path in sorted(SITE_DIR.rglob("*.html")):
        relative_path = html_path.relative_to(SITE_DIR).as_posix()
        page_url = urljoin(home_url.rstrip("/") + "/", quote(relative_path))
        for tag, attribute, reference in parse_html(relative_path).references:
            try:
                raw = urlsplit(reference)
            except ValueError:
                failures.append(f"{relative_path}: invalid {tag}[{attribute}] URL: {reference}")
                continue
            if (raw.scheme and raw.scheme not in {"http", "https"}) or not raw.path:
                continue
            resolved = urlsplit(urljoin(page_url, reference))
            if (resolved.scheme, resolved.netloc) != (home.scheme, home.netloc):
                continue
            path = unquote(resolved.path)
            if path == base_path.rstrip("/"):
                path = base_path
            # Absolute URLs may point to other sites on this origin. Relative
            # references must retain this site's deployment path (e.g. /blog/).
            if not path.startswith(base_path):
                assert_true(
                    bool(raw.netloc),
                    f"{relative_path}: {tag}[{attribute}] is outside site base path {base_path}: {reference}",
                    failures,
                )
                continue
            target = (root / path[len(base_path):]).resolve()
            if target.is_dir():
                target /= "index.html"
            assert_true(
                target.is_relative_to(root) and target.is_file(),
                f"{relative_path}: {tag}[{attribute}] target does not exist: {reference}",
                failures,
            )


def validate_pagination_canonicals(failures: list[str]) -> None:
    """Each real pager describes itself; alias and retired-tag redirects do not."""
    home_url = parse_html("index.html").canonical_url or ""
    for html_path in sorted(SITE_DIR.rglob("index.html")):
        relative_path = html_path.relative_to(SITE_DIR).as_posix()
        if not re.search(r"(?:^|/)page/[0-9]+/index\.html$", relative_path):
            continue
        page = parse_html(relative_path)
        if any(item.get("http-equiv", "").lower() == "refresh" for item in page.meta):
            continue
        expected = urljoin(home_url, quote(relative_path.removesuffix("index.html")))
        assert_true(
            len(page.canonical_urls) == 1
            and unquote(page.canonical_urls[0]) == unquote(expected),
            f"{relative_path}: pagination canonical should be {expected}",
            failures,
        )


def validate_home_navigation(failures: list[str]) -> None:
    """Validate the complete dated home list against published source articles."""
    repo = Path(__file__).resolve().parent.parent
    home = parse_html("index.html")
    home_url = home.canonical_url or ""
    posts: dict[str, dict] = {}
    categories: dict[str, set[str]] = {name: set() for name in ARTICLE_CATEGORIES}
    for source in sorted((repo / "content/posts").glob("*.md")):
        if source.stem == "_index":
            continue
        try:
            metadata, _ = read_markdown(source)
            metadata = {key.lower(): value for key, value in metadata.items()}
            slug = metadata.get("slug") or source.stem
            # Drafts, future and expired articles are not necessarily in this build.
            if not (SITE_DIR / f"posts/{slug}/index.html").is_file():
                continue
            published = aware_datetime(metadata.get("date"))
        except (OSError, ValueError, TypeError, yaml.YAMLError) as error:
            failures.append(f"{source.name}: cannot validate home entry: {error}")
            continue
        for name in metadata.get("categories", []):
            if name in categories:
                categories[name].add(slug)
        if metadata.get("hiddeninhomelist") is not True:
            posts[slug] = {"date": published}

    category_links = [(attrs, text) for attrs, text in home.links if "data-home-category" in attrs]
    assert_true(
        [attrs.get("data-home-category") for attrs, _ in category_links] == list(HOME_CATEGORY_ORDER),
        "home page should have exactly one category entry in this order: " + " / ".join(HOME_CATEGORY_ORDER),
        failures,
    )
    for attrs, text in category_links:
        name = attrs.get("data-home-category")
        if name not in categories:
            continue
        expected_url = urljoin(home_url, f"categories/{quote(name)}/")
        assert_true(
            unquote(urljoin(home_url, attrs.get("href") or "")) == unquote(expected_url),
            f"home page {name} entry should target its category page",
            failures,
        )
        assert_true(
            text == CATEGORY_LABELS[name],
            f"home page {name} entry should display {CATEGORY_LABELS[name]}",
            failures,
        )
        try:
            count = int(attrs.get("data-count"))
        except (TypeError, ValueError):
            count = -1
        assert_true(
            count == len(categories[name]),
            f"home page {name} data-count should match its published article count ({len(categories[name])})",
            failures,
        )

    # Compare dates rather than an arbitrary order among articles with equal dates.
    # Full coverage below still rejects repeated or missing articles across pages.
    page_size = 10
    expected_dates = sorted((post["date"] for post in posts.values()), reverse=True)
    page_count = max(1, (len(posts) + page_size - 1) // page_size)
    expected_pagers = {f"page/{number}/index.html" for number in range(2, page_count + 1)}
    actual_pagers = {
        path.relative_to(SITE_DIR).as_posix()
        for path in (SITE_DIR / "page").glob("*/index.html")
        if path.parent.name != "1"
    }
    assert_true(actual_pagers == expected_pagers, "home pagination should contain every expected page and no extra pages", failures)
    actual_slugs: list[str | None] = []
    for number in range(1, page_count + 1):
        relative_path = "index.html" if number == 1 else f"page/{number}/index.html"
        page = parse_html(relative_path)
        offset = (number - 1) * page_size
        expected_page_dates = expected_dates[offset:offset + page_size]
        slugs = [entry.get("slug") for entry in page.post_entries]
        actual_slugs.extend(slugs)
        assert_true(
            len(slugs) == len(expected_page_dates),
            f"{relative_path}: home list should contain {len(expected_page_dates)} articles",
            failures,
        )
        assert_true(
            all(slug in posts for slug in slugs),
            f"{relative_path}: home list should contain only published, visible articles",
            failures,
        )
        if all(slug in posts for slug in slugs):
            assert_true(
                [posts[slug]["date"] for slug in slugs] == expected_page_dates,
                f"{relative_path}: home list should show the expected newest articles in publication order",
                failures,
            )
        for entry in page.post_entries:
            links = entry["links"]
            slug = entry["slug"]
            assert_true(len(links) == 1, f"{relative_path}: {slug} should have one article title link", failures)
            if len(links) != 1:
                continue
            attrs, title = links[0]
            expected_url = urljoin(home_url, f"posts/{quote(str(slug))}/")
            assert_true(
                attrs.get("data-post-link") == slug and bool(title.strip())
                and unquote(urljoin(home_url, attrs.get("href") or "")) == unquote(expected_url),
                f"{relative_path}: {slug} title link should identify and target its article",
                failures,
            )
        if number < page_count:
            expected_next = urljoin(home_url, f"page/{number + 1}/")
            assert_true(
                any(urljoin(home_url, attrs.get("href") or "") == expected_next for attrs, _ in page.links),
                f"{relative_path}: home list should link to its next page",
                failures,
            )
    assert_true(
        len(actual_slugs) == len(set(actual_slugs)) and set(actual_slugs) == set(posts),
        "home pagination should show every visible article exactly once",
        failures,
    )


def validate_reading_paths(failures: list[str]) -> None:
    """The topic directory, backlinks and next reads share one ordered list."""
    repo = Path(__file__).resolve().parent.parent
    definitions = json.loads((repo / "data/reading_paths.json").read_text(encoding="utf-8"))
    expected: dict[str, list[str]] = {}
    for definition in definitions["paths"]:
        topic = definition["topic"].strip("/")
        topic_slug = topic.rsplit("/", 1)[-1]
        posts = [
            entry["post"].strip("/")
            for group in definition["groups"]
            for entry in group["entries"]
        ]
        topic_page = parse_html(f"{topic}/index.html")
        directory = [
            attrs for attrs, _ in topic_page.links
            if "data-reading-path-post" in attrs
        ]
        assert_true(
            [attrs.get("data-reading-path-post") for attrs in directory]
            == [post.rsplit("/", 1)[-1] for post in posts],
            f"{topic}: directory should preserve its reading order",
            failures,
        )
        for index, post in enumerate(posts):
            expected.setdefault(post, []).append(topic_slug)
            page = parse_html(f"{post}/index.html")
            home_links = [
                attrs for attrs, _ in page.links
                if attrs.get("data-reading-path-home") == topic_slug
            ]
            next_links = [
                attrs for attrs, _ in page.links
                if attrs.get("data-reading-path-next") == topic_slug
            ]
            assert_true(
                len(home_links) == 1
                and url_path_ends_with(home_links[0].get("href"), topic),
                f"{post}: should link back to {topic} once in reading navigation",
                failures,
            )
            if index + 1 < len(posts):
                assert_true(
                    len(next_links) == 1
                    and url_path_ends_with(next_links[0].get("href"), posts[index + 1]),
                    f"{post}: next read in {topic} should be {posts[index + 1]}",
                    failures,
                )
            else:
                assert_true(not next_links, f"{post}: final entry in {topic} should not invent a next read", failures)
    for path in (SITE_DIR / "posts").glob("*/index.html"):
        post = path.parent.relative_to(SITE_DIR).as_posix()
        page = parse_html(f"{post}/index.html")
        actual = [attrs["data-reading-path-home"] for attrs, _ in page.links if "data-reading-path-home" in attrs]
        assert_true(
            sorted(actual) == sorted(expected.get(post, [])),
            f"{post}: reading navigation should match its topic memberships",
            failures,
        )


def validate_learning_navigation(failures: list[str]) -> None:
    """Learning state comes from source metadata; membership follows this build."""
    repo = Path(__file__).resolve().parent.parent
    home_url = parse_html("index.html").canonical_url or ""
    learning_url = urljoin(home_url, "learning/")
    statuses = ("pending", "done", "unmarked")
    posts: dict[str, dict[str, str]] = {}
    for source in sorted((repo / "content/posts").glob("*.md")):
        if source.stem == "_index":
            continue
        try:
            metadata, _ = read_markdown(source)
            slug = metadata.get("slug") or source.stem
            relative_path = f"posts/{slug}/index.html"
            # Include only generated posts, including preview-only posts if built.
            if not (SITE_DIR / relative_path).is_file():
                continue
            status = metadata.get("learning_status", "unmarked")
            if status not in statuses or ("learning_status" in metadata and status == "unmarked"):
                raise ValueError("learning_status should be pending or done, or omitted")
            posts[slug] = {
                "status": status,
                "path": relative_path,
                "edit": "https://github.com/QianKuang8/blog/edit/main/"
                + quote(source.relative_to(repo).as_posix()),
            }
        except (OSError, ValueError, TypeError, yaml.YAMLError) as error:
            failures.append(f"{source.name}: cannot validate learning entry: {error}")

    page = parse_html("learning/index.html")
    groups = page.learning_groups
    assert_true(
        [group["attrs"].get("data-learning-group") for group in groups] == list(statuses),
        "learning/index.html should have one pending, done and unmarked group in order",
        failures,
    )
    entries = [(attrs, title) for attrs, title in page.links if "data-learning-post" in attrs]
    edit_links = [attrs for attrs, _ in page.links if "data-learning-edit" in attrs]
    actual_slugs = [attrs.get("data-learning-post") for attrs, _ in entries]
    assert_true(
        len(actual_slugs) == len(set(actual_slugs)) and set(actual_slugs) == set(posts),
        "learning/index.html should show every generated article exactly once",
        failures,
    )
    edit_slugs = [attrs.get("data-learning-edit") for attrs in edit_links]
    assert_true(
        len(edit_slugs) == len(set(edit_slugs)) and set(edit_slugs) == set(posts),
        "learning/index.html should have exactly one edit link for every generated article",
        failures,
    )
    for attrs in edit_links:
        slug = attrs.get("data-learning-edit")
        expected = posts.get(slug)
        if expected is not None:
            assert_true(
                unquote(attrs.get("href") or "") == unquote(expected["edit"]),
                f"learning/index.html: {slug} edit link should target its actual source file on GitHub",
                failures,
            )
    grouped_count = 0
    grouped_edit_count = 0
    for group in groups:
        attrs = group["attrs"]
        status = attrs.get("data-learning-group")
        expected_count = sum(post["status"] == status for post in posts.values())
        assert_true(
            attrs.get("data-count") == str(expected_count),
            f"learning/index.html: {status} data-count should match source status count ({expected_count})",
            failures,
        )
        assert_true(
            attrs.get("id") == f"learning-{status}" and "hidden" not in attrs
            and (group["tag"] == "section" if status == "pending" else group["tag"] == "details" and "open" not in attrs),
            f"learning/index.html: {status} should have a stable anchor and the expected default expansion",
            failures,
        )
        links = [(attrs, title) for attrs, title in group["links"] if "data-learning-post" in attrs]
        grouped_count += len(links)
        group_edits = [attrs for attrs, _ in group["links"] if "data-learning-edit" in attrs]
        grouped_edit_count += len(group_edits)
        assert_true(
            {attrs.get("data-learning-edit") for attrs in group_edits}
            == {attrs.get("data-learning-post") for attrs, _ in links},
            f"learning/index.html: {status} edit links should match the articles in this group",
            failures,
        )
        for entry_attrs, title in links:
            slug = entry_attrs.get("data-learning-post")
            expected = posts.get(slug)
            if expected is None:
                continue
            assert_true(
                entry_attrs.get("data-learning-status") == status == expected["status"],
                f"learning/index.html: {slug} should belong to its source learning status ({expected['status']})",
                failures,
            )
            expected_url = urljoin(home_url, f"posts/{quote(slug)}/")
            assert_true(
                bool(title.strip()) and unquote(urljoin(home_url, entry_attrs.get("href") or "")) == unquote(expected_url),
                f"learning/index.html: {slug} title link should target its ordinary article URL",
                failures,
            )
    assert_true(
        grouped_count == len(entries),
        "learning/index.html: article title links should belong to exactly one learning group",
        failures,
    )
    assert_true(
        grouped_edit_count == len(edit_links),
        "learning/index.html: edit links should belong to exactly one learning group",
        failures,
    )

    for post in posts.values():
        assert_true(
            not parse_html(post["path"]).learning_controls,
            f"{post['path']}: article page should not contain learning controls or status",
            failures,
        )

    pending_count = str(sum(post["status"] == "pending" for post in posts.values()))
    required_pages = {"index.html", "learning/index.html", *(post["path"] for post in posts.values())}
    for path in sorted(SITE_DIR.rglob("*.html")):
        relative_path = path.relative_to(SITE_DIR).as_posix()
        menu = parse_html(relative_path).main_menu_links
        if not menu and relative_path not in required_pages:
            continue
        links = [attrs for attrs, _ in menu if "data-learning-nav" in attrs]
        assert_true(
            len(links) == 1 and links[0].get("data-pending-count") == pending_count
            and urljoin(home_url, links[0].get("href") or "") == learning_url,
            f"{relative_path}: sidebar should link to the learning list with pending count {pending_count}",
            failures,
        )


def rss_items(
    relative_path: str, failures: list[str]
) -> list[dict[str, str]] | None:
    xml = read_html(relative_path)
    if not xml:
        failures.append(f"{relative_path} should be generated")
        return None
    try:
        root = ElementTree.fromstring(xml)
    except ElementTree.ParseError as error:
        failures.append(f"{relative_path} should be valid RSS XML: {error}")
        return None
    if root.tag.rsplit("}", 1)[-1] != "rss":
        failures.append(f"{relative_path} should contain an RSS document")
        return None

    items: list[dict[str, str]] = []
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] != "item":
            continue
        items.append(
            {
                child.tag.rsplit("}", 1)[-1]: (child.text or "").strip()
                for child in element
            }
        )
    return items


def validate_tag_navigation(failures: list[str]) -> None:
    """Check browse coverage, source attribution, and retired URL compatibility."""
    repo = Path(__file__).resolve().parent.parent
    groups = json.loads((repo / "data/tag_groups.json").read_text(encoding="utf-8"))
    sources = set(groups["sources"])
    retired = set(groups["retired"])
    registered = list(groups["sources"]) + list(groups["other"])
    for group in groups["topics"]:
        registered.extend(group["tags"])
        registered.extend(group.get("details", []))
    assert_true(len(registered) == len(set(registered)), "tag groups should not repeat tags", failures)

    expected: dict[str, set[str]] = {}
    for source in sorted((repo / "content/posts").glob("*.md")):
        try:
            metadata, _ = read_markdown(source)
        except (OSError, ValueError, TypeError, yaml.YAMLError) as error:
            failures.append(f"{source.name}: invalid frontmatter: {error}")
            continue
        tags = metadata.get("tags")
        if metadata.get("draft") is True and not (SITE_DIR / f"posts/{source.stem}/index.html").is_file():
            continue
        if not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags):
            failures.append(f"{source.name}: tags should be a YAML array of strings")
            continue
        assert_true(not retired.intersection(tags), f"{source.name}: retired tag is still assigned", failures)
        assert_true(set(tags) <= set(registered), f"{source.name}: tag is not registered in a group", failures)
        post_path = f"posts/{source.stem}/index.html"
        # Validate draft/future metadata, but only inspect pages in this build.
        if not (SITE_DIR / post_path).is_file():
            continue
        page = parse_html(post_path)
        actual = [attrs for attrs, _ in page.links if attrs.get("data-tag")]
        assert_true(
            sorted(attrs["data-tag"] for attrs in actual) == sorted(tags),
            f"{post_path}: footer should show each assigned tag exactly once",
            failures,
        )
        for attrs in actual:
            tag = attrs["data-tag"]
            kind = "source" if tag in sources else "topic"
            assert_true(attrs.get("data-tag-kind") == kind, f"{post_path}: {tag} has wrong tag role", failures)
            assert_true(url_path_ends_with(attrs.get("href"), f"tags/{tag}"), f"{post_path}: {tag} URL changed", failures)
        labels = (["主题"] if set(tags) - sources else []) + (["来源"] if set(tags) & sources else [])
        assert_true(page.post_tag_labels == labels, f"{post_path}: topic and source rows should be separate", failures)
        for tag in tags:
            expected.setdefault(tag, set()).add(normalized_url_path(page.canonical_url))

    page = parse_html("tags/index.html")
    expected_groups = [group["id"] for group in groups["topics"]] + ["sources", "other"]
    assert_true(page.tag_groups == expected_groups, "tag directory groups should have a stable order and no ungrouped tags", failures)
    chips = [attrs for attrs, _ in page.links if attrs.get("data-tag")]
    assert_true(
        sorted(attrs["data-tag"] for attrs in chips) == sorted(expected),
        "tag directory should list every active tag exactly once and hide retired tags",
        failures,
    )
    assert_true(set(expected) <= set(registered), "all active tags should be registered in tag groups", failures)
    for attrs in chips:
        tag = attrs["data-tag"]
        kind = "source" if tag in sources else "topic"
        assert_true(attrs.get("data-tag-kind") == kind, f"tag directory: {tag} has wrong tag role", failures)
        assert_true(attrs.get("data-count") == str(len(expected[tag])), f"tag directory: {tag} count differs from its articles", failures)
        feed = rss_items(f"tags/{tag}/index.xml", failures)
        if feed is not None:
            assert_true(
                {normalized_url_path(item.get("link")) for item in feed} == expected[tag],
                f"tags/{tag}: archive feed should match assigned articles",
                failures,
            )

    for legacy_path, target in (
        ("tags/视频笔记/index.html", "categories/视频笔记"),
        ("tags/视频笔记/page/1/index.html", "tags/视频笔记"),
        ("tags/视频笔记/page/2/index.html", "categories/视频笔记/page/2"),
        ("tags/博客推荐/page/1/index.html", "tags/博客推荐"),
    ):
        legacy = parse_html(legacy_path)
        assert_true(url_path_ends_with(legacy.canonical_url, target), f"{legacy_path}: canonical should point to the replacement", failures)
        assert_true(
            any(item.get("http-equiv", "").lower() == "refresh" and legacy.canonical_url in (item.get("content") or "") for item in legacy.meta) if legacy.canonical_url else False,
            f"{legacy_path}: should redirect to its canonical URL",
            failures,
        )
    old_feed = rss_items("tags/视频笔记/index.xml", failures)
    category_feed = rss_items("categories/视频笔记/index.xml", failures)
    if old_feed is not None and category_feed is not None:
        assert_true(
            [item.get("link") for item in old_feed] == [item.get("link") for item in category_feed],
            "retired video tag RSS should continue to follow the video category",
            failures,
        )
    old_blog = parse_html("tags/博客推荐/index.html")
    old_blog_feed = rss_items("tags/博客推荐/index.xml", failures)
    for slug in ("five-agent-skills-i-use-every-day", "prompt-engineering-guide"):
        assert_true(any(url_path_ends_with(attrs.get("href"), f"posts/{slug}") for attrs, _ in old_blog.links), f"retired recommendation page should keep {slug}", failures)
        if old_blog_feed is not None:
            assert_true(any(url_path_ends_with(item.get("link"), f"posts/{slug}") for item in old_blog_feed), f"retired recommendation RSS should keep {slug}", failures)


def main() -> int:
    failures: list[str] = []

    home_schema = json_ld("index.html", failures)
    people = [item for item in home_schema if item.get("@type") == "Person"]
    assert_true(bool(people), "home page JSON-LD should describe Qian as a Person", failures)
    if people:
        assert_true(
            "https://github.com/QianKuang8" in people[0].get("sameAs", []),
            "home page Person schema should include the GitHub profile in sameAs",
            failures,
        )

    for relative_path in (
        "archives/index.html",
        "categories/index.html",
        "search/index.html",
        "tags/index.html",
        "topics/index.html",
        "learning/index.html",
    ):
        assert_true(
            bool(read_html(relative_path)),
            f"{relative_path} should be generated",
            failures,
        )
        page_schema = json_ld(relative_path, failures)
        assert_true(
            not any(item.get("@type") == "BlogPosting" for item in page_schema),
            f"{relative_path} should not emit BlogPosting JSON-LD",
            failures,
        )

    home_page = parse_html("index.html")
    article_categories = source_article_categories(failures)
    category_urls = {
        unquote(urljoin(home_page.canonical_url or "", quote(path.removesuffix("index.html")))): CATEGORY_LABELS[term]
        for path, (term, _) in article_categories.items()
    }
    assert_true(
        not any(
            " ".join(text.split()) == "栏目"
            or url_path_ends_with(attrs.get("href"), "categories")
            for attrs, text in home_page.main_menu_links
        ),
        "main menu should not contain a categories link",
        failures,
    )
    validate_home_navigation(failures)
    for relative_path in ("robots.txt", "sitemap.xml"):
        assert_true(bool(read_html(relative_path)), f"{relative_path} should be generated", failures)

    home_feed_items = rss_items("index.xml", failures)
    if home_feed_items is not None:
        assert_true(
            bool(home_feed_items),
            "index.xml should contain at least one item",
            failures,
        )
        assert_true(
            not any(url_path_ends_with(item.get("link"), "learning") for item in home_feed_items),
            "index.xml should not include the learning utility page",
            failures,
        )
    categories_feed_items = rss_items("categories/index.xml", failures)
    if categories_feed_items is not None:
        assert_true(
            bool(categories_feed_items),
            "categories/index.xml should contain at least one item",
            failures,
        )
    home_json = read_html("index.json")
    assert_true(bool(home_json), "index.json should be generated", failures)
    if home_json:
        try:
            home_index = json.loads(home_json)
        except json.JSONDecodeError as error:
            failures.append(f"index.json should contain valid JSON: {error}")
        else:
            assert_true(
                isinstance(home_index, list) and bool(home_index),
                "index.json should contain a non-empty list",
                failures,
            )
            if isinstance(home_index, list):
                search_urls: list[str] = []
                for index, item in enumerate(home_index):
                    if not isinstance(item, dict):
                        failures.append(f"index.json item {index}: should be an object")
                        continue
                    for field in ("title", "content", "summary", "permalink", "category", "date"):
                        assert_true(
                            isinstance(item.get(field), str),
                            f"index.json item {index}: {field} should be a string",
                            failures,
                        )
                    tags = item.get("tags")
                    assert_true(
                        isinstance(tags, list) and all(isinstance(tag, str) and tag.strip() for tag in tags),
                        f"index.json item {index}: tags should be an array of non-empty strings",
                        failures,
                    )
                    category = item.get("category")
                    validate_search_category(item, index, category_urls, failures)
                    if category != "专题":
                        try:
                            date.fromisoformat(str(item.get("date")))
                        except ValueError:
                            failures.append(f"index.json item {index}: should include the article's publication date")
                    if isinstance(item.get("permalink"), str):
                        search_urls.append(item["permalink"])
                assert_true(len(search_urls) == len(set(search_urls)), "index.json should not repeat search URLs", failures)
                assert_true(
                    not any(url_path_ends_with(url, "learning") for url in search_urls),
                    "index.json should not include the learning utility page",
                    failures,
                )
                assert_true(
                    any(
                        isinstance(item, dict)
                        and isinstance(item.get("permalink"), str)
                        and "/posts/" in urlsplit(item["permalink"]).path
                        for item in home_index
                    ),
                    "index.json should contain at least one post permalink",
                    failures,
                )

    for category_name, category_path in ARTICLE_CATEGORIES.items():
        category_html = read_html(category_path)
        assert_true(
            bool(category_html),
            f"{category_path} should be generated",
            failures,
        )
        assert_true(
            ("h1", CATEGORY_LABELS[category_name]) in parse_html(category_path).headings,
            f"{category_path} should display the {CATEGORY_LABELS[category_name]} category heading",
            failures,
        )

        category_rss_path = category_path.removesuffix("index.html") + "index.xml"
        feed_items = rss_items(category_rss_path, failures)
        if feed_items is not None:
            for attrs, _ in home_page.links:
                if attrs.get("data-home-category") != category_name:
                    continue
                assert_true(
                    attrs.get("data-count") == str(len(feed_items)),
                    f"home page {category_name} data-count should match its RSS item count",
                    failures,
                )

    tags_page = parse_html("tags/index.html")
    assert_true(
        ("h1", "主题浏览") in tags_page.headings,
        "tags page heading should be localized",
        failures,
    )

    categories_page = parse_html("categories/index.html")
    assert_true(
        ("h1", "栏目") in categories_page.headings,
        "categories page heading should be localized",
        failures,
    )

    posts_dir = SITE_DIR / "posts"
    post_count = 0
    for post_path in sorted(posts_dir.rglob("*.html")):
        relative_path = post_path.relative_to(SITE_DIR).as_posix()
        post_page = parse_html(relative_path)
        if not post_page.class_counts.get("post-single"):
            continue
        post_count += 1
        schemas = [
            item for item in json_ld(relative_path, failures)
            if item.get("@type") == "BlogPosting"
        ]
        assert_true(
            len(schemas) == 1,
            f"{relative_path} should contain exactly one BlogPosting JSON-LD object",
            failures,
        )
        if schemas:
            schema = schemas[0]
            published = schema_datetime(schema, "datePublished", relative_path, failures)
            modified = schema_datetime(schema, "dateModified", relative_path, failures)
            validate_post_meta(
                relative_path, post_page, schema, published, modified, failures
            )
        if not post_page.post_meta:
            continue
        validate_article_category(relative_path, post_page, article_categories, failures)

    assert_true(post_count > 0, "at least one post page should be generated", failures)
    validate_tag_navigation(failures)
    validate_local_references(failures)
    validate_pagination_canonicals(failures)
    validate_reading_paths(failures)
    validate_learning_navigation(failures)

    search_page = parse_html("search/index.html")
    assert_true(
        any(tag == "h1" and text.startswith("搜索") for tag, text in search_page.headings),
        "search page heading should be localized",
        failures,
    )
    assert_true(
        any(
            item.get("name") == "robots"
            and item.get("content") == "noindex, nofollow"
            for item in search_page.meta
        ),
        "search page should be noindex in production output",
        failures,
    )

    if failures:
        print("Site validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Site validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
