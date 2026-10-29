"""Tests for the writing tools: starting an external-article draft, adding its figures, and the lastmod reminder."""

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
from add_image import add_image, image_format, remove_image, with_image_source, without_image_source
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

    def test_draft_lists_the_original_images_and_must_get_its_own_title(self):
        content = "Text.\n\n![Loop](https://example.com/loop.png)\n\n![](https://www.youtube.com/watch?v=abc)\n\n【2†Image†cdn.example.com】\n"
        notes = create_post(self.repo, "pictures", "https://example.com/post", {**DEFUDDLE, "content": content}, NOW)
        self.assertIn("the original has 1 image(s), listed in the draft: add the useful ones with scripts/add_image.py, or record image_note", notes)
        self.assertIn("1 image placeholder(s) have no address: take each image's src from the page and write ![title](URL) in the archive", notes)
        draft = self.repo / "content/posts/pictures.md"
        text = draft.read_text(encoding="utf-8")
        self.assertIn("\n   - https://example.com/loop.png\n", text)
        self.assertNotIn("youtube", text)
        self.assertIn("不沿用原题", text)
        self.assertIn("提取结果里没有图片", (self.repo / "content/posts/product-evals.md").read_text(encoding="utf-8"))
        # Publishing the draft as generated is caught: the original title, the lost image address and the missing figure choice.
        draft.write_text(text.replace("draft: true\n", "").replace('summary: ""', 'summary: "S"').replace('description: ""', 'description: "D"'), encoding="utf-8")
        failures = "\n".join(validate_content(self.repo))
        self.assertIn("content/posts/pictures.md: title repeats the original title", failures)
        self.assertIn("sources/archive/orig/pictures.md: 1 image placeholder(s) have no address", failures)
        self.assertIn("content/posts/pictures.md: the original has 2 image(s) but the article uses none", failures)

    def test_publication_dates_and_authors_are_read_from_common_formats(self):
        for value, expected in (("2026-03-11T08:00:00Z", "2026-03-11"), ("March 11, 2026", "2026-03-11"),
                                ("11 Mar 2026", "2026-03-11"), ("", None), ("soon", None)):
            with self.subTest(value=value):
                self.assertEqual(published_date(value), expected)
        schema = {"author": "", "schemaOrgData": [{"author": [{"name": "A"}, {"name": "B"}]}]}
        self.assertEqual(author_name(schema), "A, B")
        self.assertIsNone(author_name({"author": "", "metaTags": [{"property": "article:author", "content": "https://x.com/a"}]}))


PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16


class AddImageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        for directory in ("content/posts", "sources/orig", "sources/archive/orig", "config/_default", "data"):
            (self.repo / directory).mkdir(parents=True)
        for name in ("categories.json", "tag_groups.json"):
            shutil.copy(REPO / "data" / name, self.repo / "data" / name)
        (self.repo / "config/_default/config.yaml").write_text("baseURL: https://example.com/blog/\n")
        self.url = "https://eugeneyan.com/writing/product-evals/"
        create_post(self.repo, "product-evals", self.url, DEFUDDLE, NOW)
        self.archive = self.repo / "sources/archive/orig/product-evals.md"

    def add(self, name="loop", data=PNG, **changes):
        arguments = {"title": "Eval loop", "source_url": "https://cdn.example.com/loop.webp", "method": "原图文件，未改动", **changes}
        return add_image(self.repo, "product-evals", name, data, now=NOW, **arguments)

    def test_saves_the_bytes_by_their_format_and_records_them(self):
        path, record = self.add()
        self.assertEqual(path, "/images/product-evals/loop.png", "the extension follows the bytes, not the URL")
        self.assertEqual((self.repo / "static/images/product-evals/loop.png").read_bytes(), PNG)
        entry = {"title": "Eval loop", "path": path, "source_url": "https://cdn.example.com/loop.webp",
                 "method": "原图文件，未改动", "retrieved_at": "2026-10-26T18:00:00+08:00"}
        self.assertEqual(record["image_sources"], [entry])
        self.add("chart", b"\xff\xd8\xff\xe0rest", title="Chart")
        archived, body = read_markdown(self.archive)
        self.assertEqual([item["path"] for item in archived["image_sources"]], [path, "/images/product-evals/chart.jpg"])
        self.assertEqual(archived["title"], DEFUDDLE["title"])
        self.assertIn("## First, label some data", body)
        self.assertEqual(read_markdown(self.repo / "sources/orig/product-evals.md"), (archived, ""))
        # A published article that uses both figures passes the checks, archive comparison included.
        post = self.repo / "content/posts/product-evals.md"
        text = post.read_text(encoding="utf-8").replace("draft: true\n", "").replace('summary: ""', 'summary: "S"').replace('description: ""', 'description: "D"')
        text = text.replace(f'title: "{DEFUDDLE["title"]}"', 'title: "Eugene Yan 的产品评估三步法"')
        figures = "".join(f"![Figure]({image})\n\n*图 {number}：原图，来源：[原文]({self.url})。*\n\n"
                          for number, image in enumerate((path, "/images/product-evals/chart.jpg"), 1))
        post.write_text(text.replace("## 原文", figures + "## 原文"), encoding="utf-8")
        self.assertEqual(validate_content(self.repo), [])

    def test_refuses_html_existing_files_and_bad_names(self):
        with self.assertRaisesRegex(ValueError, "not a PNG, JPEG, GIF, WebP or SVG file"):
            self.add(data=b"<!DOCTYPE html><html>captcha</html>")
        self.add()
        with self.assertRaisesRegex(ValueError, "already exists: static/images/product-evals/loop.png"):
            self.add()
        for name in ("Loop", "loop.png", ""):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "lowercase letters"):
                self.add(name)
        with self.assertRaisesRegex(ValueError, "--source-url must be an absolute HTTP"):
            self.add("other", source_url="loop.png")
        with self.assertRaisesRegex(ValueError, "run scripts/new_post.py first"):
            add_image(self.repo, "missing", "loop", PNG, "Title", "https://example.com/a.png", "原图文件，未改动", NOW)
        self.assertEqual(len(read_markdown(self.archive)[0]["image_sources"]), 1, "failed calls record nothing")

    def test_appends_to_existing_lists_in_either_indentation(self):
        entry = {"title": "New", "path": "/images/x/new.png", "source_url": "https://example.com/new.png",
                 "method": "原图文件，未改动", "retrieved_at": "2026-10-26T18:00:00+08:00"}
        old = "  - title: Old\n    path: /images/x/old.png\n"
        for listing in ("image_sources:\n" + old, "image_sources:\n" + old.replace("  - ", "- ").replace("    ", "  "), "image_sources: []\n"):
            with self.subTest(listing=listing):
                text = f"---\ntitle: T\n{listing}extractor: defuddle\n---\n\nBody text.\n"
                updated = with_image_source(text, entry)
                self.assertEqual(yaml.safe_load(updated.split("---\n")[1])["image_sources"][-1], entry)
                # Every other line, and the archived text, stays exactly as it was.
                self.assertTrue(updated.startswith("---\ntitle: T\nimage_sources:"))
                self.assertTrue(updated.endswith("extractor: defuddle\n---\n\nBody text.\n"))
        with self.assertRaisesRegex(ValueError, "not a block list"):
            with_image_source("---\ntitle: T\nimage_sources: [{title: Old}]\n---\nBody\n", entry)

    def test_removes_figures_and_their_records(self):
        self.add()
        self.add("chart", b"\xff\xd8\xff\xe0rest", title="Chart")
        self.assertEqual(remove_image(self.repo, "product-evals", "loop"), "/images/product-evals/loop.png")
        self.assertFalse((self.repo / "static/images/product-evals/loop.png").exists())
        archived = read_markdown(self.archive)[0]
        self.assertEqual([entry["path"] for entry in archived["image_sources"]], ["/images/product-evals/chart.jpg"])
        self.assertEqual(read_markdown(self.repo / "sources/orig/product-evals.md"), (archived, ""))
        # The last figure takes the image_sources key with it; the note says why none is used.
        remove_image(self.repo, "product-evals", "chart.jpg", note="原文只有一张装饰性封面图，不选用。")
        archived, body = read_markdown(self.archive)
        self.assertNotIn("image_sources", archived)
        self.assertEqual(archived["image_note"], "原文只有一张装饰性封面图，不选用。")
        self.assertIn("## First, label some data", body)
        self.assertFalse((self.repo / "static/images/product-evals").exists())
        self.assertEqual(validate_content(self.repo), [])
        with self.assertRaisesRegex(ValueError, "no single image named chart in static/images/product-evals/"):
            remove_image(self.repo, "product-evals", "chart")

    def test_remove_waits_until_no_page_uses_the_figure(self):
        path, _ = self.add()
        post = self.repo / "content/posts/product-evals.md"
        post.write_text(post.read_text(encoding="utf-8") + f"\n![Eval loop]({path})\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "still used by content/posts/product-evals.md; remove the figure and its caption"):
            remove_image(self.repo, "product-evals", "loop")
        self.assertTrue((self.repo / "static/images/product-evals/loop.png").exists())
        self.assertEqual(len(read_markdown(self.archive)[0]["image_sources"]), 1)

    def test_removes_entries_in_either_indentation_and_replaces_the_note(self):
        entries = "  - title: Old\n    path: /images/x/old.png\n  - title: New\n    path: /images/x/new.png\n"
        for listing in (entries, entries.replace("  - ", "- ").replace("    ", "  ")):
            with self.subTest(listing=listing):
                text = f"---\ntitle: T\nimage_sources:\n{listing}image_note: \"old\"\nextractor: defuddle\n---\n\nBody text.\n"
                updated = without_image_source(text, "/images/x/old.png", note="new")
                self.assertEqual(yaml.safe_load(updated.split("---\n")[1]), {
                    "title": "T", "image_sources": [{"title": "New", "path": "/images/x/new.png"}],
                    "image_note": "new", "extractor": "defuddle"})
                self.assertTrue(updated.endswith("---\n\nBody text.\n"))
        with self.assertRaisesRegex(ValueError, "image_sources has no entry for /images/x/missing.png"):
            without_image_source(f"---\ntitle: T\nimage_sources:\n{entries}---\nBody\n", "/images/x/missing.png")

    def test_formats_are_recognized_from_their_bytes(self):
        for data, expected in ((PNG, "png"), (b"\xff\xd8\xff\xdb", "jpg"), (b"GIF89a....", "gif"),
                               (b"RIFF\x00\x00\x00\x00WEBPVP8 ", "webp"), (b"<?xml version='1.0'?><svg xmlns='x'/>", "svg"),
                               (b"<html><svg/></html>", None), (b"", None)):
            with self.subTest(data=data[:12]):
                self.assertEqual(image_format(data), expected)


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
            ({**self.metadata, "title": "Renamed"}, "First paragraph.\n"),
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
