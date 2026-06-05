---
date: '2026-06-05T21:28:00+08:00'
lastmod: '2026-06-05T21:28:00+08:00'
title: 'Harrison Chase 谈长程 Agent：核心仍是上下文和 Harness'
summary: "解读 Harrison Chase 关于 long-horizon agents 的访谈：长程 Agent 开始可用，不只是模型变强，而是 planning、compaction、file system、traces 和人类评估共同构成了更成熟的 harness。"
description: "从 LangChain Harrison Chase 访谈看 long-horizon agents、context engineering、agent harness、traces 和 memory"
tags: ["agent", "context-engineering", "harness-engineering"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

这期 [Harrison Chase 访谈](https://www.youtube.com/watch?v=vtugjs2chdA) 很适合放在 context engineering 主题下看。Harrison 的核心判断是：long-horizon agents 终于开始可用了，但原因不是单一的模型突破，而是模型能力、harness 工程、上下文压缩、规划工具和文件系统环境一起成熟。

访谈一开始就点到 context engineering 的关键：单次 LLM 调用里，prompt 和上下文由代码决定；Agent 跑到第 14 步时，前 13 步可能已经拉进了任意信息，你并不知道那一刻上下文里到底有什么。Traces 的价值就在这里，它让你看见 Agent 运行过程中上下文如何变化。

## 长程 Agent 最适合先产出 first draft

Harrison 对 long-horizon agent 的适用场景判断很务实。他认为当前最好的形态，是让 Agent 长时间运行，产出某种 first draft，再交给人审查。Coding 是典型例子：Agent 提 PR，人再 review。研究、AI SRE、报告生成、客服升级前的背景整理，也都符合这个模式。

这个判断很重要，因为它避开了“完全自治”的幻觉。当前 Agent 还很难达到 99% 可靠性，但它们可以做大量探索性、整理性、草稿性工作。只要产品流程允许人类在关键点介入，长程 Agent 就已经有明显价值。

## Harness 和模型在共同演化

访谈里对 model、framework、harness 的区分也很有用。模型是 messages in / messages out；framework 提供工具、模型切换、memory 等抽象；harness 更 opinionated，会内置 planning tool、compaction、文件系统工具等具体工作方式。

Harrison 特别提到 context window 变大但不是无限，所以长程 Agent 必须考虑 compaction。文件系统工具也变得重要，因为它们给 Agent 提供了外部状态和可操作环境。我的理解是，file-system-based harness 并不是偶然流行，而是模型训练、开发者工作流和长上下文管理共同选择出来的形态。

## Traces 会成为改进 Agent 的反馈资产

访谈后半谈到 human judgment、LLM-as-judge、LangSmith traces 和 memory。Agent 做很多类人判断任务，不能只靠程序断言评估，因此需要人类标注 trace，也需要校准过的 LLM judge 作为代理评价器。

更有意思的是让 coding agent 拉取 traces、诊断哪里错了，然后把修复带回代码库。Harrison 甚至提到 Agent 可以根据交互反馈修改自己的 instruction 文件。这是很典型的 evolve context：把运行轨迹变成下一轮改进的输入。

## 我的判断：长程 Agent 的 UI 会围绕异步管理和状态查看展开

访谈里关于 UI 的部分也很值得记。长程 Agent 默认会异步运行，人不会坐着等一天。但当它产出结果或需要纠正时，又需要切回同步沟通。用户还需要查看它操作的 state，比如目录、文件、报告、任务板。

所以长程 Agent 的交互不太像纯聊天，更像“异步任务队列 + 同步协作界面 + 状态浏览器”。这和 coding agent 当前的形态已经很接近：后台跑任务，完成后看 diff、看测试、进入对话修正。

如果要总结这期访谈，我会说：long-horizon agent 的关键不是让模型一直想，而是给它一个能长时间工作、能被观察、能被纠正、能沉淀经验的环境。

## 原文

- [Context Engineering Our Way to Long-Horizon Agents: LangChain's Harrison Chase](https://www.youtube.com/watch?v=vtugjs2chdA)
