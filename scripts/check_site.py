#!/usr/bin/env python3
"""Validate generated Hugo output for blog-specific SEO and navigation rules."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


SITE_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("public")


def read_html(relative_path: str) -> str:
    path = SITE_DIR / relative_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def json_ld(relative_path: str) -> list[dict]:
    html = read_html(relative_path)
    if not html:
        return []
    scripts = re.findall(
        r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
        html,
        flags=re.S,
    )
    return [json.loads(script) for script in scripts]


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

    tags_html = read_html("tags/index.html")
    assert_true("<h1>标签</h1>" in tags_html, "tags page heading should be localized", failures)

    search_html = read_html("search/index.html")
    assert_true("<h1>搜索" in search_html, "search page heading should be localized", failures)
    assert_true(
        'name="robots" content="noindex, nofollow"' in search_html,
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
