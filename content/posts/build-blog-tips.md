---
date: '2024-12-08T00:00:00+08:00'
lastmod: '2026-09-21T10:11:16+08:00'
title: "维护这个 Hugo 博客：从本地写作到 GitHub Pages 发布"
summary: "记录本站从创建文章、本地预览、构建检查到 GitHub Pages 部署的操作顺序，以及主题和 PDF 子模块的处理方式。"
description: "Hugo 与 PaperMod 博客的日常维护步骤，涵盖文章元信息、子模块、站点检查和部署验收。"
tags: ["blog"]
categories: ["原创文章"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

这个博客使用 Hugo 生成静态页面，PaperMod 提供主题，GitHub Pages 负责托管。日常写作主要修改 Markdown 文件，但从“文章写完”到“读者能看到”，还要经过本地构建、资源检查和线上部署。这里把这条路径记下来，便于以后维护。

以下步骤按 2026 年 9 月 21 日的仓库配置整理，适用于本站。具体版本以仓库 workflow 为准；迁移到别的 Hugo 项目时，需要重新核对目录、主题和部署路径。

## 先准备主题和 PDF

首次克隆后，在仓库根目录初始化子模块：

```bash
git submodule update --init --recursive
```

主题位于 `themes/PaperMod`，PDF 位于 `static/pdfs`，两者都由独立仓库提供。主仓库记录它们的提交指针，目录存在并不代表内容已经下载完整。文章引用 PDF 时，还应确认相应文件确实在子模块中。

站点配置集中在 `config/_default/config.yaml`，包括站点地址、导航、分页和 PaperMod 选项。修改时优先沿用已有配置，每次只调整需要的部分，再查看生成页面；直接覆盖主题示例容易丢失本站的导航和路径约定。

## 写文章时，把首次发布和修订时间分开

创建文章：

```bash
hugo new content content/posts/my-post.md
```

文章位于 `content/posts/`。写作前检查 frontmatter：标题要说明讨论对象，摘要要让读者知道能获得什么，栏目只能从“原创文章”“好文分享”“视频笔记”中选择一个。

`date` 保存首次发布时间，修订旧文时保留；`lastmod` 记录内容更新，修改标题、摘要或正文时才更新。两者都使用带时区的时间，例如 `2026-09-21T10:00:00+08:00`。纯标签整理不修改内容时间，避免让读者误以为文章重新核验过。

外部文章另存原文归档，视频笔记另存来源记录，并链接公开 PDF。完整约定在仓库的 `WORKFLOW.md` 与 `BLOG_PROMPTS.md` 中。

## 本地预览与正式构建各检查一次

写作时启动预览：

```bash
hugo server -D
```

`-D` 会显示草稿，适合检查尚未发布的文章。本站以桌面阅读为目标，重点看标题、目录、代码块、表格和图片是否清楚，再顺着文章点击相关链接。

提交前执行正式构建与站点检查：

```bash
hugo
python3 scripts/check_site.py public
```

正式构建会按站点配置排除草稿和未来文章。若预览中有文章、正式产物却没有，先检查 `draft` 与发布时间，再确认 `public/posts/` 中生成了对应目录。检查脚本负责站点规则和资源引用，正文事实与表达仍需要人工审校。

## 推送以后，确认部署和线上页面

本站直接在 `main` 提交日常修改。先检查差异，按文件添加本次文章与来源材料，再使用单行提交信息。推送后，GitHub Actions 的 `Deploy Hugo site to Pages` workflow 会构建并部署。

验收要看到两个结果：workflow 部署成功，以及线上目标页面确实显示本次修改。文章带 PDF 时，还要打开站点 PDF 和固定版本的 GitHub 文件链接。PDF 内容更新则先提交、推送 PDF 仓库，再更新博客中的子模块指针，避免博客引用尚未公开的文件。

## 参考资料

- [Hugo：部署到 GitHub Pages](https://gohugo.io/hosting-and-deployment/hosting-on-github/)
- [Hugo：快速开始](https://gohugo.io/getting-started/quick-start/)
- [PaperMod：安装与配置](https://github.com/adityatelange/hugo-PaperMod/wiki/Installation)
