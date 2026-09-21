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


if __name__ == "__main__":
    unittest.main()
