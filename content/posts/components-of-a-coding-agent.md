---
date: '2026-06-05T21:30:00+08:00'
lastmod: '2026-06-05T21:30:00+08:00'
title: 'Coding Agent 的六个组件：模型之外的系统才是关键'
summary: "解读 Sebastian Raschka 的 coding agent 组件文章：Claude Code、Codex 这类工具的能力不只来自模型，而来自 repo context、prompt shape、工具、上下文压缩、session memory 和 bounded subagents 的组合。"
description: "从 Components of A Coding Agent 看 coding harness 的上下文、工具、记忆、缓存和子代理设计"
tags: ["agentic-coding", "agent", "context-engineering"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Sebastian Raschka 这篇 [Components of A Coding Agent](https://magazine.sebastianraschka.com/p/components-of-a-coding-agent) 适合当作 coding agent 的系统导览。它最重要的价值，是把 Claude Code、Codex CLI 这类工具从“模型很强”这个模糊说法里拆出来，说明真正让它们变强的是周围的 harness。

文章先区分 LLM、reasoning model、agent 和 harness。LLM 是核心模型，reasoning model 是更愿意花推理计算的模型，agent 是反复调用模型并在环境中行动的循环，harness 则是管理上下文、工具、prompt、状态和控制流的软件支架。Coding harness 是这个概念在软件工程里的特例。

## 模型只是引擎，harness 才是驾驶系统

文章里有个判断很重要：coding 工作不只是 next-token generation。真实编码需要 repo navigation、搜索、函数查找、diff 应用、测试执行、错误检查和上下文维护。

这解释了为什么同一个模型放在聊天界面和 coding agent 里表现会很不同。聊天界面主要依赖用户手工提供上下文；coding harness 会帮模型持续观察仓库、执行命令、读取错误、修改文件、再验证。

我的理解是，coding agent 的能力来自模型和环境的耦合。没有 harness，模型会像一个只会口述代码的助手；有了 harness，它才进入可以执行、反馈和迭代的工作循环。

## 六个组件对应六个工程问题

文章列了六个组件：Live Repo Context、Prompt Shape and Cache Reuse、Tool Access and Use、Minimizing Context Bloat、Structured Session Memory、Delegation With Bounded Subagents。

Live repo context 解决的是“模型怎么知道当前代码库”。它不是一次性上传全部文件，而是通过搜索、读取、索引和局部上下文补全，让模型在需要时拿到相关信息。

Prompt shape and cache reuse 解决成本和延迟。稳定 prompt 前缀、可复用工具定义和项目记忆，会直接影响长会话体验。Tool access and use 解决行动能力，但工具不是越多越好；工具定义会占上下文，功能重叠也会干扰选择。

Minimizing context bloat 处理长会话污染。Structured session memory 则把会话经验和项目规则以更有结构的方式保存下来。Bounded subagents 用于研究、验证或并行任务，但强调 bounded，因为不受控的 delegation 会带来成本和协调问题。

## 这篇文章最好的地方，是把产品体验还原成系统细节

很多人使用 Claude Code 或 Codex 时，会把体验差异归因于模型。文章提醒我们，harness 可能才是产品差异的重要来源。相同模型，如果 repo context 组织得不好、工具空间混乱、缓存命中率低、session memory 不稳定，表现就会差很多。

反过来，一个好的 harness 可以让非最强模型也显得更聪明。它把模型要处理的问题变小，把相关上下文放到正确位置，把验证反馈及时送回循环。

## 我的判断：coding agent 会越来越像开发环境而不是聊天框

这篇文章让我更确信，coding agent 的未来不只是“聊天框里写代码”。它更像一个开发环境：有文件系统视角，有工具链，有状态记忆，有成本优化，有上下文路由，有任务隔离。

这也意味着评估 coding agent 时，不能只看模型 benchmark。我们还要看它如何读取仓库、如何选择工具、如何缓存上下文、如何处理长会话、如何限制 subagent、如何把失败转成记忆。

如果说模型是引擎，coding harness 就是方向盘、仪表盘、刹车、导航和维修手册。没有这些，强引擎也很难稳定开到目的地。

## 原文

- [Components of A Coding Agent](https://magazine.sebastianraschka.com/p/components-of-a-coding-agent)
