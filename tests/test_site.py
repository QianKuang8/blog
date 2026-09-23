"""Regression checks for generated-site invariants, independent of live content."""

from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_site


class SiteFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.patch = patch.object(check_site, "SITE_DIR", self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        check_site.parse_html.cache_clear()
        self.addCleanup(check_site.parse_html.cache_clear)
        self.write("index.html", '<link rel="canonical" href="https://example.org/blog/">')

    def write(self, name, html):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")

class PaginationCanonicalTests(SiteFixture):
    def failures(self):
        failures = []
        check_site.validate_pagination_canonicals(failures)
        return failures

    def test_pager_must_not_canonicalize_to_first_page(self):
        self.write("posts/page/2/index.html", '<link rel="canonical" href="https://example.org/blog/posts/">')
        self.assertEqual(len(self.failures()), 1)

    def test_home_pager_must_describe_its_own_page(self):
        self.write("page/2/index.html", '<link rel="canonical" href="https://example.org/blog/">')
        self.assertEqual(len(self.failures()), 1)

    def test_self_canonical_with_encoded_chinese_path(self):
        self.write("tags/主题/page/2/index.html", '<link rel="canonical" href="https://example.org/blog/tags/%E4%B8%BB%E9%A2%98/page/2/">')
        self.assertEqual(self.failures(), [])

    def test_duplicate_canonical_is_rejected(self):
        link = '<link rel="canonical" href="https://example.org/blog/posts/page/2/">'
        self.write("posts/page/2/index.html", link + link)
        self.assertEqual(len(self.failures()), 1)

    def test_legacy_redirect_preserves_replacement(self):
        self.write("tags/视频笔记/page/2/index.html", '<meta http-equiv="refresh" content="0; url=/blog/categories/视频笔记/page/2/"><link rel="canonical" href="https://example.org/blog/categories/视频笔记/page/2/">')
        self.assertEqual(self.failures(), [])


class HomeNavigationTests(SiteFixture):
    def setUp(self):
        super().setUp()
        source_patch = patch.object(check_site, "__file__", str(self.root / "scripts/check_site.py"))
        source_patch.start()
        self.addCleanup(source_patch.stop)
        names = check_site.HOME_CATEGORY_ORDER
        for number in range(1, 13):
            self.write(f"content/posts/post-{number}.md", (
                f"---\ndate: '2026-09-{number:02}T12:00:00+08:00'\n"
                f"categories: ['{names[(number - 1) % 3]}']\n---\nArticle\n"
            ))
            self.write(f"posts/post-{number}/index.html", "Article")
        self.write("content/posts/hidden.md", (
            "---\ndate: '2026-09-20T12:00:00+08:00'\n"
            "categories: ['原创文章']\nhiddenInHomeList: true\n---\nHidden\n"
        ))
        self.write("posts/hidden/index.html", "Hidden article")
        self.write("content/posts/draft.md", (
            "---\ndate: '2026-09-21T12:00:00+08:00'\n"
            "categories: ['原创文章']\ndraft: true\n---\nDraft\n"
        ))
        self.slugs = [f"post-{number}" for number in range(12, 0, -1)]
        self.render_pages()

    def row(self, slug):
        return (f'<article data-post-entry="{slug}"><h2>'
                f'<a data-post-link="{slug}" href="/blog/posts/{slug}/">{slug}</a>'
                '</h2></article>')

    def render_pages(self, slugs=None, counts=(5, 4, 4)):
        slugs = self.slugs if slugs is None else slugs
        categories = ''.join(
            f'<a data-home-category="{name}" data-count="{count}" href="/blog/categories/{name}/">{check_site.CATEGORY_LABELS[name]}</a>'
            for name, count in zip(check_site.HOME_CATEGORY_ORDER, counts)
        )
        self.write("index.html", '<link rel="canonical" href="https://example.org/blog/">'
                   + categories + ''.join(map(self.row, slugs[:10]))
                   + '<a href="/blog/page/2/">下一页</a>')
        self.write("page/2/index.html", '<link rel="canonical" href="https://example.org/blog/page/2/">'
                   + ''.join(map(self.row, slugs[10:])))

    def failures(self):
        check_site.parse_html.cache_clear()
        failures = []
        check_site.validate_home_navigation(failures)
        return failures

    def test_latest_posts_mix_categories_with_full_pagination(self):
        self.assertEqual(self.failures(), [])

    def test_reversed_dates_are_rejected(self):
        changed = self.slugs.copy()
        changed[0], changed[1] = changed[1], changed[0]
        self.render_pages(changed)
        self.assertTrue(any("publication order" in failure for failure in self.failures()))

    def test_missing_latest_post_is_rejected(self):
        self.render_pages(self.slugs[1:])
        self.assertTrue(any("exactly once" in failure for failure in self.failures()))

    def test_duplicate_article_on_different_pages_is_rejected(self):
        self.render_pages(self.slugs[:-1] + [self.slugs[0]])
        self.assertTrue(any("exactly once" in failure for failure in self.failures()))

    def test_hidden_home_article_remains_in_category_count_but_not_home_list(self):
        self.assertEqual(self.failures(), [])
        self.render_pages(["hidden"] + self.slugs[1:])
        self.assertTrue(any("visible articles" in failure for failure in self.failures()))

    def test_category_count_uses_all_published_members(self):
        self.render_pages(counts=(4, 4, 4))
        self.assertTrue(any("data-count" in failure for failure in self.failures()))

    def test_category_link_must_use_this_site_and_its_deployment_path(self):
        path = self.root / "index.html"
        self.write("index.html", path.read_text().replace(
            'href="/blog/categories/原创文章/"', 'href="https://other.test/blog/categories/原创文章/"'
        ))
        self.assertTrue(any("target its category" in failure for failure in self.failures()))

    def test_category_display_rename_preserves_original_url(self):
        self.assertEqual(self.failures(), [])
        path = self.root / "index.html"
        self.write("index.html", path.read_text().replace(
            'href="/blog/categories/原创文章/"', 'href="/blog/categories/研究与实践/"'
        ))
        self.assertTrue(any("target its category" in failure for failure in self.failures()))

    def test_category_navigation_does_not_show_legacy_label(self):
        path = self.root / "index.html"
        self.write("index.html", path.read_text().replace('>研究与实践</a>', '>原创文章</a>'))
        self.assertTrue(any("should display" in failure for failure in self.failures()))

    def test_title_link_cannot_target_a_different_article(self):
        path = self.root / "index.html"
        self.write("index.html", path.read_text().replace('href="/blog/posts/post-12/"', 'href="/blog/posts/post-11/"'))
        self.assertTrue(any("target its article" in failure for failure in self.failures()))

    def test_missing_pagination_page_or_next_link_is_rejected(self):
        (self.root / "page/2/index.html").unlink()
        self.assertTrue(any("every expected page" in failure for failure in self.failures()))
        self.render_pages()
        path = self.root / "index.html"
        self.write("index.html", path.read_text().replace('<a href="/blog/page/2/">下一页</a>', ''))
        self.assertTrue(any("link to its next page" in failure for failure in self.failures()))


class ArticleCategoryTests(SiteFixture):
    def setUp(self):
        super().setUp()
        source_patch = patch.object(check_site, "__file__", str(self.root / "scripts/check_site.py"))
        source_patch.start()
        self.addCleanup(source_patch.stop)
        for slug, term in (("original", "原创文章"), ("reading", "好文分享"), ("book", "好文分享")):
            self.write(f"content/posts/{slug}.md", f"---\ncategories: ['{term}']\n---\nArticle\n")
            self.write(f"posts/{slug}/index.html", "Article")
        self.write("sources/orig/book.md", "---\nsource_type: book\n---\nBook evidence\n")

    def category_link(self, term, label, href=None):
        href = href or f"/blog/categories/{term}/"
        return f'<a class="article-type" data-category-term="{term}" href="{href}">{label}</a>'

    def failures(self, slug, html):
        failures = []
        categories = check_site.source_article_categories(failures)
        page = check_site.PageParser()
        page.feed(html)
        check_site.validate_article_category(f"posts/{slug}/index.html", page, categories, failures)
        return failures

    def test_new_display_names_keep_original_category_identity_and_url(self):
        self.assertEqual(self.failures("original", self.category_link("原创文章", "研究与实践")), [])
        self.assertEqual(self.failures("reading", self.category_link("好文分享", "文章解读")), [])

    def test_book_evidence_selects_book_label_without_creating_category(self):
        self.assertEqual(self.failures("book", self.category_link("好文分享", "书籍导读")), [])
        failures = self.failures("book", self.category_link("好文分享", "文章解读"))
        self.assertTrue(any("displayed as 书籍导读" in failure for failure in failures))

    def test_article_cannot_use_book_label_without_book_evidence(self):
        failures = self.failures("reading", self.category_link("好文分享", "书籍导读"))
        self.assertTrue(any("displayed as 文章解读" in failure for failure in failures))

    def test_explicit_slug_selects_generated_page_and_book_evidence(self):
        self.write("content/posts/reading.md", "---\nslug: reading-book\ncategories: ['好文分享']\n---\nArticle\n")
        self.write("posts/reading-book/index.html", "Article")
        self.write("sources/orig/reading-book.md", "---\nsource_type: book\n---\nBook evidence\n")
        self.assertEqual(self.failures("reading-book", self.category_link("好文分享", "书籍导读")), [])

    def test_renamed_or_external_category_url_is_rejected(self):
        for href in ("/blog/categories/研究与实践/", "https://other.test/blog/categories/原创文章/"):
            with self.subTest(href=href):
                failures = self.failures("original", self.category_link("原创文章", "研究与实践", href))
                self.assertTrue(any("original category URL" in failure for failure in failures))

    def test_category_identity_must_match_source_even_when_link_and_label_match(self):
        html = self.category_link("原创文章", "研究与实践").replace(
            'data-category-term="原创文章"', 'data-category-term="好文分享"'
        )
        self.assertTrue(any("identity should match" in failure for failure in self.failures("original", html)))

    def test_duplicate_article_categories_are_rejected(self):
        html = self.category_link("原创文章", "研究与实践")
        self.assertTrue(any("exactly one article category" in failure for failure in self.failures("original", html + html)))

    def test_multiple_source_categories_are_rejected(self):
        self.write("content/posts/original.md", "---\ncategories: ['原创文章', '好文分享']\n---\nArticle\n")
        failures = self.failures("original", self.category_link("原创文章", "研究与实践"))
        self.assertTrue(any("exactly one supported source category" in failure for failure in failures))

    def test_search_uses_category_label_even_for_book_subtype(self):
        category_urls = {"https://example.org/blog/posts/book/": "阅读与解读"}
        item = {"permalink": "https://example.org/blog/posts/book/", "category": "阅读与解读"}
        failures = []
        check_site.validate_search_category(item, 0, category_urls, failures)
        self.assertEqual(failures, [])
        for label in ("好文分享", "研究与实践", "书籍导读", "专题"):
            with self.subTest(label=label):
                failures = []
                check_site.validate_search_category({**item, "category": label}, 0, category_urls, failures)
                self.assertTrue(failures)


class ReadingPathTests(SiteFixture):
    def setUp(self):
        super().setUp()
        source_patch = patch.object(check_site, "__file__", str(self.root / "scripts/check_site.py"))
        source_patch.start()
        self.addCleanup(source_patch.stop)
        self.write("data/reading_paths.json", json.dumps({"paths": [{
            "topic": "/topics/example", "groups": [{"entries": [
                {"post": "/posts/one", "reason": "Start here."},
                {"post": "/posts/two", "reason": "Continue here."},
            ]}],
        }]}))
        self.write("topics/example/index.html", '<a data-reading-path-post="one" href="/blog/posts/one/">One</a><a data-reading-path-post="two" href="/blog/posts/two/">Two</a>')
        self.home = '<a data-reading-path-home="example" href="/blog/topics/example/">Example</a>'
        self.write("posts/one/index.html", self.home + '<a data-reading-path-next="example" href="/blog/posts/two/">Two</a>')
        self.write("posts/two/index.html", self.home)

    def failures(self):
        failures = []
        check_site.validate_reading_paths(failures)
        return failures

    def test_bidirectional_path_with_next_read(self):
        self.assertEqual(self.failures(), [])

    def test_missing_backlink_fails(self):
        self.write("posts/two/index.html", "No navigation")
        self.assertTrue(self.failures())

    def test_wrong_next_read_fails(self):
        self.write("posts/one/index.html", self.home + '<a data-reading-path-next="example" href="/blog/posts/one/">One</a>')
        self.assertTrue(self.failures())

    def test_final_entry_must_not_loop_to_start(self):
        self.write("posts/two/index.html", self.home + '<a data-reading-path-next="example" href="/blog/posts/one/">One</a>')
        self.assertTrue(self.failures())


class MainMenuParserTests(unittest.TestCase):
    def test_nav_menu_tracks_nested_lists_and_stops_at_its_closing_tag(self):
        parser = check_site.PageParser()
        parser.feed('<nav id="menu"><ul><li><a href="/one/">One</a></li></ul>'
                    '<a href="/two/">Two</a></nav><a href="/outside/">Outside</a>')
        self.assertEqual([text for _, text in parser.main_menu_links], ["One", "Two"])

    def test_legacy_ul_menu_remains_supported(self):
        parser = check_site.PageParser()
        parser.feed('<ul id="menu"><li><a href="/one/">One</a></li></ul><a href="/outside/">Outside</a>')
        self.assertEqual([text for _, text in parser.main_menu_links], ["One"])


class LearningNavigationTests(SiteFixture):
    def setUp(self):
        super().setUp()
        source_patch = patch.object(check_site, "__file__", str(self.root / "scripts/check_site.py"))
        source_patch.start()
        self.addCleanup(source_patch.stop)
        self.posts = {"waiting": "pending", "learned": "done", "video": "unmarked"}
        self.nav = '<nav id="menu"><a data-learning-nav data-pending-count="1" href="/blog/learning/">学习清单</a></nav>'
        self.write("index.html", '<link rel="canonical" href="https://example.org/blog/">' + self.nav)
        for slug, status in self.posts.items():
            filename = "original-filename" if slug == "learned" else slug
            metadata = f"slug: {slug}\n" if filename != slug else ""
            metadata += "categories: ['视频笔记']\n"
            if status != "unmarked":
                metadata += f"learning_status: {status}\n"
            self.write(f"content/posts/{filename}.md", f"---\n{metadata}---\nArticle\n")
            self.write(f"posts/{slug}/index.html", self.nav + (
                f'<section data-learning-record data-learning-status="{status}" hidden>'
                f'<a data-learning-edit href="https://github.com/QianKuang8/blog/edit/main/content/posts/{filename}.md">Edit</a>'
                f'<a data-learning-back href="/blog/learning/#learning-{status}">Back</a></section>'
            ))
        for slug, condition in (("draft", "draft: true"), ("future", "date: '2099-01-01T00:00:00Z'"), ("expired", "expiryDate: '2000-01-01T00:00:00Z'")):
            self.write(f"content/posts/{slug}.md", f"---\n{condition}\nlearning_status: pending\n---\nNot in this build\n")
        self.render_learning()

    def entry(self, slug):
        return (f'<a data-learning-post="{slug}" data-learning-status="{self.posts[slug]}" '
                f'href="/blog/posts/{slug}/?learning=1">{slug}</a>')

    def render_learning(self, assignments=None):
        assignments = assignments or {status: [slug for slug in self.posts if self.posts[slug] == status]
                                      for status in ("pending", "done", "unmarked")}
        html = self.nav
        for status, slugs in assignments.items():
            tag = "section" if status == "pending" else "details"
            html += (f'<{tag} id="learning-{status}" data-learning-group="{status}" data-count="{len(slugs)}">'
                     + ''.join(self.entry(slug) for slug in slugs) + f'</{tag}>')
        self.write("learning/index.html", html)

    def replace(self, path, before, after):
        self.write(path, (self.root / path).read_text().replace(before, after))

    def failures(self):
        check_site.parse_html.cache_clear()
        failures = []
        check_site.validate_learning_navigation(failures)
        return failures

    def assert_failure(self, expected):
        self.assertTrue(any(expected in failure for failure in self.failures()), self.failures())

    def test_source_status_and_generated_membership_define_list(self):
        self.assertEqual(self.failures(), [])
        # Hugo's emitted artifact decides inclusion, even in a preview build.
        source = self.root / "content/posts/waiting.md"
        source.write_text(source.read_text().replace("---\n", "---\ndraft: true\ndate: '2099-01-01T00:00:00Z'\n", 1))
        self.assertEqual(self.failures(), [])

    def test_missing_and_duplicate_articles_are_rejected(self):
        self.replace("learning/index.html", self.entry("video"), "")
        self.assert_failure("exactly once")
        self.render_learning()
        self.replace("learning/index.html", self.entry("waiting"), self.entry("waiting") * 2)
        self.assert_failure("exactly once")

    def test_article_must_be_inside_its_source_status_group(self):
        self.render_learning({"pending": ["video"], "done": ["learned"], "unmarked": ["waiting"]})
        self.assert_failure("source learning status")
        self.render_learning()
        self.replace("learning/index.html", self.entry("waiting"), "")
        self.write("learning/index.html", (self.root / "learning/index.html").read_text() + self.entry("waiting"))
        self.assert_failure("exactly one learning group")

    def test_group_counts_follow_source_state(self):
        self.replace("learning/index.html", 'data-count="1"', 'data-count="2"')
        self.assert_failure("data-count should match source status count")

    def test_group_anchors_and_default_expansion_are_checked(self):
        self.replace("learning/index.html", '<details id="learning-done"', '<details open id="learning-done"')
        self.assert_failure("expected default expansion")
        self.render_learning()
        self.replace("learning/index.html", 'id="learning-unmarked"', 'id="other"')
        self.assert_failure("stable anchor")

    def test_title_link_preserves_site_article_and_learning_context(self):
        for href in ("/blog/posts/waiting/", "/blog/posts/video/?learning=1", "https://other.test/blog/posts/waiting/?learning=1"):
            with self.subTest(href=href):
                self.render_learning()
                self.replace("learning/index.html", '/blog/posts/waiting/?learning=1', href)
                self.assert_failure("title link should target its article with learning=1")

    def test_footer_is_hidden_until_learning_context_and_uses_source_state(self):
        self.replace("posts/waiting/index.html", ' hidden>', '>')
        self.assert_failure("should start hidden")
        self.replace("posts/video/index.html", 'data-learning-status="unmarked"', 'data-learning-status="done"')
        self.assert_failure("match source status (unmarked)")

    def test_explicit_slug_must_edit_real_source_filename(self):
        self.assertEqual(self.failures(), [])
        self.replace("posts/learned/index.html", '/content/posts/original-filename.md', '/content/posts/learned.md')
        self.assert_failure("actual source file on GitHub")

    def test_footer_links_must_be_inside_record_and_return_to_correct_group(self):
        self.replace("posts/waiting/index.html", '#learning-pending', '#learning-done')
        self.assert_failure("back link should target its status group")
        self.replace("posts/video/index.html", '<a data-learning-edit', '</section><a data-learning-edit')
        self.assert_failure("actual source file on GitHub")

    def test_sidebar_pending_count_and_destination_are_checked(self):
        self.replace("posts/video/index.html", 'data-pending-count="1"', 'data-pending-count="3"')
        self.assert_failure("sidebar should link to the learning list with pending count 1")
        self.replace("index.html", 'href="/blog/learning/"', 'href="/learning/"')
        self.assert_failure("index.html: sidebar")


if __name__ == "__main__":
    unittest.main()
