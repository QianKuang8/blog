# Defuddle Orig Workflow Design

**Goal:** Make `sources/<slug>.orig.md` a required artifact for every article and use it as the controlled fallback when `nlm` cannot ingest a URL directly.

**Scope:** Update the blog publishing workflow documentation only. No changes to Hugo templates, content rendering, or deployment.

## Approved Decisions

1. Every article must have `sources/<slug>.orig.md` before publication can continue.
2. `sources/<slug>.orig.md` is generated primarily with `defuddle parse <url> --md`.
3. If `defuddle` cannot produce `orig.md`, the article is paused and recorded in `sources/failed-sources.md` until the user manually resolves the source.
4. `nlm` still prefers `nlm source add <nb-id> --url "<url>"`.
5. If `nlm source add --url` fails, retry with `nlm source add <nb-id> --file sources/<slug>.orig.md`.
6. Blog writing should use both `sources/<slug>.nlm.md` and `sources/<slug>.orig.md`.

## Why This Shape

- `orig.md` becomes a stable, git-tracked source artifact instead of an optional convenience file.
- `nlm --url` remains the primary ingestion path, so the workflow does not assume `defuddle` is a universal crawler.
- The fallback stays narrow and predictable: only `orig.md`, no automatic branching into multiple fetch tools.

## Files To Update

- `WORKFLOW.md`

