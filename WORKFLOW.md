# 博客发布流程

本文件记录各类文章从收集到发布的流程和目录约定。硬性规则（时间、栏目、标签数量、学习状态、来源、PDF、提交）见 [AGENTS.md](AGENTS.md)，写作与审校标准见 [BLOG_PROMPTS.md](BLOG_PROMPTS.md)，历史决策见 [docs/decisions.md](docs/decisions.md)。这里只写流程和机制，不复述上述规则。

博客定位为知识管理：主要为自己回查，也方便读者按问题阅读。

---

## 构建与验证范围

发布前运行 `.venv/bin/python scripts/build_site.py`。它依次执行：

1. `scripts/check_content.py` 检查源文件：必需元数据、显式时区、`lastmod >= date`、单一合法栏目、已登记且未停用的标签、未知 frontmatter 字段、来源记录（外部文章只有元信息、无人引用的记录；本地克隆了私有归档时，公开记录须与归档 frontmatter 一致）、专题页的 `date`/`lastmod` 不晚于当前时间（专题页没有 `date` 时 Hugo 以 `lastmod` 为发布时间，未来时间会让页面被跳过）、站内链接不写死 `/blog/`，文章、专题页和推荐理由的“避免的表达”（BLOG_PROMPTS.md），以及视频的来源字段、原视频链接、PDF 路径、子模块、站点与固定 GitHub 链接。
2. 在新的临时目录做干净的 Hugo 构建，并比对产物中的 PDF 字节。
3. `scripts/check_site.py` 检查产物：站内链接与资源存在、每页唯一且指向自身的 canonical、每页 `<html lang>` 等于配置的 `languageCode`（`zh-CN`）、sitemap 不收录 noindex 或跳转页、文章 JSON-LD、搜索索引覆盖全部文章并带上各自来源记录的原文标题、文章页的复制按钮内容、文章类型标签、专题目录与文末导航、学习清单分组与编辑链接、停用标签的兼容入口。

全部通过才替换 `public/`，失败时保留上次通过的产物。直接运行 `hugo` 只用于调试。检查不联网，也不能代替事实审校或线上链接核验。

推送到 `main` 后，GitHub Actions 运行同样的测试和构建再部署。CI 缓存 `resources/_gen`（图片的 WebP 版本和 CSS），图片、`assets/`、图片渲染钩子或配置不变时直接复用；只改 `docs/` 或根目录说明文档（`*.md`）的提交不触发部署，需要时可在 Actions 页面手动运行。

---

## 栏目体系

`categories` 回答“这是什么类型的文章”，`tags` 中的主题标签回答“文章在谈什么”，来源标签回答“原文来自哪里”，`topics` 是人工维护的阅读路径。

| 内部栏目值 | 页面显示名 | 适用范围 | 来源要求 |
|------------|------------|----------|----------|
| `好文分享` | 阅读与解读 | 基于外部网页文章或书籍整理的中文解读 | `sources/orig/<slug>.md`；书籍保存证据记录，不归档全文 |
| `原创文章` | 研究与实践 | 个人实践、研究、观点或工具清单 | 没有强制来源文件 |
| `视频笔记` | 视频笔记 | 基于课程、访谈或演讲整理的主题式笔记 | `sources/video/<slug>.md` 和对应 PDF |

栏目登记在 `data/categories.json`（顺序、来源目录、文章类型标签），模板和检查脚本都从这里读取；显示名在 `content/categories/<内部栏目值>/_index.md` 维护。“阅读与解读”的文章默认显示“文章解读”，来源记录设置 `source_type: book` 时显示“书籍导读”，两者都链接到原栏目；搜索结果使用栏目显示名。

首页按时间倒序每页 10 篇，主题入口跳到主题浏览页的对应分组。首页、栏目和标签详情共用文章条目与分页模板，每个分页的 canonical 指向自身。左侧提供最新文章、主题浏览、阅读专题、学习清单、归档和搜索入口；文章页可切换专注阅读。站点不提供 RSS。

