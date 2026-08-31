# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Hugo 静态博客，使用 PaperMod 主题，通过 GitHub Pages 部署。

## 常用命令

```bash
# 创建新博文
hugo new content content/posts/my-post.md

# 本地预览（包含草稿）
hugo server -D

# 构建静态文件到 public/
hugo

# 初始化所有 submodule（主题与 PDF）
git submodule update --init --recursive

# static/pdfs submodule 建立后，只按需下载 PDF
git submodule update --init --depth 1 static/pdfs
```

## 博文结构

博文位于 `content/posts/`，使用以下 frontmatter 格式：

```yaml
---
date: '2024-12-08T17:22:55+08:00'
lastmod: '2024-12-08T17:22:55+08:00'
title: '标题'
summary: "摘要"
description: "描述"
tags: ["tag1", "tag2"]
author: "Qian"
isCJKLanguage: true
showToc: true
---
```

## 相关文档

- 处理 `inbox.md` 中的文章队列、生成原文归档、发布博文时，参阅 [WORKFLOW.md](WORKFLOW.md)
- 撰写或审校外部文章、视频笔记时，参阅 [BLOG_PROMPTS.md](BLOG_PROMPTS.md)
- 视频来源记录、PDF 仓库、submodule、发布和回滚规则以 [WORKFLOW.md](WORKFLOW.md) 为准

## 规则

- 日期格式必须带时区（如 `2024-12-08T17:22:55+08:00`），否则可能被解析为未来时间导致文章不显示
- 更新博文后一定要更新 `lastmod` 日期
- 视频笔记必须使用 `sources/video/<slug>.md` 保存来源、时间戳和证据边界
- PDF 使用选定源文件，不压缩、不重新编码，只提交到公开 `blog-pdfs` 仓库；博客主仓库仅提交 `static/pdfs` submodule 指针
- 不要把 PDF 作为博客主仓库的普通文件提交，也不要用 `git add .` 代替对主仓库和 submodule 的分别检查
- 更新 PDF 时，先提交并推送 PDF 仓库，再更新博客 submodule 指针、文章链接和 `lastmod`
- 发布视频笔记前必须确认 Hugo 产物中存在对应 PDF，并检查原视频、站点 PDF 和 GitHub 源文件链接
- 提交时只使用一行 git commit 信息
- 更新博文后应主动 commit，或至少询问用户是否需要 commit
