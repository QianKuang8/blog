# Orig Frontmatter Sample Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Convert one sample `sources/orig` archive into the new frontmatter-based format and verify the output is suitable as the default template.

**Architecture:** Reuse the existing defuddle-cleaned body for the sample article, fetch metadata fields with `defuddle parse -p`, prepend YAML frontmatter, and keep the rest of the file unchanged. This limits scope to one archive file while producing a concrete format the user can review.

**Tech Stack:** Markdown, YAML frontmatter, defuddle CLI

---

### Task 1: Capture Design Intent in Repo Docs

**Files:**
- Create: `docs/plans/2026-04-08-orig-frontmatter-design.md`

**Step 1: Write the design doc**

Include:
- why `defuddle --md` alone is insufficient for archive ergonomics
- the selected single-file frontmatter design
- the initial metadata schema
- rejected alternatives

**Step 2: Verify the file exists**

Run: `sed -n '1,220p' docs/plans/2026-04-08-orig-frontmatter-design.md`
Expected: design doc renders with the chosen schema

### Task 2: Fetch Metadata for the Sample Source

**Files:**
- Read: `sources/orig/building-effective-agents.md`

**Step 1: Fetch title**

Run: `defuddle parse https://www.anthropic.com/engineering/building-effective-agents -p title`
Expected: page title string

**Step 2: Fetch description**

Run: `defuddle parse https://www.anthropic.com/engineering/building-effective-agents -p description`
Expected: page description string or empty output

**Step 3: Fetch domain**

Run: `defuddle parse https://www.anthropic.com/engineering/building-effective-agents -p domain`
Expected: source domain string

### Task 3: Update the Sample Orig File

**Files:**
- Modify: `sources/orig/building-effective-agents.md`

**Step 1: Add YAML frontmatter**

Prepend:

```yaml
---
title: "..."
source_url: "https://www.anthropic.com/engineering/building-effective-agents"
domain: "..."
description: "..."
retrieved_at: "..."
extractor: "defuddle"
---
```

**Step 2: Preserve the body**

Keep the existing cleaned markdown body after the frontmatter with no content rewrite.

### Task 4: Verify the Sample Output

**Files:**
- Verify: `sources/orig/building-effective-agents.md`

**Step 1: Inspect the top of the file**

Run: `sed -n '1,24p' sources/orig/building-effective-agents.md`
Expected: frontmatter followed by the original body

**Step 2: Confirm the file still has substantial body content**

Run: `wc -l sources/orig/building-effective-agents.md`
Expected: line count remains materially above 200

### Task 5: Review Workspace State

**Files:**
- Verify: `docs/plans/2026-04-08-orig-frontmatter-design.md`
- Verify: `docs/plans/2026-04-08-orig-frontmatter-implementation.md`
- Verify: `sources/orig/building-effective-agents.md`

**Step 1: Check git status**

Run: `git status --short`
Expected: only the intended new docs and sample file changes appear, plus any unrelated pre-existing untracked files

**Step 2: Present the sample to the user**

Expected: the user can evaluate whether the schema should become the default format for all future `orig` files
