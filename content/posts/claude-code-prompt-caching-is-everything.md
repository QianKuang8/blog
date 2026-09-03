---
date: '2026-06-05T21:30:00+08:00'
lastmod: '2026-06-05T21:30:00+08:00'
title: 'Prompt Caching 是 Claude Code Harness 的隐形地基'
summary: "解读 Claude Code 团队关于 prompt caching 的经验：缓存不是成本优化小技巧，而是决定长轨迹 Agent 能不能低延迟、低成本运行的系统约束。"
description: "从 Claude Code 的 prompt caching 实践看静态前缀、工具稳定性、上下文分叉和 cache hit rate 运维"
tags: ["agentic-coding", "context-engineering", "harness-engineering"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Claude Code 团队这篇 [Prompt Caching Is Everything](https://x.com/trq212/status/2024574133011673516) 很短，但信息密度很高。它真正想说的是：对于长时间运行、上下文很重的 coding agent，prompt caching 不是“省钱优化”，而是产品形态能不能成立的基础条件。

文章说 Claude Code 的整个 harness 都围绕 prompt caching 构建。高 cache hit rate 能降低成本和延迟，也能支撑更宽松的订阅用量；团队甚至会对 cache hit rate 设告警，太低时按事故处理。这个细节很重要，因为它把 caching 从工程技巧提升到了运行指标。

## 缓存的核心约束是 prefix matching

文章最关键的机制是 prefix matching。API 会从请求开头开始缓存，直到 cache control breakpoint。也就是说，越靠前的内容越需要稳定；一旦前缀中间变化，后面的缓存都会受影响。

Claude Code 的顺序是：静态 system prompt 和 tools 放最前，全局缓存；Claude.md 在项目内缓存；session context 在会话内缓存；conversation messages 放最后。这个顺序的原则很清楚：共享范围越大的内容越靠前，变化越频繁的内容越靠后。

听起来简单，但文章提醒这件事非常脆弱。比如把精确时间戳放进静态 system prompt、非确定性地打乱 tool order、在会话中更新工具参数，都可能破坏缓存。我的理解是，prompt 在这里已经不是一段文本，而是一种需要稳定布局的数据结构。

## 状态变化不要随便改 system prompt

文章另一个有用建议是：用 messages 表达更新，而不是修改 prompt 本体。比如时间变化、用户文件变化、进入某种模式，都可能让人想改 system prompt。但这会导致 cache miss，成本可能很高。

同理，不要在会话中途换模型，不要随意增删工具。Plan Mode 的例子尤其有意思：不要因为进入 plan mode 就换一套工具，而是把 plan mode 建模成工具状态转换。Tool Search 也是类似思路：不要把所有工具塞进上下文，也不要中途删工具，而是通过延迟加载让工具暴露更稳定。

这说明 prompt caching 会反过来塑造产品架构。你不能只问“怎样让模型知道当前模式”，还要问“这种模式表达会不会破坏稳定前缀”。

## 分叉上下文也要 cache-safe

长会话里经常需要 side computation，比如 compaction、summarization、skill execution。文章提到 fork 操作要共享父会话前缀，使用相同的 cache-safe 参数，这样才能命中父上下文缓存。

这个点很容易被低估。很多人把 compaction 当成单独任务，但如果它每次都以不同工具、不同模型、不同 system prompt 发起，成本会非常高。对长轨迹 Agent 来说，旁路任务也必须服从缓存布局。

## 我的判断：缓存约束会进入 Agent 架构设计

我读完最大的感受是，prompt caching 不是最后才加的优化，而是从第一天就会影响 harness 设计。工具顺序、模式切换、上下文分层、fork 参数、项目记忆位置，都会因为缓存约束而改变。

这也解释了为什么成熟 coding agent 看起来有很多奇怪的产品细节：为什么一些状态用消息表达，为什么工具列表不轻易变化，为什么 Claude.md 这种项目记忆有固定位置。这些不只是 UX 或 prompt 风格问题，而是成本、延迟和上下文工程共同作用的结果。

所以如果要做长时间运行的 Agent，我会把 cache hit rate 当成和测试通过率、任务完成率同级的指标。它不直接代表智能，但它决定了智能能不能以可承受的成本持续运行。

## 原文

- [Lessons from Building Claude Code: Prompt Caching Is Everything](https://x.com/trq212/status/2024574133011673516)
