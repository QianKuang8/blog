# 博客发布流程

> 生成时间：2026-03-20，更新：2026-09-21

## 核心目标

**知识管理型博客**，发布到个人 Hugo 博客，主要为自己记录，同时也方便读者浏览。

---

## 决策汇总

| 环节 | 决策 | 说明 |
|------|------|------|
| **发布目标** | 知识管理型，个人网站 | 方便自己回查，也帮助读者按问题阅读 |
| **技术栈** | Hugo + 自建模板与样式 | 博文位于 `content/posts/`，展示层位于 `layouts/` 与 `assets/` |
| **内容组织** | 单篇文章 + categories + tags | 栏目区分文章类型，tags 表达主题与来源，topics 提供阅读路径 |
| **视频笔记** | 单篇解读 + 视频来源记录 | 来源记录保存到 `sources/video/<slug>.md` |
| **PDF 资产** | 独立公开仓库 + submodule | 源 PDF 不压缩，挂载到 `static/pdfs` |
| **inbox.md 定位** | 待发布队列 | 处理完后移除，目标是清空 |
| **原文归档** | 外部网页文章必须有 `sources/orig/<slug>.md` | 默认用 defuddle 生成，拿不到则暂停发布 |
| **写作依据** | `sources/orig/` 或 `sources/video/` | 按内容类型选择，不再要求 NotebookLM / `nlm` 摘要材料 |
| **撰写内容** | 按文章用途组织 | 解读、研究、教程与清单使用各自的写作和审校标准 |
| **发布节奏** | 分批处理 | 每 5-10 篇处理一次 |
| **提交与部署** | 直接提交主分支 `main` | 本地构建和检查后提交、推送；现有 workflow 负责部署，无需 PR |
| **多 tag 处理** | Hugo 多 tag 机制 | frontmatter 里写多个 tags |
| **积累文章** | 分批处理 | 按主题分批，慢慢清空 inbox.md |
| **categories 管理** | 3 个栏目，单选 | 内部值保留 `好文分享`、`原创文章`、`视频笔记`；显示为阅读与解读、研究与实践、视频笔记 |
| **tags 管理** | 主题标签 + 按需维护的来源标签 | 已维护 7 个机构或媒体来源，见下方 tag 体系表 |

---

## 页面预览与验证范围

本站面向桌面阅读，不要求手机适配。新增或修改文章、图表和页面样式时，只检查桌面显示效果；除非用户明确要求，否则不做窄屏或手机视口验证，也不为移动端调整排版。

发布时使用 `scripts/build_site.py` 完成源文件校验、干净 Hugo 构建和站点检查，再完成适用的外部链接及线上部署核验。首次使用时按 README 建立 Python 虚拟环境并安装 `requirements.txt`。

构建入口先检查文章和来源记录，在新的临时目录中构建并检查 PDF 字节与站点产物；全部通过后才替换 `public/`。构建失败时保留上次通过验证的产物。直接运行 `hugo` 仍可用于调试，但不作为发布检查结果，因为旧输出可能残留。

`scripts/check_content.py` 使用 YAML 解析器检查发布态文章的必需元数据、显式时区、`lastmod >= date`、单一合法栏目，以及对应的原文或视频来源记录。`draft: true` 的文章可以尚未完成；未来日期但未标草稿的文章也必须完整。当前存量已具备全部来源记录，不设置历史豁免。视频还检查来源字段、原视频链接、PDF 路径、submodule、站点与固定 GitHub 链接，以及构建前后的文件字节。该检查不联网，也不能代替文章事实审校或线上链接检查。

---

## 栏目体系

`categories` 回答“这是什么类型的文章”，`tags` 中的主题标签回答“文章在谈什么”，来源标签回答“原文来自哪里”，`topics` 则是人工维护的主题阅读路径。来源标签沿用 Hugo tags，不新增栏目或 taxonomy。

每篇文章必须且只能选择一个栏目：

