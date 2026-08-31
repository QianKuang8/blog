# Qian's Blog

这是一个基于 Hugo 和 PaperMod 的个人静态博客，通过 GitHub Pages 部署。

常用命令：

```bash
hugo server -D
hugo
```

发布流程、文章 frontmatter 规范和原文归档要求见 [WORKFLOW.md](WORKFLOW.md)。

## 视频笔记与 PDF

视频来源记录保存在 `sources/video/`。公开 PDF 使用未压缩的选定源文件，存放在独立公开仓库 `QianKuang8/blog-pdfs`，并通过 `static/pdfs` submodule 挂载到站点。本流程在 PDF 仓库和 submodule 完成初始化后启用。

普通 `git clone` 不下载 PDF。需要完整初始化主题和 PDF 时运行：

```bash
git submodule update --init --recursive
```

完成 `static/pdfs` 初始化后，只按需下载 PDF submodule：

```bash
git submodule update --init --depth 1 static/pdfs
```

PDF 的复制校验、提交顺序、文章链接和回滚规则见 [WORKFLOW.md](WORKFLOW.md)，视频笔记写作与审校要求见 [BLOG_PROMPTS.md](BLOG_PROMPTS.md)。
