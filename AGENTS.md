# AGENTS.md

本文件适用于当前仓库及其所有子目录。

## 项目概述

- 这是一个 Hugo 静态博客仓库。
- 主题使用 PaperMod。
- 站点通过 GitHub Pages 部署。

## 常用命令

在仓库根目录执行：

```bash
# 创建新博文
hugo new content content/posts/my-post.md

# 本地预览（包含草稿）
hugo server -D

# 构建静态文件到 public/
hugo
```

## 博文结构

- 博文位于 `content/posts/`。
- 新增或修改博文时，使用以下 frontmatter 结构：

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

- 处理 `inbox.md` 中的文章队列、生成摘要、发布博文时，先阅读 [WORKFLOW.md](WORKFLOW.md)。

## 规则

- frontmatter 中的日期必须带时区，例如 `2024-12-08T17:22:55+08:00`。否则文章可能被解析为未来时间并导致不显示。
- 更新博文后，必须同步更新 `lastmod`。
- 提交时只使用单行 git commit 信息。
- 更新博文后，应主动提交；如果当前任务不适合直接提交，至少先询问用户是否需要提交。
