---
title: "Context Engineering 阅读路径"
description: "从历史线索、上下文选择和隔离，到文件系统、缓存与任务成本，串起 Qian's blog 中关于 Context Engineering 的文章。"
summary: "从找回工作线索到减少无效搜索，理解上下文工程怎样影响 Agent 的任务质量与成本。"
lastmod: "2026-10-26T12:25:04+08:00"
hideMeta: true
showToc: true
isCJKLanguage: true
---

Agent 每一步做得对不对，很大程度上取决于这一步的输入里有什么：任务目标、相关文件、工具说明、之前的执行结果。上下文工程处理的就是这件事：决定哪些信息进入模型的窗口、以什么形式进入、什么时候移出。这条路径的 11 篇文章先给出概念框架，再看具体机制，最后落到长任务的成本。

## 先分清几篇相近的文章

站内有五篇文章都以上下文工程为主题，标题相近，回答的问题各不相同：

| 文章 | 原文 | 回答的问题 |
| --- | --- | --- |
| [上下文工程的四个动作]({{< relref "/posts/why-context-engineering-needed.md" >}}) | 周星星，2025-09 | 用写入、选择、压缩、隔离四个动作梳理任务里的信息流，并讨论检索、摘要和交接各自会丢什么 |
| [管理 Agent 每一步能看到的信息]({{< relref "/posts/context-engineering-for-agents.md" >}}) | Lance Martin，2025-06 | 四类方法的原始分类，以及每类方法对应的工程做法 |
| [检查模型每一步实际看到了什么]({{< relref "/posts/the-rise-of-context-engineering.md" >}}) | LangChain，2025-06 | 上下文工程的定义，以及怎样沿输入构造过程排查失败 |
| [长程 Agent 的上下文设计]({{< relref "/posts/effective-agent-design.md" >}}) | Lance Martin，2026-01 | 半年后的实践汇总：用计算环境保存状态、按需发现能力、缓存和交接 |
| [Manus 上下文工程]({{< relref "/posts/manus-context-engineering.md" >}}) | Manus，2025-07 | 一个产品团队怎样处理缓存前缀、动作空间和失败记录 |

前两篇在路径里，讲的是同一套框架：Lance Martin 的文章提出分类，周星星的中文文章按任务状态的生命周期重新展开，更容易代入具体任务，所以路径先读它。后三篇暂时不在路径里：想排查 Agent 为什么出错，可以接着读 LangChain 那篇；想看半年后的实践汇总，读 Lance Martin 的第二篇；想看一个完整的生产案例，读 Manus。

## 路径怎样展开

**先理解核心问题。** 两篇框架文章提供了一套词汇。第三篇 Computer History 是一个具体场景：Agent 要接着做一段被打断的工作，必须分清三类信息：可以参考的历史线索、需要重新核对的当前来源，以及只能来自用户的授权。

**再看具体机制。** Cursor 的动态上下文发现和 LangChain 的文件系统文章讲的是同一个做法：完整资料存进文件，窗口里只放摘要和读取入口。前者是产品实现，给出了 MCP 工具按需加载后总 token 减少 46.9% 的数据；后者解释这样做为什么有效，以及保存下来的信息仍然要靠检索才能用上。Subagents 一篇讲隔离：探索交给独立的上下文，主会话只接收结果，代价是交接时可能丢信息。

**最后看长任务与成本。** Harrison Chase 的访谈把上下文、trace 和人工审查放在一起，说明长程 Agent 怎样维持任务连续性。后面四篇都和成本有关：Claude Code 一篇解释缓存前缀的机制；Cursor 和 Claude Platform 两篇给出可以照着检查的调整清单，以及各自报告的降幅；Uber 一篇把成本拆到模型选择、工具调用和上下文路径，再用任务质量检验每项优化。

读完这条路径，应该能回答三个问题：一条信息该常驻窗口、按需读取，还是交给子任务处理；压缩历史时，丢掉哪些内容会让下一步出错；为了缓存命中调整上下文布局时，怎样同时检查任务质量。

{{% reading_path %}}

## 继续探索

- [context-engineering 标签]({{< relref "/tags/context-engineering" >}})
- [agent 标签]({{< relref "/tags/agent" >}})
