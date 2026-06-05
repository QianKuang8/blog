---
date: '2026-06-05T21:28:00+08:00'
lastmod: '2026-06-05T21:28:00+08:00'
title: 'Agentic Coding 的边界：瓶颈会转移到 Review 和隐性知识'
summary: "解读 tisonkun 关于 Agentic Coding 边界的文章：AI 能生成 plausible code，但高质量软件仍受限于复杂度控制、可量化回归指标、Review 带宽和隐性知识供给。"
description: "从 Agentic Coding 的边界看 AI 生成代码、软件工程实践、测试、review、隐性知识和高质量软件生产"
tags: ["agentic-coding", "agent", "harness-engineering"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

tisonkun 这篇 [Agentic Coding 的边界](https://mp.weixin.qq.com/s/x_FUUG4wBUqYs1H5DUtpgQ) 很值得读，因为它没有停留在“AI 会不会取代程序员”的口号，而是具体讨论 Agentic Coding 在高质量软件生产里会撞到哪些边界。

文章开头的判断很清楚：以目前 LLM 能力，生成疑似正确的方案、流程或代码完全可以做到；但从 plausible prototype 到经得起考验的产品，中间仍然有 AI 不能自动覆盖的鸿沟。

## 现有代码质量会反过来训练 Agent 的坏习惯

文章说“大部分现有代码都是 Big Ball of Mud”。这句话刺耳，但对 Agentic Coding 很关键。模型从大量历史代码和文本中学习，而现实里的代码本来就有很多就地补丁、过度复用、选项膨胀和复杂 if-else。

所以 AI 很容易生成“看起来能跑”的短平快代码。解决办法不是让 AI 更努力，而是用软件工程实践降低复杂度，提高上下文信息密度。文章提到领域设计语言、限界上下文、活文档等实践，都是在给 Agent 提供更清晰的工作环境。

## 最大瓶颈之一是可量化回归指标不足

文章把 Agentic Coding 和 AI 下围棋做对比。围棋有清晰终局目标和可回归信号，而现实软件需求大部分没有这么可靠的指标。测试能覆盖一部分，但很多用户体验、架构质量、隐性约束很难自动度量。

这点我非常认同。Agentic Coding 真正要大规模提升生产力，需要更好的工程回归指标。否则 AI 生成越快，Review 压力越大。因为“看起来像对的”代码可能最危险。

## 隐性知识仍然需要真人提供

文章还强调隐性知识。很多高质量决策来自人对业务、生态、库、论文、历史坑的组合记忆。这些知识未必在语料库里，也未必能被搜索到。

这说明高质量 Agentic Coding 的上限，不只取决于模型能力，还取决于人能不能把隐性知识转成 spec、skill、示例、测试和约束。人不写每一行代码，不代表人不提供关键上下文。

## 我的判断：Agentic Coding 的核心工作会变成设计和审查

这篇文章让我更克制地看 Agentic Coding。它确实能提高原型速度、探索速度和重复实现速度，但高质量软件的主要成本本来就不全在打字，而在需求澄清、边界判断、设计取舍、测试设计、代码审查和长期维护。

AI 会把“写代码”的成本压低，但会把瓶颈推向 Review 带宽和上下文质量。谁能更好地提供隐性知识、构造可验证目标、维护低复杂度代码库，谁就更能吃到 Agentic Coding 的收益。

所以 Agentic Coding 的边界不是“AI 会不会写代码”，而是“我们有没有足够好的工程系统来判断它写得对不对”。

## 原文

- [Agentic Coding 的边界](https://mp.weixin.qq.com/s/x_FUUG4wBUqYs1H5DUtpgQ)
