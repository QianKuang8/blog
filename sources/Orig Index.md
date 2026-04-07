# Orig Index

这个目录给 Obsidian 用，仓库本身仍然是唯一的文件来源。

## 目录说明

- `sources/orig/`: 原文归档。每篇待写文章先落一份原文 Markdown 到这里。
- `sources/nlm/`: `nlm` 生成的摘要报告，和 `orig/` 里的 slug 保持一致。
- `sources/failed/`: 抓取或处理失败的记录，集中写在 `failed-sources.md`。

## 快速导航

- [原文归档](orig/)
- [摘要报告](nlm/)
- [失败记录](failed/failed-sources.md)
- [发布流程](../WORKFLOW.md)

## 规则

- `.obsidian/` 只保留在本地，不提交到 git。
- 这里的文件就是 Hugo 仓库里的真实文件，不维护额外副本。
