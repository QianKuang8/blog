---
title: "Harness Engineering 阅读路径"
description: "从工具、权限、反馈、评估和可观测性，串起 Qian's blog 中关于 Harness Engineering 的文章。"
summary: "从工具、权限、反馈、评估和可观测性，串起 Qian's blog 中关于 Harness Engineering 的文章。"
hideMeta: true
showToc: true
isCJKLanguage: true
---

这条路径关注一个更工程化的问题：当模型已经能做很多事之后，怎样把它放进一个可观察、可约束、可迭代的系统里。

## 先理解 Harness 为什么重要

- [Long-running Harness 的关键，不是多 Agent，而是把判断外置]({{< relref "/posts/harness-design-long-running-apps.md" >}})：从长时间运行任务理解 harness 的控制面。
- [Agent-first 软件工程：Harness Engineering 改变的是组织方式]({{< relref "/posts/harness-engineering-leveraging-codex-in-an-agent-first-world.md" >}})：看 harness 如何改变团队协作和交付方式。
- [Harness Engineering 和 SDD 不是竞争关系]({{< relref "/posts/harness-engineering-vs-sdd.md" >}})：把 harness 和规格驱动开发放在同一张图里看。

## 再看工具和权限

- [Seeing Like an Agent：工具设计要贴着模型能力走]({{< relref "/posts/claude-code-seeing-like-an-agent.md" >}})：理解 action space 为什么要贴着模型的实际使用方式设计。
- [Claude Code Auto Mode：把批准按钮改造成分类器问题]({{< relref "/posts/claude-code-auto-mode.md" >}})：从权限分类器看 agent 控制系统。
- [Claude Code 怎么用 Skills：扩展点要按工作类型分层]({{< relref "/posts/claude-code-how-we-use-skills.md" >}})：看 skills 如何成为可复用的任务包。

## 最后看反馈和观测

- [AI 原生软件工程：可观测性和可控制性会变成核心能力]({{< relref "/posts/ai-native-software-engineering-observability-control.md" >}})：把 trace、可控性和组织转型放在一起看。
- [Improving Deep Agents with Harness Engineering：优化 Agent 要看 trace，而不是只改 prompt]({{< relref "/posts/improving-deep-agents-with-harness-engineering.md" >}})：理解失败分析和评估闭环。
- [Harness 工程可视化：人要开始读取系统结构]({{< relref "/posts/harness-engineering-visual-control.md" >}})：看可视化为什么是控制面，而不是装饰。

## 继续探索

- [harness-engineering 标签]({{< relref "/tags/harness-engineering" >}})
- [agent 标签]({{< relref "/tags/agent" >}})
