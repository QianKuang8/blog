---
date: '2024-12-08T00:00:00+08:00'
lastmod: '2026-10-20T10:22:37+08:00'
title: "维护这个 Hugo 博客：从本地写作到 GitHub Pages 发布"
summary: "记录本站从准备环境、写文章、本地预览、正式构建到 GitHub Pages 部署的操作顺序，以及 PDF 子模块和私有原文归档的处理方式。"
description: "自建模板的 Hugo 博客日常维护步骤，涵盖环境准备、文章元信息、站内链接、构建检查和部署验收。"
tags: ["blog"]
categories: ["原创文章"]
author: "Qian"
isCJKLanguage: true
showToc: true
learning_status: done
---

这个博客使用 Hugo 生成静态页面，GitHub Pages 负责托管。页面模板在 `layouts/`，样式和脚本在 `assets/`，都直接放在仓库里，不依赖外部主题。日常写作主要修改 Markdown 文件，但从“文章写完”到“读者能看到”，还要经过本地构建、自动检查和线上部署。这里把这条路径记下来，便于以后维护。

![左侧自上而下依次是写文章、本地预览、正式构建、推送到 main 和验收五个阶段；正式构建一行展开 build_site.py 的检查文章和来源记录、临时目录干净构建、检查产物、全部通过才替换 public/，任何一步失败都保留上一次通过检查的产物；推送后 GitHub Actions 依次校验 Hugo 安装包 checksum、运行测试、用同一个 build_site.py 构建并部署，最后确认 workflow 部署成功和线上页面显示本次修改。](/images/original/build-blog-tips/blog-publish-pipeline.svg)

*图 1：本文绘制，依据 2026 年 10 月 10 日的仓库配置与本文步骤整理。本地正式构建和 GitHub Actions 调用同一个 build_site.py，检查不通过时不会替换 public/。*

以下步骤按 2026 年 10 月 10 日的仓库配置整理。环境准备、预览、正式构建和测试命令当天用 Hugo 0.157.0 与 Python 3.13 实际跑通；推送后的部署部分依据仓库 workflow 整理，没有在当天单独复跑。迁移到别的 Hugo 项目时，需要重新核对目录和部署路径。

## 首次准备：Hugo、校验环境和 PDF

Hugo 使用 extended 版本，版本号与 `.github/workflows/hugo.yaml` 中的 `HUGO_VERSION` 保持一致。本地和 CI 用同一个版本，排查构建差异时才有可比性。

构建检查脚本需要 Python 3.10 以上，依赖装在仓库内的虚拟环境：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

视频笔记的 PDF 放在公开仓库 `blog-pdfs`，通过 `static/pdfs` 子模块挂到站点。普通 `git clone` 不会下载它：

```bash
git submodule update --init static/pdfs
```

正式构建会核对文章里固定到某个提交的 GitHub PDF 链接，所以要拉取完整历史。只做预览时可以加 `--depth 1` 浅克隆；之后需要正式构建，再运行 `git -C static/pdfs fetch --unshallow` 补齐历史。

外部文章的原文全文不放在这个公开仓库，而是放在私有仓库 `blog-sources`，需要该仓库的访问权限。只有写外部文章解读时才需要它，克隆到被 git 忽略的 `sources/archive/`：

```bash
git clone https://github.com/QianKuang8/blog-sources.git sources/archive
```

## 写文章：元信息、时间和站内链接

创建文章：

```bash
hugo new content content/posts/my-post.md
hugo new content --kind video content/posts/my-video.md  # 视频笔记，默认待学习
```

两个模板生成的都是草稿（`draft: true`），写完后删掉这一行才会发布。写作前检查 frontmatter：标题要说明讨论对象，摘要要让读者知道能获得什么。`categories` 只能填 `原创文章`、`好文分享`、`视频笔记` 中的一个，页面上分别显示为“研究与实践”“阅读与解读”“视频笔记”。标签要已经登记在 `data/tag_groups.json` 中，新标签先登记分组再使用。

`date` 保存首次发布时间，修订旧文时保留；`lastmod` 记录内容更新，修改标题、摘要、description 或正文时才更新。两者都使用带时区的时间，例如 `2026-09-21T10:00:00+08:00`。纯标签整理不修改内容时间，避免让读者误以为文章重新核验过。

站内图片和 PDF 从站点根目录写起，例如 `/images/<slug>/figure.svg` 或 `/pdfs/standalone/<slug>.pdf`，不要写部署路径 `/blog/`。模板渲染 Markdown 链接和图片时会自动补上，以后部署路径变化也不用改文章；正文里手写的 HTML 标签不经过这一步。

外部文章在 `sources/orig/` 保留只有元信息的来源记录，视频笔记在 `sources/video/` 保存来源记录并链接公开 PDF。完整约定在仓库的 `WORKFLOW.md` 与 `BLOG_PROMPTS.md` 中。

## 本地预览与正式构建各检查一次

写作时启动预览：

```bash
hugo server -D
```

`-D` 会显示草稿，适合检查尚未发布的文章。本站以桌面阅读为目标，重点看标题、目录、代码块、表格和图片是否清楚，再顺着文章点击相关链接。

提交前执行正式构建：

```bash
.venv/bin/python scripts/build_site.py
```

这个入口分三步：先检查文章和来源记录（必填字段、时区、栏目、标签、PDF 字节和固定链接），再在临时目录做一次干净的 Hugo 构建，最后检查产物（站内链接、canonical、sitemap、搜索索引、专题导航和学习清单）。全部通过后才替换 `public/`；任何一步失败都会保留上一次通过检查的产物。直接运行 `hugo` 也能生成页面，但旧文件可能残留在 `public/`，不适合作为发布前的检查结果。

修改了模板或检查脚本时，再跑一遍测试：

```bash
.venv/bin/python -m unittest discover -s tests
node --test tests/search.test.mjs
```

正式构建会按配置排除草稿和未来文章。若预览中有文章、正式产物却没有，先检查是否还带着 `draft: true`。检查脚本只负责站点规则和资源引用，正文事实与表达仍需要人工审校。

## 推送以后，确认部署和线上页面

本站直接在 `main` 提交日常修改。先检查差异，按文件添加本次文章与来源记录，再使用单行提交信息。推送后，GitHub Actions 的 `Deploy Hugo site to Pages` workflow 会先校验 Hugo 安装包的 checksum，再运行测试，并用同一个 `build_site.py` 构建，最后部署。

验收要看到两个结果：workflow 部署成功，以及线上目标页面确实显示本次修改。文章带 PDF 时，还要打开站点 PDF 和固定版本的 GitHub 文件链接。PDF 内容更新时，先提交并推送 PDF 仓库，再更新博客中的子模块指针，避免博客引用尚未公开的文件。

## 参考资料

- [Hugo：部署到 GitHub Pages](https://gohugo.io/hosting-and-deployment/hosting-on-github/)
- [Hugo：快速开始](https://gohugo.io/getting-started/quick-start/)
- [Hugo：链接渲染钩子](https://gohugo.io/render-hooks/links/)
