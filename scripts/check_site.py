#!/usr/bin/env python3
"""Validate generated Hugo output: links, canonical URLs, search index and navigation data."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree

import yaml

from check_content import aware_datetime, load_categories, post_paths, post_slug, read_markdown
from site_output import Site


REPO = Path(__file__).resolve().parents[1]
REQUIRED_OUTPUTS = (
    "index.html", "404.html", "archives/index.html", "categories/index.html", "search/index.html",
    "tags/index.html", "topics/index.html", "learning/index.html", "robots.txt", "sitemap.xml", "index.json",
)
LEARNING_GROUPS = ("pending", "done", "unmarked")


def generated_posts(site: Site, repo: Path, failures: list[str]) -> list[dict]:
    """Source metadata for the posts in this build (drafts, future and expired posts may be absent)."""
    posts = []
    for path in post_paths(repo):
        try:
            metadata, _ = read_markdown(path)
        except (OSError, ValueError, TypeError, yaml.YAMLError) as error:
            failures.append(f"{path.relative_to(repo)}: {error}")
            continue
        slug = post_slug(path, metadata)
        output = f"posts/{slug}/index.html"
        if site.exists(output):
            terms = metadata.get("categories")
            term = terms[0] if isinstance(terms, list) and len(terms) == 1 else None
            posts.append({"source": path, "slug": slug, "output": output, "metadata": metadata, "term": term})
    if not posts:
        failures.append("posts: no article pages were generated")
    return posts


def check_required_outputs(site: Site, categories: dict, failures: list[str]) -> None:
    for path in (*REQUIRED_OUTPUTS, *(f"categories/{term}/index.html" for term in categories)):
        if not site.exists(path):
            failures.append(f"{path}: should be generated")


def check_canonicals(site: Site, failures: list[str]) -> None:
    """Every page names one canonical URL; real pages (pagers included) name themselves."""
    for path in site.html_paths():
        page = site.page(path)
        if len(page.canonical_urls) != 1:
            failures.append(f"{path}: should have exactly one canonical URL")
            continue
        # Redirects name their replacement; a canonical on another site is a deliberate choice.
        if page.is_redirect or site.resolve(page.canonical_url) is None:
            continue
        if not site.same_url(page.canonical_url, site.url_of(path)):
            failures.append(f"{path}: canonical URL should be {site.url_of(path)}")


def check_languages(site: Site, language: str | None, failures: list[str]) -> None:
    """Every page, redirects included, declares the configured languageCode."""
    for path in site.html_paths():
        if site.page(path).lang != language:
            failures.append(f"{path}: <html lang> should be {language} (languageCode in config/_default/config.yaml)")


def check_local_references(site: Site, failures: list[str]) -> None:
    home = urlsplit(site.home_url)
    root = site.root.resolve()
    for path in site.html_paths():
        for tag, attribute, reference in site.page(path).references:
            try:
                raw = urlsplit(reference)
                resolved = urlsplit(urljoin(site.url_of(path), reference))
            except ValueError:
                failures.append(f"{path}: invalid {tag}[{attribute}] URL: {reference}")
                continue
            if (raw.scheme and raw.scheme not in {"http", "https"}) or not raw.path:
                continue
            if (resolved.scheme, resolved.netloc) != (home.scheme, home.netloc):
                continue
            target = site.resolve(reference, path)
            if target is None:
                # Absolute URLs may name other sites on this origin; relative ones must keep the base path.
                if not raw.netloc:
                    failures.append(f"{path}: {tag}[{attribute}] is outside the site path {site.base_path}: {reference}")
                continue
            file = root / target
            if file.is_dir():
                file /= "index.html"
            if not (file.resolve().is_relative_to(root) and file.is_file()):
                failures.append(f"{path}: {tag}[{attribute}] target does not exist: {reference}")


def check_sitemap(site: Site, failures: list[str]) -> None:
    try:
        sitemap = ElementTree.fromstring(site.read("sitemap.xml"))
    except ElementTree.ParseError as error:
        failures.append(f"sitemap.xml: invalid XML: {error}")
        return
    for element in sitemap.iter():
        if element.tag.rsplit("}", 1)[-1] != "loc":
            continue
        url = (element.text or "").strip()
        target = site.resolve(url)
        if target is None or not site.exists(target):
            failures.append(f"sitemap.xml: {url} is not a generated page")
        elif target.endswith(".html") and (site.page(target).is_noindex or site.page(target).is_redirect):
            failures.append(f"sitemap.xml: {url} is noindex or a redirect; exclude it with sitemap.disable")


def check_structured_data(site: Site, posts: list[dict], failures: list[str]) -> None:
    articles_pages = {post["output"] for post in posts}
    for path in site.html_paths():
        items = []
        for script in site.page(path).json_ld:
            try:
                items.append(json.loads(script))
            except json.JSONDecodeError as error:
                failures.append(f"{path}: invalid JSON-LD: {error}")
        articles = [item for item in items if isinstance(item, dict) and item.get("@type") == "BlogPosting"]
        if path not in articles_pages:
            if articles:
                failures.append(f"{path}: only article pages should describe a BlogPosting")
            continue
        if len(articles) != 1:
            failures.append(f"{path}: should contain exactly one BlogPosting")
            continue
        try:
            published = aware_datetime(articles[0].get("datePublished"))
            modified = aware_datetime(articles[0].get("dateModified"))
            if published.year == 1 or modified < published:
                raise ValueError("zero or reversed dates")
        except (ValueError, TypeError):
            failures.append(f"{path}: BlogPosting needs real datePublished <= dateModified with timezones")


def check_search_index(site: Site, repo: Path, posts: list[dict], categories: dict, failures: list[str]) -> None:
    try:
        index = json.loads(site.read("index.json"))
    except json.JSONDecodeError as error:
        failures.append(f"index.json: invalid JSON: {error}")
        return
    if not isinstance(index, list):
        failures.append("index.json: should contain a list")
        return
    expected = {
        unquote(site.url_of(post["output"])): categories[post["term"]]["label"]
        for post in posts if post["term"] in categories
    }
    # Search also matches the original's title, so each article carries its source record's title.
    sources = {}
    for post in posts:
        source = (categories.get(post["term"]) or {}).get("source")
        record = repo / "sources" / str(source) / f"{post['slug']}.md"
        title = read_markdown(record)[0].get("title") if source and record.is_file() else None
        sources[unquote(site.url_of(post["output"]))] = title or ""
    seen = []
    for number, item in enumerate(index):
        fields = ("title", "content", "summary", "permalink", "category", "date")
        if (
            not isinstance(item, dict)
            or not all(isinstance(item.get(field), str) for field in fields)
            or not isinstance(item.get("tags"), list)
            or not all(isinstance(tag, str) and tag.strip() for tag in item["tags"])
        ):
            failures.append(f"index.json item {number}: needs string {', '.join(fields)} and a list of tags")
            continue
        url = unquote(item["permalink"])
        seen.append(url)
        if url in expected:
            if item["category"] != expected[url]:
                failures.append(f"index.json item {number}: category should be {expected[url]}")
            try:
                date.fromisoformat(item["date"])
            except ValueError:
                failures.append(f"index.json item {number}: should include the publication date")
            if item.get("source_title", "") != sources.get(url, ""):
                failures.append(f"index.json item {number}: source_title should be {sources.get(url) or 'empty'}, as in its source record")
        elif item["category"] != "专题" or "/topics/" not in urlsplit(url).path:
            failures.append(f"index.json item {number}: should be an article or a topic")
    if len(seen) != len(set(seen)):
        failures.append("index.json: should not repeat URLs")
    for url in sorted(set(expected) - set(seen)):
        failures.append(f"index.json: missing article {url}")


def check_article_types(site: Site, repo: Path, posts: list[dict], categories: dict, failures: list[str]) -> None:
    """Article type labels derive from data/categories.json and book source records."""
    for post in posts:
        if any(str(key).lower() == "hidemeta" and value is True for key, value in post["metadata"].items()):
            continue
        config = categories.get(post["term"])
        if config is None:
            failures.append(f"{post['output']}: unsupported category {post['term']}")
            continue
        label = config.get("articleType") or config["label"]
        record = repo / "sources" / str(config.get("source")) / f"{post['slug']}.md"
        if config.get("bookType") and record.is_file() and read_markdown(record)[0].get("source_type") == "book":
            label = config["bookType"]
        links = [
            (attrs, text) for attrs, text in site.page(post["output"]).links
            if "article-type" in (attrs.get("class") or "").split()
        ]
        if len(links) != 1 or links[0][0].get("data-category-term") != post["term"] or links[0][1] != label:
            failures.append(f"{post['output']}: should show one article type {label} for category {post['term']}")
        elif site.resolve(links[0][0].get("href") or "", post["output"]) != f"categories/{post['term']}/index.html":
            failures.append(f"{post['output']}: article type should link to categories/{post['term']}/")


def check_source_lines(site: Site, repo: Path, posts: list[dict], categories: dict, failures: list[str]) -> None:
    """A post with a source record links it once under the heading; other posts show no source line."""
    for post in posts:
        source = (categories.get(post["term"]) or {}).get("source")
        record = repo / "sources" / str(source) / f"{post['slug']}.md"
        url = read_markdown(record)[0].get("source_url") if source and record.is_file() else None
        links = [unquote(attrs.get("href") or "") for attrs, _ in site.page(post["output"]).links_with("data-source-link")]
        if links != ([unquote(url)] if url else []):
            failures.append(f"{post['output']}: source line should link {url} once" if url else f"{post['output']}: should not show a source line")


def check_copy_buttons(site: Site, repo: Path, posts: list[dict], categories: dict, failures: list[str]) -> None:
    """Each post copies "title URL" of itself, and of its original when it has a source record."""
    for post in posts:
        expected = [f"{post['metadata'].get('title')} {unquote(site.url_of(post['output']))}"]
        source = (categories.get(post["term"]) or {}).get("source")
        record = repo / "sources" / str(source) / f"{post['slug']}.md"
        if source and record.is_file() and (data := read_markdown(record)[0]).get("source_url"):
            expected.append(f"{data.get('title')} {data['source_url']}")
        actual = [unquote(text) for text in site.page(post["output"]).copy_texts]
        if sorted(actual) != sorted(unquote(text) for text in expected):
            failures.append(f"{post['output']}: copy buttons should copy {expected}, found {actual}")


def check_reading_paths(site: Site, repo: Path, failures: list[str]) -> None:
    """Topic directories, backlinks and next reads follow data/reading_paths.json."""
    definitions = json.loads((repo / "data/reading_paths.json").read_text(encoding="utf-8"))
    memberships: dict[str, list[str]] = {}
    for definition in definitions["paths"]:
        topic = definition["topic"].strip("/")
        topic_slug = topic.rsplit("/", 1)[-1]
        posts = [entry["post"].strip("/") for group in definition["groups"] for entry in group["entries"]]
        directory = [attrs.get("data-reading-path-post") for attrs, _ in site.page(f"{topic}/index.html").links_with("data-reading-path-post")]
        if directory != [post.rsplit("/", 1)[-1] for post in posts]:
            failures.append(f"{topic}: directory should list its posts in reading order")
        for index, post in enumerate(posts):
            memberships.setdefault(post, []).append(topic_slug)
            page_path = f"{post}/index.html"
            page = site.page(page_path)
            homes = [attrs for attrs, _ in page.links if attrs.get("data-reading-path-home") == topic_slug]
            nexts = [attrs for attrs, _ in page.links if attrs.get("data-reading-path-next") == topic_slug]
            if len(homes) != 1 or site.resolve(homes[0].get("href") or "", page_path) != f"{topic}/index.html":
                failures.append(f"{post}: should link back to {topic} once")
            following = [f"{posts[index + 1]}/index.html"] if index + 1 < len(posts) else []
            if [site.resolve(attrs.get("href") or "", page_path) for attrs in nexts] != following:
                failures.append(f"{post}: next read in {topic} should be {following[0] if following else 'absent'}")
    for path in sorted(site.root.glob("posts/*/index.html")):
        post = path.parent.relative_to(site.root).as_posix()
        actual = [attrs["data-reading-path-home"] for attrs, _ in site.page(f"{post}/index.html").links_with("data-reading-path-home")]
        if sorted(actual) != sorted(memberships.get(post, [])):
            failures.append(f"{post}: reading navigation should match its topic memberships")


def check_related_posts(site: Site, repo: Path, posts: list[dict], failures: list[str]) -> None:
    """Related posts share a topic tag, skip next reads, and appear whenever a candidate exists."""
    sources = set(json.loads((repo / "data/tag_groups.json").read_text(encoding="utf-8")).get("sources", []))
    topics = {post["output"]: set(post["metadata"].get("tags") or []) - sources for post in posts}
    for post in posts:
        page = site.page(post["output"])
        nexts = {site.resolve(attrs.get("href") or "", post["output"]) for attrs, _ in page.links_with("data-reading-path-next")}
        related = [site.resolve(attrs.get("href") or "", post["output"]) for attrs, _ in page.links_with("data-related-post")]
        candidates = {output for output, tags in topics.items() if tags & topics[post["output"]]} - {post["output"]} - nexts
        if len(related) > 3 or len(related) != len(set(related)):
            failures.append(f"{post['output']}: related posts should list at most three distinct articles")
        for target in related:
            if target not in candidates:
                failures.append(f"{post['output']}: related post {target} should be another article sharing a topic tag, not a next read")
        if candidates and not related:
            failures.append(f"{post['output']}: related posts are missing although other articles share its topic tags")


def check_learning_list(site: Site, repo: Path, posts: list[dict], failures: list[str]) -> None:
    """Learning state comes from source metadata; article pages stay free of it."""
    config = yaml.safe_load((repo / "config/_default/config.yaml").read_text(encoding="utf-8"))
    edit_base = config["params"]["contentEditURL"].rstrip("/")
    status_of = {post["slug"]: post["metadata"].get("learning_status", "unmarked") for post in posts}
    page = site.page("learning/index.html")
    groups = [group["attrs"].get("data-learning-group") for group in page.learning_groups]
    if sorted(groups) != sorted(LEARNING_GROUPS):
        failures.append("learning/index.html: should have one pending, done and unmarked group")
    entries = [attrs.get("data-learning-post") for attrs, _ in page.links_with("data-learning-post")]
    if sorted(entries) != sorted(status_of):
        failures.append("learning/index.html: should list every generated article exactly once")
    grouped = 0
    for group in page.learning_groups:
        status = group["attrs"].get("data-learning-group")
        for attrs, title in group["links"]:
            slug = attrs.get("data-learning-post")
            if slug is None:
                continue
            grouped += 1
            if slug in status_of and (status_of[slug] != status or attrs.get("data-learning-status") != status):
                failures.append(f"learning/index.html: {slug} belongs in the {status_of[slug]} group")
            href = attrs.get("href") or ""
            if not title or urlsplit(href).query or site.resolve(href, "learning/index.html") != f"posts/{slug}/index.html":
                failures.append(f"learning/index.html: {slug} should link to its ordinary article URL")
    if grouped != len(entries):
        failures.append("learning/index.html: every article should sit inside one learning group")
    edits: dict[str, list[str]] = {}
    for attrs, _ in page.links_with("data-learning-edit"):
        edits.setdefault(attrs["data-learning-edit"] or "", []).append(unquote(attrs.get("href") or ""))
    for post in posts:
        expected = f"{edit_base}/{post['source'].relative_to(repo / 'content').as_posix()}"
        if edits.get(post["slug"]) != [expected]:
            failures.append(f"learning/index.html: {post['slug']} needs one GitHub edit link to {expected}")
        if site.page(post["output"]).learning_controls:
            failures.append(f"{post['output']}: article pages should not contain learning controls or status")
    pending = str(sum(status == "pending" for status in status_of.values()))
    nav = site.page("index.html").links_with("data-learning-nav")
    if len(nav) != 1 or nav[0][0].get("data-pending-count") != pending or site.resolve(nav[0][0].get("href") or "", "index.html") != "learning/index.html":
        failures.append(f"index.html: sidebar should link to the learning list with pending count {pending}")


def check_legacy_entries(site: Site, repo: Path, failures: list[str]) -> None:
    """Retired tag pages keep working: they redirect to a category or keep listing their posts."""
    for index in sorted((repo / "content/tags").glob("*/_index.md")):
        metadata, _ = read_markdown(index)
        tag = index.parent.name
        if category := metadata.get("legacyCategory"):
            pagers = sorted(
                path.relative_to(site.root).as_posix()
                for path in (site.root / "tags" / tag / "page").glob("*/index.html")
                if path.parent.name != "1"
            )
            for path in (f"tags/{tag}/index.html", *pagers):
                target = f"categories/{category}/{path.removeprefix(f'tags/{tag}/')}"
                page = site.page(path)
                if not (page.is_redirect and site.same_url(page.canonical_url, site.url_of(target))):
                    failures.append(f"{path}: should redirect to {site.url_of(target)}")
        for slug in metadata.get("legacyPosts") or []:
            path = f"tags/{tag}/index.html"
            if not any(site.resolve(attrs.get("href") or "", path) == f"posts/{slug}/index.html" for attrs, _ in site.page(path).links):
                failures.append(f"{path}: should keep linking to posts/{slug}/")


def check_site(site_dir: Path, repo: Path = REPO, base_url: str | None = None) -> list[str]:
    failures: list[str] = []
    site = Site(site_dir)
    config = yaml.safe_load((repo / "config/_default/config.yaml").read_text(encoding="utf-8"))
    expected_home = base_url or config["baseURL"]
    if site.home_url.rstrip("/") != expected_home.rstrip("/"):
        return [f"index.html: canonical URL should be the site base URL {expected_home}"]
    categories = load_categories(repo)
    posts = generated_posts(site, repo, failures)
    check_required_outputs(site, categories, failures)
    check_canonicals(site, failures)
    check_languages(site, config.get("languageCode"), failures)
    check_local_references(site, failures)
    check_sitemap(site, failures)
    check_structured_data(site, posts, failures)
    check_search_index(site, repo, posts, categories, failures)
    check_article_types(site, repo, posts, categories, failures)
    check_source_lines(site, repo, posts, categories, failures)
    check_copy_buttons(site, repo, posts, categories, failures)
    check_reading_paths(site, repo, failures)
    check_related_posts(site, repo, posts, failures)
    check_learning_list(site, repo, posts, failures)
    check_legacy_entries(site, repo, failures)
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site_dir", nargs="?", type=Path, default=Path("public"))
    parser.add_argument("--base-url", help="the baseURL the site was built with (default: config baseURL)")
    args = parser.parse_args(argv)
    failures = check_site(args.site_dir, base_url=args.base_url)
    if failures:
        print("Site validation failed:")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print("Site validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
