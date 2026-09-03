---
date: '2026-08-31T15:45:00+08:00'
lastmod: '2026-08-31T15:45:00+08:00'
title: 'Claude Code 的上下文管理：1M Context 不是银弹，会用才是'
summary: "Claude Code 团队详细拆解了 context rot、compaction、rewind 和 subagent 四种上下文管理机制，核心信息是：大窗口解决了容量问题，但没有解决质量问题。"
description: "从 Claude Code 的上下文管理实践看 1M context window 下的 session 策略和 compaction 陷阱"
tags: ["agentic-coding", "context-engineering"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Claude Code 团队的 Thariq Shihipar 发了一篇 [Using Claude Code: session management and 1M context](https://claude.com/blog/using-claude-code-session-management-and-1m-context)，系统梳理了 Claude Code 在 1M context window 下的上下文管理策略。这篇文章最有价值的地方不是介绍新功能，而是把"context rot"这个平时被模糊带过的问题讲透了，并给出了一套实操决策框架。

## Context Rot：大窗口解决了容量，但没解决质量

Claude Code 的 context window 现在有 100 万 token，理论上足够跑很长的任务。但文章开篇就点明了一个关键矛盾：**context 越大，模型表现不一定越好**。

这就是 context rot——随着 context 增长，attention 被分散到更多 token 上，早期的无关内容开始干扰当前任务的推理质量。换句话说，1M context 意味着你*可以*塞进更多信息，但不意味着你*应该*。

这个观察对所有使用长轨迹 agent 的人都很重要。很多人拿到大 context window 后的第一反应是"不用管上下文了"，但实际上大窗口只是把"context 不够用"的硬约束换成了"context 质量下降"的软约束。后者更隐蔽，也更难调试。

## 每个 Turn 都是一个分叉点

文章最有用的框架是把每个 agent turn 结束后的状态定义为一个**分叉点**，你有五种选择：

1. **Continue** —— 继续当前 session，不做任何上下文管理
2. **Rewind** —— 回退到之前的某个消息，从那里重新开始
3. **Clear** —— 清空 session，手动写一个 brief 带入新 session
4. **Compact** —— 让模型总结当前 session，在摘要基础上继续
5. **Subagent** —— 把下一段工作交给一个独立 context 的子 agent

大多数人默认选 1，但文章的核心论点是：**主动选择其他四种，往往能带来更好的结果**。

## Rewind 比纠正更高效

这是文章中我认为最反直觉的建议。当 Claude 走了一条错误路径时，多数人的本能反应是发一条"那个不对，试试 X"。但作者建议用 `/rewind`（或双击 Esc）回退到错误发生前的状态，然后用你学到的信息重新 prompt。

为什么这比纠正更好？因为纠正会在 context 里留下错误尝试的全部痕迹——错误的 tool call、错误的输出、你的纠正指令——这些都是噪音，会加剧 context rot。而 rewind 直接从 context 里移除了这些内容。

更有意思的是 rewind 还支持 "summarize from here"，让 Claude 先总结失败尝试中学到的教训，生成一条"来自未来自己的消息"，然后在回退后的干净 context 上重新开始。这本质上是用信息压缩来保留有价值的认知，同时丢弃无价值的执行细节。

## Compact 的陷阱：模型最笨的时候在做最重要的事

Compact（`/compact`）让模型总结当前 session，然后用摘要替换原始历史继续工作。听起来很合理，但文章指出了一个重要的隐患：**autocompact 发生时，模型正处于 context rot 最严重的状态**。

作者举了一个典型场景：你在一个长 session 里做了大量调试，autocompact 触发时模型总结了调试过程，但你接下来的指令是"修一下我们在 bar.ts 里看到的那个 warning"。因为 session 焦点一直在调试上，那个 warning 很可能已经被摘要丢掉了。

这解释了为什么很多人反馈 compact 后 agent 会"忘记"一些重要信息。不是 compact 机制有 bug，而是模型在做信息压缩时的能力受到了 context rot 的影响。

作者的建议是：在 1M context 的条件下，你有更多时间在 context 还不太长的时候**主动** compact，而不是等 autocompact 被动触发。主动 compact 时还可以加指令引导摘要方向：`/compact focus on the auth refactor, drop the test debugging`。

## Clear vs Compact：谁控制信息选择很重要

文章把 `/clear`（清空 session）和 `/compact` 做了明确对比，核心差异是**信息选择权**：

- **Compact**：模型决定什么重要，自动生成摘要。省力，但你无法完全控制保留什么。
- **Clear**：你自己写 brief，手动描述关键约束、相关文件和已排除的方案。更费力，但 context 完全由你决定。

这个区分在实践中非常有用。如果你只是在一个任务中间需要减负，compact 就够了。但如果你要切换到一个新方向，或者之前的探索大部分都不再相关，clear + 手写 brief 是更干净的选择。

## Subagent：只要结论，不要过程

Subagent 的使用场景很清晰：当你知道某段工作会产生大量中间输出，但你只需要最终结论时，用 subagent 在独立 context 里完成，只把结果带回主 session。

文章给的心理测试很实用：**"我还需要这个 tool output 本身，还是只需要它的结论？"** 如果是后者，就适合用 subagent。

典型场景包括：

- 让 subagent 遍历另一个 codebase，总结它的 auth 实现方式
- 让 subagent 根据 spec 验证当前实现
- 让 subagent 基于 git changes 写文档

这些任务的共同特点是中间过程（大量文件读取、搜索、比对）产生的 token 远多于最终有价值的输出。

## 决策框架

文章最后给了一个简洁的决策表：

| 场景 | 选择 | 原因 |
|------|------|------|
| 同一任务，context 仍然相关 | Continue | context 里的信息还有用，不值得重建 |
| Claude 走错了路 | Rewind | 保留有用的文件读取，丢弃失败尝试 |
| 任务中段但 session 膨胀 | Compact + 引导 | 省力，但要主动引导摘要方向 |
| 开始全新任务 | Clear | 零 rot，你控制带入什么 |
| 下一步会产生大量中间输出 | Subagent | 中间噪音留在子 context，只要结论 |

## 我的看法

这篇文章让我意识到，context management 不是一个可以忽略的实现细节，而是使用 coding agent 的核心技能。

以前我用 agent 时基本是"一路 continue 到底"，遇到问题就发纠正指令。看完这篇才明白，这种方式在短 session 里问题不大，但一旦任务变长，context rot 会让 agent 表现持续下降，而你很难意识到是 context 质量的问题。

最让我有启发的是 rewind 的使用方式。把错误尝试从 context 里完全移除，而不是在上面叠加纠正，这个思路改变了我对"如何与 agent 协作"的理解。纠正是人类对话的自然方式，但对 agent 来说，干净的 context 比详细的纠正历史更有价值。

另外，compact 的陷阱也值得所有用长 session 的人注意。autocompact 在模型最弱的时候做最关键的信息压缩，这几乎是一个系统设计层面的 trade-off。在 agent infra 层面，这可能意味着 compaction 需要独立的、不受 context rot 影响的总结能力。

## 原文

- [Using Claude Code: session management and 1M context](https://claude.com/blog/using-claude-code-session-management-and-1m-context)
