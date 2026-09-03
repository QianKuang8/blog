#!/usr/bin/env python3
"""Validate generated Hugo output for blog-specific SEO and navigation rules."""

from __future__ import annotations

from datetime import date
from functools import lru_cache
from html.parser import HTMLParser
import json
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit
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
        self.main_menu_links: list[tuple[dict[str, str | None], str]] = []
        self.meta: list[dict[str, str | None]] = []
        self.headings: list[tuple[str, str]] = []
        self.class_counts: dict[str, int] = {}
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
        self._section_depth = 0
        self._shelf_contexts: list[tuple[int, dict[str, object]]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        classes = class_names(attributes)
        for class_name in classes:
            self.class_counts[class_name] = self.class_counts.get(class_name, 0) + 1

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
        if self._json_ld_parts is not None:
            self._json_ld_parts.append(data)
        if self._link_attrs is not None:
            self._link_parts.append(data)
        if self._heading_tag is not None:
            self._heading_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
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


def json_ld(relative_path: str) -> list[dict]:
    return [json.loads(script) for script in parse_html(relative_path).json_ld_scripts]


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


def main() -> int:
    failures: list[str] = []

    home_schema = json_ld("index.html")
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
        page_schema = json_ld(relative_path)
        assert_true(
            not any(item.get("@type") == "BlogPosting" for item in page_schema),
            f"{relative_path} should not emit BlogPosting JSON-LD",
            failures,
        )

    post_schema = json_ld("posts/claude-code-prompt-caching-is-everything/index.html")
    assert_true(
        any(
            item.get("@type") == "BlogPosting"
            and not str(item.get("datePublished", "")).startswith("0001")
            for item in post_schema
        ),
        "post pages should still emit BlogPosting JSON-LD with a real date",
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
    for post_path in sorted(posts_dir.glob("*/index.html")):
        relative_path = post_path.relative_to(SITE_DIR).as_posix()
        if not any(
            item.get("@type") == "BlogPosting" for item in json_ld(relative_path)
        ):
            continue
        post_page = parse_html(relative_path)
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
