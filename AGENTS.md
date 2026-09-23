# AGENTS.md

本文件适用于当前仓库及其所有子目录。

## 项目概述

- 这是一个 Hugo 静态博客仓库。
- 展示层使用仓库内自建 Hugo 模板与样式，不依赖外部主题。
- 站点通过 GitHub Pages 部署。
- 日常修改直接提交到主分支 `main`，推送后由现有 workflow 构建部署；不要求 PR。

## 常用命令

在仓库根目录执行：

```bash
# 创建新博文
hugo new content content/posts/my-post.md

# 创建视频笔记（默认待学习）
hugo new content --kind video content/posts/my-video.md

# 本地预览（包含草稿）
hugo server -D

# 首次安装校验依赖（Python 3.10+）
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# 正式构建并校验；通过后才替换 public/
.venv/bin/python scripts/build_site.py

# 单独检查源文件与已生成站点
.venv/bin/python scripts/check_content.py
.venv/bin/python scripts/check_site.py public

# 初始化 PDF submodule
git submodule update --init --recursive

# static/pdfs submodule 建立后，只按需下载 PDF
git submodule update --init --depth 1 static/pdfs
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
categories: ["原创文章"]
author: "Qian"
isCJKLanguage: true
showToc: true
---
```

## 相关文档

- 处理 `inbox.md` 中的文章队列、生成原文归档、发布博文时，先阅读 [WORKFLOW.md](WORKFLOW.md)。
- 撰写或审校博客文章时，先阅读 [BLOG_PROMPTS.md](BLOG_PROMPTS.md)。
- 视频来源记录、PDF 仓库、submodule、发布和回滚规则以 [WORKFLOW.md](WORKFLOW.md) 为准。

## 规则

- frontmatter 中的日期必须带时区，例如 `2024-12-08T17:22:55+08:00`。否则文章可能被解析为未来时间并导致不显示。
- 新建文章时设置 `date`；修订已有文章保留首次发布的 `date`。
- 每篇文章必须且只能属于一个栏目：`好文分享`、`原创文章` 或 `视频笔记`。栏目使用 `categories`；`tags` 通常包含 1-3 个主题标签，并可额外添加 1 个来源标签。没有合适主题的非技术视频可使用 `tags: []`，不为凑数创建标签。
- 栏目内部值和既有 URL 保持稳定，页面显示名分别为“阅读与解读”“研究与实践”“视频笔记”。“阅读与解读”的单篇类型显示为“文章解读”；对应来源记录设置 `source_type: book` 时显示为“书籍导读”，不新增文章分类字段。
- 主题浏览页默认展开 Agent 系统、AI 编程、模型与产业、软件工程，以及次要的已维护来源；站点与环境折叠展示。分组与来源角色在 `data/tag_groups.json` 维护，显示名称在 `content/tags/<tag>/_index.md` 维护。标签 slug 与既有 URL 保持稳定。
- `视频笔记` 与 `博客推荐` 已停用，不再写入文章 tags；前者使用同名栏目，旧标签入口、分页与 RSS 保留兼容。
- 外部文章的原始发布者属于 `WORKFLOW.md` 已维护的来源时，添加对应来源标签。按原文来源判定，不因内容提到某公司或产品而添加；其他来源暂不强制打标。来源域名与标签映射统一维护在 `WORKFLOW.md`。
- 修改标题、摘要、description 或正文时，必须同步更新 `lastmod`；纯栏目、标签、学习状态或格式整理保留原有 `lastmod`，避免制造虚假的内容更新时间。
- 学习状态保存在文章 frontmatter 的可选字段 `learning_status`，只允许字符串 `pending`（待学习）或 `done`（已学习）；缺少字段表示未标记，不写空值或 `unmarked`。新增视频笔记默认 `pending`，普通文章只有在用户确认已读后才写 `done`；不根据已发布、已生成笔记或 PDF 推断学习状态，未经用户确认不批量补标历史文章。修订文章或 PDF 时保留已有状态。2026-09-23 按用户明确确认，将当时全部 76 篇非视频文章初始化为 `done`，14 篇视频文章保持未标记；这不改变后续新文章的默认规则。
- 学习记录和 GitHub 编辑入口集中在 `/learning/` 的各文章条目中；文章阅读链接使用普通 URL，文章页、首页及普通文章列表不显示学习状态或学习编辑入口。状态修改提交并推送后，随 GitHub Pages 部署同步到各设备；浏览器不保存学习状态。
- 视频笔记必须使用 `sources/video/<slug>.md` 保存来源、时间戳和证据边界。
- PDF 使用选定源文件，不压缩、不重新编码，只提交到公开 `blog-pdfs` 仓库；博客主仓库仅提交 `static/pdfs` submodule 指针。
- 不要把 PDF 作为博客主仓库的普通文件提交，也不要用 `git add .` 代替对主仓库和 submodule 的分别检查。
- 更新 PDF 时，先提交并推送 PDF 仓库，再更新博客 submodule 指针、文章链接和 `lastmod`。
- 发布视频笔记前必须确认 Hugo 产物中存在对应 PDF，并检查原视频、站点 PDF 和 GitHub 源文件链接。
- 正式构建统一使用 `scripts/build_site.py`，避免旧 `public/` 文件干扰校验；校验器只豁免明确标记 `draft: true` 的未完成文章。固定 PDF 链接可以指向旧提交，但该提交中的文件必须与当前 PDF 字节一致；浅克隆缺少历史时先手动补齐，校验器不自动联网。
- 专题阅读顺序和推荐理由统一维护在 `data/reading_paths.json`，专题通过 `reading_path` shortcode 展示，文章末尾自动回链和推荐下一篇。仅修改关系数据或模板时保留文章 `lastmod`；修改文章正文或专题文字时按既有规则更新。
- 提交时只使用单行 git commit 信息。
- 更新博文后，应主动提交；如果当前任务不适合直接提交，至少先询问用户是否需要提交。