| 内部栏目值 | 页面显示名 | 适用范围 | 来源要求 |
|------------|------------|----------|----------|
| `好文分享` | 阅读与解读 | 基于外部网页文章或书籍整理的中文解读 | 必须有 `sources/orig/<slug>.md`；书籍保存证据记录，不归档全文 |
| `原创文章` | 研究与实践 | 个人实践、研究、观点或工具清单 | 没有强制来源文件 |
| `视频笔记` | 视频笔记 | 基于课程、访谈或演讲整理的主题式笔记 | 必须有 `sources/video/<slug>.md` 和对应 PDF |

frontmatter 使用单值数组，便于 Hugo 生成 `/categories/` 及各栏目列表：

```yaml
categories: ["原创文章"]
```

栏目显示名在 `content/categories/<内部栏目值>/_index.md` 维护，内部值与旧 URL 不变。文章列表和正文元信息进一步区分“阅读与解读”的内容形式：默认显示“文章解读”，对应 `sources/orig/<slug>.md` 的 frontmatter 设置 `source_type: book` 时显示“书籍导读”。这两个标识都链接到原有栏目，不新增顶级栏目或文章字段；搜索结果使用栏目显示名。

新建文章时设置 `date` 和 `lastmod`，修订已有文章保留首次发布的 `date`。纯栏目、标签或格式整理不修改 `lastmod`；只有标题、摘要、description 或正文发生变化时才更新内容时间。`视频笔记` 不再写入 tags，历史标签入口转向同名栏目，原分页与 RSS 继续可用。

首页按时间倒序展示文章，每页 10 篇；新读者引导链接到阅读专题，主题入口链接到主题浏览页的对应分组，栏目链接进入对应 taxonomy 页面继续分页浏览。首页、栏目、标签详情共用文章条目和分页模板，并为每个分页生成指向自身的 canonical。文章条目突出标题与摘要，类型、日期、阅读时长和至多两个主题标签放在次要位置。左侧只保留最新文章、主题浏览、阅读专题、归档和搜索五个固定入口；文章页可切换专注阅读。

---

## Tag 体系

> 确定于 2026-04-05，后续根据写作需要可能增减

**规则：** Hugo tags 数据保持平铺，主题浏览页按主题、已维护来源、站点与环境分组展示。标签 slug 保持稳定，显示名称可以使用易读的中文或品牌名称。一篇文章通常标 1-3 个主题 tag，可额外添加 1 个来源 tag；来源 tag 不占主题数量。没有合适主题的非技术视频可以使用 `tags: []`。

说明：以下 tag 体系主要约束外部 AI 技术文章解读；个人记录、环境初始化、博客维护、非 AI 工程文章可使用少量非 AI tag，但应避免使用 `default` 这类无信息量标签。

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
| `行业动向` | 主题 tag | 行业趋势、开源生态、商业变化、跨模型发展趋势；不作为课程、新闻或单一产品实现文章的兜底标签 |

### 非 AI / 个人记录 tag

| Tag | 类型 | 说明 |
|-----|------|------|
| `blog` | 个人记录 | 博客搭建、写作和维护 |
| `init` | 个人记录 | 本机初始化、开发环境配置 |
| `arm` | 工程主题 | Arm / 多架构迁移 |
| `架构迁移` | 工程主题 | 基础设施或系统架构迁移 |
| `software-design` | 工程主题 | 软件设计、模块边界、信息隐藏与复杂性管理 |

### 标签选择

- 先选最能描述文章内容的主题，再按需要补充，通常保持 1-3 个主题 tag；来源标签单独按下方规则添加。
- `agent` 适合跨任务的 Agent 机制，例如 Computer History 和 Skill 复用；`agentic-coding` 适合 AI 编程产品、工作流和工程实践。只有两个范围都形成独立主线时才同时使用，不因为编程产品使用了 Agent 就顺带添加 `agent`。
- 视频笔记只用 `categories` 表示内容形式，按正文另选主题。沟通、组织管理等非技术文章没有合适既有主题时可用 `tags: []`；持续积累同类内容后再考虑新增主题，不强套 AI 标签。
- `行业动向` 是否保留取决于正文有没有充分展开趋势、生态、产业经济或竞争格局；单一产品功能和实现文章优先使用具体技术主题。不得仅为了减少数量而移除有依据的标签。
- `next-edit`、`apply`、`speculative-edit` 是代码编辑的细分入口，保留检索价值，即使文章较少也不自动删除。其他主题分组只是导航组织，Context、Harness、Agent 等交叉主题不强制归入单一父级。
- 新增 tag 前先检查既有含义，避免同义词、大小写变体和没有检索价值的标签；旧入口需要迁移时保留兼容链接。

