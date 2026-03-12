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

## 规则

- 日期格式必须带时区（如 `2024-12-08T17:22:55+08:00`），否则可能被解析为未来时间导致文章不显示
- 更新博文后一定要更新 `lastmod` 日期
- 提交时只使用一行 git commit 信息
