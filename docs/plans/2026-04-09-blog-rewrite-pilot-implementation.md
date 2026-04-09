# Blog Rewrite Pilot Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rewrite three pilot blog posts using the new `orig + nlm` backed "博客解读" structure and establish a reusable standard for the remaining article set.

**Architecture:** Use each post’s current published draft as the baseline, then re-read both `sources/orig/<slug>.md` and `sources/nlm/<slug>.md` to identify the article’s true thesis, strongest technical mechanisms, and missing trade-offs. Rewrite the post around a new narrative order, update metadata fields that describe the piece, and verify that Hugo still builds.

**Tech Stack:** Hugo content markdown, YAML frontmatter, local source archives under `sources/orig/`, generated reports under `sources/nlm/`

---

### Task 1: Finalize The Rewrite Standard

**Files:**
- Create: `docs/plans/2026-04-09-blog-rewrite-pilot-design.md`

**Step 1: Write the pilot design doc**

Document:
- the selected three-post pilot set
- the desired "博客解读" target style
- the rewrite rules
- the success criteria

**Step 2: Verify the design doc**

Run: `sed -n '1,240p' docs/plans/2026-04-09-blog-rewrite-pilot-design.md`
Expected: design doc clearly states the rewrite standard and pilot scope

### Task 2: Gather Source Material For All Three Posts

**Files:**
- Read: `content/posts/building-effective-agents.md`
- Read: `sources/orig/building-effective-agents.md`
- Read: `sources/nlm/building-effective-agents.md`
- Read: `content/posts/copilot-next-edit-suggestions.md`
- Read: `sources/orig/copilot-next-edit-suggestions.md`
- Read: `sources/nlm/copilot-next-edit-suggestions.md`
- Read: `content/posts/unrolling-codex-agent-loop.md`
- Read: `sources/orig/unrolling-codex-agent-loop.md`
- Read: `sources/nlm/unrolling-codex-agent-loop.md`

**Step 1: Identify current article weaknesses**

For each post, note:
- where the opening is too generic
- where the article mirrors source order too closely
- where key trade-offs or judgments are missing

**Step 2: Identify the replacement structure**

For each post, define:
- opening thesis
- 4-6 target sections
- one explicit personal conclusion

### Task 3: Rewrite `building-effective-agents`

**Files:**
- Modify: `content/posts/building-effective-agents.md`

**Step 1: Update frontmatter text fields**

Refresh:
- `summary`
- `description` if needed
- `lastmod`

**Step 2: Rewrite the body**

Restructure the article into a blog essay that explains:
- why the article matters
- why Anthropic’s real contribution is methodological, not framework-specific
- how to interpret the workflow/agent distinction
- what the operational lessons are for production teams
- what your own takeaway is

**Step 3: Keep the source section**

Retain a compact `## 原文` section at the end.

### Task 4: Rewrite `copilot-next-edit-suggestions`

**Files:**
- Modify: `content/posts/copilot-next-edit-suggestions.md`

**Step 1: Update frontmatter text fields**

Refresh:
- `summary`
- `description` if needed
- `lastmod`

**Step 2: Rewrite the body**

Restructure the article into a blog essay that explains:
- why NES is a shift in programming interaction, not just a new autocomplete feature
- why edit history matters more than static snapshots
- what the UX and latency trade-offs imply
- where the product still has unsolved hand-off problems
- what your own interpretation is

**Step 3: Keep the source section**

Retain a compact `## 原文` section at the end.

### Task 5: Rewrite `unrolling-codex-agent-loop`

**Files:**
- Modify: `content/posts/unrolling-codex-agent-loop.md`

**Step 1: Update frontmatter text fields**

Refresh:
- `summary`
- `description` if needed
- `lastmod`

**Step 2: Rewrite the body**

Restructure the article into a blog essay that explains:
- why agent loop is the real product boundary
- how the reasoning/execution loop actually works
- why statelessness, append-only history, and prompt caching belong in the same system discussion
- what this reveals about production-grade coding agents
- what your own takeaway is

**Step 3: Keep the source section**

Retain a compact `## 原文` section at the end.

### Task 6: Verify The Pilot Batch

**Files:**
- Verify: `content/posts/building-effective-agents.md`
- Verify: `content/posts/copilot-next-edit-suggestions.md`
- Verify: `content/posts/unrolling-codex-agent-loop.md`

**Step 1: Inspect rewritten openings**

Run:
- `sed -n '1,120p' content/posts/building-effective-agents.md`
- `sed -n '1,120p' content/posts/copilot-next-edit-suggestions.md`
- `sed -n '1,120p' content/posts/unrolling-codex-agent-loop.md`

Expected: each post opens with a stronger thesis and a cleaner structure

**Step 2: Build Hugo**

Run: `hugo`
Expected: successful build with no content regressions

**Step 3: Review diff scope**

Run: `git diff -- content/posts/building-effective-agents.md content/posts/copilot-next-edit-suggestions.md content/posts/unrolling-codex-agent-loop.md`
Expected: changes are limited to the three pilot posts and reflect the intended structural rewrite