搜索主要用来找出文章转发给别人：按空格拆分关键词，每个词都要出现在标题、原文标题、标签、摘要或正文中，按命中位置排序（标题优先），同一级新文章在前；不做模糊匹配。找到后在文章页复制：元信息行末的链接图标复制“本文标题 本文链接”，“原文”行末的复制图标复制“原文标题 原文链接”（只在有来源记录的文章上出现）。按钮在浏览器支持剪贴板时才显示。

## 个人学习记录

学习状态保存在 `content/posts/<slug>.md` 的 `learning_status`，以 GitHub 仓库为唯一记录，取值规则见 AGENTS.md。`done` 表示完成过一轮学习，不表示完全掌握。

侧栏“学习清单”进入 `/learning/` 并显示待学习数量。清单默认展开待学习，已学习和未标记折叠；每个条目提供学习状态、普通文章链接和“GitHub 编辑”入口。可以在本地修改 Markdown，也可以从编辑入口修改同一文件；推送并部署后各设备同步。仓库和学习记录都公开，编辑权限由 GitHub 管理。

---

## Tag 体系

Hugo tags 保持平铺，主题浏览页按主题、已维护来源、站点与环境分组展示。标签数量见 AGENTS.md，来源标签不占主题数量。个人记录、环境初始化、博客维护等非 AI 文章可用少量非 AI tag，但避免 `default` 这类无信息量标签。

| Tag | 类型 | 说明 |
|-----|------|------|
| `code-editing` | 宽 tag | AI 代码编辑总类 |
| `next-edit` | 细 tag | Next Edit 预测（cursor tab、copilot NES、zed、augment） |
| `apply` | 细 tag | Apply / Unified Diffs |
| `speculative-edit` | 细 tag | Speculative Edits 辅助代码编辑 |
| `model-engineering` | 细 tag | 模型架构、推理优化、Serving、KV Cache 等模型工程 |
| `agent` | 宽 tag | Agent 通用（架构、工程、设计），不限于编程任务 |
| `agentic-coding` | 细 tag | Coding Agent 产品和对比 |
| `harness-engineering` | 细 tag | Harness Engineering |
| `context-engineering` | 细 tag | Context Engineering |
| `prompt-engineering` | 细 tag | Prompt Engineering |
| `skills` | 细 tag | Agent Skills：Skill 的设计、触发、分发、录制与改进 |
| `evals` | 细 tag | 评估方法：任务与评分器设计、benchmark 有效性、评估结果怎样支持迭代与上线判断 |
| `行业动向` | 主题 tag | 行业趋势、开源生态、商业变化、跨模型发展趋势；不作为课程、新闻或单一产品实现文章的兜底标签 |
| `software-design` | 工程主题 | 软件设计、模块边界、信息隐藏与复杂性管理 |
| `架构迁移` | 工程主题 | 基础设施或系统架构迁移 |
| `arm` | 工程主题 | Arm / 多架构迁移 |
| `blog` | 个人记录 | 博客搭建、写作和维护 |
| `init` | 个人记录 | 本机初始化、开发环境配置 |

### 标签选择

- 先选最能描述文章内容的主题，再按需补充；来源标签按下方规则单独添加。
- `agent` 适合跨任务的 Agent 机制，例如 Computer History；`agentic-coding` 适合 AI 编程产品、工作流和工程实践。只有两条主线都独立成立时才同时使用。
- `skills` 只用于以 Skill 本身为主题的文章，正文顺带提到 Skill 时不加；`evals` 只用于以评估方法为主题的文章，仅用评测分数说明某项改进时不加。它们比 `agent`、`harness-engineering` 更准确时替换宽标签，主题标签仍保持 1-3 个。
- 视频笔记只用栏目表示内容形式，按正文另选主题。用 `tags: []` 的非技术文章积累到一定数量后，再考虑新增主题。
- `行业动向` 只在正文充分展开趋势、生态、产业经济或竞争格局时使用；单一产品功能和实现文章优先用具体技术主题。不为减少数量而移除有依据的标签。
- `next-edit`、`apply`、`speculative-edit` 是代码编辑的细分入口，即使文章少也保留。Context、Harness、Agent 等交叉主题不强制归入单一父级。
- 新增 tag 前检查既有含义，避免同义词、大小写变体和没有检索价值的标签；旧入口需要迁移时保留兼容链接。

