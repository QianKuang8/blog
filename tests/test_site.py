"""Regression checks for generated-site invariants, independent of live content."""

from pathlib import Path
import json
import shutil
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import check_site
from site_output import Page, Site


class SiteFixture(unittest.TestCase):
    """A generated site in `site/` beside a minimal source repository in `repo/`."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "site"
        self.repo = Path(self.temp.name) / "repo"
        for directory in ("config/_default", "data", "content/posts"):
            (self.repo / directory).mkdir(parents=True)
        shutil.copy(REPO / "data/categories.json", self.repo / "data/categories.json")
        (self.repo / "config/_default/config.yaml").write_text(
            "baseURL: https://example.org/blog/\n"
            "params:\n  contentEditURL: https://github.com/QianKuang8/blog/edit/main/content\n"
        )
        for term, label in (("原创文章", "研究与实践"), ("好文分享", "阅读与解读"), ("视频笔记", "视频笔记")):
            self.write_source(f"content/categories/{term}/_index.md", f"---\ntitle: {label}\n---\n")
        self.write("index.html", '<link rel="canonical" href="https://example.org/blog/">')

    def write(self, name, html):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")

    def write_source(self, name, text):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def replace(self, name, before, after):
        self.write(name, (self.root / name).read_text(encoding="utf-8").replace(before, after))

    def site(self):
        return Site(self.root)

    def posts(self):
        return check_site.generated_posts(self.site(), self.repo, [])

    def categories(self):
        return check_site.load_categories(self.repo)


class CanonicalTests(SiteFixture):
    def failures(self):
        failures = []
        check_site.check_canonicals(self.site(), failures)
        return failures

    def test_pager_must_not_canonicalize_to_first_page(self):
        self.write("posts/page/2/index.html", '<link rel="canonical" href="https://example.org/blog/posts/">')
        self.assertEqual(len(self.failures()), 1)

    def test_self_canonical_with_encoded_chinese_path(self):
        self.write("tags/主题/page/2/index.html", '<link rel="canonical" href="https://example.org/blog/tags/%E4%B8%BB%E9%A2%98/page/2/">')
        self.assertEqual(self.failures(), [])

    def test_missing_or_duplicate_canonical_is_rejected(self):
        link = '<link rel="canonical" href="https://example.org/blog/posts/page/2/">'
        for html in ("", link + link):
            with self.subTest(html=html):
                self.write("posts/page/2/index.html", html)
                self.assertEqual(len(self.failures()), 1)

    def test_redirect_names_its_replacement(self):
        self.write("tags/old/index.html", '<meta http-equiv="refresh" content="0; url=/blog/categories/new/"><link rel="canonical" href="https://example.org/blog/categories/new/">')
        self.assertEqual(self.failures(), [])


class LocalReferenceTests(SiteFixture):
    def failures(self):
        failures = []
        check_site.check_local_references(self.site(), failures)
        return failures

    def test_existing_targets_and_other_sites_pass(self):
        self.write("posts/one/index.html", '<a href="/blog/posts/two/">Two</a><img src="../../images/a.svg"><a href="https://other.test/x">X</a><a href="#top">Top</a>')
        self.write("posts/two/index.html", "")
        self.write("images/a.svg", "<svg/>")
        self.assertEqual(self.failures(), [])

    def test_missing_target_is_rejected(self):
        self.write("posts/one/index.html", '<a href="/blog/pdfs/missing.pdf">PDF</a>')
        self.assertIn("target does not exist", "\n".join(self.failures()))

    def test_every_srcset_candidate_must_exist(self):
        self.write("images/a.png", "png")
        self.write("images/a_720.webp", "webp")
        self.write("posts/one/index.html", '<img src="/blog/images/a_720.webp" srcset="/blog/images/a_720.webp 720w, /blog/images/a_1440.webp 1440w">')
        failures = self.failures()
        self.assertEqual(len(failures), 1)
        self.assertIn("img[srcset] target does not exist: /blog/images/a_1440.webp", failures[0])

    def test_relative_reference_must_keep_the_site_path(self):
        self.write("posts/one/index.html", '<a href="/pdfs/file.pdf">PDF</a>')
        self.assertIn("outside the site path", "\n".join(self.failures()))


class SitemapTests(SiteFixture):
    def failures(self):
        failures = []
        check_site.check_sitemap(self.site(), failures)
        return failures

    def sitemap(self, *paths):
        self.write("sitemap.xml", '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                   + "".join(f"<url><loc>https://example.org/blog/{path}</loc></url>" for path in paths) + "</urlset>")

    def test_indexable_pages_pass(self):
        self.write("posts/one/index.html", '<meta name="robots" content="index, follow">')
        self.sitemap("", "posts/one/")
        self.assertEqual(self.failures(), [])

    def test_noindex_redirect_and_missing_pages_are_rejected(self):
        self.write("search/index.html", '<meta name="robots" content="noindex, nofollow">')
        self.write("tags/old/index.html", '<meta http-equiv="refresh" content="0; url=/blog/">')
        self.sitemap("search/", "tags/old/", "missing/")
        self.assertEqual(len(self.failures()), 3)


class ArticleTests(SiteFixture):
    def setUp(self):
        super().setUp()
        for slug, term in (("original", "原创文章"), ("reading", "好文分享"), ("book", "好文分享")):
            self.write_source(f"content/posts/{slug}.md", f"---\ncategories: ['{term}']\nlearning_status: done\n---\nArticle\n")
            self.write(f"posts/{slug}/index.html", self.article(term, "研究与实践" if slug == "original" else "文章解读"))
        self.write_source("sources/orig/book.md", "---\nsource_type: book\n---\nBook evidence\n")
        self.replace("posts/book/index.html", ">文章解读<", ">书籍导读<")

    def article(self, term, label, date="2026-01-02T00:00:00+08:00"):
        schema = {"@type": "BlogPosting", "datePublished": "2026-01-01T00:00:00+08:00", "dateModified": date}
        return (f'<script type="application/ld+json">{json.dumps(schema)}</script>'
                f'<a class="article-type" data-category-term="{term}" href="/blog/categories/{term}/">{label}</a>')

    def type_failures(self):
        failures = []
        check_site.check_article_types(self.site(), self.repo, self.posts(), self.categories(), failures)
        return failures

    def test_category_labels_and_book_type(self):
        self.assertEqual(self.type_failures(), [])

    def test_book_type_requires_book_evidence(self):
        self.replace("posts/reading/index.html", ">文章解读<", ">书籍导读<")
        self.assertIn("posts/reading/index.html", "\n".join(self.type_failures()))
        self.replace("posts/reading/index.html", ">书籍导读<", ">文章解读<")
        self.replace("posts/book/index.html", ">书籍导读<", ">文章解读<")
        self.assertIn("posts/book/index.html", "\n".join(self.type_failures()))

    def test_type_link_must_keep_category_identity_and_url(self):
        for before, after in (('data-category-term="原创文章"', 'data-category-term="好文分享"'),
                              ("/blog/categories/原创文章/", "/blog/categories/研究与实践/")):
            with self.subTest(after=after):
                self.write("posts/original/index.html", self.article("原创文章", "研究与实践").replace(before, after))
                self.assertIn("posts/original/index.html", "\n".join(self.type_failures()))

    def test_blogposting_appears_once_on_articles_only(self):
        failures = []
        check_site.check_structured_data(self.site(), self.posts(), failures)
        self.assertEqual(failures, [])
        self.write("posts/reading/index.html", self.article("好文分享", "文章解读", date="2025-01-01T00:00:00+08:00"))
        self.write("archives/index.html", self.article("原创文章", "研究与实践"))
        failures = []
        check_site.check_structured_data(self.site(), self.posts(), failures)
        self.assertEqual(len(failures), 2, failures)

    def search_failures(self, index):
        self.write("index.json", json.dumps(index, ensure_ascii=False))
        failures = []
        check_site.check_search_index(self.site(), self.posts(), self.categories(), failures)
        return failures

    def search_item(self, slug, category):
        return {"title": slug, "content": "", "summary": "", "permalink": f"https://example.org/blog/posts/{slug}/",
                "category": category, "date": "2026-01-01", "tags": []}

    def test_search_index_covers_articles_with_category_labels(self):
        items = [self.search_item("original", "研究与实践"), self.search_item("reading", "阅读与解读"),
                 self.search_item("book", "阅读与解读"),
                 {**self.search_item("topic", "专题"), "permalink": "https://example.org/blog/topics/topic/", "date": ""}]
        self.assertEqual(self.search_failures(items), [])
        self.assertTrue(self.search_failures(items[1:]))
        self.assertTrue(self.search_failures([*items, items[0]]))
        self.assertTrue(self.search_failures([{**items[0], "category": "原创文章"}, *items[1:]]))


class ReadingPathTests(SiteFixture):
    def setUp(self):
        super().setUp()
        self.write_source("data/reading_paths.json", json.dumps({"paths": [{
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
        check_site.check_reading_paths(self.site(), self.repo, failures)
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

    def test_directory_order_is_checked(self):
        self.write("topics/example/index.html", '<a data-reading-path-post="two" href="/blog/posts/two/">Two</a><a data-reading-path-post="one" href="/blog/posts/one/">One</a>')
        self.assertTrue(self.failures())


class LearningListTests(SiteFixture):
    def setUp(self):
        super().setUp()
        self.posts_status = {"waiting": "pending", "learned": "done", "video": "unmarked"}
        self.nav = '<nav><a data-learning-nav data-pending-count="1" href="/blog/learning/">学习清单</a></nav>'
        self.write("index.html", '<link rel="canonical" href="https://example.org/blog/">' + self.nav)
        for slug, status in self.posts_status.items():
            filename = "original-filename" if slug == "learned" else slug
            metadata = f"slug: {slug}\n" if filename != slug else ""
            if status != "unmarked":
                metadata += f"learning_status: {status}\n"
            self.write_source(f"content/posts/{filename}.md", f"---\ncategories: ['视频笔记']\n{metadata}---\nArticle\n")
            self.write(f"posts/{slug}/index.html", self.nav + "<article>Article body</article>")
        # Not generated in this build, so not expected in the list.
        self.write_source("content/posts/draft.md", "---\ndraft: true\nlearning_status: pending\n---\nDraft\n")
        self.render()

    def entry(self, slug):
        return (f'<a data-learning-post="{slug}" data-learning-status="{self.posts_status[slug]}" '
                f'href="/blog/posts/{slug}/">{slug}</a>')

    def edit_link(self, slug):
        filename = "original-filename" if slug == "learned" else slug
        return f'<a data-learning-edit="{slug}" href="https://github.com/QianKuang8/blog/edit/main/content/posts/{filename}.md">Edit</a>'

    def render(self, assignments=None):
        assignments = assignments or {status: [slug for slug in self.posts_status if self.posts_status[slug] == status]
                                      for status in ("pending", "done", "unmarked")}
        html = self.nav
        for status, slugs in assignments.items():
            tag = "section" if status == "pending" else "details"
            html += (f'<{tag} id="learning-{status}" data-learning-group="{status}">'
                     + "".join(self.entry(slug) + self.edit_link(slug) for slug in slugs) + f"</{tag}>")
        self.write("learning/index.html", html)

    def failures(self):
        failures = []
        check_site.check_learning_list(self.site(), self.repo, self.posts(), failures)
        return failures

    def assert_failure(self, expected):
        failures = self.failures()
        self.assertTrue(any(expected in failure for failure in failures), failures)

    def test_source_status_and_generated_membership_define_list(self):
        self.assertEqual(self.failures(), [])

    def test_missing_and_duplicate_articles_are_rejected(self):
        self.replace("learning/index.html", self.entry("video"), "")
        self.assert_failure("every generated article exactly once")
        self.render()
        self.replace("learning/index.html", self.entry("waiting"), self.entry("waiting") * 2)
        self.assert_failure("every generated article exactly once")

    def test_article_must_be_inside_its_source_status_group(self):
        self.render({"pending": ["video"], "done": ["learned"], "unmarked": ["waiting"]})
        self.assert_failure("belongs in the")
        self.render()
        self.replace("learning/index.html", self.entry("waiting"), "")
        self.write("learning/index.html", (self.root / "learning/index.html").read_text() + self.entry("waiting"))
        self.assert_failure("inside one learning group")

    def test_title_link_uses_ordinary_article_url(self):
        for href in ("/blog/posts/waiting/?learning=1", "/blog/posts/video/", "https://other.test/blog/posts/waiting/"):
            with self.subTest(href=href):
                self.render()
                self.replace("learning/index.html", 'href="/blog/posts/waiting/"', f'href="{href}"')
                self.assert_failure("ordinary article URL")

    def test_article_pages_reject_learning_controls(self):
        for control in ('<section data-learning-record hidden></section>', '<span data-learning-status="done">已学习</span>', self.edit_link("waiting")):
            with self.subTest(control=control):
                self.write("posts/waiting/index.html", self.nav + control)
                self.assert_failure("should not contain learning controls")

    def test_edit_link_targets_the_real_source_file_once(self):
        self.replace("learning/index.html", "/content/posts/original-filename.md", "/content/posts/learned.md")
        self.assert_failure("learned needs one GitHub edit link")
        self.render()
        self.replace("learning/index.html", self.edit_link("waiting"), self.edit_link("waiting") * 2)
        self.assert_failure("waiting needs one GitHub edit link")

    def test_sidebar_pending_count_and_destination_are_checked(self):
        self.replace("index.html", 'data-pending-count="1"', 'data-pending-count="3"')
        self.assert_failure("pending count 1")
        self.replace("index.html", 'data-pending-count="3" href="/blog/learning/"', 'data-pending-count="1" href="/learning/"')
        self.assert_failure("pending count 1")


class LegacyEntryTests(SiteFixture):
    def setUp(self):
        super().setUp()
        self.write_source("content/tags/old-video/_index.md", "---\nlegacyCategory: 视频笔记\n---\n")
        self.write_source("content/tags/old-picks/_index.md", "---\nlegacyPosts: [kept]\n---\n")
        self.redirect("tags/old-video/index.html", "categories/视频笔记/")
        self.redirect("tags/old-video/page/2/index.html", "categories/视频笔记/page/2/")
        self.write("tags/old-picks/index.html", '<a href="/blog/posts/kept/">Kept</a>')

    def redirect(self, path, target):
        url = f"https://example.org/blog/{target}"
        self.write(path, f'<link rel="canonical" href="{url}"><meta http-equiv="refresh" content="0; url={url}">')

    def failures(self):
        failures = []
        check_site.check_legacy_entries(self.site(), self.repo, failures)
        return failures

    def test_retired_entries_keep_working(self):
        self.assertEqual(self.failures(), [])

    def test_wrong_redirect_and_lost_post_are_rejected(self):
        self.redirect("tags/old-video/page/2/index.html", "categories/视频笔记/")
        self.write("tags/old-picks/index.html", "")
        self.assertEqual(len(self.failures()), 2)


class PageParserTests(unittest.TestCase):
    def test_learning_groups_collect_nested_links(self):
        page = Page('<section data-learning-group="pending"><ol><li><a href="/a/">A</a></li></ol></section><a href="/b/">B</a>')
        self.assertEqual([text for _, text in page.learning_groups[0]["links"]], ["A"])
        self.assertEqual([text for _, text in page.links], ["A", "B"])


if __name__ == "__main__":
    unittest.main()
