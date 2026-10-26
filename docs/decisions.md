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
| 2026-10-20 | 文章末尾新增“相关文章”：模板按共同主题标签为每篇选出最多 3 篇，单个标签权重为 100 除以使用该标签的文章数，来源标签减半且不能单独构成相关；同分取较新的文章，跳过专题路径中的下一篇。产物检查核对相关链接共享主题标签、不重复、不指向自身或专题下一篇，并在存在候选时必须出现。 |
| 2026-10-20 | 统一旧图注：文章解读与视频笔记的图注一律以“图 N：”加标注（原图、原页面图表截图、局部截取、重绘、本文绘制）开头并按顺序编号，`check_content.py` 同步检查。改写了 9 段旧图注，并把 6 处“原文配图”改为“原图”；更正 Cognition 与 GLM 两张重绘图的来源说明，二者原文另有同主题示意图。 |
| 2026-10-26 | 新增主题标签 `evals`（评估（Evals））与 `skills`（Agent Skills），归入 Agent 系统分组。13 篇以评估或 Skill 为主题的文章改用新标签，并替换被覆盖的 `agent`、`harness-engineering`、`agentic-coding` 与 1 处 `行业动向`，每篇主题标签仍不超过 3 个；纯标签调整，保留 `lastmod`。 |
| 2026-10-26 | 来源记录统一 `author` 与 `published_at`，文章标题下方显示原文、原书或原视频的标题、作者与发布日期，`check_content.py` 要求每条记录写明 `published_at`（可为 `null`），`check_site.py` 核对每篇有来源记录的文章只链接一次原文。补录 60 条缺失日期：defuddle 元数据、原页面元数据（微信 `create_time`、YouTube、Uber、z.ai 等）与归档正文；3 篇知乎文章无法访问原页，按“编辑于”日期与正文事件只记录到月；`llm-oss-landscape` 与 Prompt Engineering Guide 为持续更新的仓库或网站，记为 `null`。更正 `unrolling-codex-agent-loop` 误记的剪藏日期（原文为 2026-01-23）。 |
| 2026-10-26 | Context Engineering 专题页新增导读样稿：区分站内 5 篇相近的上下文工程文章（其中 3 篇尚不在路径中），并说明路径三个阶段各篇的分工；确认风格与篇幅后再推广到其他专题。 |
| 2026-10-26 | 文风规则：BLOG_PROMPTS.md 新增“避免的表达”，`check_content.py` 对文章、专题页和专题推荐理由拒绝“真正”“接成／接回／连成”、每篇超过 1 处“不是……而是”、超过 3 处“边界”，以及“把…接成／连起来／变成”式标题（代码、引用块、链接文字和“直接成本”“模块边界”等常用词组不计）；限定语每千字超过 6 次只提示。44 篇文章据此修订，10 篇改标题，13 篇精简限定语并对照原文；4 个独立 reviewer 审校后返修，同时更正 2 处归因：Week 9 的内外双层循环出自 Kauderer-Abrams 本人，agentic-coding-boundary 中模型模仿补丁写法的判断来自作者对训练语料的推理。 |