### 标签展示与兼容入口

- `data/tag_groups.json` 维护主题分组、细分技术、来源、站点与环境和停用标签；`content/tags/<tag>/_index.md` 的 `title` 维护显示名称。新增标签先登记分组，否则构建检查会失败。
- 主题浏览页默认展开 Agent 系统、AI 编程、模型与产业、软件工程；`skills`、`evals` 在 Agent 系统组，`software-design`、`架构迁移`、`arm` 在软件工程组。分组锚点为 `group-<id>`，供首页主题入口跳转。
- 来源放在主题索引之后，显示为“已维护来源”，并说明不是完整来源索引；只含 `blog`、`init` 的“站点与环境”折叠展示。文章底部将主题与来源分行显示。`init` 显示为“开发环境”，`blog` 为“博客维护”，`apply` 为“代码应用（Apply）”。
- `视频笔记` 标签已停用：`/tags/视频笔记/` 及其分页跳转到对应栏目页（`legacyCategory`）。
- `博客推荐` 标签已停用：`/tags/博客推荐/` 保留两篇历史文章链接（`legacyPosts`），旧分页入口继续可用。

### 来源标签

来源标签与主题标签共用 `tags`，使用小写机构或媒体名，多词用连字符连接。目前维护：

| Tag | 判定依据 |
|-----|----------|
| `openai` | 原文发布于 `openai.com` 或已确认属于 OpenAI 的官方发布渠道 |
| `anthropic` | 原文发布于 `anthropic.com`、`claude.com` 或已确认属于 Anthropic 的官方发布渠道 |
| `langchain` | 原文发布于 `blog.langchain.com` 或已确认属于 LangChain 的官方发布渠道 |
| `cursor` | 原文发布于 `cursor.com`（含 `www.cursor.com`）或已确认属于 Cursor 的官方发布渠道 |
| `github` | 原文发布于 `github.blog`、`githubnext.com` 或已确认属于 GitHub 自身的官方发布渠道；托管在 `github.com` 的其他组织仓库不据此归入 |
| `uber` | 原文发布于 `uber.com`（含 `www.uber.com`）的官方博客或其他已确认的 Uber 官方发布渠道 |
| `latent-space` | 原文由 Latent Space 发布，例如 `latent.space`（含 `www.latent.space`）上的文章或访谈 |

- 以 `sources/orig/<slug>.md` 的 `source_url` 和文章实际主要来源为准。
- 只是引用官方文档、讨论某家公司或产品，不构成来源归属；第三方转载优先核对原始出处。
- 员工个人博客、个人社交账号与第三方媒体不自动视为被报道公司的官方渠道；媒体原创文章与访谈按媒体自身归属，例如 Latent Space 的 Claude Code 访谈标 `latent-space`。来源不明确时先不加。
- 微信公众号、X、YouTube 和 GitHub 等平台不直接代表原始发布者，应核对具体账号或仓库所属组织；例如 Lex Fridman 的 Cursor 团队访谈不标 `cursor`。
- 原创文章、工具清单不因使用某家公司产品或引用其资料而添加来源标签；视频按 `sources/video/` 的官方发布渠道核对，不按讲者任职公司推断。

示例：`tags: ["context-engineering", "prompt-engineering", "anthropic"]`。

## 专题与文章内链

专题保存在 `content/topics/`，用于课程目录、问题索引和精选阅读路径。

- 专题用 `reading_path` shortcode 展示 `data/reading_paths.json` 中的文章顺序、分组和推荐理由，标题取自文章页面。文章末尾根据同一份数据显示所属路径和下一篇。
- 文末“相关文章”由 `layouts/partials/related_posts.html` 按共同主题标签生成：越少见的标签权重越高，来源标签只算一半，已作为专题下一篇的文章不重复列出。
- 课程目录按周次或内容顺序列出文章，说明每篇回答什么问题；系列文章链接回目录。
- 问题型专题说明适合谁、从哪里开始以及条目关系，可以同时收录三个栏目的文章。
- 重点文章可补 1-3 个确有帮助的站内链接（`relref`），说明用于补背景、看机制或理解边界。
- 发布或修订文章时，检查是否适合补入已有专题；新建专题需有明确问题和足够的现有内容。专题保持精选。

