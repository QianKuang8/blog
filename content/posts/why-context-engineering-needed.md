---
date: '2026-06-05T21:34:00+08:00'
lastmod: '2026-06-05T21:34:00+08:00'
title: '为什么需要 Context Engineering：Agent 的问题常常是上下文系统问题'
summary: "解读周星星关于 Context Engineering 的文章：上下文工程不是 prompt engineering 的新包装，而是在 Agent 系统里动态写入、选择、压缩和隔离上下文的系统学科。"
description: "从 Context Engineering 看 Prompt、RAG、Memory、Tools、MCP、多 Agent、上下文压缩和 Agent 评估"
tags: ["context-engineering", "agent", "prompt-engineering"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

周星星这篇 [为什么我们需要 Context Engineering？](https://zhuanlan.zhihu.com/p/1953085369328337945) 适合放在 context engineering 主题的入口位置。它的价值不是给出一个全新的概念，而是把很多 Agent 开发者已经在做的事情归到一个系统框架里：如何让模型在正确时刻看到正确上下文。

文章开头把 Context Engineering 说成一门可以开 4 学分课的系统学科，课程会覆盖 Prompt、RAG、Memory、Tools 和 MCP、主流 Agent 框架、Agent 评估，以及 Claude Code / Deep Research 这类实际案例。我觉得这个判断很准确。上下文工程不是“写好提示词”的小技巧，而是 Agent 系统设计里的核心控制面。

## Prompt Engineering 只是其中一部分

文章反复强调，Prompt Engineering 是 Context Engineering 的子集。一个 prompt 里可能包含系统指令、用户输入、短期记忆、长期记忆、RAG 检索结果、工具定义等内容；但 Context Engineering 关心的不是静态拼 prompt，而是动态组织上下文。

比如一个多 Agent 系统里，当前 sub-agent 要不要看到其他 sub-agent 的结果？应该看到全部，还是摘要？应该从知识库召回什么？工具定义要不要全部塞进去？当前任务产生的信息，哪些应该写回 memory、scratchpad 或 state，供后续任务使用？

这些问题都不是一句 prompt 能解决的。它们涉及写入上下文、选择上下文、压缩上下文、隔离上下文，以及这些机制如何在 Agent 工作流中协同。

## 上下文太长和太短都会坏

文章把 Context Engineering 的痛点归结为信噪比平衡。太长不行，太短也不行。

太长的问题很直观。虽然很多模型宣称支持很长上下文，但作者举了自己做观点聚类的经验：输入在 32K 以下效果不错，超过 32K 后出现明显退化，超过 100K 甚至可能出现乱码和重复。文章还引用 “How Long Contexts Fail” 的四类失败：Context Poisoning、Context Distraction、Context Confusion、Context Clash。

这些分类很有用。很多 Agent 失败并不是模型不会做，而是上下文里有幻觉、噪音、无关信息或互相冲突的信息。模型越努力使用上下文，错误上下文的破坏力越大。

但上下文太短也不行。文章用邮件 Agent 举例：如果只看到“明天有空快速聊一下吗？”，模型只能机械回复；如果它能访问日历、过往邮件、通讯录和发邮件工具，回复就会更自然也更可执行。

所以 Context Engineering 的目标不是“尽量少给”或“尽量多给”，而是让系统能按任务选择合适的信息密度。

## Write、Select、Compress、Isolate 是很好的工程框架

文章引用 Lance Martin 的四分法：Write Context、Select Context、Compress Context、Isolate Context。我觉得这是目前最适合工程落地的一套心智模型。

Write Context 关注把有价值的信息写到上下文窗口之外，比如长期记忆、scratchpad、LangGraph State。Manus 把计划写进 `todo.md`，执行过程中不断修改，就是典型 scratchpad。State 则是把 Agent 运行中的中间变量作为独立状态保存，而不是全塞进 messages。

Select Context 关注在合适时刻召回信息。RAG 是最常见例子，工具选择也是。工具太多时，如果全部放进上下文，模型会被参数名、描述和相似工具干扰；用 RAG 召回相关工具，或像 Manus 那样建立统一工具命名体系，本质上都是在降低 context confusion。

Compress Context 关注上下文过长时如何保留关键 token。文章提到 Claude Code 在上下文接近满时会自动 compact，也提到 trim、rerank、Provence 这类剪裁方式。这里的关键不是压缩得越狠越好，而是要保留当前任务需要的语义。

Isolate Context 则关注把上下文拆开。多 Agent 天然需要隔离：搜索 Agent、回答 Agent、judge Agent 不应该看到完全相同的信息。judge 只需要回答和评估标准，未必需要全部搜索过程。隔离做得好，系统能花更多 token，又不会让单个上下文窗口被噪音淹没。

## 我的判断：Context Engineering 是 Agent 时代的系统设计语言

这篇文章后半还讨论了 single agent 和 multi-agent 之争。Anthropic 的多 Agent 研究系统更适合广度优先任务，Cognition 则提醒多 Agent 容易割裂上下文、造成协作失败。作者的判断比较克制：未来可能走向更强的 single agent，同时保留少量 sub-agent 处理广度优先任务。

我赞同这个方向。Multi-agent 不应该被当成炫技结构，它真正成立的场景，是任务天然可拆、上下文需要隔离、token 预算能被更有效分配。否则多个 Agent 只是多个不共享状态的脑袋，最后还要人类收拾冲突。

所以 Context Engineering 的意义，不是给 Prompt Engineering 换个更时髦的名字。它是在告诉我们：Agent 的可靠性很大一部分来自上下文系统，而不只是模型本身。

一个成熟的 Agent 系统，需要知道哪些信息应该写下来，哪些信息应该召回，哪些信息应该压缩，哪些信息应该隔离。模型能力越强，这些工程问题越重要。因为强模型会更积极地利用你给它的一切上下文，包括那些错误、过时、冲突和多余的信息。

这也是为什么我觉得 Context Engineering 会留下来。即使未来单个模型更强，系统仍然需要决定它在每一步“看见什么”。

## 原文

- [为什么我们需要 Context Engineering？](https://zhuanlan.zhihu.com/p/1953085369328337945)
