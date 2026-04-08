# Orig Frontmatter Metadata Design

**Goal:** Define a sample and a reusable format for `sources/orig/<slug>.md` so each archived source file can carry stable metadata and cleaned article content in one place.

## Context

The current `defuddle parse <url> --md` flow produces clean markdown body content, but it does not embed metadata in the output file. That is acceptable for raw text extraction, but it is weak for repo-based knowledge management because the archive file itself does not tell the reader where it came from or when it was retrieved.

The blog workflow already treats `sources/orig/<slug>.md` as a required artifact. Adding lightweight frontmatter makes the file self-describing while keeping the body readable in Obsidian and easy to reuse for downstream summarization.

## Decision

Use a single-file format:

1. YAML frontmatter at the top of each `sources/orig/<slug>.md`
2. Defuddle-cleaned markdown body below the frontmatter

The sample metadata schema is:

```yaml
---
title: "Building effective agents"
source_url: "https://www.anthropic.com/engineering/building-effective-agents"
domain: "anthropic.com"
description: "..."
retrieved_at: "2026-04-08T20:55:00+08:00"
extractor: "defuddle"
---
```

## Why This Shape

- One file remains the source of truth, which matches the existing `sources/orig/<slug>.md` workflow.
- Frontmatter is already natural in this repo because Hugo content uses the same convention.
- Obsidian can read the file cleanly without extra tooling.
- Later automation can parse metadata deterministically.
- The body stays clean because the metadata block is small and fixed.

## Rejected Alternatives

### Sidecar metadata file

Store metadata in `sources/orig/<slug>.meta.yaml` and keep `orig` as pure body markdown.

- Pros: pure body content
- Cons: two-file management, weaker ergonomics, easier to drift

### Markdown metadata section

Store metadata in a top-level "Metadata" heading.

- Pros: human-readable
- Cons: not stable enough for automation, harder to parse consistently

## Constraints

- The frontmatter must stay minimal.
- The archive file is for source tracking, not for Hugo publication.
- Retrieval time should include timezone, matching repo conventions.
- Missing metadata should not block archive generation if the body can be captured, but the preferred path is to populate all six fields above.

## Initial Sample

Apply the format first to:

- `sources/orig/building-effective-agents.md`

If the sample looks correct, the same schema can become the default format for future `orig` generation.