---

## 文件结构

```
blog/
├── inbox.md                # 待处理文章队列（标题 + 链接），处理完移除
├── content/
│   ├── posts/              # 博文
│   ├── topics/             # 阅读专题
│   ├── categories/         # 栏目显示名与说明
│   └── tags/               # 标签显示名、说明与停用入口
├── data/                   # categories.json、tag_groups.json、reading_paths.json
├── layouts/、assets/        # 模板、样式与脚本
├── sources/
│   ├── orig/<slug>.md      # 外部文章来源元信息（公开，只有 frontmatter）
│   ├── video/<slug>.md     # 视频来源、章节时间戳与证据边界
│   ├── failed/failed-sources.md  # 抓取失败记录
│   └── archive/            # 私有仓库 blog-sources 的克隆（git 忽略）
│       └── orig/<slug>.md  # 外部文章全文
├── static/
│   ├── images/<slug>/      # 文章配图
│   └── pdfs/               # 子模块：公开仓库 blog-pdfs
├── scripts/                # build_site.py、check_*.py、new_post.py、source_record.py、lastmod_reminder.py、hooks/
└── tests/
```

slug 在文章、来源记录、私有归档和 PDF 之间保持一致。`sources/Orig Index.md` 是给 Obsidian 用的导航页。

## 原文归档

外部网页文章的全文受版权保护，不能放在公开仓库。归档分成两份：

- **私有全文**：`sources/archive/orig/<slug>.md`，即私有仓库 `QianKuang8/blog-sources` 的 `orig/<slug>.md`。frontmatter 之后接 defuddle 提取和清洗后的 Markdown 正文，是写作与审校的依据。
- **公开元信息**：`sources/orig/<slug>.md`，只有同一份 frontmatter，由 `scripts/source_record.py <slug>` 从私有全文生成。构建检查拒绝带正文的公开记录（书籍证据记录除外）。修改 frontmatter（例如补 `related_sources`）时先改私有全文，再重新生成公开记录，两边保持一致。

首次使用时按 AGENTS.md“常用命令”把私有仓库克隆到 `sources/archive/`。

frontmatter 推荐字段：

```yaml
---
title: "原文标题"
source_url: "https://..."
domain: "example.com"
author: "作者或发布机构"
published_at: "2025-11-23"
description: "原文描述"
retrieved_at: "2026-04-08T21:01:02+08:00"
extractor: "defuddle"
---
```

- `source_url` 指向原文；书籍记录使用作者或出版社的官方书籍页面。
- `published_at` 必填，写原文页面标明的发布日期（加引号的 `"YYYY-MM-DD"`）。defuddle 的 `--json` 输出里的 `published` 通常可用；剪藏或抓取日期不能代替。页面只能确定到月或年时写 `"YYYY-MM"` 或 `"YYYY"`，确实没有发布日期（持续更新的网站、仓库）时写 `null`。
- `author` 写作者姓名；没有署名时写发布机构或公众号名，多位作者用英文逗号加空格分隔，不知道时省略。文章页标题下方会显示“原文 / 原书 / 原视频：标题、作者、日期”，视频记录取 `channel` 与 `published_at`。
- `domain` 优先取提取工具的元信息，为空时从 URL 主域名补齐。
- `retrieved_at` 必须带时区。
- 正文之前不额外插入“Metadata”标题；抓取说明写在 frontmatter 的 `extraction_note`。
- 一篇文章依据多份原文时，主记录用 `related_sources: ["<slug>"]` 列出其余记录（例如 Uber Arm 迁移的第二篇）。

### 书籍导读

书籍导读归入 `好文分享`，沿用 `sources/orig/<slug>.md`，设置 `source_type: book` 和 `extractor: manual-book-evidence`，保留 `title`、`source_url`、`domain`、`description`、`retrieved_at`。与网页文章不同，书籍记录的正文是公开的证据索引：作者、版本、出版信息，以及关键论点对应的章节和证据边界；不包含原书或译本全文。写法见 BLOG_PROMPTS.md。

