"""Regression tests for publication contracts, using isolated source/PDF repos."""

from pathlib import Path
from html import escape
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_content import validate_content


class ContentValidationTests(unittest.TestCase):
    def setUp(self):
        # Isolate fixture repos from machine-level hooks and background tracers.
        git_environment = patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull})
        git_environment.start()
        self.addCleanup(git_environment.stop)
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        for directory in ("content/posts", "sources/orig", "sources/video", "config/_default", "static/pdfs/standalone"):
            (self.repo / directory).mkdir(parents=True)
        (self.repo / "config/_default/config.yaml").write_text("baseURL: https://example.com/blog/\n")
        self.post = self.repo / "content/posts/example.md"
        self.metadata = {
            "date": "2026-01-01T12:00:00+08:00", "lastmod": "2026-01-02T12:00:00+08:00",
            "title": "Example", "summary": "Summary", "description": "Description", "author": "Qian",
            "tags": [], "categories": ["原创文章"], "isCJKLanguage": True, "showToc": True,
        }
        self.write_post()

    def write_markdown(self, path, metadata, body="Article body.", flow=False):
        path.write_text("---\n" + yaml.safe_dump(metadata, allow_unicode=True, default_flow_style=flow) + "---\n" + body)

    def write_post(self, body="Article body.", flow=False):
        self.write_markdown(self.post, self.metadata, body, flow)

    def git(self, directory, *args):
        return subprocess.check_output(["git", "-C", str(directory), *args], text=True, stderr=subprocess.DEVNULL).strip()

    def add_source(self, video=False):
        self.metadata["categories"] = ["视频笔记" if video else "好文分享"]
        self.source = self.repo / "sources" / ("video" if video else "orig") / "example.md"
        self.record = {
            "title": "Original", "source_url": "https://example.com/original",
            "retrieved_at": "2026-01-01T12:00:00+08:00", "description": "Original description",
            "domain": "example.com", "extractor": "defuddle",
        }
        self.write_markdown(self.source, self.record)
        self.write_post()

    def add_video(self):
        self.add_source(video=True)
        self.pdf_root = self.repo / "static/pdfs"
        self.pdf = self.pdf_root / "standalone/example.pdf"
        self.pdf.write_bytes(b"%PDF-1.4\nFixture PDF bytes\n")
        for directory in (self.repo, self.pdf_root):
            self.git(directory, "init", "-q")
        self.git(self.pdf_root, "add", "standalone/example.pdf")
        self.git(self.pdf_root, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "Add fixture")
        self.commit = self.git(self.pdf_root, "rev-parse", "HEAD")
        self.git(self.repo, "update-index", "--add", "--cacheinfo", f"160000,{self.commit},static/pdfs")
        self.record.update(source_type="video", channel="Example channel", duration="30:00", pdf_path="standalone/example.pdf")
        self.write_markdown(self.source, self.record)
        self.body = (
            "[Original](https://example.com/original)\n"
            "[PDF](/blog/pdfs/standalone/example.pdf)\n"
            f"[Source](https://github.com/QianKuang8/blog-pdfs/blob/{self.commit[:7]}/standalone/example.pdf)\n"
        )
        self.write_post(self.body)

    def assert_failure(self, expected, site=None):
        self.assertIn(expected, "\n".join(validate_content(self.repo, site)))

    def video_urls(self):
        return [
            self.record["source_url"], "/blog/pdfs/standalone/example.pdf",
            f"https://github.com/QianKuang8/blog-pdfs/blob/{self.commit[:7]}/standalone/example.pdf",
        ]

    def add_video_site(self):
        site = self.repo / "public"
        (site / "pdfs/standalone").mkdir(parents=True)
        (site / "pdfs/standalone/example.pdf").write_bytes(self.pdf.read_bytes())
        (site / "posts/example").mkdir(parents=True)
        (site / "posts/example/index.html").write_text(
            "".join(f'<a href="{escape(url)}">Link</a>' for url in self.video_urls())
        )
        return site

    def test_yaml_block_and_flow_lists_are_supported(self):
        for flow in (False, True):
            with self.subTest(flow=flow):
                self.write_post(flow=flow)
                self.assertEqual(validate_content(self.repo), [])

    def test_unquoted_yaml_timestamp_is_supported(self):
        self.post.write_text(self.post.read_text().replace("'2026-01-01T12:00:00+08:00'", "2026-01-01T12:00:00+08:00"))
        self.assertEqual(validate_content(self.repo), [])

    def test_utc_z_timestamp_is_supported(self):
        self.metadata["date"] = "2026-01-01T04:00:00Z"
        self.write_post()
        self.assertEqual(validate_content(self.repo), [])

    def test_missing_timezone(self):
        self.metadata["date"] = "2026-01-01T12:00:00"
        self.write_post()
        self.assert_failure("date must be an ISO 8601 datetime with a timezone")

    def test_lastmod_before_publication(self):
        self.metadata["lastmod"] = "2025-01-01T12:00:00+08:00"
        self.write_post()
        self.assert_failure("lastmod must not precede date")

    def test_required_fields_and_single_category(self):
        self.metadata.update(title="", categories=["原创文章", "好文分享"])
        self.write_post()
        self.assert_failure("title must be a nonempty string")
        self.assert_failure("categories must be a list containing exactly one")

    def test_duplicate_yaml_keys_fail(self):
        self.post.write_text(self.post.read_text().replace("---\n", "---\ntitle: Duplicate\n", 1))
        self.assert_failure("duplicate YAML key: title")

    def test_incomplete_draft_is_allowed_but_string_draft_is_not(self):
        self.write_markdown(self.post, {"draft": True}, "")
        self.assertEqual(validate_content(self.repo), [])
        self.write_markdown(self.post, {"draft": "true"}, "")
        self.assert_failure("draft must be a YAML boolean")

    def test_deleted_original_source(self):
        self.add_source()
        self.assertEqual(validate_content(self.repo), [])
        self.source.unlink()
        self.assert_failure("sources/orig/example.md")

    def test_source_metadata_and_body_are_required(self):
        self.add_source()
        del self.record["retrieved_at"]
        self.write_markdown(self.source, self.record, "")
        self.assert_failure("retrieved_at must be an ISO 8601 datetime")
        self.assert_failure("source record body must not be empty")

    def test_malformed_source_url_is_reported(self):
        self.add_source()
        self.record["source_url"] = "https://[broken"
        self.write_markdown(self.source, self.record)
        self.assert_failure("source_url must be an absolute HTTP(S) URL")

    def test_legacy_transcript_article_uses_its_category(self):
        self.add_source()
        self.write_post("This old article includes a video transcript.")
        self.assertEqual(validate_content(self.repo), [])

    def test_valid_video_accepts_resolvable_short_commit(self):
        self.add_video()
        self.assertEqual(validate_content(self.repo), [])

    def test_deleted_video_source(self):
        self.add_video()
        self.source.unlink()
        self.assert_failure("sources/video/example.md")

    def test_pdf_path_cannot_escape_submodule(self):
        self.add_video()
        self.record["pdf_path"] = "standalone/../../example.pdf"
        self.write_markdown(self.source, self.record)
        self.assert_failure("pdf_path must be standalone/<slug>.pdf")

    def test_missing_pdf_and_mismatched_links(self):
        self.add_video()
        self.write_post(self.body.replace("/blog/pdfs/standalone/example.pdf", "/blog/pdfs/standalone/wrong.pdf").replace(self.commit[:7], "main"))
        self.assert_failure("missing site PDF link")
        self.assert_failure("GitHub PDF link must pin a commit")
        self.pdf.unlink()
        self.assert_failure("PDF is missing from static/pdfs")

    def test_javascript_url_does_not_count_as_a_site_pdf_link(self):
        self.add_video()
        self.write_post(self.body.replace("[PDF](/blog/", "[PDF](javascript:/blog/"))
        self.assert_failure("missing site PDF link")

    def test_malformed_video_body_link_is_reported(self):
        self.add_video()
        self.write_post(self.body + "[Bad link](https://[broken)\n")
        self.assert_failure("malformed link URL")

    def test_code_and_comments_do_not_satisfy_required_video_links(self):
        self.add_video()
        examples = [
            "\n".join(f"`{line}`" for line in self.body.splitlines()),
            f"<!--\n{self.body}\n-->",
            f"```markdown\n{self.body}\n```",
            f"<pre><code>{self.body}</code></pre>",
        ]
        for body in examples:
            with self.subTest(body=body):
                self.write_post(body)
                for kind in ("site PDF", "fixed GitHub PDF", "original video"):
                    self.assert_failure(f"missing {kind} link")

    def test_unused_reference_definitions_do_not_count_as_links(self):
        self.add_video()
        self.write_post("Article body.\n\n" + "\n".join(f"[ref{i}]: {url}" for i, url in enumerate(self.video_urls())))
        for kind in ("site PDF", "fixed GitHub PDF", "original video"):
            self.assert_failure(f"missing {kind} link")

    def test_used_full_collapsed_and_shortcut_references_are_supported(self):
        self.add_video()
        definitions = "\n".join(f"[ref{i}]: {url}" for i, url in enumerate(self.video_urls()))
        self.write_post("[Original][REF0]\n\n[ref1][]\n\n[ref2]\n\n" + definitions)
        self.assertEqual(validate_content(self.repo), [])

    def test_other_pdf_further_reading_is_allowed_but_does_not_replace_own_pdf(self):
        self.add_video()
        other_link = "[Further reading](https://github.com/QianKuang8/blog-pdfs/blob/main/standalone/other.pdf)\n"
        self.write_post(self.body + other_link)
        self.assertEqual(validate_content(self.repo), [])
        self.write_post(self.body.replace(self.video_urls()[2], "https://example.com/unrelated") + other_link)
        self.assert_failure("missing fixed GitHub PDF link")

    def test_rendered_page_must_contain_real_video_anchors(self):
        self.add_video()
        site = self.add_video_site()
        page = site / "posts/example/index.html"
        anchors = page.read_text()
        self.assertEqual(validate_content(self.repo, site), [])
        for html in (f"<pre><code>{anchors}</code></pre>", f"<!--{anchors}-->", escape(anchors)):
            with self.subTest(html=html):
                page.write_text(html)
                for kind in ("site PDF", "fixed GitHub PDF", "original video"):
                    self.assert_failure(f"rendered page: missing {kind} link", site)

    def test_fixed_link_must_match_current_pdf_bytes(self):
        self.add_video()
        self.pdf.write_bytes(b"%PDF-1.4\nChanged PDF bytes\n")
        self.git(self.pdf_root, "add", "standalone/example.pdf")
        self.git(self.pdf_root, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "Update PDF")
        self.assert_failure("GitHub PDF link points to different PDF bytes")

    def test_generated_pdf_bytes_are_compared(self):
        self.add_video()
        site = self.add_video_site()
        output_pdf = site / "pdfs/standalone/example.pdf"
        self.assertEqual(validate_content(self.repo, site), [])
        output_pdf.write_bytes(b"corrupt")
        self.assert_failure("generated PDF is missing or differs", site)


if __name__ == "__main__":
    unittest.main()