### 标签展示与兼容入口

- `data/tag_groups.json` 维护主题分组、细分技术、来源、站点与环境的顺序和角色，`content/tags/<tag>/_index.md` 的 `title` 维护显示名称。新增标签时同步补充分组，避免落入临时“其他主题”区域。
- 主题浏览页采用文字索引，默认展开 Agent 系统、AI 编程、模型与产业、软件工程；`software-design`、`架构迁移`、`arm` 放在软件工程组。分组使用稳定的 `group-<id>` 锚点，供首页主题入口跳转。
- 来源放在主题索引之后，显示为“已维护来源”，并说明不是完整来源索引；仅含 `blog`、`init` 的“站点与环境”折叠展示。文章底部继续将主题与来源分行显示。`init` 显示为“开发环境”，`blog` 为“博客维护”，`apply` 为“代码应用（Apply）”，不改变原有 URL。
- `视频笔记` 标签已停用：`/tags/视频笔记/` 及旧分页转向对应栏目页；旧 RSS 从当前视频栏目生成。
- `博客推荐` 标签已停用：`/tags/博客推荐/` 保留两篇历史文章链接，旧分页入口与 RSS 继续可用。新文章使用具体主题，不再添加该标签。
- 停用标签不出现在标签导航或文章标签中。历史入口通过 `legacyCategory` 或 `legacyPosts` 指定兼容内容，不再依赖文章携带旧标签。
- `layouts/_default/single.html` 是自建文章模板，调用 `post_tags.html` 展示标签并补充阅读路径；正文、目录、专注阅读沿用全站排版变量。
- `layouts/partials/head.html` 管理样式、脚本、RSS 和 SEO；`canonical_url.html` 与列表共用 `list_pages.html` 的分页集合。搜索使用独立保存的 Fuse 依赖，许可位于 `assets/js/vendor/`，发布副本位于 `static/licenses/`。

### 来源标签

来源标签与主题标签共用 `tags`，统一使用小写机构或媒体名，多词用连字符连接。目前维护以下来源：

| Tag | 判定依据 |
|-----|----------|
| `openai` | 原文发布于 `openai.com` 或已确认属于 OpenAI 的官方发布渠道 |
| `anthropic` | 原文发布于 `anthropic.com`、`claude.com` 或已确认属于 Anthropic 的官方发布渠道 |
| `langchain` | 原文发布于 `blog.langchain.com` 或已确认属于 LangChain 的官方发布渠道 |
| `cursor` | 原文发布于 `cursor.com`（含 `www.cursor.com`）或已确认属于 Cursor 的官方发布渠道 |
| `github` | 原文发布于 `github.blog`、`githubnext.com` 或已确认属于 GitHub 自身的官方发布渠道；托管在 `github.com` 的其他组织仓库不据此归入 |
| `uber` | 原文发布于 `uber.com`（含 `www.uber.com`）的官方博客或其他已确认的 Uber 官方发布渠道 |
| `latent-space` | 原文由 Latent Space 发布，例如 `latent.space`（含 `www.latent.space`）上的文章或访谈 |