原书、完整译稿、HTML 或 PDF 只存放在私有仓库 `QianKuang8/books`，不进入本仓库、`blog-pdfs` 或站点产物，该仓库不开启 GitHub Pages。从博客回查时，入口标注“个人阅读资料（需仓库权限）”；普通读者使用官方书籍链接。

## 外部文章工作流

```
1. 收集：看到好文章 → 记录到 inbox.md（标题 + 链接）
2. 批量处理（按主题分批，每批 5-10 篇）
   ├─ 2a. scripts/new_post.py 生成私有全文、公开元信息和文章草稿（必选）
   ├─ 2b. 检查全文是否有完整 metadata + 正文，补齐脚本提示的字段
   ├─ 2c. 确认 categories: ["好文分享"] 和 tags
   ├─ 2d. 基于私有全文撰写博客文章，并检查原文图表、选取有解释价值的配图
   └─ 2e. 按 BLOG_PROMPTS.md 做发布前 review
3. 发布：hugo server -D 预览 → scripts/build_site.py → 分别提交两个仓库并推送
4. 清理：从 inbox.md 移除已发布条目
```

单篇命令：

```bash
# 1. 用 defuddle 抓取全文，写出私有全文、公开元信息和草稿 content/posts/<slug>.md（draft: true）
.venv/bin/python scripts/new_post.py <slug> "https://..."
# 输出的 check: 行列出需要手工确认的字段：没有发布日期、作者或描述。
# defuddle 漏掉发布日期或作者时，用 --published YYYY-MM-DD、--author 补上；已保存的 defuddle JSON 可用 --from-json 读入。
# 抓取失败则记录到 sources/failed/failed-sources.md，并暂停这篇文章。
# 之后修改 frontmatter（补 related_sources、image_sources 等）时先改私有全文，再运行
# .venv/bin/python scripts/source_record.py <slug>

# 2. 写草稿：换成中文标题，删去 draft 和开头注释，预览并正式构建
hugo server -D
.venv/bin/python scripts/build_site.py

# 3. 私有仓库提交全文
git -C sources/archive add orig/<slug>.md
git -C sources/archive commit -m "add: <slug>"
git -C sources/archive push

# 4. 本仓库提交文章和元信息，从 inbox.md 移除对应条目
git add content/posts/<slug>.md sources/orig/<slug>.md
git commit -m "add: 文章标题"
```

注意事项：

- 没有私有全文就不要继续发布；拿不到时由用户提供替代 URL、复制的文本或本地文件，先补齐全文再继续。
- `defuddle` 适合标准文章页；对知乎、X、微信、视频页、重 JS 页面不要假设一定成功。不要自动尝试 defuddle 之外的抓取方案，除非用户授权。
- 批量处理时不因个别失败暂停整个批次，成功的继续；批次结束后把 `failed-sources.md` 中的失败项汇报给用户。
- 哪些文章提交前必须经过独立 reviewer，见 BLOG_PROMPTS.md“Reviewer / Subagent 流程”。

失败记录格式：

```markdown
### [日期] 批次名称

| URL | 失败原因 | 补档来源 | 状态 |
|-----|---------|---------|------|
| https://... | 无法访问 | - | 待处理 |
```

---

## 外部文章配图

