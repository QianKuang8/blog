---
date: '2026-06-05T21:30:00+08:00'
lastmod: '2026-06-05T21:30:00+08:00'
title: '5 个 Agent Skills：把经验变成可重复调用的流程'
summary: "解读 Matt Pocock 的 Agent Skills 实践：skills 的价值不是多写几段提示词，而是把设计澄清、PRD、任务拆分、TDD 和架构整理这些工程习惯固化成可重复工作流。"
description: "从 Matt Pocock 的 5 个日常 Agent Skills 看 AI 编程中的流程固化、TDD 和 agent-friendly 代码库"
tags: ["agent", "prompt-engineering", "博客推荐"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Matt Pocock 这篇 [5 Agent Skills I Use Every Day](https://www.aihero.dev/5-agent-skills-i-use-every-day) 的价值不在于列了 5 个技能，而在于它说明了一件很实用的事：当 AI 变成“随时可调度的一组工程师”时，流程比灵感更重要。

作者的判断很直接：这些工程师没有记忆，不会天然记住你过去怎么做事。于是你需要严格、清晰、可复用的流程，让它们每次都沿着相同路径工作。Skills 就是把这些流程编码下来的一种方式。

## 这 5 个 skills 其实覆盖了一个开发闭环

文章提到的 skills 包括 `/grill-me`、`/to-prd`、`/to-issues`、`/tdd` 和 `/improve-codebase-architecture`。单独看，它们像 5 个工具；放在一起看，其实是一条从想法到实现再到代码库整理的链路。

`/grill-me` 用来逼问方案，把设计树上的分支逐个走清楚。它的有趣之处在于，skill 不长，但触发的是一种行为模式：不要急着写，先把含糊处问穿。

`/to-prd` 把对话转成文档，解决“口头想法很快散掉”的问题。`/to-issues` 再把 PRD 拆成可以执行的任务，特别强调 vertical slices，也就是尽早暴露未知问题的小切片。`/tdd` 把实现过程约束到红绿重构。最后 `/improve-codebase-architecture` 处理更长期的问题：让代码库变得更适合 Agent 工作。

这条链路很接近成熟软件工程，只是载体变成了 skills。

## Skills 的价值在于降低反复指导成本

很多人写 prompt 时会把同样的话一遍遍复制给模型：先问清楚需求、不要直接实现、写测试、拆任务、注意架构。Skills 的意义是把这些“每次都要说”的流程收起来，变成可调用能力。

作者提到一个很重要的观点：如果代码库本身很糟，AI 只会在这个糟糕结构里继续生产糟糕代码。这个判断很现实。Agent 的输出高度依赖上下文质量，而代码库就是它最重要的上下文之一。

所以 architecture skill 不是为了抽象而抽象，而是为了提高 Agent 的工作条件：更清晰的边界、更少的泥球、更容易定位的责任、更适合测试和修改的结构。

## 好 skill 不一定长，但要卡在正确时机

文章里的 `/grill-me` 只有很短几句话，但作者说它非常有影响力。这说明 skill 的有效性不由长度决定，而由触发时机和行为约束决定。

一个好 skill 要能在模型最容易走偏的时候出现。比如模型想立刻实现时，grill-me 把它拉回设计澄清；模型要写代码时，tdd 把它拉回验证循环；模型面对大需求时，to-issues 把它拉回可执行切片。

我的理解是，skills 更像“流程断点”，不是知识库。它们把关键工程习惯插入 Agent 的工作路径。

## 我的判断：Skills 是轻量级 harness

这篇文章让我更倾向于把 skills 看作轻量级 harness。它不一定有复杂工具、评估器或外部状态机，但它把人类工程师的偏好、习惯和流程固定下来，让 Agent 不必每次重新从自然语言里猜。

当然，skill 也不是越多越好。真正值得写成 skill 的，是那些反复出现、容易走偏、又能通过固定流程明显改善结果的任务。一次性的口味偏好不一定值得沉淀，稳定的工程动作值得。

所以这篇文章适合当作一个起点：先不要追求庞大技能库，先找出你每天都在重复提醒 AI 的 3 到 5 件事，把它们写成可调用流程。

## 原文

- [5 Agent Skills I Use Every Day](https://www.aihero.dev/5-agent-skills-i-use-every-day)
