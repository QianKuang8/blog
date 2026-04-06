---
date: '2026-04-06T10:10:00+08:00'
lastmod: '2026-04-06T10:10:00+08:00'
title: 'Agent Engineering：一门新学科的诞生'
summary: "解读 LangChain 文章：为什么传统软件工程无法驯服非确定性 Agent 系统，Agent Engineering 作为融合产品思维、工程能力和数据科学的多学科方法，以及 Ship-to-Learn 迭代策略。"
description: "Agent Engineering 作为新学科的框架与方法论"
tags: ["agent"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

解读 LangChain 博客 [Agent Engineering: A New Discipline](https://blog.langchain.com/agent-engineering-a-new-discipline/)。

## 核心问题：生产环境的可靠性鸿沟

将 LLM Agent 从本地开发推向生产，暴露了传统软件工程的根本局限。传统工程基于确定性状态机，而 Agent 是概率推理引擎——用户行为开放式，系统响应随机。

### 传统工程手册为什么失败

1. **无限输入方差**：自然语言创造了无限状态空间的输入，数学上不可能映射每种用户流程
2. **随机偏差**：Agent 可能以预生产测试中不可见的方式偏离预期逻辑
3. **非线性推理路径**：标准部署检查清单无法覆盖多步推理和自主工具调用

### Agent ≠ 简单 LLM 应用

- **自然语言输入即通用边缘情况**：没有"标准输入"，每个交互都是独特的边缘情况
- **逻辑不可观测**：核心逻辑在模型推理中而非硬编码启发式里，传统断点调试无效。微调 prompt 可能引发巨大行为变化
- **非二元性能状态**：系统 99.99% 可用但功能可能已经"脱轨"——误用工具或逻辑不成立的结论，HTTP 状态码无法反映

## Agent Engineering 框架

Agent Engineering 是通过**构建、测试、发布、观察、改进**的持续生命周期来加固非确定性系统的迭代过程，融合三种核心技能：

| 技能 | 技术职责 |
|------|---------|
| **产品思维** | 设计 prompt 逻辑（可能涉及数千行）；映射"待完成任务"以复制人类判断；定义评估标准 |
| **工程能力** | 开发工具调用接口；构建流式和中断处理的 UI/UX；实现持久执行、HITL 暂停和记忆管理 |
| **数据科学** | 构建评估体系和监控框架；A/B 测试；对广泛使用模式和复杂非线性交互进行错误分析 |

## 基础设施需求

来自 Vanta、Cloudflare 等组织的生产实践总结：

1. **持久执行**：运行时必须在长时间多步任务中维护状态、可恢复
2. **Human-in-the-Loop**：架构必须支持异步暂停以验证高风险决策
3. **高级记忆管理**：跨碎片化交互持久化和检索上下文
4. **工具集成层**：LLM 与外部函数和服务的安全交互
5. **细粒度追踪**：捕获每个模型决策的完整上下文——不仅是日志错误，而是影响每个决策的**确切上下文**

## Workflow vs Agency

架构的本质是在确定性控制和自主能力之间找平衡：

- **Workflow**：确定性、预定义路径，开发者控制执行
- **Agency**：LLM 基于推理、上下文和工具可用性决定执行路径

## Ship-to-Learn 策略

这不是风格选择，而是技术必然。因为每个自然语言输入都是边缘情况，传统穷举预发布测试数学上不可能。必须"合理测试"后"发布学习"——生产数据成为回归测试的主要来源，真实世界的 trace 提供加固 prompt 和工具定义所需的边缘情况。

## 迭代改进循环

1. **Build**：确定 Workflow/Agency 比例
2. **Test**：捕获 prompt 级错误和工具定义逻辑缺陷
3. **Ship**：获取真实生产 trace，发现未预期的输入模式
4. **Observe**：追踪每个交互和工具调用，对生产数据运行评估
5. **Refine**：分析失败模式，修改 prompt 和工具定义，问题 case 回归测试套件

成功标准：能在**天而非季度**内发布逻辑改进。Clay（潜在客户研究、CRM 更新）和 LinkedIn（人才扫描排名）证明，将 Agent 视为迭代系统时能交付显著业务价值。

## 原文

- [Agent Engineering: A New Discipline | LangChain](https://blog.langchain.com/agent-engineering-a-new-discipline/)