- 选图标准、图注格式与发布前的图片检查见 BLOG_PROMPTS.md 的“配图要求”。写作时检查原页面，defuddle 提取的正文可能遗漏交互图表，不据此判断原文没有图。
- 选用的图片存入 `static/images/<slug>/`，正文引用 `/images/<slug>/...`。
- 构建时，图片渲染钩子为 PNG、JPEG、WebP 生成 720 与 1440 宽的 WebP 显示版本，并让图片链接到原图；SVG 原样显示。原图文件保持不变，不手工压缩，也不另存缩小版。
- 优先取得清晰的原图文件；交互图表截取原页面中的完整图表区域。
- 在私有归档 frontmatter 的 `image_sources` 中记录图片标题、站内路径、原图或页面 URL、取得方式和时间，再运行 `scripts/source_record.py <slug>` 同步公开元信息。重绘或局部截取须说明处理方式。
- `scripts/check_content.py` 会拒绝以下情况：
  - 所有文章：图片没有 alt；不是 `/images/...` 下实际存在的文件；`static/images/` 中有无人引用的文件。
  - 文章解读与视频笔记：图片后面一段不是斜体图注；图注开头不是 BLOG_PROMPTS.md 规定的“图 N：”加标注，或编号不是按顺序从 1 开始。
  - 文章解读：用到的站内图片没有列入 `image_sources`；`image_sources` 条目字段不全，或指向文章没有用到的图片。书籍导读的来源记录手工维护，`image_sources` 直接写在 `sources/orig/<slug>.md`。

## 视频笔记与 PDF

新建视频笔记使用专用模板，自动设置视频栏目和 `learning_status: pending`：

```bash
hugo new content --kind video content/posts/<slug>.md
```

模板生成草稿；发布前补全摘要、正文、来源记录和 PDF 链接，并移除 `draft: true`。

### 来源记录

视频不走 defuddle 流程。每篇视频笔记先创建 `sources/video/<slug>.md`（公开，正文是自己整理的证据）：

```yaml
---
title: "原视频标题"
source_url: "https://..."
source_type: "video"
channel: "频道或机构"
speaker: "讲者（若可得）"
published_at: "视频发布日期（若可得）"
duration: "视频时长"
retrieved_at: "2026-08-31T12:00:00+08:00"
series: "系列名称（若有）"
pdf_path: "standalone/<slug>.pdf"
---
```

正文记录视频章节和关键时间戳、使用的字幕轨道或课程材料、讲者观点与整理者归纳及未确认内容的边界，以及文章与 PDF 的映射。不提交完整字幕、视频、音频、全量抽帧、生成日志或本地绝对路径。

### PDF 存储

- PDF 母版由本地学习工作区保存，不进入本仓库。公开版可以改成稳定的英文文件名，不在文件名中维护 `v1`、`v2`。
- 复制后用 `cmp` 或 SHA-256 确认字节未变。
- 公开仓库 `https://github.com/QianKuang8/blog-pdfs` 只有 `standalone/<slug>.pdf` 与 `stanford-mse435/week-<nn>-<slug>.pdf` 两类路径，本仓库通过 `static/pdfs` 子模块固定其提交。
- 文章链接站点 PDF（从站点根目录写 `/pdfs/<pdf-path>`，模板补部署路径），同时提供固定到 PDF 提交的 GitHub 链接 `https://github.com/QianKuang8/blog-pdfs/blob/<pdf-commit>/<pdf-path>`。

普通 `git clone` 不下载子模块。正式构建需要解析固定链接的提交，因此用 `git submodule update --init static/pdfs` 拉取完整历史；只预览时可加 `--depth 1`，之后再用 `git -C static/pdfs fetch --unshallow` 补齐。未初始化时 Hugo 仍能编译文章，但 PDF 链接不可用，正式构建会报错。

固定链接可以指向旧提交，只要该路径的文件字节与当前 PDF 相同；更新了 PDF 字节必须同步更新固定链接。

### 发布、更新与回滚

```text
1. 检查视频来源、公开边界和 PDF 内容
2. 创建或更新 sources/video/<slug>.md
3. 将选定源 PDF 复制到 blog-pdfs 的约定路径，用 cmp 或 SHA-256 验证字节一致
4. 在 blog-pdfs 提交并推送
5. 在本仓库更新 static/pdfs 子模块指针
6. 创建或更新 content/posts/<slug>.md，同步更新 lastmod
7. 运行 scripts/build_site.py
8. 提交并推送本仓库
```

不能只更新 PDF 仓库而遗漏子模块指针。回滚时回退本仓库中的文章和子模块指针；PDF 仓库历史继续保留。发布后确认原视频链接、站点 PDF 链接和 GitHub 源文件链接与当前版本一致。
