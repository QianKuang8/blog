# 博客发布流程

> 生成时间：2026-03-20，更新：2026-08-31

## 核心目标

**知识管理型博客**，发布到个人 Hugo 博客，主要为自己记录，同时也方便读者浏览。

---

## 决策汇总

| 环节 | 决策 | 说明 |
|------|------|------|
| **发布目标** | 知识管理型，个人网站 | 主要是 A，偏向 C |
| **技术栈** | Hugo + PaperMod 主题 | 博文位于 `content/posts/` |
| **内容组织** | 单篇文章 + Hugo tags | Hugo 自动生成 `/tags/xxx/` 合集页面 |
| **视频笔记** | 单篇解读 + 视频来源记录 | 来源记录保存到 `sources/video/<slug>.md` |
| **PDF 资产** | 独立公开仓库 + submodule | 源 PDF 不压缩，挂载到 `static/pdfs` |
| **inbox.md 定位** | 待发布队列 | 处理完后移除，目标是清空 |
| **原文归档** | 外部网页文章必须有 `sources/orig/<slug>.md` | 默认用 defuddle 生成，拿不到则暂停发布 |
| **写作依据** | `sources/orig/` 或 `sources/video/` | 按内容类型选择，不再要求 NotebookLM / `nlm` 摘要材料 |
| **撰写内容** | 原文解读 + 个人思考 | A/B 灵活处理，不做关联分析 |
| **发布节奏** | 分批处理 | 每 5-10 篇处理一次 |
| **多 tag 处理** | Hugo 多 tag 机制 | frontmatter 里写多个 tags |
| **积累文章** | 分批处理 | 按主题分批，慢慢清空 inbox.md |
| **tags 管理** | 13 个 tag，粗细结合 | 见下方 tag 体系表 |

---

## Tag 体系

> 确定于 2026-04-05，后续根据写作需要可能增减

**规则：** 单层平铺（Hugo tags）、技术概念英文/类型中文，一篇文章标 1-3 个 tag。

说明：以下 tag 体系主要约束外部 AI 技术文章解读；个人记录、环境初始化、博客维护、非 AI 工程文章可使用少量非 AI tag，但应避免使用 `default` 这类无信息量标签。

| Tag | 类型 | 说明 |
|-----|------|------|
| `code-editing` | 宽 tag | AI 代码编辑总类 |
| `next-edit` | 细 tag | Next Edit 预测（cursor tab、copilot NES、zed、augment） |
| `apply` | 细 tag | Apply / Unified Diffs |
| `speculative-edit` | 细 tag | Speculative Edits 辅助代码编辑 |
| `model-engineering` | 细 tag | 模型架构、推理优化、Serving、KV Cache 等模型工程 |
| `agent` | 细 tag | Agent 通用（架构、工程、设计） |
| `agentic-coding` | 细 tag | Coding Agent 产品和对比 |
| `harness-engineering` | 细 tag | Harness Engineering |
| `context-engineering` | 细 tag | Context Engineering |
| `prompt-engineering` | 细 tag | Prompt Engineering |
| `行业动向` | 中文类型 | 行业趋势、开源生态、LLM 发展 |
| `视频笔记` | 中文类型 | 视频访谈、课程和演讲的解读文章 |
| `博客推荐` | 特殊 | 博客源推荐文章 |

### 非 AI / 个人记录 tag

| Tag | 类型 | 说明 |
|-----|------|------|
| `blog` | 个人记录 | 博客搭建、写作和维护 |
| `init` | 个人记录 | 本机初始化、开发环境配置 |
| `arm` | 工程主题 | Arm / 多架构迁移 |
| `架构迁移` | 工程主题 | 基础设施或系统架构迁移 |

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
├── static/pdfs/          # 目标挂载点：公开 blog-pdfs 仓库的 submodule
└── WORKFLOW.md           # 本文档
```

**命名约定：**
- `sources/orig/<slug>.md` 存放外部文章解读的原文归档，是写作的主要输入；个人笔记、清单、博客维护记录这类没有单一原文的文章可不创建
- `sources/video/<slug>.md` 存放视频笔记的来源元信息、章节时间戳和证据边界；不要把视频伪装成 defuddle 原文归档
- `sources/nlm/` 仅保留历史摘要材料，不再要求新增或补齐
- slug 与最终博文 slug 保持一致，便于查找对应关系
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
- `source_url` 是原文唯一来源
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

未初始化 `static/pdfs` 时，本地 Hugo 仍可编译文章，但 PDF 链接在本地预览中不可用。GitHub Pages workflow 必须在运行 Hugo 前检出 submodule。

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
8. 运行 Hugo 构建并检查 PDF 产物与文章链接
9. 提交并推送博客仓库
```

不能让博客仓库指向只存在于本地、尚未推送的 PDF commit，也不能只更新 PDF 仓库而遗漏博客 submodule 指针。

回滚时优先回退博客仓库中的文章和 submodule 指针；PDF 仓库历史继续保留，不通过删除历史完成回滚。

发布前至少检查：

```bash
git submodule status --recursive
hugo
test -f public/pdfs/<pdf-path>
cmp static/pdfs/<pdf-path> public/pdfs/<pdf-path>
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
   ├─ 2c. 确认 tags
   ├─ 2d. 基于原文归档撰写博客文章
   └─ 2e. 按 BLOG_PROMPTS.md 做发布前 review

3. 发布
   ├─ 创建 content/posts/<slug>.md
   ├─ hugo server -D 预览
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
author: "Qian"
isCJKLanguage: true
showToc: true
---

## 正文内容

原文要点 + 个人思考 + 原文链接
```

## 博客写作风格

后续技术博客默认采用 **博客解读** 风格，而不是纯摘要、纯资料卡片或提纲式笔记。

写作时先阅读 [BLOG_PROMPTS.md](BLOG_PROMPTS.md)，按其中的写作 prompt、发布前检查 prompt 和可选 subagent 流程执行。

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
- PDF 资产挂载点: `static/pdfs/`
- 写作 prompts: `BLOG_PROMPTS.md`
- 博客配置: `config/_default/config.yaml`
