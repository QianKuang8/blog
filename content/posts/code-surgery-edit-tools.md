---
date: '2026-04-05T15:30:00+08:00'
lastmod: '2026-04-05T15:30:00+08:00'
title: 'Code Surgery：AI 编辑代码的五种工程架构'
summary: "综述 Codex、Aider、OpenHands、RooCode、Cursor 五个工具的代码编辑架构，对比 Patch、Diff、Search/Replace、Line Operations、AI-Assisted Apply 五种编辑格式。"
description: "综述 AI 编辑代码的五种工程架构和编辑格式对比"
tags: ["code-editing"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

解读 Fabian Hertwig 博客 [Code Surgery](https://fabianhertwig.com/blog/coding-assistants-file-edits/) 的技术方案。

## 核心挑战："交接"问题

LLM 没有文件系统访问权限，必须通过工具/API 进行**间接状态操作**。这创造了一个高风险的"交接"——LLM 内部的代码表示必须映射到实际文件状态。失败通常因为 LLM 基于**过时或不完整的文件视图**操作。

四大工程挑战：
- **定位目标**：找到精确的插入/修改点，尤其文件状态已偏离 LLM 上次快照时
- **跨文件变更**：跨多文件编排原子更新
- **风格维护**：保持缩进、行尾、空格约定
- **失败管理**：通过诊断反馈构建健壮的恢复循环

## 五种编辑格式

| 格式 | 机制 | 使用工具 |
|------|------|---------|
| **Patch** | 用上下文行锚定而非脆弱行号 | Codex, Aider |
| **Diff** | 逐行差异（Unified Diff） | Aider, OpenHands |
| **Search/Replace** | 用分隔符标识搜索和替换块 | Aider, RooCode |
| **Line Operations** | 基于精确行号指定编辑 | OpenHands |
| **AI-Assisted Apply** | 用专门的 "Apply" 模型解释 sketch 并执行集成 | Cursor, OpenHands |

## 五个工具的架构对比

### Codex：上下文锚定 Patch

- 用 `@@` 标记基于函数/类定义定位编辑区域
- 依赖空格前缀的上下文行精确定位
- **渐进式匹配策略**：精确匹配 → 忽略行尾差异 → 忽略空白差异
- 失败反馈用结构化 JSON（期望行 vs 实际行）

### Aider：可插拔多格式架构

- 模块化 "coder" 类设计，可按 LLM 能力切换 EditBlock / Unified Diff 格式
- **分层搜索**：精确 → 忽略空白 → 保持缩进 → **模糊匹配**（用 `difflib` 计算相似度）
- 失败反馈用自然语言指令，建议正确目标并只要求重发失败块（省 token）

### OpenHands：混合传统/Draft-Editor

- 正则检测处理标准 patch 格式
- 可选 "draft editor" 模式：用专门 system prompt 指示辅助 LLM 重写指定行范围
- 显式要求处理占位注释（如 `# no changes needed before this line`），替换为原始未变代码

### RooCode：Middle-Out 模糊匹配

- 从估计行位置开始向外扩展搜索
- 用 **Levenshtein 距离**评分相似度
- **缩进保持**：捕获原始前导空白，执行相对缩进映射

### Cursor：专用 Apply 模型

- 两步 "Sketching vs Applying" 架构
- 理由：通用推理模型擅长逻辑但常在**机械语法应用**上出错
- 将集成工作卸载给自定义训练的 Apply 模型，处理结构细微差别

## 工程原则总结

1. **分层匹配**：从严格上下文要求开始，逐级降级到模糊策略
2. **缩进完整性**：必须捕获原始空白并应用相对缩进映射
3. **可操作反馈**：提供诊断数据（实际行 vs 期望行），而非简单报 "Failure"
4. **格式标准化**：避免行号，用清晰的 SEARCH/REPLACE 或 BEFORE/AFTER 分隔符

## 三大设计权衡

- **行号 vs 符号上下文**：行号脆弱（外部变更导致偏移），符号上下文更鲁棒
- **严格 vs 模糊匹配**：严格确定性强但失败率高，模糊成功率高但有误匹配风险
- **通用推理 vs 专用模型**：单模型简单但遇"语法天花板"，双模型（Apply 模型）将代码集成视为独立的机械任务

## 原文

- [Code Surgery: How AI Assistants Make Precise Edits to Your Files](https://fabianhertwig.com/blog/coding-assistants-file-edits/)
