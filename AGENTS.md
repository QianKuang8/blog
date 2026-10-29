# AGENTS.md

本文件适用于当前仓库及其所有子目录，只列硬性规则。每条规则只写在一处，其他文档引用而不复述：硬性规则和常用命令在本文件，流程与目录约定在 WORKFLOW.md，写作与审校标准在 BLOG_PROMPTS.md（见文末文档索引）。

## 项目概述

- Hugo 静态博客，模板与样式在仓库内（`layouts/`、`assets/`），不依赖外部主题。
- 推送 `main` 后由 `.github/workflows/hugo.yaml` 测试、构建并部署到 GitHub Pages。
- 仓库公开。第三方文章全文只放私有仓库 `QianKuang8/blog-sources`，书籍原文与译稿只放私有仓库 `QianKuang8/books`。

## 常用命令

在仓库根目录执行：

```bash
# 每个克隆首次使用时：固定本仓库的提交身份（云环境启动脚本也应执行）
sh scripts/setup_git_identity.sh

# 首次：校验依赖（Python 3.10+）与 PDF 子模块（正式构建需要完整历史）
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
git submodule update --init static/pdfs

# 首次：启用提交前的 lastmod 提醒（只提示，不阻止提交）
git config core.hooksPath scripts/hooks

# 写外部文章解读时：克隆私有原文归档（目录已被 git 忽略）
git clone https://github.com/QianKuang8/blog-sources.git sources/archive

# 外部文章：抓取全文写入私有归档，生成公开来源记录和文章草稿（草稿开头列出剩余步骤和原文图片）
.venv/bin/python scripts/new_post.py <slug> <url>

# 外部文章选用配图：保存原图到 static/images/<slug>/，登记 image_sources 并同步公开记录
.venv/bin/python scripts/add_image.py <slug> <name> <图片 URL 或本地文件> --title "图片标题"
# 撤下配图：先从文章删掉图片和图注，再删除文件与 image_sources 记录（文章不再有图时加 --image-note "原因"）
.venv/bin/python scripts/add_image.py <slug> <name> --remove

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

可选字段只有 `learning_status`、`draft`、`slug` 等模板实际读取的键；未知字段会被 `scripts/check_content.py` 拒绝（允许列表见其中的 `POST_KEYS`），视频时长、系列等信息写在正文里。

## 规则

**时间**
- 日期必须带时区，否则文章可能被当成未来时间而不显示。
- 新建时 `date` 和 `lastmod` 用当前时间，用户指定日期时按其要求；修订保留首次发布的 `date`。
- 摘要、description 或正文变化时更新 `lastmod`；正文包括配图、图注和新增的导航或推荐链接。
- 只改标题、栏目、标签（包括补来源标签）、学习状态、已有链接的路径写法、随标题同步的链接文字或格式时保留原 `lastmod`；只改 `data/reading_paths.json` 或模板时，文章的 `lastmod` 也不变。

**栏目与标签**
- 每篇文章只属于一个栏目：`好文分享`、`原创文章` 或 `视频笔记`。内部值和 URL 保持稳定，不新增文章分类字段；登记方式和显示名见 WORKFLOW.md“栏目体系”。
- `tags` 通常 1-3 个主题标签，可另加 1 个来源标签；没有合适主题的非技术文章（例如沟通、管理类视频笔记）用 `tags: []`。标签必须登记在 `data/tag_groups.json`，slug 保持稳定。
- 外部文章的原始发布者属于已维护来源时必须加来源标签；标签选择和来源判定见 WORKFLOW.md“Tag 体系”。
- `视频笔记`、`博客推荐` 标签已停用，不再写入文章；旧标签页面与分页保留兼容。

**学习状态**
- 可选字段 `learning_status` 只允许 `pending`（待学习）或 `done`（已学习）；省略表示未标记，不写空值或 `unmarked`。
- 新视频笔记默认 `pending`；普通文章只在用户确认已读后写 `done`。写作、发布、笔记或 PDF 都不算已学习，未经确认不批量补标，修订时保留已有状态。
- 学习状态和 GitHub 编辑入口只出现在 `/learning/`；文章正文、文章页、首页和普通列表不显示，浏览器不保存状态。

**来源与链接**
- 外部文章：`sources/orig/<slug>.md` 只有 frontmatter，由 `scripts/source_record.py` 从私有归档 `sources/archive/orig/<slug>.md` 生成；全文提交到 `blog-sources`，先于本仓库提交。
- 外部文章遇到 403、提取为空或正文不完整时，默认按 WORKFLOW.md“抓取失败与替代来源补档”继续尝试浏览器、作者其他发布渠道或可信同文转载，无需逐次请求授权；仍无法取得可确认来源的完整正文时，再暂停并请用户提供材料。
- 一篇文章用到多份来源时，在主来源记录的 `related_sources` 中列出其余记录；无人引用的来源记录会被检查拒绝。
- 视频笔记必须有 `sources/video/<slug>.md`，记录来源、时间戳和证据边界。
- 站内图片与 PDF 从站点根目录写（`/images/...`、`/pdfs/...`），不写 `/blog/` 前缀；引用站内文章用 `relref`。

**外部文章：标题与配图**
- 新增外部文章按 WORKFLOW.md“外部文章工作流”的单篇步骤逐项完成，`new_post.py` 生成的草稿开头也列出了这些步骤。
- 标题由本站自己写：按 BLOG_PROMPTS.md“标题”，来源在前，冒号后写这篇最值得记住的内容；不沿用原题，原题已经是中文也一样。用户请求里“文章标题为……”这类说法默认指原文标题，用来核对是哪一篇；只有用户明确要求博客标题用某个写法时才照用。检查会拒绝与来源记录 `title` 相同的标题。
- 配图用来提高可读性，可以是原图、重绘、本文绘制或其他一手来源的图，选图顺序与要求见 BLOG_PROMPTS.md“配图要求”；写作前先逐张看过原文图片。所有配图都用 `scripts/add_image.py` 保存并登记 `image_sources`。原文有图而本文一张不用时，在私有归档 frontmatter 写 `image_note`，说明原文有哪些图、为什么不用，再运行 `source_record.py`。
- 私有归档要保留每张原文图片的地址。页面读取工具把图片换成占位符（如 `【2†Image†…】`）时，从页面 HTML 的 `src`／`data-src` 补回 `![标题](URL)`；转载方添加的关注横幅、二维码等推广图不属于原文，不写入归档。克隆了私有归档时，检查会拒绝没有地址的占位符，以及原文有图、文章无图又没有 `image_note` 的文章。

**PDF**
- PDF 使用选定源文件，不压缩、不重新编码，只提交到公开仓库 `blog-pdfs`；本仓库只提交 `static/pdfs` 子模块指针。两个仓库分别检查、分别提交，不用 `git add .` 代替。
- 先提交并推送 `blog-pdfs`，再更新子模块指针和文章。路径、固定链接与回滚见 WORKFLOW.md“视频笔记与 PDF”。

**构建与展示**
- 正式构建统一用 `scripts/build_site.py`；校验器只豁免 `draft: true` 的文章。
- 文章、专题页和专题推荐理由遵守 BLOG_PROMPTS.md 的“避免的表达”，超出限额的写法会被 `check_content.py` 拒绝。
- 专题顺序和推荐理由只在 `data/reading_paths.json` 维护。
- 文末“相关文章”自动生成，不手工维护推荐列表；推荐不合适时调整标签（生成方式见 WORKFLOW.md“专题与文章内链”）。
- 站点以桌面阅读为准，日常只检查桌面显示；窄屏只有单栏回退样式，除非用户要求，不做手机适配或验证。

**提交**
- 本仓库的 author 和 committer 均使用 `QianKuang8 <71264725+QianKuang8@users.noreply.github.com>`。提交前执行 `sh scripts/setup_git_identity.sh` 并核对输出；不继承云环境的全局身份，不用 `--author` 或 `GIT_AUTHOR_*` / `GIT_COMMITTER_*` 覆盖。
- 直接在 `main` 上修改、提交并 `git push origin main`；不新建分支，不开 PR，也不做 merge。`blog-sources` 与 `blog-pdfs` 两个仓库同样直接提交到各自的 `main`。
- 只用单行 git commit 信息。
- 更新博文后主动提交；不适合直接提交时，先询问用户。

## 文档索引

- [README.md](README.md)：给人看的简介与目录结构。
- [WORKFLOW.md](WORKFLOW.md)：构建检查、栏目与标签体系、外部文章、视频笔记、PDF 与专题的处理流程。处理 `inbox.md`、生成来源记录或发布前先读。
- [BLOG_PROMPTS.md](BLOG_PROMPTS.md)：写作与审校标准，包括“避免的表达”和 reviewer 流程。撰写或审校文章前先读。
- [docs/decisions.md](docs/decisions.md)：历史决策与一次性操作记录。
