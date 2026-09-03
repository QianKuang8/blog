---
date: '2026-06-05T21:30:00+08:00'
lastmod: '2026-06-05T21:30:00+08:00'
title: 'Effective Agent Design：长程 Agent 的核心是上下文管理'
summary: "解读 Lance Martin 对 Agent 设计模式的梳理：给 Agent 一台电脑、多层 action space、渐进暴露、缓存、隔离和演化，本质上都在解决有限上下文如何承载长任务。"
description: "从 Effective Agent Design 看长程 Agent 的计算环境、工具空间、上下文缓存、隔离和演化策略"
tags: ["agent", "context-engineering", "harness-engineering"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Lance Martin 这篇 [Effective Agent Design](https://x.com/RLanceMartin/status/2009683038272401719) 是一篇很好的 Agent 设计模式速记。它把很多看似分散的经验放在一起：给 Agent 一台电脑、设计多层 action space、渐进暴露信息、offload context、cache context、isolate context、evolve context。

我觉得它真正讨论的问题是：长程 Agent 不是靠一次强推理完成任务，而是靠一个持续管理上下文、工具和状态的系统。

## 给 Agent 一台电脑，是为了获得持久环境

文章第一点是 Give Agents A Computer。这几年很多成功 Agent 都不是纯聊天界面，而是让模型拥有某种计算环境：文件系统、shell、CLI、脚本、浏览器或虚拟机。

这背后的价值不是“模型会用电脑很酷”，而是环境提供了持久状态和可验证动作。文件系统可以保存中间结果，shell 可以运行测试和脚本，工具结果可以变成下一步的证据。相比一次性输出答案，Agent 更像在环境里反复观察和行动。

这也是 Claude Code、Manus、Codex 这类系统比普通聊天更强的原因之一。模型本身固然重要，但环境让模型获得了可迭代的工作方式。

## Action space 要分层，而不是堆工具

文章提到 multi-layer action space。工具定义会占上下文，工具过多也会让模型困惑，尤其是功能重叠时。有效 Agent 往往不是暴露几十上百个工具，而是用少量基础工具加上渐进式发现机制。

我的理解是，多层 action space 的关键是把“可用能力”和“当前暴露能力”分开。模型不需要每一秒都看见所有工具，它需要在当前步骤看到足够清楚、足够可执行的选择。

Progressive disclosure 也服务于这个目标：先暴露少量高层能力，再按需要加载细节。这样既减少上下文负担，也降低选择错误工具的概率。

## Offload、Cache、Isolate 都是上下文管理

文章中间几节其实可以合并成一句话：上下文是有限资源，要被工程化管理。

Offload context 是把不该长期塞在窗口里的信息放到外部，比如文件、数据库、记忆系统或工具状态。Cache context 是复用稳定前缀，避免每轮重复支付相同上下文成本。Isolate context 是用子任务、子 agent 或独立环境隔离不同问题，避免相互污染。

这些策略解决的不是同一个表面问题，但底层都指向“有限工作内存如何支撑长任务”。如果所有信息都堆进主窗口，Agent 迟早会遇到 distraction、confusion 或 clash。如果所有子任务都在同一个上下文里展开，失败路径和无关探索会影响后续判断。

## Evolve Context 指向自我改进的 harness

文章最后的 evolve context 更值得细想。一个 Agent 系统如果只是每次从零开始，它就很难把失败经验沉淀下来。真正有价值的是把经验变成可复用上下文：runbook、skill、memory、工具脚本、项目规范、评估指标。

这也是我理解的 harness engineering：不是在 prompt 里训斥模型不要再犯错，而是把错误转化成系统资产。发现工具太多就做 tool search；发现上下文污染就做隔离；发现 prompt cache 被破坏就调整布局；发现同类任务反复失败就写 skill 或测试。

## 我的判断：Agent 设计正在从 prompt 问题变成资源管理问题

这篇文章的价值在于，它把 Agent 设计从“模型够不够聪明”移到了“系统如何组织模型的工作条件”。

电脑给它环境，action space 给它可控动作，progressive disclosure 控制信息暴露，cache 降低运行成本，isolation 降低污染，evolution 沉淀经验。每一项都不是神秘技巧，而是资源管理：管理上下文、注意力、工具、成本和状态。

所以我会把 Effective Agent Design 看成一张工程清单。做 Agent 时不要先问“要不要 multi-agent”，而要问：这个系统的工作内存在哪里，长期状态在哪里，工具如何暴露，失败如何被反馈，经验如何变成下一次的上下文。

## 原文

- [Effective Agent Design](https://x.com/RLanceMartin/status/2009683038272401719)
