# 博客发布流程

> 生成时间：2026-03-20，更新：2026-04-18

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
| **摘要用途** | 自己看 + 读者看 | 对特别有意思的文章单开深度解读 |
| **摘要生成** | 手动 NotebookLM 摘要 + `sources/orig/<slug>.md` 双材料 | 不再使用 `nlm` CLI；由用户手动创建 NotebookLM 文档/摘要后放入 `sources/nlm/<slug>.md` |
| **撰写内容** | 整理摘要 + 个人思考 | A/B 灵活处理，不做关联分析 |
| **发布节奏** | 分批处理 | 每 5-10 篇处理一次 |
| **多 tag 处理** | Hugo 多 tag 机制 | frontmatter 里写多个 tags |
| **积累文章** | 分批处理 | 按主题分批，慢慢清空 inbox.md |
| **tags 管理** | 12 个 tag，粗细结合 | 见下方 tag 体系表 |

---

## Tag 体系

> 确定于 2026-04-05，后续根据摘要结果可能增减

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
│   ├── nlm/
│   │   └── <slug>.md     # 用户手动从 NotebookLM 复制/导出的摘要材料
│   └── failed/
│       └── failed-sources.md # 失败记录
├── content/posts/        # 已发布博文
└── WORKFLOW.md           # 本文档
```

**命名约定：**
- `sources/orig/<slug>.md` 存放原文归档，`sources/nlm/<slug>.md` 存放用户手动生成的 NotebookLM 摘要材料
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
- 归档文件不用于 Hugo 发布，仅用于原文留存、阅读和下游摘要流程

---

## 工作流

```
1. 收集
   看到好文章 → 记录到 inbox.md（标题 + 链接）

2. 批量处理（按主题分批）
   ├─ 2a. 生成并保存 sources/orig/<slug>.md（defuddle，必选）
   ├─ 2b. 等待用户在 NotebookLM Web 手动创建文档/摘要
   ├─ 2c. 用户将 NotebookLM 摘要复制或导出到 sources/nlm/<slug>.md
   ├─ 2d. 检查 sources/nlm/<slug>.md 是否存在且内容可用
   ├─ 2e. 确认 tags
   └─ 2f. 撰写博客文章（结合原文归档 + NotebookLM 摘要）

3. 发布
   ├─ 创建 content/posts/<slug>.md
   ├─ hugo server -D 预览
   └─ git commit & push

4. 清理
   └─ 从 inbox.md 移除已发布的条目
```

### 单篇文章处理流程（手动 NotebookLM）

```bash
# 1. 先生成原文归档（必选）
#    1a. 用 defuddle 抓取正文 markdown
defuddle parse "https://..." --md -o sources/orig/<slug>.md
#    1b. 补齐 frontmatter：title/source_url/domain/description/retrieved_at/extractor
# 如果这一步失败，记录到 sources/failed/failed-sources.md，并暂停这篇文章
```

2. 用户在 NotebookLM Web 中手动创建文档

- Notebook 名称建议使用原文标题
- Source 优先添加原文 URL
- 如果 NotebookLM 无法读取 URL，则上传 `sources/orig/<slug>.md`
- 使用以下提示词生成摘要：

```text
请用中文生成这篇博客的技术摘要，重点包括：
1) 核心问题定义
2) 技术方案和架构
3) 训练数据和方法
4) 与同类方案的差异
5) 关键设计决策和 trade-off

保持技术深度，适合有 AI 工程背景的读者。
```

3. 用户将 NotebookLM 摘要保存到本仓库

- 将 NotebookLM 输出复制或导出为 markdown
- 保存为 `sources/nlm/<slug>.md`
- 文件名 `<slug>` 必须与 `sources/orig/<slug>.md`、最终博文 slug 保持一致
- 如果用户只提供了剪贴板文本或本地文件，先整理成 `sources/nlm/<slug>.md`

4. 基于双材料撰写中文博客文章

```bash
# 创建 content/posts/<slug>.md
# 按博客文章格式填写 frontmatter
# 结合 sources/orig/<slug>.md 和 sources/nlm/<slug>.md
# 中文整理摘要内容 + 个人思考 + 原文链接

# 预览
hugo server -D

# 确认 OK 后，从 inbox.md 移除对应条目

