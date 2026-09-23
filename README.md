# Qian's Blog

这是一个使用 Hugo 和自建展示层的个人静态博客，通过 GitHub Pages 部署。页面模板位于 `layouts/`，统一样式位于 `assets/css/site.css`，正文导航、专注阅读、主题切换和代码复制位于 `assets/js/site.js`。

常用命令：

```bash
# 首次使用：Python 3.10+，安装校验依赖
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# 日常预览（含草稿）
hugo server -D

# 正式构建：校验源文件、构建空目录、检查产物，全部通过后替换 public/
.venv/bin/python scripts/build_site.py

# 单独检查源文件，或运行回归测试
.venv/bin/python scripts/check_content.py
.venv/bin/python -m unittest discover -s tests
node --test tests/search.test.mjs
```

日常在 `main` 修改，使用上述构建入口验证后提交、推送，由现有 GitHub Pages workflow 部署。无需 PR。本地与 CI 使用同一个构建入口；它只替换仓库根目录的 `public/`，拒绝符号链接目标，失败时保留上一份验证通过的产物。CI 的 Hugo 版本固定在 [hugo.yaml](.github/workflows/hugo.yaml) 的 `HUGO_VERSION`，本地排查构建差异时使用同一版本。

仓库约束见 [AGENTS.md](AGENTS.md)，发布流程和来源归档见 [WORKFLOW.md](WORKFLOW.md)，按文章用途选择的写作与审校标准见 [BLOG_PROMPTS.md](BLOG_PROMPTS.md)。

博文保存在 `content/posts/`，专题目录在 `content/topics/`，精选文章及推荐理由统一维护在 `data/reading_paths.json`。专题通过 `reading_path` shortcode 展示阅读顺序，文章末尾自动显示所属专题和下一读；修改关系表后检查专题和文章两端的桌面呈现。

## 学习清单

侧栏的“学习清单”（`/learning/`）集中展示待学习、已学习和未标记的文章。待学习默认展开，其余分组折叠；每个条目提供学习状态、文章阅读链接和 GitHub 编辑入口。阅读链接使用普通 URL，文章页、首页及普通文章列表保持原样。

在文章 frontmatter 中填写 `learning_status: pending`（待学习）或 `learning_status: done`（已学习）；省略字段表示未标记。新增视频笔记默认待学习，普通文章只在确认已读后标记，未经用户确认不自动补标历史文章。单独修改状态不更新 `lastmod`，修订文章或 PDF 也不重置状态。

2026-09-23 按用户确认，将当时 76 篇非视频文章初始化为已学习，14 篇视频文章保持未标记；未来新文章仍按上述规则处理。

状态随 Markdown 提交、推送，并在 GitHub Pages 部署完成后跨设备同步。可以在本地修改文件，或从学习清单进入 GitHub 编辑；学习记录公开，浏览器不保存学习状态。

## 视频笔记与 PDF

创建默认待学习的视频笔记草稿：

```bash
hugo new content --kind video content/posts/my-video.md
```

视频来源记录保存在 `sources/video/`。公开 PDF 使用未压缩的选定源文件，存放在独立公开仓库 `QianKuang8/blog-pdfs`，并通过 `static/pdfs` submodule 挂载到站点。本流程在 PDF 仓库和 submodule 完成初始化后启用。

普通 `git clone` 不下载 PDF。需要完整初始化主题和 PDF 时运行：

```bash
git submodule update --init --recursive
```

完成 `static/pdfs` 初始化后，只按需下载 PDF submodule：

```bash
git submodule update --init --depth 1 static/pdfs
```

浅克隆可用于预览；正式构建会离线核对文章固定 GitHub 链接的提交及 PDF 字节。首次核验缺少的历史提交时，手动运行 `git -C static/pdfs fetch --unshallow`，此后校验器不会自动联网。当前 PDF 与旧提交中的文件字节相同时，已有的固定旧提交链接仍然有效。

PDF 的复制校验、提交顺序、文章链接和回滚规则见 [WORKFLOW.md](WORKFLOW.md)，视频笔记写作与审校要求见 [BLOG_PROMPTS.md](BLOG_PROMPTS.md)。