- 以 `sources/orig/<slug>.md` 的 `source_url` 和文章实际主要来源为准；历史文章没有归档时，核对正文的原文链接。
- 外部文章明确来自上述发布者时必须添加对应标签。只是引用官方文档、讨论某家公司或产品，不构成来源归属；第三方转载优先核对原始出处。
- 员工个人博客、个人社交账号与第三方媒体不自动视为被报道公司的官方渠道；媒体原创文章与访谈按媒体自身归属，例如 Latent Space 的 Claude Code 访谈标 `latent-space`。来源不明确时先不添加，其他来源按检索需要扩展。
- 微信公众号、X、YouTube 和 GitHub 等平台不直接代表原始发布者，应核对具体账号或仓库所属组织；例如 Lex Fridman 的 Cursor 团队访谈不标 `cursor`。
- 原创文章、工具清单不因使用某家公司产品或引用其资料而添加来源标签；视频来源按 `sources/video/` 的官方发布渠道核对，不按讲者任职公司推断。
- 补历史来源标签时保留原有 `date` 与 `lastmod`。来源入口为 `/tags/<tag>/`，页面说明位于 `content/tags/<tag>/_index.md`。

示例：`tags: ["context-engineering", "prompt-engineering", "anthropic"]`。

## 专题与文章内链

专题保存在 `content/topics/`，用于课程目录、问题索引和精选阅读路径；沿用现有页面模板，通过 `content/topics/_index.md` 提供入口。

- 精选文章的顺序、分组和推荐理由统一维护在 `data/reading_paths.json`，对应专题使用 `reading_path` shortcode 展示；标题从 Hugo 文章页面获取。文章末尾根据同一关系表自动显示所属阅读路径和下一篇，避免两端手工维护失配。
- 课程目录按周次或内容顺序列出文章，说明每篇回答什么问题；系列文章链接回目录。
- 问题型专题说明适合谁、从哪里开始，以及条目之间的关系。它可以同时收录原创文章、视频笔记和好文分享。
- 重点文章可补 1-3 个确有帮助的站内链接，并说明用于补背景、看机制或理解边界。使用 Hugo `relref` 引用已有文章与专题。
- 发布或修订文章时，检查是否适合补入已有专题；新建专题需有明确问题和足够的现有内容支撑。专题保持精选，避免重复堆积同类条目。
- 专题目录使用 `content/topics/` 的元数据约定，不添加文章栏目；新增论证完整的专题文章仍放在 `content/posts/` 并选择一个栏目。向博文正文增加导航或推荐链接时更新 `lastmod`，保留 `date`。

---

## 文件结构

```
blog/
├── inbox.md              # 待处理文章队列（标题 + 链接 + 分类）
├── sources/              # 所有原材料（不发布，仅 git 管理）
│   ├── Orig Index.md     # Obsidian 导航索引
│   ├── orig/
│   │   └── <slug>.md     # defuddle 生成的原文存档（必选）
│   ├── video/
│   │   └── <slug>.md     # 视频来源、章节时间戳与证据边界
│   ├── nlm/              # 历史摘要材料（保留，不再作为流程输入）
│   └── failed/
│       └── failed-sources.md # 失败记录
├── content/posts/        # 已发布博文
├── content/categories/   # 栏目总页与三个栏目说明
├── content/topics/       # 课程目录、问题索引与精选阅读路径
├── static/pdfs/          # 目标挂载点：公开 blog-pdfs 仓库的 submodule
└── WORKFLOW.md           # 本文档
```

**命名约定：**
- `sources/orig/<slug>.md` 存放外部文章解读的原文归档，是写作的主要输入；个人笔记、清单、博客维护记录这类没有单一原文的文章可不创建
- `sources/video/<slug>.md` 存放视频笔记的来源元信息、章节时间戳和证据边界；不要把视频伪装成 defuddle 原文归档
- `sources/nlm/` 仅保留历史摘要材料，不再要求新增或补齐
- slug 与最终博文 slug 保持一致，便于查找对应关系

### 书籍导读

书籍导读归入 `好文分享`，沿用 `sources/orig/<slug>.md` 保存可复核的来源记录。书籍记录明确设置 `source_type: book` 和 `extractor: manual-book-evidence`，保留通用的 `title`、`source_url`、`domain`、`description`、`retrieved_at`；正文记录作者、版本、出版信息，以及关键论点对应的章节和证据边界。`source_url` 使用作者或出版社的官方书籍页面。该记录是书籍证据索引，不是网页全文抓取，也不将私人译本全文写入公开仓库。

