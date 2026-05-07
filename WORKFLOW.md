# 博客发布流程

> 生成时间：2026-03-20，更新：2026-05-07

## 核心目标

**知识管理型博客**，发布到个人 Hugo 博客，主要为自己记录，同时也方便读者浏览。

---

## 决策汇总

| 环节 | 决策 | 说明 |
|------|------|------|
| **发布目标** | 知识管理型，个人网站 | 主要是 A，偏向 C |
| **技术栈** | Hugo + PaperMod 主题 | 博文位于 `content/posts/` |
| **内容组织** | 单篇文章 + Hugo tags | Hugo 自动生成 `/tags/xxx/` 合集页面 |
| **inbox.md 定位** | 待发布队列 | 处理完后移除，目标是清空 |
| **原文归档** | `sources/orig/<slug>.md` 为必选项 | 默认用 defuddle 生成，拿不到则暂停发布 |
| **写作依据** | `sources/orig/<slug>.md` 原文归档 | 不再要求 NotebookLM / `nlm` 摘要材料 |
| **撰写内容** | 原文解读 + 个人思考 | A/B 灵活处理，不做关联分析 |
| **发布节奏** | 分批处理 | 每 5-10 篇处理一次 |
| **多 tag 处理** | Hugo 多 tag 机制 | frontmatter 里写多个 tags |
| **积累文章** | 分批处理 | 按主题分批，慢慢清空 inbox.md |
| **tags 管理** | 12 个 tag，粗细结合 | 见下方 tag 体系表 |

---

## Tag 体系

> 确定于 2026-04-05，后续根据写作需要可能增减

**规则：** 单层平铺（Hugo tags）、技术概念英文/类型中文、一篇文章标 1-3 个 tag

| Tag | 类型 | 说明 |
|-----|------|------|
| `code-editing` | 宽 tag | AI 代码编辑总类 |
| `next-edit` | 细 tag | Next Edit 预测（cursor tab、copilot NES、zed、augment） |
| `apply` | 细 tag | Apply / Unified Diffs |
| `speculative-edit` | 细 tag | Speculative Decoding 辅助生成 |
| `agent` | 细 tag | Agent 通用（架构、工程、设计） |
| `agentic-coding` | 细 tag | Coding Agent 产品和对比 |
| `harness-engineering` | 细 tag | Harness Engineering |
| `context-engineering` | 细 tag | Context Engineering |
| `prompt-engineering` | 细 tag | Prompt Engineering |
| `行业动向` | 中文类型 | 行业趋势、开源生态、LLM 发展 |
| `博客推荐` | 特殊 | 博客源推荐文章 |

---

## 文件结构

```
blog/
├── inbox.md              # 待处理文章队列（标题 + 链接 + 分类）
├── sources/              # 所有原材料（不发布，仅 git 管理）
│   ├── Orig Index.md     # Obsidian 导航索引
│   ├── orig/
│   │   └── <slug>.md     # defuddle 生成的原文存档（必选）
│   ├── nlm/              # 历史摘要材料（保留，不再作为流程输入）
│   └── failed/
│       └── failed-sources.md # 失败记录
├── content/posts/        # 已发布博文
└── WORKFLOW.md           # 本文档
```

**命名约定：**
- `sources/orig/<slug>.md` 存放原文归档，是写作的主要输入
- `sources/nlm/` 仅保留历史摘要材料，不再要求新增或补齐
- slug 与最终博文 slug 保持一致，便于查找对应关系
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

## 工作流

```
1. 收集
   看到好文章 → 记录到 inbox.md（标题 + 链接）

2. 批量处理（按主题分批）
   ├─ 2a. 生成并保存 sources/orig/<slug>.md（defuddle，必选）
   ├─ 2b. 检查原文归档是否有完整 metadata + 正文
   ├─ 2c. 确认 tags
   └─ 2d. 基于原文归档撰写博客文章

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

# 提交
git add content/posts/<slug>.md sources/ && git commit -m "add: 文章标题"
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

- [x] **商量 tag 列表** — 12 个 tag，粗细结合，详见上方 tag 体系表
- [x] **移除摘要流程** — 不再使用 NotebookLM / `nlm`，直接基于 `sources/orig/` 写作
- [ ] **处理第一批文章** — Next Edit 批次剩余 5 篇

---

## 相关文件

- 文章队列: `inbox.md`
- 原材料目录: `sources/`
- 博文目录: `content/posts/`
- 写作 prompts: `BLOG_PROMPTS.md`
- 博客配置: `config.yaml`
