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


SITE_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("public")
ARTICLE_CATEGORIES = {
    "好文分享": "categories/好文分享/index.html",
    "原创文章": "categories/原创文章/index.html",
    "视频笔记": "categories/视频笔记/index.html",
}
HOME_CATEGORY_ORDER = ("原创文章", "视频笔记", "好文分享")


def class_names(attributes: dict[str, str | None]) -> set[str]:
    return set((attributes.get("class") or "").split())


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.json_ld_scripts: list[str] = []
        self.links: list[tuple[dict[str, str | None], str]] = []
        self.references: list[tuple[str, str, str]] = []
        self.canonical_url: str | None = None
        self.post_meta: list[str] = []
        self.post_meta_fields: set[str] = set()
        self.main_menu_links: list[tuple[dict[str, str | None], str]] = []
        self.meta: list[dict[str, str | None]] = []
        self.headings: list[tuple[str, str]] = []
        self.class_counts: dict[str, int] = {}
        self.post_tag_labels: list[str | None] = []
        self.tag_groups: list[str] = []
        self.home_category_shelves: list[dict[str, object]] = []
        self._json_ld_parts: list[str] | None = None
        self._link_attrs: dict[str, str | None] | None = None
        self._link_parts: list[str] = []
        self._link_in_main_menu = False
        self._link_shelf: dict[str, object] | None = None
        self._link_is_category_all = False
        self._link_is_category_preview = False
        self._link_preview_datetime: str | None = None
        self._heading_tag: str | None = None
        self._heading_parts: list[str] = []
        self._main_menu_depth = 0
        self._post_meta_depth = 0
        self._post_meta_parts: list[str] = []
        self._section_depth = 0
        self._shelf_contexts: list[tuple[int, dict[str, object]]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        classes = class_names(attributes)
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

        if tag == "ul":
            if self._main_menu_depth:
                self._main_menu_depth += 1
            elif attributes.get("id") == "menu":
                self._main_menu_depth = 1

        if tag == "section":
            self._section_depth += 1
            if "home-category-shelf" in classes:
                shelf: dict[str, object] = {
                    "category": attributes.get("data-category"),
                    "data_count": attributes.get("data-count"),
                    "previews": [],
                    "all_links": [],
                }
                self.home_category_shelves.append(shelf)
                self._shelf_contexts.append((self._section_depth, shelf))

        active_shelf = self._shelf_contexts[-1][1] if self._shelf_contexts else None

        if tag == "script" and attributes.get("type") == "application/ld+json":
            self._json_ld_parts = []
        elif tag == "a":
            self._link_attrs = attributes
            self._link_parts = []
            self._link_in_main_menu = self._main_menu_depth > 0
            self._link_shelf = active_shelf
            self._link_is_category_all = "home-category-all" in classes
            self._link_is_category_preview = "home-category-preview" in classes
            self._link_preview_datetime = None
        elif tag == "meta":
            self.meta.append(attributes)
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._heading_tag = tag
            self._heading_parts = []

        if tag == "time" and self._link_is_category_preview:
            self._link_preview_datetime = attributes.get("datetime")

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
            if self._link_shelf is not None and self._link_is_category_all:
                all_links = self._link_shelf["all_links"]
                assert isinstance(all_links, list)
                all_links.append(link)
            if self._link_shelf is not None and self._link_is_category_preview:
                previews = self._link_shelf["previews"]
                assert isinstance(previews, list)
                previews.append(
                    {
                        "href": self._link_attrs.get("href"),
                        "datetime": self._link_preview_datetime,
                    }
                )
            self._link_attrs = None
            self._link_parts = []
            self._link_in_main_menu = False
            self._link_shelf = None
            self._link_is_category_all = False
            self._link_is_category_preview = False
            self._link_preview_datetime = None
        elif tag == self._heading_tag:
            self.headings.append(
                (self._heading_tag, "".join(self._heading_parts).strip())
            )
            self._heading_tag = None
            self._heading_parts = []

        if tag == "section":
            if (
                self._shelf_contexts
                and self._shelf_contexts[-1][0] == self._section_depth
            ):
                self._shelf_contexts.pop()
            self._section_depth = max(0, self._section_depth - 1)
        elif tag == "ul" and self._main_menu_depth:
            self._main_menu_depth -= 1


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
    # PaperMod omits the container entirely when hideMeta is enabled.
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
        frontmatter = source.read_text(encoding="utf-8").split("---", 2)[1]
        match = re.search(r"^tags:\s*(\[.*\])$", frontmatter, re.MULTILINE)
        if not match:
            failures.append(f"{source.name}: tags should be an array")
            continue
        tags = json.loads(match.group(1))
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
    assert_true(
        not any(
            " ".join(text.split()) == "栏目"
            or url_path_ends_with(attrs.get("href"), "categories")
            for attrs, text in home_page.main_menu_links
        ),
        "main menu should not contain a categories link",
        failures,
    )
    assert_true(
        home_page.class_counts.get("post-entry", 0) == 0,
        "home page should not contain post-entry cards",
        failures,
    )
    assert_true(
        home_page.class_counts.get("pagination", 0) == 0,
        "home page should not contain pagination",
        failures,
    )

    shelf_categories = [
        shelf.get("category") for shelf in home_page.home_category_shelves
    ]
    assert_true(
        shelf_categories == list(HOME_CATEGORY_ORDER),
        "home page category shelves should appear in this order: "
        + " / ".join(HOME_CATEGORY_ORDER),
        failures,
    )

    home_feed_items = rss_items("index.xml", failures)
    if home_feed_items is not None:
        assert_true(
            bool(home_feed_items),
            "index.xml should contain at least one item",
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
            category_name in category_html,
            f"{category_path} should identify the {category_name} category",
            failures,
        )

        category_rss_path = category_path.removesuffix("index.html") + "index.xml"
        feed_items = rss_items(category_rss_path, failures)
        matching_shelves = [
            shelf
            for shelf in home_page.home_category_shelves
            if shelf.get("category") == category_name
        ]
        assert_true(
            len(matching_shelves) == 1,
            f"home page should contain exactly one {category_name} shelf",
            failures,
        )
        if not matching_shelves:
            continue

        shelf = matching_shelves[0]
        previews = shelf.get("previews")
        assert isinstance(previews, list)
        assert_true(
            len(previews) == 2,
            f"the {category_name} shelf should contain exactly two previews",
            failures,
        )
        data_count = shelf.get("data_count")
        try:
            parsed_data_count = int(data_count)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            failures.append(
                f"the {category_name} shelf should have an integer data-count"
            )
        else:
            if feed_items is not None:
                assert_true(
                    parsed_data_count == len(feed_items),
                    f"the {category_name} shelf data-count should match its RSS item count",
                    failures,
                )

        if feed_items is not None:
            feed_paths = {
                normalized_url_path(item.get("link")) for item in feed_items
            }
            preview_dates: list[date] = []
            preview_paths: list[str] = []
            for preview in previews:
                assert isinstance(preview, dict)
                href = preview.get("href")
                preview_path = normalized_url_path(
                    href if isinstance(href, str) else None
                )
                preview_paths.append(preview_path)
                assert_true(
                    bool(preview_path) and preview_path in feed_paths,
                    f"the {category_name} shelf preview should belong to its RSS feed",
                    failures,
                )

                datetime_value = preview.get("datetime")
                try:
                    preview_dates.append(date.fromisoformat(str(datetime_value)))
                except ValueError:
                    failures.append(
                        f"the {category_name} shelf preview should have an ISO date"
                    )

            assert_true(
                len(preview_paths) == len(set(preview_paths)),
                f"the {category_name} shelf previews should link to distinct posts",
                failures,
            )
            if len(preview_dates) == len(previews):
                assert_true(
                    preview_dates == sorted(preview_dates, reverse=True),
                    f"the {category_name} shelf previews should be newest first",
                    failures,
                )

        all_links = shelf.get("all_links")
        assert isinstance(all_links, list)
        assert_true(
            len(all_links) == 1,
            f"the {category_name} shelf should contain exactly one view-all link",
            failures,
        )
        if len(all_links) == 1:
            attrs, text = all_links[0]
            assert_true(
                " ".join(text.split()).startswith("查看全部"),
                f"the {category_name} shelf view-all link should be labeled 查看全部",
                failures,
            )
            assert_true(
                attrs.get("aria-label") == f"查看全部{category_name}",
                f"the {category_name} shelf view-all link should have a category-specific aria-label",
                failures,
            )
            assert_true(
                url_path_ends_with(attrs.get("href"), f"categories/{category_name}"),
                f"the {category_name} shelf view-all link should target its category page",
                failures,
            )

    tags_page = parse_html("tags/index.html")
    assert_true(
        ("h1", "标签") in tags_page.headings,
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
        article_types = [
            text
            for attrs, text in post_page.links
            if "article-type" in (attrs.get("class") or "").split()
        ]
        assert_true(
            len(article_types) == 1,
            f"{relative_path} should have exactly one article category",
            failures,
        )
        if article_types:
            assert_true(
                article_types[0] in ARTICLE_CATEGORIES,
                f"{relative_path} has an unsupported article category: {article_types[0]}",
                failures,
            )

    assert_true(post_count > 0, "at least one post page should be generated", failures)
    validate_tag_navigation(failures)
    validate_local_references(failures)

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
