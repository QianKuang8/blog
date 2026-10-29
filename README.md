# Qian's Blog

使用 Hugo 和自建模板的个人静态博客，部署在 GitHub Pages：<https://qiankuang8.github.io/blog/>。

## 快速上手

需要 Python 3.10+ 和 Hugo extended，Hugo 版本号与 [hugo.yaml](.github/workflows/hugo.yaml) 中的 `HUGO_VERSION` 一致。安装依赖、预览、正式构建、测试和起稿的命令见 [AGENTS.md](AGENTS.md) 的“常用命令”。推送 `main` 后由 workflow 测试、构建并部署。

## 目录

| 路径 | 内容 |
|------|------|
| `content/posts/` | 博文 |
| `content/topics/` | 阅读专题；文章顺序和推荐理由在 `data/reading_paths.json` |
| `content/categories/`、`content/tags/` | 栏目与标签的显示名和说明 |
| `data/` | 栏目（`categories.json`）、标签分组（`tag_groups.json`）、阅读路径 |
| `layouts/`、`assets/` | 模板、样式和脚本（主题切换、专注阅读、代码复制、搜索） |
| `sources/orig/` | 外部文章的来源元信息；全文在私有仓库 `blog-sources`，按需克隆到被忽略的 `sources/archive/` |
| `sources/video/` | 视频笔记的来源、时间戳与证据边界 |
| `static/pdfs/` | 子模块，指向公开仓库 `blog-pdfs` |
| `scripts/` | 构建入口、源文件与产物检查、外部文章起稿、配图保存与来源记录生成、提交前的 `lastmod` 提醒（`hooks/`） |
| `docs/` | 历史决策记录与审查记录 |

## 文档

- [AGENTS.md](AGENTS.md)：常用命令和必须遵守的规则（时间、栏目、标签、学习状态、来源、PDF、提交）。
- [WORKFLOW.md](WORKFLOW.md)：外部文章、视频笔记、PDF、标签和专题的处理流程。
- [BLOG_PROMPTS.md](BLOG_PROMPTS.md)：按文章用途区分的写作与审校标准。
- [docs/decisions.md](docs/decisions.md)：历史决策与一次性操作。

学习清单在站点的 `/learning/`：文章 frontmatter 的 `learning_status` 决定分组，可在本地修改或从清单里的 GitHub 编辑入口修改，推送部署后各设备同步。
