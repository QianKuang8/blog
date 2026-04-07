# Obsidian Orig Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reorganize `orig` and `nlm` artifacts so the blog repo can be used directly as an Obsidian vault with a single shared copy of each source file.

**Architecture:** Keep the repo as the canonical store, move source artifacts into function-specific subdirectories under `sources/`, and update the documented workflow to match. Obsidian remains a local interface over the same files, with `.obsidian/` ignored by git.

**Tech Stack:** Hugo content repo, Markdown, git, Obsidian vault conventions

---

### Task 1: Ignore Local Obsidian State

**Files:**
- Modify: `.gitignore`

**Step 1: Check current ignore rules**

Run: `rg -n '^\\.obsidian/?$' .gitignore`
Expected: no match or a single existing ignore rule

**Step 2: Add the minimal ignore rule**

Add:

```gitignore
.obsidian/
```

**Step 3: Verify the rule is present once**

Run: `rg -n '^\\.obsidian/?$' .gitignore`
Expected: one match

**Step 4: Commit**

```bash
git add .gitignore
git commit -m "chore: ignore local obsidian config"
```

### Task 2: Reorganize Source Material Directories

**Files:**
- Create: `sources/orig/`
- Create: `sources/nlm/`
- Create: `sources/failed/`
- Move: `sources/*.orig.md`
- Move: `sources/*.nlm.md`
- Move: `sources/failed-sources.md`

**Step 1: Create the target directories**

Run: `mkdir -p sources/orig sources/nlm sources/failed`
Expected: directories exist with no error

**Step 2: Move existing `orig` files into `sources/orig/`**

Run: `mv sources/*.orig.md sources/orig/`
Expected: all existing `orig` files move successfully

**Step 3: Move existing `nlm` files into `sources/nlm/`**

Run: `mv sources/*.nlm.md sources/nlm/`
Expected: all existing `nlm` files move successfully

**Step 4: Move the failure log into `sources/failed/`**

Run: `mv sources/failed-sources.md sources/failed/failed-sources.md`
Expected: the failure log exists at the new path

**Step 5: Verify the new layout**

Run: `find sources -maxdepth 2 -type f | sort`
Expected: files appear only under `sources/orig/`, `sources/nlm/`, and `sources/failed/`

**Step 6: Commit**

```bash
git add sources
git commit -m "refactor: reorganize source material directories"
```

### Task 3: Update Workflow Documentation

**Files:**
- Modify: `WORKFLOW.md`

**Step 1: Replace old path references**

Update every workflow example and explanation so they reference:

```text
sources/orig/<slug>.md
sources/nlm/<slug>.md
sources/failed/failed-sources.md
```

**Step 2: Update the directory tree**

Make the `sources/` tree in `WORKFLOW.md` match the new layout exactly.

**Step 3: Update command examples**

Revise examples such as:

```bash
defuddle parse "https://..." --md -o sources/orig/<slug>.md
nlm source add <nb-id> --file sources/orig/<slug>.md
nlm download report <notebook-id> --output sources/nlm/<slug>.md
```

**Step 4: Verify no stale paths remain**

Run: `rg -n 'sources/<slug>|\\.orig\\.md|\\.nlm\\.md|failed-sources\\.md' WORKFLOW.md`
Expected: only the new directory layout appears where intended

**Step 5: Commit**

```bash
git add WORKFLOW.md
git commit -m "docs: update workflow for obsidian source layout"
```

### Task 4: Add a Lightweight Obsidian Index Note

**Files:**
- Create: `sources/Orig Index.md`

**Step 1: Create a minimal index note**

Include:
- purpose of `sources/orig/`
- purpose of `sources/nlm/`
- purpose of `sources/failed/`
- quick navigation links
- the rule that `.obsidian/` stays local

**Step 2: Keep it intentionally lightweight**

Do not add a full task system, per-article metadata duplication, or Bases configuration in this phase.

**Step 3: Verify the note reads cleanly in plain Markdown**

Run: `sed -n '1,200p' "sources/Orig Index.md"`
Expected: concise navigation note with correct paths

**Step 4: Commit**

```bash
git add "sources/Orig Index.md"
git commit -m "docs: add obsidian source index note"
```

### Task 5: Final Verification

**Files:**
- Verify: `.gitignore`
- Verify: `WORKFLOW.md`
- Verify: `sources/`

**Step 1: Check git status**

Run: `git status --short`
Expected: clean working tree after commits

**Step 2: Check for stale top-level source files**

Run: `find sources -maxdepth 1 -type f | sort`
Expected: no stray `*.orig.md`, `*.nlm.md`, or `failed-sources.md` at the `sources/` root except the optional index note

**Step 3: Check the workflow doc for new paths**

Run: `rg -n 'sources/(orig|nlm|failed)' WORKFLOW.md`
Expected: updated references across the workflow

**Step 4: Optional smoke check**

Run: `hugo`
Expected: successful build with no content-path regressions

**Step 5: Final commit if needed**

```bash
git add .gitignore WORKFLOW.md sources
git commit -m "chore: finish obsidian-friendly source migration"
```
