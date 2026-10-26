# AGENTS.md

本文件适用于当前仓库及其所有子目录，只列硬性规则；流程细节见文末文档索引。

## 项目概述

- Hugo 静态博客，模板与样式在仓库内（`layouts/`、`assets/`），不依赖外部主题。
- 通过 GitHub Pages 部署。所有修改直接在 `main` 上提交并推送，推送后由 `.github/workflows/hugo.yaml` 构建部署。
- 仓库公开。第三方文章全文只放私有仓库 `QianKuang8/blog-sources`，书籍资料只放私有仓库 `QianKuang8/books`。

## 常用命令

在仓库根目录执行：

```bash
# 首次：校验依赖（Python 3.10+）与 PDF 子模块（正式构建需要完整历史）
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
git submodule update --init static/pdfs

# 首次：启用提交前的 lastmod 提醒（只提示，不阻止提交）
git config core.hooksPath scripts/hooks

# 写外部文章解读时：克隆私有原文归档（目录已被 git 忽略）
git clone https://github.com/QianKuang8/blog-sources.git sources/archive

# 外部文章：抓取全文写入私有归档，生成公开来源记录和文章草稿
.venv/bin/python scripts/new_post.py <slug> <url>

# 新文章 / 视频笔记（默认待学习）
hugo new content content/posts/my-post.md
hugo new content --kind video content/posts/my-video.md

# 修改私有归档的 frontmatter 后，重新生成公开的来源记录
.venv/bin/python scripts/source_record.py <slug>

# 本地预览（含草稿）
hugo server -D

# 正式构建：检查源文件 → 干净构建 → 检查产物，全部通过才替换 public/
.venv/bin/python scripts/build_site.py

# 修改模板或脚本后
.venv/bin/python -m unittest discover -s tests
node --test tests/search.test.mjs
```

## 博文 frontmatter

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

可选字段只有 `learning_status`、`draft`、`slug` 等模板实际读取的键；未知字段会被 `scripts/check_content.py` 拒绝（允许列表见其中的 `POST_KEYS`）。

## 规则

**时间**
- 日期必须带时区，否则文章可能被当成未来时间而不显示。
- 新建时设置 `date`；修订保留首次发布的 `date`。
- 修改标题、摘要、description 或正文时更新 `lastmod`；纯栏目、标签、学习状态、链接路径或格式整理保留原 `lastmod`。

**栏目与标签**
- 每篇文章只属于一个栏目：`好文分享`、`原创文章` 或 `视频笔记`，登记在 `data/categories.json`。内部值和 URL 保持稳定，显示名在 `content/categories/<栏目>/_index.md` 维护（阅读与解读、研究与实践、视频笔记）。
- “阅读与解读”的单篇类型显示为“文章解读”；来源记录设置 `source_type: book` 时显示为“书籍导读”。不新增文章分类字段。
- `tags` 通常 1-3 个主题标签，可另加 1 个来源标签；没有合适主题的非技术视频用 `tags: []`。标签必须登记在 `data/tag_groups.json`，显示名在 `content/tags/<tag>/_index.md`，slug 保持稳定。
- `视频笔记`、`博客推荐` 标签已停用，不再写入文章；旧标签页面与分页保留兼容。
- 外部文章的原始发布者属于已维护来源时添加来源标签，按原文来源判定，映射见 `WORKFLOW.md`。

**学习状态**
- 可选字段 `learning_status` 只允许 `pending`（待学习）或 `done`（已学习）；省略表示未标记，不写空值或 `unmarked`。
- 新视频笔记默认 `pending`；普通文章只在用户确认已读后写 `done`。不根据发布、笔记或 PDF 推断，未经确认不批量补标，修订时保留已有状态。
- 学习状态和 GitHub 编辑入口只出现在 `/learning/`；文章页、首页和普通列表不显示，浏览器不保存状态。

**来源与链接**
- 外部文章：`sources/orig/<slug>.md` 只保存元信息（frontmatter），全文保存在私有归档 `sources/archive/orig/<slug>.md` 并单独提交到 `blog-sources`。不要把第三方全文提交到本仓库。
- 一篇文章用到多份来源时，在主来源记录的 `related_sources` 中列出其余记录；无人引用的来源记录会被检查拒绝。
- 视频笔记必须有 `sources/video/<slug>.md`，记录来源、时间戳和证据边界。
- 站内图片与 PDF 从站点根目录写（`/images/...`、`/pdfs/...`），不写 `/blog/` 前缀；引用站内文章用 `relref`。

**PDF**
- 使用选定源文件，不压缩、不重新编码，只提交到公开仓库 `blog-pdfs`；本仓库只提交 `static/pdfs` 子模块指针，不用 `git add .` 代替对两个仓库的分别检查。
- 更新 PDF：先提交并推送 PDF 仓库，再更新子模块指针、文章链接和 `lastmod`。
- 视频笔记发布前确认产物中有对应 PDF，并检查原视频、站点 PDF 与固定提交的 GitHub 链接。固定链接可以指向旧提交，但文件字节必须与当前 PDF 一致；浅克隆缺历史时手动 `git -C static/pdfs fetch --unshallow`，校验器不联网。

**构建与展示**
- 正式构建统一用 `scripts/build_site.py`；校验器只豁免 `draft: true` 的文章。
- 文章、专题页和专题推荐理由遵守 BLOG_PROMPTS.md 的“避免的表达”：`check_content.py` 拒绝超出限额的套话和“把…接成／变成…”式标题，限定语过密时只给出提示。
- 专题顺序和推荐理由只在 `data/reading_paths.json` 维护；只改关系数据或模板时保留文章 `lastmod`。
- 文末“相关文章”由 `layouts/partials/related_posts.html` 按共同主题标签自动生成：越少见的标签权重越高，来源标签只算一半，已作为专题下一篇的文章不重复列出。不手工维护推荐列表；推荐不合适时调整标签。
- 站点以桌面阅读为准，日常只检查桌面显示；窄屏只有单栏回退样式，除非用户要求，不做手机适配或验证。

**提交**
- 直接在 `main` 上修改、提交并 `git push origin main`；不新建分支，不开 PR，也不做 merge。`blog-sources` 与 `blog-pdfs` 两个仓库同样直接提交到各自的 `main`。
- 只用单行 git commit 信息。
- 更新博文后主动提交；不适合直接提交时，先询问用户。

## 文档索引

- [README.md](README.md)：给人看的快速上手与目录结构。
- [WORKFLOW.md](WORKFLOW.md)：外部文章、视频笔记、PDF、标签与专题的处理流程。处理 `inbox.md`、生成来源记录或发布前先读。
- [BLOG_PROMPTS.md](BLOG_PROMPTS.md)：写作与审校标准。撰写或审校文章前先读。
- [docs/decisions.md](docs/decisions.md)：历史决策与一次性操作记录。
