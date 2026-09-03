---
date: '2026-06-05T21:30:00+08:00'
lastmod: '2026-06-05T21:30:00+08:00'
title: 'Claude Auto-Caching：把共享上下文从成本中心变成复用资产'
summary: "解读 Lance Martin 关于 Claude prompt auto-caching 的说明：缓存的价值不只是省钱，而是让无状态 API 下的 Agent 循环可以反复复用稳定上下文。"
description: "从 Claude prompt auto-caching 看 prefill 复用、cache_control、cached token 成本和 agent loop 的上下文结构"
tags: ["context-engineering", "agent", "harness-engineering"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Lance Martin 这篇 [Prompt auto-caching with Claude](https://x.com/RLanceMartin/status/2024573404888911886) 可以和 Claude Code 的 prompt caching 经验一起看。前者解释机制，后者展示在真实 coding agent 里的系统后果。

文章的核心很直接：很多 AI 应用，尤其是 Agent，每一轮都会带上大量相同上下文。Claude Messages API 是无状态的，不会自动记住过去动作，所以 harness 必须把历史动作、工具说明、通用指令和新上下文重新打包。没有缓存时，每一轮都要为几乎相同的上下文付完整成本。

Prompt caching 的价值就在这里：相同前缀的 prefill 计算可以复用。文章提到 cached input tokens 的价格是非缓存 token 的 10%，这让缓存不仅影响延迟，也直接影响产品成本。

## Agent 循环天然适合缓存

Agent 的工作方式是循环：观察环境、选择动作、调用工具、拿到新结果，再进入下一轮。每一轮新增的信息其实只占上下文的一小部分，大量内容是稳定的：系统指令、工具定义、已有历史、项目规则。

如果这些内容每轮都重新 prefill，成本会随着上下文膨胀迅速放大。缓存把这些稳定内容变成可复用资产。我的理解是，这也是为什么 Manus、Claude Code 这类长轨迹产品都会强调 cache hit rate：它不是锦上添花，而是决定 agent loop 是否经济可行。

## Auto-caching 降低了使用门槛

文章提到 Claude API 增加了 auto-caching，让开发者更容易通过一个 `cache_control` 参数缓存 prompt。它不要求开发者自己实现底层 KV cache，而是把“哪些内容值得作为可复用块”暴露成 API 层能力。

但这并不意味着开发者可以不管上下文结构。缓存仍然依赖相同内容的复用，尤其是前缀稳定性。你仍然需要思考哪些信息应该稳定放置，哪些信息应该作为动态消息追加，哪些内容不该每轮扰动。

换句话说，auto-caching 降低的是接入复杂度，不是架构思考成本。

## 缓存让 context engineering 更像系统设计

这篇文章最值得带走的不是“加 cache_control 可以省钱”，而是它让 context engineering 变成更具体的系统设计问题。

你要决定上下文如何分层：全局系统指令、工具定义、项目级记忆、会话历史、当前工具结果。你还要决定哪些层稳定、哪些层可变、哪些变化应该通过消息增量表达。最后还要用指标验证 cache hit rate，而不是只靠感觉。

这和传统软件里的缓存设计有相似之处：缓存命中率、失效策略、数据布局都会影响系统行为。不同的是，这里缓存的不是数据库查询结果，而是模型对上下文前缀的计算。

## 我的判断：缓存是 Agent 规模化的经济边界

很多 Agent 讨论会聚焦能力：模型能不能规划，工具能不能用，任务能不能跑很久。但只要进入产品化，经济边界同样重要。一个每轮都烧完整上下文的 Agent，即使能力不错，也很难支撑真实高频使用。

Prompt auto-caching 的意义，是让“长上下文 + 多轮工具调用”从实验室体验走向可运营系统。但它也要求开发者认真对待 prompt 布局。上下文不是随便拼出来的文本，而是有复用结构、成本结构和失效风险的运行时资产。

## 原文

- [Prompt auto-caching with Claude](https://x.com/RLanceMartin/status/2024573404888911886)