导读以自主概括、解释和适量引用组织，保留作者与作品署名；当前 AI 编程等延伸讨论须与原书观点区分。需要归档仅供个人学习使用的原书、完整译稿、HTML 或 PDF 时，存入独立私有仓库，不进入博客主仓库、公开 `blog-pdfs`、submodule 或站点构建产物，也不发布公开阅读页。需要从博客回查时，入口标注“个人阅读资料（需仓库权限）”；普通读者使用官方书籍链接。私人资料仓库不开启 GitHub Pages。
- PDF 使用稳定的英文 slug 文件名，不在文件名中维护 `v1`、`v2`；历史版本由 PDF 仓库提交和博客 submodule 指针追踪
- `blog-pdfs` 只使用 `standalone/` 与 `stanford-mse435/` 两个顶层目录
- 功能性文件集中在 `sources/failed/`（如 `sources/failed/failed-sources.md`）

## 原文归档格式

`sources/orig/<slug>.md` 默认使用单文件格式：

1. 文件头部使用 YAML frontmatter 保存元信息
2. 文件正文保存 `defuddle` 提取和清洗后的 markdown 内容

推荐字段如下：

```yaml
---
title: "原文标题"
source_url: "https://..."
domain: "example.com"
description: "原文描述"
retrieved_at: "2026-04-08T21:01:02+08:00"
extractor: "defuddle"
---
```

说明：
- 网页归档的 `source_url` 指向原文来源；书籍记录使用官方书籍页面，正文证据按“书籍导读”约定定位到具体版本与章节
- `domain` 优先从提取工具元信息获取；如果为空，可从 URL 主域名补齐
- `retrieved_at` 必须带时区
- frontmatter 之后直接接正文，不额外插入“Metadata”标题
- 归档文件不用于 Hugo 发布，仅用于原文留存、阅读和下游写作流程

---

## 视频笔记与 PDF 资产

### 来源记录

视频笔记不走 defuddle 原文归档流程。每篇视频笔记必须先创建 `sources/video/<slug>.md`，最小格式如下：

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

正文记录以下内容：

- 视频章节和关键时间戳
- 使用的字幕轨道、课程材料或补充来源
- 讲者明确表达的观点、整理者归纳和未确认内容之间的边界
- 对应博客文章与 PDF 的映射

不在来源记录中提交完整字幕、视频、音频、全量抽帧、生成日志或本地绝对路径。

### PDF 存储约定

- PDF 母版来自本地学习工作区，母版仍由该工作区保存，不进入博客主仓库
- 公开版直接使用选定的源 PDF，不压缩、不重新编码；允许改成稳定的英文文件名
- 复制后使用 `cmp` 或 SHA-256 确认文件字节未改变
- PDF 只提交到公开仓库 `https://github.com/QianKuang8/blog-pdfs`
- 博客主仓库通过 `static/pdfs` submodule 固定 PDF 仓库 commit；禁止把 PDF 作为博客主仓库的普通 Git 文件提交
- PDF 仓库使用以下目录：

```text
standalone/<slug>.pdf
stanford-mse435/week-<nn>-<slug>.pdf
```

对应站点地址为：

```text
/blog/pdfs/standalone/<slug>.pdf
/blog/pdfs/stanford-mse435/week-<nn>-<slug>.pdf
```

文章优先链接站点 PDF，并同时提供固定到 PDF commit 的 GitHub 源文件链接：

```text
https://github.com/QianKuang8/blog-pdfs/blob/<pdf-commit>/<pdf-path>
```

### Submodule 使用

本节约定在公开 `blog-pdfs` 仓库创建、并将其挂载为 `static/pdfs` submodule 后生效；完成初始化前不要运行 PDF 专用命令或发布 PDF 链接。

普通 `git clone` 不自动下载 submodule。完整初始化主题和 PDF：

```bash
git submodule update --init --recursive
```

只按需下载 PDF 仓库当前版本：

