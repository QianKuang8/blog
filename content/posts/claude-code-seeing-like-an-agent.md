---
date: '2026-06-05T21:30:00+08:00'
lastmod: '2026-06-05T21:30:00+08:00'
title: 'Seeing Like an Agent：工具设计要贴着模型能力走'
summary: "解读 Claude Code 团队关于 action space 的经验：给 Agent 设计工具，不是把所有能力都暴露出来，而是观察模型如何理解、选择和使用工具，再把工具形状调到它能稳定发挥的位置。"
description: "从 Claude Code 的 AskUserQuestion 工具设计看 coding agent 的 action space、elicitation 和工具边界"
tags: ["agentic-coding", "agent", "harness-engineering"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Thariq Shihipar 这篇 [Seeing like an Agent](https://x.com/trq212/status/2027463795355095314) 值得读，因为它讲的不是“给 Agent 更多工具”，而是一个更细的工程问题：**工具要长成模型能理解、愿意使用、不会误用的样子。**

文章从 action space 讲起。Claude 可以通过 tool calling 行动，但工具可以有很多形态：bash、skills、code execution，或者一堆面向具体任务的小工具。问题是，工具越多不一定越好；工具越强也不一定更稳。真正的问题是：模型面对任务时，会怎样看见这些工具？

作者用解数学题做类比。纸、计算器、电脑都能帮忙，但它们对人的要求不同。纸最基础，计算器更强但要会操作，电脑最强但需要知道怎么写代码。Agent 也一样。你不能只按人类工程师的抽象来设计工具，而要反过来观察模型自己的能力边界。

## AskUserQuestion 的三次尝试

文章最具体的例子是 AskUserQuestion 工具。目标很简单：降低 Claude 向用户提问的摩擦，提高沟通带宽。但实现过程说明了工具设计为什么不是拍脑袋。

第一次尝试是在 ExitPlanTool 里加一个问题数组，让 Claude 在提交计划时顺带提出问题。这实现起来最容易，但会让语义变混：工具到底是在“提交计划”，还是在“询问计划前的问题”？如果用户回答和计划冲突，Claude 是否还要再次调用 ExitPlanTool？一个工具同时承载两个阶段，模型就会开始犹豫。

第二次尝试是改输出格式，让 Claude 用某种 markdown 结构写问题，再由系统解析成 UI。这个方案很通用，但不可靠。Claude 可能多写一句话，可能少写选项，也可能换一种格式。对于 UI 驱动的交互来说，“大多数时候格式对”并不够。

第三次才是单独的 AskUserQuestion 工具。它把“问用户问题”从自然语言输出里抽出来，变成一个结构化 action。我的理解是，这里的关键不是工具本身多复杂，而是它把语义边界切清楚了：现在 Claude 不是在顺手写几个问题，而是在明确进入一个“向用户索取信息”的动作。

## 工具边界比工具数量更重要

这篇文章给我的启发是，Agent harness 里的工具设计很像 API 设计，但 API 的调用者不是人，而是模型。人类看一个 API 会读文档、理解抽象、推断边界；模型则会在上下文、工具名、参数结构和过往轨迹里做概率性选择。

所以工具设计要关注几个问题：工具名是否表达了明确动作，参数是否让模型知道什么信息是必须的，工具是否混合了两个阶段，失败时模型能不能恢复，输出是否会引导下一步正确行动。

AskUserQuestion 失败的前两版，都不是“功能做不到”，而是 action space 没对齐模型的决策方式。ExitPlanTool 版本把计划和提问耦合在一起；markdown 版本把结构化动作交给不稳定文本格式。最后独立工具成功，是因为它把模型要做的动作显式化了。

## 我的判断：好工具是给模型降认知负担

很多 Agent 设计会倾向于给模型更强的工具，比如一个大而全的 code execution，或者几十个面向具体场景的专用工具。但这篇文章提醒我，更强不等于更可用。

好的工具不是把人类能力全部塞给模型，而是降低模型在行动前的判断成本。它应该让模型容易知道什么时候用、怎么用、用了以后下一步是什么。工具越贴近模型稳定掌握的动作模式，越能提升系统可靠性。

所以“see like an agent”不是一句漂亮话，而是一种调试方法：读模型输出，观察它为什么没问问题、为什么选错工具、为什么在某个格式上不稳定，然后改变 action space，而不是反复在 prompt 里喊“请严格遵守”。

## 原文

- [Lessons from Building Claude Code: Seeing like an Agent](https://x.com/trq212/status/2027463795355095314)
