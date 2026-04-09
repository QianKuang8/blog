# Blog Rewrite Pilot Design

**Goal:** Redesign three existing posts into a clearer "博客解读" style so the repo can establish a repeatable rewrite standard before expanding to the rest of the article set.

## Scope

Pilot files:

- `content/posts/building-effective-agents.md`
- `content/posts/copilot-next-edit-suggestions.md`
- `content/posts/unrolling-codex-agent-loop.md`

Reference materials:

- `sources/orig/<slug>.md`
- `sources/nlm/<slug>.md`

## Why A Pilot First

The current posts were drafted before `orig` became a required archive artifact. They already contain useful information, but most of them read more like dense technical notes than finished blog essays. The pilot should define a stable rewrite pattern before the same work is repeated across the other posts.

## Chosen Style

Target style: **博客解读**, not pure technical notes.

That means each post should still preserve technical density, but the article should be organized around a judgment:

- why this article matters
- what problem it is actually trying to solve
- what the most important mechanism or design choice is
- what trade-off or limitation is easy to miss
- what my own conclusion is after reading it

## Rewrite Rules

### 1. Opening With A Thesis

Do not start with a generic "解读某篇文章". The intro should first answer:

- why this piece is worth reading
- what its real contribution is
- what kind of reader should care

The source link can remain in the opening paragraph, but it should not be the whole opening.

### 2. Reorganize Around Understanding, Not Source Order

Do not follow the original article structure mechanically. Rebuild the body around a cleaner progression:

1. 问题是什么
2. 方案或机制是什么
3. 最重要的 trade-off 是什么
4. 我的判断是什么

The exact section names can change per article, but the article should feel like an argument, not a transcript.

### 3. Keep 4-6 Meaningful Sections

Avoid long enumerations of weakly connected bullets. Prefer a smaller number of sections with stronger narrative progression. Lists are still allowed when the source truly contains taxonomy or architecture patterns, but each list should support a clear point.

### 4. Add A Distinct Personal Conclusion

Each post must include at least one section that is clearly an interpretation rather than a restatement. This is the key shift from "知识卡片" to "博客解读".

### 5. Preserve Technical Substance

Rewriting should not make the post fluffier. Important mechanics, terms, and trade-offs should remain explicit. The pilot is successful only if readability improves without losing density.

### 6. Keep A Stable Ending

End with a short "原文" or "延伸阅读" section so the reader can jump to the source directly.

## Pilot Selection Rationale

The three pilot posts deliberately span different source types:

- `building-effective-agents`: long-form official engineering essay
- `copilot-next-edit-suggestions`: product + research style feature explanation
- `unrolling-codex-agent-loop`: architecture-heavy systems writeup from a Chinese source archive

If one rewrite pattern works across these three, it is likely robust enough for the rest of the set.

## Expected Output

For each pilot article:

- updated `summary`
- updated `description` if needed
- refreshed `lastmod`
- rewritten body using the new structure

## Success Criteria

- A reader can understand the article’s main point within the opening section.
- The post reads like an essay with a point of view, not a memo.
- The source archive materially influences the rewritten structure and detail.
- The three pilots feel stylistically consistent even though the topics differ.

## Adoption

This pilot style has been accepted as the default style for subsequent technical blog rewrites in this repo.

The operational version of these rules should live in:

- `WORKFLOW.md`

This design doc remains as the rationale and original pilot definition.