```bash
git submodule update --init --depth 1 static/pdfs
```

未初始化 `static/pdfs` 时，本地 Hugo 仍可编译文章，但 PDF 链接在本地预览中不可用，正式构建会报错。GitHub Pages workflow 必须在构建前检出 submodule。

正式校验需要解析文章固定 GitHub 链接的 PDF 提交。短 SHA 在本地唯一可解析时仍有效；链接可以固定在旧提交，只要该路径的文件字节与当前 submodule 中的 PDF 相同。若更新了 PDF 字节，必须同步更新固定链接。浅克隆可能缺少旧提交，此时先手动运行 `git -C static/pdfs fetch --unshallow`；校验器不会自动获取历史或请求远端。

### 发布、更新与回滚

首次发布或更新 PDF 时，严格按以下顺序执行：

```text
1. 检查视频来源、公开边界和 PDF 内容
2. 创建或更新 sources/video/<slug>.md
3. 将选定源 PDF 复制到 blog-pdfs 的约定路径
4. 使用 cmp 或 SHA-256 验证源文件与目标文件字节一致
5. 在 blog-pdfs 提交并推送 PDF commit
6. 在博客仓库更新 static/pdfs submodule 指针
7. 创建或更新 content/posts/<slug>.md，并同步更新 lastmod
8. 运行 scripts/build_site.py 构建并检查 PDF 产物与文章链接
9. 提交并推送博客仓库
```

不能让博客仓库指向只存在于本地、尚未推送的 PDF commit，也不能只更新 PDF 仓库而遗漏博客 submodule 指针。

回滚时优先回退博客仓库中的文章和 submodule 指针；PDF 仓库历史继续保留，不通过删除历史完成回滚。

发布前至少检查：

```bash
git submodule status --recursive
.venv/bin/python scripts/build_site.py
```

文章还必须确认原视频链接、站点 PDF 链接和 GitHub 源文件链接与当前发布版本一致。

---

## 外部文章工作流

```
1. 收集
   看到好文章 → 记录到 inbox.md（标题 + 链接）

2. 批量处理（按主题分批）
   ├─ 2a. 生成并保存 sources/orig/<slug>.md（defuddle，必选）
   ├─ 2b. 检查原文归档是否有完整 metadata + 正文
   ├─ 2c. 确认 `categories: ["好文分享"]` 和 tags
   ├─ 2d. 基于原文归档撰写博客文章
   └─ 2e. 按 BLOG_PROMPTS.md 做发布前 review

3. 发布
   ├─ 创建 content/posts/<slug>.md
   ├─ hugo server -D 预览
   ├─ .venv/bin/python scripts/build_site.py
   └─ git commit & push

4. 清理
   └─ 从 inbox.md 移除已发布的条目
```

### 单篇文章处理流程

```bash
# 1. 先生成原文归档（必选）
#    1a. 用 defuddle 抓取正文 markdown
defuddle parse "https://..." --md -o sources/orig/<slug>.md
#    1b. 补齐 frontmatter：title/source_url/domain/description/retrieved_at/extractor
# 如果这一步失败，记录到 sources/failed/failed-sources.md，并暂停这篇文章
```

2. 基于原文归档撰写中文博客文章

```bash
# 创建 content/posts/<slug>.md
# 按博客文章格式填写 frontmatter
# 结合 sources/orig/<slug>.md
# 中文整理原文要点 + 个人思考 + 原文链接

# 预览
hugo server -D

# 构建并检查生成站点
.venv/bin/python scripts/build_site.py

# 确认 OK 后，从 inbox.md 移除对应条目

# 提交当前文章及其原文归档；其它实际改动按文件逐项添加
git add content/posts/<slug>.md sources/orig/<slug>.md
git commit -m "add: 文章标题"
```

