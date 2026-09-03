---
date: '2026-06-05T21:30:00+08:00'
lastmod: '2026-06-05T21:48:35+08:00'
title: 'Claude Code 怎么用 Skills：扩展点要按工作类型分层'
summary: "解读 Claude Code 团队关于 Skills 的经验：好 Skill 不只是 markdown，而是可携带脚本、数据、hook 和渐进式上下文的任务包；它的分类、触发和分发方式决定了是否真的能被团队复用。"
description: "从 Claude Code 团队的 Skills 实践看 skill 类型、description 触发、progressive disclosure、hooks、marketplace 和评估"
tags: ["agentic-coding", "agent", "harness-engineering"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Thariq Shihipar 这篇 [How We Use Skills](https://x.com/trq212/status/2033949937936085378) 是目前最值得看的 Claude Code Skills 实战总结之一。它的重点不是解释什么是 skill，而是告诉你：在一个真实团队里，哪些类型的 skills 值得做，怎么写才不会变成噪音。

文章开头先纠正一个误解：Skills 不只是 markdown 文件。它们是文件夹，可以包含脚本、assets、数据、配置和 hook。也就是说，一个 skill 不只是“提示词片段”，而是一个可发现、可执行、可分发的任务包。

## 分类比数量更重要

文章把 Anthropic 内部大量使用的 skills 归成几类：Library & API Reference、Product Verification、Data Fetching & Analysis、Business Process & Team Automation、Code Scaffolding & Templates、Code Quality & Review、CI/CD & Deployment、Runbooks、Infrastructure Operations。

这个分类很有用，因为它避免了一个常见误区：看到 skills 好用，就为所有事情都写一个。真正好的 skill 往往清楚落在某一类里；横跨太多类别的 skill 反而难触发、难维护、难评估。

比如 library/API reference skill 适合放内部库的 gotchas 和示例；product verification skill 适合搭配 Playwright、tmux 等工具验证输出；runbook skill 适合把故障处理流程固化。它们解决的问题不同，触发条件也应该不同。

## 好 skill 要给模型看该看的东西

文章里几个写 skill 的建议很具体。不要写显而易见的废话；要有 gotchas；要利用文件系统和 progressive disclosure；不要 railroad Claude；要认真处理 setup；description 是给模型看的，不是给人看的。

我觉得 progressive disclosure 是核心。Skill 主体不应该无限膨胀，复杂细节可以放到引用文件、脚本或资源里，让模型按需打开。这样既减少主上下文负担，也让 skill 更像一个小型知识系统。

“不要 railroad Claude”也很重要。Skill 不应该把模型锁死在一个僵硬流程里，而应该提供足够清楚的边界、经验和工具，让模型在任务中做合理判断。过度刚性的 skill 很容易在边缘场景失效。

## 分发和评估决定 skill 能否团队化

文章后半讲 marketplace、composing skills 和 measuring skills。这里的重点是，skills 一旦进入团队，就不再只是个人 prompt 收藏，而会变成工程资产。

如果没有分发机制，团队成员不知道有哪些 skills、什么时候该用、哪些已经过时。如果没有评估机制，大家也不知道一个 skill 是否真的改善了任务结果。文章提到 measuring skills，我理解这会越来越重要：skill 的效果不能只靠“感觉好用”，需要能看触发率、完成质量、失败模式和使用成本。

这和软件工程里的库管理很像。一个内部库好不好，不只取决于代码，还取决于文档、版本、示例、使用反馈和维护责任。

## 我的判断：Skill 是团队经验的最小可分发单位

这篇文章让我觉得，Skills 最有意思的定位不是“让 Claude 多会一点”，而是让团队经验可以被 Agent 读取和复用。

一个团队真正有价值的知识，往往不是抽象原则，而是具体到“这个库怎么用才不会踩坑”“这个流程怎么验收”“这个 CLI 哪些参数危险”“这个产品流程怎么跑完整”。这些知识如果只存在人的脑子里，Agent 每次都要重新猜；写成 skill，才变成可调用上下文。

所以做 skills 的关键，不是追求数量，而是找出团队里最反复、最容易出错、最值得标准化的工作，把它们变成带有脚本、参考、gotchas 和验证方式的小包。

## 原文

- [Lessons from Building Claude Code: How We Use Skills](https://x.com/trq212/status/2033949937936085378)
