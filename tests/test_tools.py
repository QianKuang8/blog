"""Tests for the writing tools: starting an external-article draft and the lastmod reminder."""

from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from check_content import read_markdown, validate_content
from lastmod_reminder import reminders
from new_post import author_name, create_post, published_date

NOW = datetime(2026, 10, 26, 18, 0, tzinfo=timezone(timedelta(hours=8)))
DEFUDDLE = {
    "title": "Product Evals in Three Simple Steps",
    "description": "Label some data, align LLM-evaluators, and run the eval harness with each change",
    "domain": "eugeneyan.com",
    "author": "",
    "published": "2025-11-23T00:00:00+00:00",
    "metaTags": [
        {"name": "author", "property": None, "content": "Eugene Yan"},
        {"name": None, "property": "article:author", "content": "https://eugeneyan.com/about/"},
    ],
    "schemaOrgData": [],
    "content": "There are three basic steps.\n\n## First, label some data\n\nText.",
}


class NewPostTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        for directory in ("content/posts", "sources/orig", "sources/archive/orig", "config/_default", "data"):
            (self.repo / directory).mkdir(parents=True)
        for name in ("categories.json", "tag_groups.json"):
            shutil.copy(REPO / "data" / name, self.repo / "data" / name)
        (self.repo / "config/_default/config.yaml").write_text("baseURL: https://example.com/blog/\n")
        url = "https://eugeneyan.com/writing/product-evals/"
        self.notes = create_post(self.repo, "product-evals", url, DEFUDDLE, NOW)

    def test_writes_archive_record_and_draft_that_pass_the_checks(self):
        archived, body = read_markdown(self.repo / "sources/archive/orig/product-evals.md")
        self.assertEqual(archived, {
            "title": "Product Evals in Three Simple Steps", "source_url": "https://eugeneyan.com/writing/product-evals/",
            "domain": "eugeneyan.com", "author": "Eugene Yan", "published_at": "2025-11-23",
            "description": DEFUDDLE["description"], "retrieved_at": "2026-10-26T18:00:00+08:00", "extractor": "defuddle",
        })
        self.assertIn("## First, label some data", body)
        public = (self.repo / "sources/orig/product-evals.md").read_text(encoding="utf-8")
        self.assertEqual(read_markdown(self.repo / "sources/orig/product-evals.md"), (archived, ""))
        self.assertNotIn("three basic steps", public)
        draft, text = read_markdown(self.repo / "content/posts/product-evals.md")
        self.assertIs(draft["draft"], True)
        self.assertEqual(draft["categories"], ["好文分享"])
        self.assertIn("- [Product Evals in Three Simple Steps — Eugene Yan](https://eugeneyan.com/writing/product-evals/)", text)
        self.assertEqual(self.notes, [])
        # The draft, its record and the archive satisfy the build checks, archive comparison included.
        self.assertEqual(validate_content(self.repo), [])

    def test_never_overwrites_and_requires_the_archive(self):
        with self.assertRaisesRegex(ValueError, "already exists: sources/archive/orig/product-evals.md"):
            create_post(self.repo, "product-evals", "https://example.com", DEFUDDLE, NOW)
        shutil.rmtree(self.repo / "sources/archive")
        with self.assertRaisesRegex(ValueError, "clone blog-sources first"):
            create_post(self.repo, "other", "https://example.com", DEFUDDLE, NOW)

    def test_rejects_bad_slugs_and_empty_extractions(self):
        with self.assertRaisesRegex(ValueError, "slug must use"):
            create_post(self.repo, "Bad Slug", "https://example.com", DEFUDDLE, NOW)
        with self.assertRaisesRegex(ValueError, "no title or no text"):
            create_post(self.repo, "empty", "https://example.com", {**DEFUDDLE, "content": " "}, NOW)
        self.assertFalse((self.repo / "content/posts/empty.md").exists())

    def test_missing_metadata_is_reported_for_manual_checks(self):
        data = {"title": "Untitled", "content": "Text.", "published": "", "author": ""}
        notes = create_post(self.repo, "bare", "https://www.example.com/post", data, NOW)
        record = read_markdown(self.repo / "sources/archive/orig/bare.md")[0]
        self.assertIsNone(record["published_at"])
        self.assertNotIn("author", record)
        self.assertEqual(record["domain"], "example.com")
        self.assertEqual(len(notes), 3)
        notes = create_post(self.repo, "dated", "https://example.com/post", data, NOW, published="2024-05", author="Example Team")
        record = read_markdown(self.repo / "sources/archive/orig/dated.md")[0]
        self.assertEqual((record["published_at"], record["author"]), ("2024-05", "Example Team"))

    def test_publication_dates_and_authors_are_read_from_common_formats(self):
        for value, expected in (("2026-03-11T08:00:00Z", "2026-03-11"), ("March 11, 2026", "2026-03-11"),
                                ("11 Mar 2026", "2026-03-11"), ("", None), ("soon", None)):
            with self.subTest(value=value):
                self.assertEqual(published_date(value), expected)
        schema = {"author": "", "schemaOrgData": [{"author": [{"name": "A"}, {"name": "B"}]}]}
        self.assertEqual(author_name(schema), "A, B")
        self.assertIsNone(author_name({"author": "", "metaTags": [{"property": "article:author", "content": "https://x.com/a"}]}))


class LastmodReminderTests(unittest.TestCase):
    def setUp(self):
        git_environment = patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull})
        git_environment.start()
        self.addCleanup(git_environment.stop)
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        self.post = self.repo / "content/posts/example.md"
        self.post.parent.mkdir(parents=True)
        self.metadata = {"lastmod": "2026-01-02T12:00:00+08:00", "title": "Example", "summary": "Summary", "tags": ["agent"]}
        self.write(self.metadata, "First paragraph.\n")
        self.git("init", "-q")
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "Add post")

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True)

    def write(self, metadata, body):
        self.post.write_text("---\n" + yaml.safe_dump(metadata, allow_unicode=True) + "---\n" + body, encoding="utf-8")
        if (self.repo / ".git").exists():
            self.git("add", ".")

    def test_text_changes_without_lastmod_are_reported(self):
        self.write({**self.metadata, "summary": "New summary"}, "First paragraph, revised.\n")
        self.assertEqual(reminders(self.repo), ["content/posts/example.md: summary, body changed but lastmod did not"])

    def test_metadata_formatting_and_dated_edits_pass_quietly(self):
        for metadata, body in (
            ({**self.metadata, "tags": ["agent", "evals"]}, "First paragraph.\n"),
            (self.metadata, "First   paragraph.\n\n"),
            ({**self.metadata, "lastmod": "2026-02-01T12:00:00+08:00"}, "Rewritten.\n"),
        ):
            with self.subTest(metadata=metadata, body=body):
                self.write(metadata, body)
                self.assertEqual(reminders(self.repo), [])

    def test_new_files_and_unstaged_edits_are_ignored(self):
        (self.repo / "content/posts/new.md").write_text("---\ntitle: New\n---\nBody\n", encoding="utf-8")
        self.git("add", ".")
        self.post.write_text(self.post.read_text(encoding="utf-8") + "Unstaged.\n", encoding="utf-8")
        self.assertEqual(reminders(self.repo), [])


if __name__ == "__main__":
    unittest.main()
