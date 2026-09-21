"""Run real Hugo builds to catch stale-output and failed-promotion regressions."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_site import build_site


@unittest.skipUnless(shutil.which("hugo"), "Hugo is required for build integration tests")
class CleanBuildTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        for directory in ("content/posts", "config/_default", "layouts/_default", "scripts"):
            (self.repo / directory).mkdir(parents=True)
        (self.repo / "config/_default/config.yaml").write_text("baseURL: https://example.com/blog/\n")
        (self.repo / "layouts/_default/single.html").write_text("<!doctype html><title>{{ .Title }}</title>{{ .Content }}")
        (self.repo / "layouts/_default/list.html").write_text("<!doctype html><title>{{ .Title }}</title>{{ range .Pages }}{{ .Title }}{{ end }}")
        # Production invokes the repository's full checker. This fixture isolates
        # build/promotion behavior without recreating the entire blog theme.
        (self.repo / "scripts/check_site.py").write_text("from pathlib import Path\nimport sys\nassert (Path(sys.argv[1]) / 'posts/keep/index.html').is_file()\n")
        content = """---
date: '2026-01-01T12:00:00+08:00'
lastmod: '2026-01-01T12:00:00+08:00'
title: Example
summary: Summary
description: Description
author: Qian
categories: [原创文章]
tags: []
isCJKLanguage: true
showToc: true
---
Article body.
"""
        for name in ("keep", "remove"):
            (self.repo / f"content/posts/{name}.md").write_text(content)

    def test_deleted_article_does_not_survive_rebuild(self):
        build_site(self.repo)
        obsolete = self.repo / "public/posts/remove/index.html"
        self.assertTrue(obsolete.is_file())
        (self.repo / "content/posts/remove.md").unlink()
        build_site(self.repo)
        self.assertFalse(obsolete.exists())
        self.assertTrue((self.repo / "public/posts/keep/index.html").is_file())

    def test_failed_source_validation_preserves_previous_output(self):
        build_site(self.repo)
        previous = (self.repo / "public/posts/keep/index.html").read_bytes()
        (self.repo / "content/posts/keep.md").write_text("invalid frontmatter")
        with self.assertRaisesRegex(ValueError, "Content validation failed"):
            build_site(self.repo)
        self.assertEqual((self.repo / "public/posts/keep/index.html").read_bytes(), previous)

    def test_failed_output_validation_preserves_previous_output(self):
        build_site(self.repo)
        previous = (self.repo / "public/posts/keep/index.html").read_bytes()
        (self.repo / "scripts/check_site.py").write_text("raise SystemExit(1)\n")
        with self.assertRaises(subprocess.CalledProcessError):
            build_site(self.repo)
        self.assertEqual((self.repo / "public/posts/keep/index.html").read_bytes(), previous)
        self.assertEqual(list(self.repo.glob(".public-build-*")), [])

    def test_public_symlink_is_rejected_without_touching_target(self):
        target = self.repo / "content"
        (self.repo / "public").symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "not a symlink"):
            build_site(self.repo)
        self.assertTrue((target / "posts/keep.md").is_file())


if __name__ == "__main__":
    unittest.main()
