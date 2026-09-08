---
title: "Context Engineering 阅读路径"
description: "从历史线索、上下文选择和隔离，到文件系统、缓存与任务成本，串起 Qian's blog 中关于 Context Engineering 的文章。"
summary: "从找回工作线索到减少无效搜索，理解上下文工程怎样影响 Agent 的任务质量与成本。"
hideMeta: true
showToc: true
isCJKLanguage: true
---

这条路径适合想理解“为什么 Agent 经常不是模型不够聪明，而是上下文系统没设计好”的读者。重点不是多塞信息，而是在正确时机给模型正确的信息形状。

## 先理解核心问题

- [为什么需要 Context Engineering：Agent 的问题常常是上下文系统问题]({{< relref "/posts/why-context-engineering-needed.md" >}})：适合作为直观起点。
- [Context Engineering for Agents：把上下文窗口当作 Agent 的工作内存]({{< relref "/posts/context-engineering-for-agents.md" >}})：从 Write、Select、Compress、Isolate 建立基本框架。
- [从电脑活动到下一步行动：Computer History]({{< relref "/posts/from-activity-to-action.md" >}})：通过接续桌面工作的场景，分清历史线索、当前来源与行动授权。

## 再看具体机制

- [Dynamic context discovery：为什么给 Agent 更少上下文反而更有效]({{< relref "/posts/dynamic-context-discovery.md" >}})：理解让 Agent 主动发现上下文的价值。
- [How agents can use filesystems for context engineering：文件系统如何成为 Agent 的外部记忆]({{< relref "/posts/filesystems-for-context-engineering.md" >}})：看文件系统为什么适合做稳定、低成本的上下文交换层。
- [Subagents 的价值：为 Claude Code 保留主线程的清醒]({{< relref "/posts/subagents-in-claude-code.md" >}})：从隔离上下文的角度理解 subagent。

## 最后看长程任务与成本

- [Harrison Chase 谈长程 Agent：核心仍是上下文和 Harness]({{< relref "/posts/context-engineering-long-horizon-agents-langchain-harrison-chase.md" >}})：把 context、planning、traces 和人类评估放在一起看。
- [Prompt Caching 是 Claude Code Harness 的隐形地基]({{< relref "/posts/claude-code-prompt-caching-is-everything.md" >}})：理解缓存约束如何反过来塑造上下文布局。
- [Uber 软件工厂：围绕有效交付优化 Agent 成本]({{< relref "/posts/uber-efficient-software-factory.md" >}})：看工具发现、关系查询与缓存怎样影响真实任务的搜索开销和完成成本。

## 继续探索

- [context-engineering 标签]({{< relref "/tags/context-engineering" >}})
- [agent 标签]({{< relref "/tags/agent" >}})
