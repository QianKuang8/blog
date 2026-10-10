# Qian's Blog

使用 Hugo 和自建模板的个人静态博客，部署在 GitHub Pages：<https://qiankuang8.github.io/blog/>。

## 快速上手

```bash
# 校验依赖（Python 3.10+）
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# PDF 子模块（视频笔记的 PDF；正式构建需要完整历史）
git submodule update --init static/pdfs

# 写作时预览（含草稿）
hugo server -D

# 正式构建：检查源文件、在临时目录干净构建、检查产物，全部通过后才替换 public/
.venv/bin/python scripts/build_site.py

# 修改模板或脚本后运行测试
.venv/bin/python -m unittest discover -s tests
node --test tests/search.test.mjs
```

Hugo 使用 extended 版本，版本号与 [hugo.yaml](.github/workflows/hugo.yaml) 中的 `HUGO_VERSION` 一致。日常在 `main` 修改，构建通过后提交、推送，由 workflow 部署；不使用 PR。

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
| `scripts/` | 构建入口、源文件与产物检查、来源记录生成 |
| `docs/` | 历史决策记录与审查记录 |

## 文档

- [AGENTS.md](AGENTS.md)：必须遵守的规则（时间、栏目、标签、学习状态、来源、PDF、提交）。
- [WORKFLOW.md](WORKFLOW.md)：外部文章、视频笔记、PDF、标签和专题的处理流程。
- [BLOG_PROMPTS.md](BLOG_PROMPTS.md)：按文章用途区分的写作与审校标准。
- [docs/decisions.md](docs/decisions.md)：历史决策与一次性操作。

学习清单在站点的 `/learning/`：文章 frontmatter 的 `learning_status` 决定分组，可在本地修改或从清单里的 GitHub 编辑入口修改，推送部署后各设备同步。
