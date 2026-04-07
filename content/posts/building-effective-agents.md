---
date: '2026-04-05T18:00:00+08:00'
lastmod: '2026-04-07T22:43:56+08:00'
title: 'Building Effective Agents：Agent 系统的架构模式与设计原则'
summary: "解读 Anthropic 经典文章，梳理 Workflow 和 Agent 两大架构范式下的 7 种可组合模式：Prompt Chaining、Routing、Parallelization、Orchestrator-Workers、Evaluator-Optimizer、Autonomous Agent，以及 ACI 设计原则。"
description: "解读 Anthropic 的 Agent 架构模式与设计原则"
tags: ["agent"]
origStatus: "missing"
author: "Qian"
isCJKLanguage: true
showToc: true
---

解读 Anthropic 工程博客 [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)。

## 核心观点：从黑盒框架到可组合模式

文章的核心论点是：生产级 Agent 系统不应依赖高层抽象框架（它们引入"抽象泄漏"，掩盖 prompt 和状态管理），而应基于**简单、可组合、透明的基本构件**来构建。

许多团队在从实验转向生产时掉入"复杂性陷阱"——过度依赖 SDK/GUI，结果无法调试和优化。Anthropic 的建议是：**直接使用 LLM API，用几行代码实现这些模式**。

## 架构分类：Workflow vs Agent

| 维度 | Workflow | Agent |
|------|----------|-------|
| 控制流 | 预定义代码路径 | LLM 自主推理循环 |
| 可预测性 | 高，一致可重复 | 低，依赖模型决策 |
| 适用场景 | 步骤明确的任务 | 路径不可预测的开放问题 |

## 7 种可组合模式

### 1. Augmented LLM（基础单元）

一切 Agent 系统的基础——为 LLM 配备**检索、工具、记忆**能力。通过 Model Context Protocol (MCP) 实现工具的标准化解耦集成。

### 2. Prompt Chaining

将任务顺序分解为多个步骤，前一步输出作为后一步输入。用延迟换准确性，每个 LLM 调用的认知负荷更小，且可插入程序化验证门。

### 3. Routing

用分类将输入导向专门的下游处理。实现关注点分离和 token 预算优化——简单查询走 Haiku，复杂问题走 Sonnet。

### 4. Parallelization

- **分段**：同时运行独立子任务（如一个生成响应、一个同步做安全检查）
- **投票**：同一任务用不同 prompt 多次执行，聚合结果以提高置信度

### 5. Orchestrator-Workers

中心 LLM 做协调器，动态分解任务、分发给 worker、综合结果。适用于子任务数量和性质无法预知的场景（如跨大型仓库的多文件编辑）。

### 6. Evaluator-Optimizer

递归循环：一个 LLM 生成响应，另一个 LLM 评估反馈，迭代优化。适合有明确评估标准、可通过多轮改进提升质量的场景。

### 7. Autonomous Agent

LLM 维持规划循环，通过工具与环境交互并推理结果。与 Workflow 不同，Agent 运行在**环境驱动循环**中，需要"真实反馈"（如代码执行结果）来评估每步进展。这要求健壮的 Agent-Computer Interface (ACI)。

## ACI 设计：像 HCI 一样认真对待

文章强调 ACI 设计应获得与 HCI 同等的工程投入：

- **防错设计（Poka-yoke）**：工具参数设计应使 LLM 难以犯常见错误。例如要求绝对路径，因为模型在多步任务中常丢失根目录
- **Thinking Tokens**：给模型足够的 token 先"思考"再调用工具，避免把自己写进死角
- **最小化格式开销**：选择 LLM 易于生成的格式，避免需要精确行号计数的 diff 格式
- **完善文档**：为工具提供清晰的 docstring、示例用法和参数边界，像对待初级开发者一样

## 三大设计权衡

1. **性能 vs 延迟/成本**：多轮推理性能更高，但 token 用量和响应时间显著增加
2. **灵活性 vs 确定性**：自主 Agent 最灵活，但有**错误累积**风险——早期失误会级联导致系统失败。任务路径明确时应优先使用 Workflow
3. **Human-in-the-loop**：高风险场景必须设置人工检查点，不仅为安全，也为确保方案符合组织标准

## 生产级 Agent 三原则

1. **简洁性**：保持最简设计，只在简单方案评估失败时才增加复杂度
2. **透明性**：显式记录和暴露 Agent 的规划步骤和工具交互
3. **严谨的工具文档**：将 ACI 视为一等公民，配合完善的文档和沙盒测试

## 原文

- [Building effective agents | Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
