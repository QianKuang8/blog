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
- [从一次演示到可复用 Skill：Codex Record & Replay 与 Claude Record a Skill]({{< relref "/posts/from-demonstration-to-skill.md" >}})：看录制证据怎样写成方法，以及 Skill、当前任务、工具与权限怎样共同决定执行。

## 最后看反馈、观测与成本

- [AI 原生软件工程：可观测性和可控制性会变成核心能力]({{< relref "/posts/ai-native-software-engineering-observability-control.md" >}})：把 trace、可控性和组织转型放在一起看。
- [Deep Agents 提分：Harness Engineering 的价值在反馈回路]({{< relref "/posts/improving-deep-agents-with-harness-engineering.md" >}})：理解失败分析和评估闭环。
- [Uber 软件工厂：围绕有效交付优化 Agent 成本]({{< relref "/posts/uber-efficient-software-factory.md" >}})：看模型分工与工具流程的改进，怎样用同一组真实任务检查质量和成本。

## 继续探索

- [harness-engineering 标签]({{< relref "/tags/harness-engineering" >}})
- [agent 标签]({{< relref "/tags/agent" >}})
