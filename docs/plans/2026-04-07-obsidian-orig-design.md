# Obsidian Orig Management Design

**Goal:** Manage `orig` as a single shared artifact inside the blog repo, while using Obsidian as the main reading and retrieval interface.

**Scope:** Reorganize source-material directories and document the new workflow. No changes to Hugo templates, rendering, or deployment.

## Approved Decisions

1. The blog repo remains the single source of truth for `orig`.
2. Obsidian should open the blog repo directly as a vault instead of using a separate mirrored vault.
3. `.obsidian/` should stay local and must not be committed.
4. `orig` stays outside published content and should not live under `content/posts/`.
5. Source materials should be split by function:
   - `sources/orig/<slug>.md`
   - `sources/nlm/<slug>.md`
   - `sources/failed/failed-sources.md`
6. `origStatus` remains a lightweight tracking field in blog post frontmatter.
7. Obsidian use should start simple:
   - browse folders directly
   - read `orig` under `sources/orig/`
   - optionally keep a lightweight index note
8. Obsidian Bases is deferred to a later phase, after the directory layout and workflow are stable.

## Why This Shape

- It keeps `orig` in git, so publication stays reproducible and `nlm --file` fallback still works.
- It avoids mirrored copies and sync conflicts between a vault and the repo.
- It gives Obsidian direct access to the real files for full-text reading and search.
- It keeps source artifacts out of published Hugo content.
- It makes the repo easier to browse by separating raw originals, generated summaries, and failure logs.

## Directory Model

```text
blog/
├── content/posts/                 # published posts
├── sources/
│   ├── orig/                      # original archived articles for reading + fallback
│   │   └── <slug>.md
│   ├── nlm/                       # generated NLM reports
│   │   └── <slug>.md
│   └── failed/
│       └── failed-sources.md
├── docs/plans/
└── .obsidian/                     # local only, gitignored
```

## Usage Model

### Repo Responsibilities

- Store the canonical `orig` files used by the publishing workflow.
- Store the canonical generated `nlm` reports.
- Keep post-level tracking state such as `origStatus`.

### Obsidian Responsibilities

- Open the repo as a vault.
- Read and search `sources/orig/` directly.
- Use folder browsing as the primary access pattern.
- Optionally use a lightweight index note for navigation and workflow hints.

## Constraints

- Hugo should continue to publish only `content/`.
- Workflow documentation and examples must stop referencing `sources/<slug>.orig.md` and `sources/<slug>.nlm.md`.
- Any future automation should treat the repo paths above as the only valid paths.

## Files To Update

- `WORKFLOW.md`
- `.gitignore`
- `sources/` contents and layout
- optional Obsidian-facing index note