**注意事项：**
- 不再使用 NotebookLM 或 `nlm` CLI 作为发布流程的一部分
- `sources/orig/<slug>.md` 是硬前置，拿不到就不要继续发布
- `sources/orig/<slug>.md` 应包含 frontmatter metadata + 正文，避免归档文件失去来源信息
- `defuddle` 更适合标准文章页；对知乎、X、微信、视频页、重 JS 页面不要假设一定成功
- sources/ 目录存放所有中间文件，纳入 git 管理
- 已存在的 `sources/nlm/` 文件作为历史材料保留，但不要求新增、不要求补齐，也不作为发布阻塞项

### 批量处理流程（推荐）

按主题分批处理多篇文章时，按以下顺序操作：

```
步骤 1：批量生成原文归档（必选）
  → 对每篇文章执行 defuddle，保存到 sources/orig/<slug>.md
  → 成功的继续，失败的记录到 sources/failed/failed-sources.md，并暂停该文章

步骤 2：检查原文归档质量
  → 确认每篇文章都有 metadata、原文 URL、正文内容
  → 根据内容确认 slug 和 tags

步骤 3：成功的文章直接走完整流程（不停顿）
  → 结合 sources/orig/<slug>.md 撰写博客文章
  → 批量处理、长文、重要文章必须在提交前走 reviewer 发布检查
  → reviewer 按 BLOG_PROMPTS.md 对照 content/posts/<slug>.md 和 sources/orig/<slug>.md 验收

步骤 4：批次结束后，汇报失败项给用户
  → 展示 sources/failed/failed-sources.md 中的记录
  → 等待用户手动解决

步骤 5：用户回来后先补齐原文归档，再继续后续流程
  → 用户可能提供：替代 URL、复制粘贴的文本、本地文件
  → 目标是先生成或补齐 sources/orig/<slug>.md
  → 原文归档准备好后，继续写作和发布
```

**原则：**
- 不要因个别失败暂停整个批次，成功的继续走
- 不要自动尝试 defuddle 之外的其他抓取替代方案
- 没有 `sources/orig/<slug>.md` 就不要继续发布
- 信息源问题由用户手动解决，直到能生成 `sources/orig/<slug>.md`
- 失败项统一记录在 `sources/failed/failed-sources.md`，格式如下：

```markdown
## 失败记录

### [日期] 批次名称

| URL | 失败原因 | 补档来源 | 状态 |
|-----|---------|---------|------|
| https://... | 无法访问 | - | 待处理 |
```

---

## 博客文章格式

```yaml
---
date: '2026-03-20T10:00:00+08:00'
lastmod: '2026-03-20T10:00:00+08:00'
title: '文章标题'
summary: "摘要"
description: "描述"
tags: ["tag1", "tag2"]
categories: ["原创文章"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

## 正文内容

原文要点 + 个人思考 + 原文链接
```

## 博客写作风格

外部文章和视频默认采用 **博客解读** 风格。原创研究、实践教程和工具清单按用途组织；清单可以使用列表，教程可以使用步骤，不要求统一写成评论文章。

写作时先阅读 [BLOG_PROMPTS.md](BLOG_PROMPTS.md)，确认任务是新写、修订还是定稿发布适配，再按对应用途的写作与审校标准执行。批量、长文、重要文章及改旧文遵守其中的独立 reviewer 流程。

工具推荐、安装教程和持续维护的清单，按实际情况记录核验日期、环境或版本及核验范围。未记录或未复跑时如实说明；不能以文章的 `lastmod` 代替实际核验时间。

---

## 待办事项

- [x] **商量 tag 列表** — 13 个 tag，粗细结合，详见上方 tag 体系表
- [x] **移除摘要流程** — 不再使用 NotebookLM / `nlm`，直接基于 `sources/orig/` 写作
- [x] **清空 inbox 文章队列** — 2026-06-05 已完成，无法作为博文发布的条目已记录在 `sources/failed/failed-sources.md`

---

## 相关文件

- 文章队列: `inbox.md`
- 原材料目录: `sources/`
- 视频来源记录: `sources/video/`
- 博文目录: `content/posts/`
- 专题与目录: `content/topics/`
- PDF 资产挂载点: `static/pdfs/`
- 写作 prompts: `BLOG_PROMPTS.md`
- 博客配置: `config/_default/config.yaml`
