---
date: '2026-06-05T21:28:00+08:00'
lastmod: '2026-06-05T21:28:00+08:00'
title: 'Harness Engineering 和 SDD 不是竞争关系'
summary: "解读《Harness Engineering 来了，SDD 还有意义吗？》：Harness 是让 Agent 可靠工作的支撑结构，而 Spec 是支撑结构里最关键的语义资产，两者不是替代关系。"
description: "从 Harness Engineering 与 Spec-Driven Development 的关系看 AI Coding 中的 spec、scaffolding、反馈回路和工程记忆"
tags: ["harness-engineering", "agentic-coding", "context-engineering"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

这篇 [Harness Engineering 来了，SDD 还有意义吗？](https://mp.weixin.qq.com/s/Laz4W0180y9yGW0b6EpUMQ) 回答了一个很实际的问题：如果 Agent harness 越来越强，我们还需要花力气写 spec、做规范驱动开发吗？

作者的结论很明确：Harness Engineering 和 SDD 不是竞争关系，而是同一件事的两个层面。Harness 是放大器，Spec 是被放大的内容。我的理解也是这样。

## Harness 解决的是 Agent 工作环境

文章引用 Mitchell Hashimoto 对 harness 的定义：每当 Agent 犯错，就工程化一个解决方案，让它不再犯同样错误。具体做法可能是 AGENTS.md、工具脚本、截图工具、测试过滤器、结构化 docs、执行计划、架构约束、反馈回路。

这说明 harness 不是一个单独工具，而是一套让 Agent 可靠工作的环境。它包括上下文、工具、规则、验证和反馈。

## Spec 解决的是语义基础

文章最关键的判断是：Spec 是 scaffolding 的核心内容之一。Agent 需要地图，不需要一开始被 1000 页说明书淹没。好的 spec 给出意图、契约、边界和下一步该查哪里。

这和 context engineering 很接近。Spec 不是静态文档，而是 Agent 可读取的语义资产。它决定 Agent 在面对任务时如何理解目标、如何判断是否偏离、如何接受反馈。

## Harness 越强，Spec 越重要

很多人会反过来想：既然 harness 越来越强，是不是 spec 可以少写？文章的观点相反：执行能力越强，错误执行的放大效应也越强。如果 spec 模糊，强 harness 只会更快地产生偏差。

我的理解是，模型和工具越强，人类越需要把注意力放在高层语义和验收标准上。以前人写代码时，很多隐含判断在脑子里；现在 Agent 执行时，这些隐含判断必须变成可发现、可引用、可维护的工程记忆。

## 我的判断：SDD 的目标不是多写文档，而是减少返工

这篇文章最值得带走的是，不要把 SDD 理解成文档崇拜。Spec 的价值不在“写得多”，而在让 Agent 读到正确意图，减少走错路后的返工。

好的 spec 应该是渐进式的、模块化的、能被测试和反馈连接起来的。它不应该变成大而全的 AGENTS.md，也不应该把实现细节全部写死。真正有效的是一张可导航地图：当前任务要看哪些约束，哪些规则会被执行，哪些测试证明完成。

所以 Harness Engineering 到来并没有削弱 SDD，反而让 SDD 的质量更关键。Agent 负责执行，人负责设计环境和语义边界。

## 原文

- [Harness Engineering 来了，SDD 还有意义吗？](https://mp.weixin.qq.com/s/Laz4W0180y9yGW0b6EpUMQ)
