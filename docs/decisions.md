# 决策记录

按时间记录影响流程的决策和一次性操作。当前规则以 [AGENTS.md](../AGENTS.md) 和 [WORKFLOW.md](../WORKFLOW.md) 为准；这里只说明来由，不作为操作依据。

| 日期 | 决策或操作 |
|------|------------|
| 2026-03-20 | 建立发布流程：知识管理型博客，外部文章先归档原文再写解读，`inbox.md` 作为待发布队列。 |
| 2026-04-05 | 确定 tag 体系：粗细结合的主题标签。 |
| 2026-04 | 停用 NotebookLM / `nlm` 摘要流程，直接基于原文归档写作；原文归档改为单文件 frontmatter + 正文格式，并可在 Obsidian 中浏览。早期设计稿保存在 git 历史的 `docs/plans/`（最后见于提交 `bd38d9b`）。 |
| 2026-06-05 | 清空 inbox 文章队列；无法发布的条目记录在 `sources/failed/failed-sources.md`。 |
| 2026-08-31 | 视频笔记使用 `sources/video/` 来源记录；PDF 移到公开仓库 `blog-pdfs`，以 `static/pdfs` 子模块挂载。 |
| 2026-09-16 | 标签按主题与来源分组，补齐来源标签；`视频笔记`、`博客推荐` 标签停用并保留兼容入口。 |
| 2026-09-17 | 站点只按桌面显示验收，不做手机适配。 |
| 2026-09-21 | 全站 87 篇文章审查与重写，记录见 [reviews/2026-09-21-blog-audit.md](reviews/2026-09-21-blog-audit.md)。同日用自建模板替换 PaperMod 主题。 |
| 2026-09-23 | 学习清单采用独立页面方案（C 方案），原型保留在 [`codex/learning-list-prototype` 分支](https://github.com/QianKuang8/blog/tree/codex/learning-list-prototype/prototypes/learning-list)。按用户明确确认，将当时全部 76 篇非视频文章（69 篇好文分享、7 篇原创文章）初始化为 `done`，14 篇视频文章保持未标记；这次初始化不作为后续新文章自动标记的依据。 |
| 2026-10-10 | 仓库整体整理：<br>• 外部文章全文（70 篇）与 `sources/nlm/` 历史摘要（24 份）迁到私有仓库 `blog-sources`；公开的 `sources/orig/` 只保留元信息，新增 `scripts/source_record.py` 生成。迁移前的全文仍存在于本仓库 git 历史中。<br>• 停用 RSS（`disableKinds: ["rss"]`），旧订阅地址不再提供。<br>• 栏目设置集中到 `data/categories.json`；文章中站内链接改为从站点根目录书写，由渲染钩子补部署路径。<br>• 文章 JSON-LD 不再内嵌全文（`articleBody`），搜索页与停用标签跳转页不进入 sitemap。<br>• 产物检查改为只验证不变量（链接、canonical、sitemap、搜索索引、专题、学习清单、兼容入口），移除对界面文案和 RSS 的断言；`origStatus` 等无用字段清理，并启用 frontmatter 字段允许列表。<br>• 窄屏增加单栏回退样式；日常仍只验收桌面。<br>• CI 安装 Hugo 时校验 checksum。<br>• 删除 `docs/plans/`。 |
| 2026-10-10 | 界面借用 [OINK](https://github.com/pgsty/oink) Paper 预设的视觉风格：暖色中性底色、二级标题尾随细线、圆角代码块、目录竖线与当前章节标记、胶囊标签、`/` 聚焦搜索；保留自建模板与绿色强调色，只参考配色与设计，不复制其代码。整体迁移到 OINK 主题也评估过，因首页、学习清单、专题与产物检查都要重写而未采用。 |
| 2026-10-19 | 正文位图改为构建时生成 WebP 显示版本（720 与 1440 宽），图片链接到原图：`static/images` 同时挂载为 assets 供渲染钩子处理，原图文件不改动；产物检查同时核对 `srcset` 中的每个候选文件。当时 9 篇配图文章的位图下载量从约 5.9 MB 降到约 1 MB（2x）。 |
| 2026-10-20 | 配图规则纳入 `scripts/check_content.py`：所有文章的图片须有 alt、是 `/images/` 下实际存在的文件，且 `static/images/` 不留无人引用的文件；文章解读与视频笔记的图片后须有斜体图注；文章解读用到的站内图片须列入 `image_sources`，条目字段完整，且不列文章未用的图片。补录了 4 张早期重绘图与 1 张书籍导读图的 `image_sources`。同日在 AGENTS.md 写明所有仓库直接在 `main` 上提交和推送，不新建分支、不开 PR。 |
