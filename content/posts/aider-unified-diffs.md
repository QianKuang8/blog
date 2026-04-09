---
date: '2026-04-05T14:30:00+08:00'
lastmod: '2026-04-09T20:11:36+08:00'
title: 'Aider：用 Unified Diff 格式解决 LLM 的"懒惰编码"问题'
summary: "解读 Aider 如何通过 Unified Diff 编辑格式将 GPT-4 Turbo 的编辑成功率从 20% 提升到 61%，懒惰输出减少 3 倍。"
description: "解读 Aider Unified Diff 编辑格式解决 LLM 懒惰编码的技术方案"
tags: ["code-editing", "apply"]
origStatus: "available"
author: "Qian"
isCJKLanguage: true
showToc: true
---

解读 Aider 博客 [Unified diffs make GPT-4 Turbo 3X less lazy](https://aider.chat/2023/12/21/unified-diffs.html) 的技术方案。

## 问题：GPT-4 Turbo 的"懒惰编码"

GPT-4 Turbo (gpt-4-1106-preview) 引入了一个严重问题：模型用 `... add logic here ...` 或 `... include original method body ...` 等占位符省略代码。

在传统的 SEARCH/REPLACE 块格式下，GPT-4 Turbo 复杂任务成功率仅 **20%**，其中 13.5% 用懒惰注释替代实际代码。

## 方案：Unified Diff 编辑格式

从块替换转向修改版的 **Unified Diff** 格式，利用 LLM 在 `git diff` 输出上的大量预训练，同时针对机器消费优化：

- **省略行号**：传统 hunk header（`@@ -2,4 +3,5 @@`）被去掉。定量分析证实 LLM 无法可靠维护行号的数学计算
- **搜索替换语义**：每个 hunk 被当作搜索替换操作——用 ` `（空格）表示上下文，`-` 表示删除，`+` 表示添加

### 粒度选择：高层 > 外科手术式

```
外科手术式（不推荐）：
- n = 5
+ number = 5

高层上下文（推荐）：
  def factorial(n):
-    if n == 0:
-        return 1
-    return n * factorial(n-1)
+    if number == 0:
+        return 1
+    return number * factorial(number-1)
```

高层 diff 提供唯一签名防止"碰撞"（小片段误匹配无关代码段），同时避免 LLM 因交错过多旧行和新行而混乱。

## 评估基准

标准基准如 Exercism（133 题）太简单，无法量化懒惰问题。Aider 构建了自定义基准：

- 用 Python `ast` 模块分析 9 个开源仓库，提取 89 个重构任务
- 目标：类中的方法重构为独立函数，方法 100-250+ AST 节点，周围类至少是方法的 2 倍大
- 验证：AST 节点数量对齐（无省略）、结构完整性、`...` 懒惰检测

## 对比结果

| 方案 | GPT-4 Turbo 成功率 | GPT-4 (June) 成功率 |
|------|-------------------|-------------------|
| **Unified Diff（无行号）** | **61%** | **59%** |
| SEARCH/REPLACE（基线） | 20% | 26% |
| 情感诉求 | < 20% | N/A |
| 结构化 JSON / Tool Calling | 低 | N/A |
| 基于行号的格式 | 低 | N/A |

关键发现：
- **模型无关性**：GPT-4 June 版从 26% 提升到 59%（上限 72%，因 28% 文件超出 8k 上下文窗口）
- **JSON 转义之痛**：JSON 格式包裹源代码容易导致转义错误
- **情感诉求无效**："用户是盲人""我会给 $2000 小费"这类提示全部不如结构化格式改进

## Flexible Patching：抗脆弱层

LLM 输出本质上不稳定——常忘记 docstring、遗漏空行、错误缩进、忘记 `+` 前缀。Aider 的补丁引擎包含多层恢复策略：

1. **Hunk 归一化**：对 LLM 提议的变更重新 diff，修复内部不一致
2. **相对前导空白**：即使 LLM 错误偏移缩进也能匹配
3. **Hunk 分片**：将失败的大 hunk 拆分为小子 hunk 部分应用

**关键数据**：在 Exercism 基准上，禁用 flexible patching 导致编辑错误 **9 倍增长**。

## 原文

- [Unified diffs make GPT-4 Turbo 3X less lazy](https://aider.chat/2023/12/21/unified-diffs.html)
