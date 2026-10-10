# Orig Index

这个目录给 Obsidian 用，仓库本身仍然是唯一的文件来源。

## 目录说明

- `sources/orig/`: 外部文章的来源元信息（公开，只有 frontmatter）。书籍导读的记录另含章节证据索引。
- `sources/archive/orig/`: 外部文章全文，来自私有仓库 `blog-sources` 的克隆，不进入本仓库。
- `sources/video/`: 视频笔记的来源、时间戳与证据边界。
- `sources/failed/`: 抓取或处理失败的记录，集中写在 `failed-sources.md`。

## 快速导航

- [来源元信息](orig/)
- [原文全文（私有归档）](archive/orig/)
- [视频来源](video/)
- [失败记录](failed/failed-sources.md)
- [发布流程](../WORKFLOW.md)

## 规则

- `.obsidian/` 与 `sources/archive/` 只保留在本地，不提交到本仓库。
- 这里的文件就是 Hugo 仓库里的真实文件，不维护额外副本。
