# 博客发布流程

> 生成时间：2026-03-20，更新：2026-04-07

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
| **摘要生成** | `nlm` 报告 + `sources/orig/<slug>.md` 双材料 | 优先 `nlm --url`，失败时回退 `--file sources/orig/<slug>.md` |
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
│   │   └── <slug>.md     # nlm 生成的摘要报告
│   └── failed/
│       └── failed-sources.md # 失败记录
├── content/posts/        # 已发布博文
└── WORKFLOW.md           # 本文档
```

**命名约定：**
- `sources/orig/<slug>.md` 存放原文归档，`sources/nlm/<slug>.md` 存放摘要报告
- slug 与最终博文 slug 保持一致，便于查找对应关系
- 功能性文件集中在 `sources/failed/`（如 `sources/failed/failed-sources.md`）

---

## 工作流

```
1. 收集
   看到好文章 → 记录到 inbox.md（标题 + 链接）

2. 批量处理（按主题分批）
   ├─ 2a. 生成并保存 sources/orig/<slug>.md（defuddle，必选）
   ├─ 2b. 创建 nlm source（优先 --url，失败时回退 --file sources/orig/<slug>.md）
   ├─ 2c. 生成摘要（nlm CLI）
   ├─ 2d. 下载摘要到 sources/nlm/<slug>.md
   ├─ 2e. 确认 tags
   └─ 2f. 撰写博客文章（结合原文归档 + nlm report）

3. 发布
   ├─ 创建 content/posts/<slug>.md
   ├─ hugo server -D 预览
   └─ git commit & push

4. 清理
   ├─ 从 inbox.md 移除已发布的条目
   └─ 删除 nlm notebook
```

### 单篇文章处理流程（nlm CLI）

```bash
# 1. 先生成原文归档（必选）
defuddle parse "https://..." --md -o sources/orig/<slug>.md
# 如果这一步失败，记录到 sources/failed/failed-sources.md，并暂停这篇文章

# 2. 创建 notebook（以文章标题命名）
nlm notebook create "文章标题"
# 记下返回的 notebook ID

# 3. 优先添加源文章 URL
nlm source add <notebook-id> --url "https://..."

# 4. 如果 URL 读取失败，回退为上传原文归档
nlm source add <notebook-id> --file sources/orig/<slug>.md

# 5. 生成摘要报告
nlm report create <notebook-id> \
  --format "Create Your Own" \
  --prompt "请用中文生成这篇博客的技术摘要，重点包括：1) 核心问题定义 2) 技术方案和架构 3) 训练数据和方法 4) 与同类方案的差异 5) 关键设计决策和 trade-off。保持技术深度，适合有 AI 工程背景的读者。" \
  --confirm

# 6. 查看生成状态（等待 status 变为 completed）
nlm studio status <notebook-id>

# 7. 下载摘要
nlm download report <notebook-id> --output sources/nlm/<slug>.md

# 8. 基于双材料撰写中文博客文章（手动/Claude 协助）
#    - 创建 content/posts/<slug>.md
#    - 按博客文章格式填写 frontmatter
#    - 结合 sources/orig/<slug>.md 和 sources/nlm/<slug>.md
#    - 中文整理摘要内容 + 个人思考 + 原文链接

# 9. 预览
hugo server -D

# 10. 确认 OK 后，从 inbox.md 移除对应条目

# 11. 清理 nlm notebook
nlm notebook delete <notebook-id> --confirm

# 12. 提交
git add content/posts/<slug>.md sources/ && git commit -m "add: 文章标题"
```

**注意事项：**
- nlm 生成的报告可能是英文，不影响——作为原材料使用，最终博客文章写中文
- `sources/orig/<slug>.md` 是硬前置，拿不到就不要继续发布
- `defuddle` 更适合标准文章页；对知乎、X、微信、视频页、重 JS 页面不要假设一定成功
- nlm session 约 20 分钟过期，长时间操作前先 `nlm login --check`
- sources/ 目录存放所有中间文件，纳入 git 管理

### 批量处理流程（推荐）

按主题分批处理多篇文章时，按以下顺序操作：

```
步骤 1：批量生成原文归档（必选）
  → 对每篇文章执行 defuddle，保存到 sources/orig/<slug>.md
  → 成功的继续，失败的记录到 sources/failed/failed-sources.md，并暂停该文章

步骤 2：对已有 sources/orig/<slug>.md 的文章创建 notebook + 添加 source
  → 先尝试 nlm source add <nb-id> --url "..."
  → 如果 URL 失败，再回退为 nlm source add <nb-id> --file sources/orig/<slug>.md

步骤 3：成功的文章直接走完整流程（不停顿）
  → 生成摘要 → 下载到 sources/nlm/<slug>.md → 结合 sources/orig/<slug>.md 撰写博客文章 → 清理

步骤 4：批次结束后，汇报失败项给用户
  → 展示 sources/failed/failed-sources.md 中的记录
  → 等待用户手动解决

步骤 5：用户回来后先补齐原文归档，再继续后续流程
  → 用户可能提供：替代 URL、复制粘贴的文本、本地文件
  → 目标是先生成或补齐 sources/orig/<slug>.md
  → 原文归档准备好后，再根据情况使用：
    - nlm source add <nb-id> --url "新URL"
    - nlm source add <nb-id> --file sources/orig/<slug>.md
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

| URL | 失败原因 | Notebook ID | 状态 |
|-----|---------|-------------|------|
| https://... | 无法访问 | xxx | 待处理 |
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

---

## 待办事项

- [x] **商量 tag 列表** — 12 个 tag，粗细结合，详见上方 tag 体系表
- [x] **验证 nlm CLI 摘要流程** — Zed Edit Prediction 已跑通，流程见上方
- [ ] **处理第一批文章** — Next Edit 批次剩余 5 篇

---

## 相关文件

- 文章队列: `inbox.md`
- 原材料目录: `sources/`
- 博文目录: `content/posts/`
- 博客配置: `config.yaml`