# 提交
git add content/posts/<slug>.md sources/ && git commit -m "add: 文章标题"
```

**注意事项：**
- 不再使用 `nlm` CLI；NotebookLM 相关动作全部由用户在 Web 端手动完成
- NotebookLM 生成的摘要可能是英文，不影响——作为原材料使用，最终博客文章写中文
- `sources/orig/<slug>.md` 是硬前置，拿不到就不要继续发布
- `sources/nlm/<slug>.md` 是推荐材料；没有它时，应先询问用户是否手动补充 NotebookLM 摘要，除非用户明确要求直接基于原文撰写
- `sources/orig/<slug>.md` 应包含 frontmatter metadata + 正文，避免归档文件失去来源信息
- `defuddle` 更适合标准文章页；对知乎、X、微信、视频页、重 JS 页面不要假设一定成功
- sources/ 目录存放所有中间文件，纳入 git 管理

### 批量处理流程（推荐）

按主题分批处理多篇文章时，按以下顺序操作：

```
步骤 1：批量生成原文归档（必选）
  → 对每篇文章执行 defuddle，保存到 sources/orig/<slug>.md
  → 成功的继续，失败的记录到 sources/failed/failed-sources.md，并暂停该文章

步骤 2：把待摘要清单交给用户手动创建 NotebookLM 文档
  → 列出每篇文章的标题、原文 URL、sources/orig/<slug>.md 路径
  → 用户在 NotebookLM Web 里手动创建 notebook/source/report
  → 用户将摘要复制或导出到 sources/nlm/<slug>.md

步骤 3：成功的文章直接走完整流程（不停顿）
  → 检查 sources/nlm/<slug>.md → 结合 sources/orig/<slug>.md 撰写博客文章

步骤 4：批次结束后，汇报失败项给用户
  → 展示 sources/failed/failed-sources.md 中的记录
  → 等待用户手动解决

步骤 5：用户回来后先补齐原文归档，再继续后续流程
  → 用户可能提供：替代 URL、复制粘贴的文本、本地文件
  → 目标是先生成或补齐 sources/orig/<slug>.md
  → 原文归档准备好后，等待用户手动创建或更新 NotebookLM 摘要
  → 用户提供摘要后，整理到 sources/nlm/<slug>.md
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

摘要 + 个人思考 + 原文链接
```

## 博客写作风格

后续技术博客默认采用 **博客解读** 风格，而不是纯摘要、纯资料卡片或提纲式笔记。

写作时遵循以下规则：

1. **开头先给判断**
   - 不要只写“解读某篇文章”。
   - 开头应先回答：这篇文章为什么值得读、它真正解决了什么问题、哪些读者应该关心它。

2. **围绕理解重组结构**
   - 不要机械跟随原文目录。
   - 正文优先按以下逻辑组织：
     - 问题是什么
     - 核心机制或方案是什么
     - 真正重要的 trade-off 是什么
     - 我的判断是什么

3. **保持文章感，而不是提纲感**
   - 尽量控制在 4-6 个真正有推进关系的小节。
   - 可以使用列表，但列表应服务于论点，而不是堆砌信息点。

4. **保留明确的个人结论**
   - 每篇文章至少有一个段落明显属于“我的看法”或“我的判断”。
   - 目标是把文章从“知识卡片”提升为“博客解读”。

5. **不牺牲技术密度**
   - 重写是为了提升理解速度和结构质量，不是为了变得更空泛。
   - 重要机制、术语、设计取舍、限制条件都应保留。

6. **统一收尾**
   - 文章结尾保留 `## 原文` 或 `## 延伸阅读`，方便回到源材料。

7. **改稿依据**
   - 修改或重写旧文时，优先同时参考：
     - `sources/orig/<slug>.md`
     - `sources/nlm/<slug>.md`
   - 如果 `sources/nlm/<slug>.md` 尚未由用户手动提供，先询问是否需要补充 NotebookLM 摘要；不要调用任何 NotebookLM CLI。
   - 不要只基于旧稿做表面润色。

---

## 待办事项

- [x] **商量 tag 列表** — 12 个 tag，粗细结合，详见上方 tag 体系表
- [x] **迁移摘要流程** — 不再使用 `nlm` CLI，改为用户手动创建 NotebookLM 摘要并保存到 `sources/nlm/`
- [ ] **处理第一批文章** — Next Edit 批次剩余 5 篇

---

## 相关文件

- 文章队列: `inbox.md`
- 原材料目录: `sources/`
- 博文目录: `content/posts/`
- 博客配置: `config.yaml`
