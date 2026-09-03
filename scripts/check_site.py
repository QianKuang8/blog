#!/usr/bin/env python3
"""Validate generated Hugo output for blog-specific SEO and navigation rules."""

from __future__ import annotations

from functools import lru_cache
from html.parser import HTMLParser
import json
import sys
from pathlib import Path
from urllib.parse import unquote


SITE_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("public")
ARTICLE_CATEGORIES = {
    "好文分享": "categories/好文分享/index.html",
    "原创文章": "categories/原创文章/index.html",
    "视频笔记": "categories/视频笔记/index.html",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.json_ld_scripts: list[str] = []
        self.links: list[tuple[dict[str, str | None], str]] = []
        self.meta: list[dict[str, str | None]] = []
        self.headings: list[tuple[str, str]] = []
        self._json_ld_parts: list[str] | None = None
        self._link_attrs: dict[str, str | None] | None = None
        self._link_parts: list[str] = []
        self._heading_tag: str | None = None
        self._heading_parts: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        if tag == "script" and attributes.get("type") == "application/ld+json":
            self._json_ld_parts = []
        elif tag == "a":
            self._link_attrs = attributes
            self._link_parts = []
        elif tag == "meta":
            self.meta.append(attributes)
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._heading_tag = tag
            self._heading_parts = []

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
            self.links.append((self._link_attrs, "".join(self._link_parts).strip()))
            self._link_attrs = None
            self._link_parts = []
        elif tag == self._heading_tag:
            self.headings.append(
                (self._heading_tag, "".join(self._heading_parts).strip())
            )
            self._heading_tag = None
            self._heading_parts = []


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

    home_html = read_html("index.html")
    home_page = parse_html("index.html")
    categories_menu_link = next(
        (
            attrs.get("href")
            for attrs, text in home_page.links
            if text == "栏目" and attrs.get("href")
        ),
        None,
    )
    assert_true(
        bool(categories_menu_link)
        and unquote(categories_menu_link).rstrip("/").endswith("/categories"),
        "main menu should link to the categories page",
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
        category_link = next(
            (
                attrs.get("href")
                for attrs, text in home_page.links
                if text == category_name and attrs.get("href")
            ),
            None,
        )
        assert_true(
            bool(category_link)
            and unquote(category_link).rstrip("/") == f"categories/{category_name}",
            f"home page should link to the {category_name} category",
            failures,
        )

    for topic_path in (
        "/blog/topics/coding-agent/",
        "/blog/topics/context-engineering/",
        "/blog/topics/harness-engineering/",
    ):
        assert_true(
            topic_path in home_html,
            f"home page should link to {topic_path}",
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
