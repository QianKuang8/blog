---
date: '2026-05-07T21:12:00+08:00'
lastmod: '2026-05-07T21:20:54+08:00'
title: 'Deep Agents 提分：Harness Engineering 的价值在反馈回路'
summary: "LangChain 这篇文章的重点不是某个提示词技巧，而是展示了如何用 trace、middleware 和验证循环，把 coding agent 的失败模式系统性转化为 harness 改进。"
description: "解读 LangChain 如何只调整 harness，就让 deepagents-cli 在 Terminal Bench 2.0 上从 52.8 提升到 66.5。"
tags: ["harness-engineering", "agent"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

LangChain 的 [Improving Deep Agents with harness engineering](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/) 很适合作为 harness engineering 的实操案例读。它没有把 agent 提升归因于换更强模型，而是刻意固定模型，只调整 harness，最后让 deepagents-cli 在 Terminal Bench 2.0 上从 52.8 提升到 66.5。

我觉得这篇文章真正讨论的问题是：当模型本身已经足够强，但行为仍然不稳定时，系统层还能做什么？答案不是继续堆 prompt，而是建立一套能观察失败、注入上下文、强制验证、调配推理预算的反馈回路。

## Harness 不是包装层，而是能力塑形层

文章对 harness engineering 的定义很直接：围绕模型构建工具、提示、执行流程和中间件，把模型“尖刺状”的智能塑造成对具体任务有用的能力。这个说法比“写好 system prompt”更准确。

在 LangChain 的实验里，harness 可调的空间很大，包括 prompt、tools、hooks、skills、sub-agent、memory 等。但他们为了控制变量，只集中改三个旋钮：system prompt、tools 和 middleware。模型固定为 `gpt-5.2-codex`，基准是 Terminal Bench 2.0，89 个任务覆盖机器学习、调试、生物等场景，运行由 Harbor 和 Daytona sandbox 编排，所有 agent action 进入 LangSmith trace。

这个实验设置的重要性在于，它把“模型进步”和“系统进步”拆开了。很多 agent 产品的提升来自模型、工具、提示、评测环境同时变化，最后很难判断到底是哪一层起作用。LangChain 这篇文章至少提供了一个更可讨论的样本：同一个模型，在更好的 harness 下，表现可以明显提升。

## Trace 是外循环的训练信号

这篇文章最有工程味的部分，是它没有从主观经验出发改 prompt，而是先看 trace。LangChain 做了一个 Trace Analyzer Skill：拉取 LangSmith 中的实验轨迹，派并行错误分析 agent 找失败模式，再由主 agent 汇总建议，最后有针对性地调整 harness。

这套流程的价值不在于“让 agent 自动改自己”这个概念有多新，而在于它把失败分析变成了可重复流程。模型内部机制不可解释，但 agent 的输入、输出、工具调用、耗时、token 和错误路径都是可观察的。对 coding agent 来说，这些 trace 往往比最终 pass/fail 更有信息量。

文章把这种方式类比为 boosting：聚焦上一轮做错的样本，再针对错误模式改进系统。这个类比很贴切，但也要注意它的风险。作者明确提到，人工在第三步仍然有帮助，因为过度针对某些任务修 harness 可能导致过拟合，对其他任务回归。

我觉得这里的关键不是全自动，而是可审计。Trace 让 harness 改动有了依据，也让“为什么要加这个 middleware、为什么要改这段 prompt”可以追溯到具体失败模式。

## 自验证不是自然发生的

LangChain 观察到的最常见失败模式很典型：agent 写完方案，重新读一遍自己的代码，觉得看起来没问题，然后停止。它没有自然进入 build-verify loop。

这和人类开发经验很接近。只读自己刚写完的代码，几乎总是更容易确认原有想法，而不是发现问题。coding agent 也是一样：如果没有外部反馈，它会停在第一个看似合理的解上。

LangChain 的做法包括两层。第一层是在 system prompt 中明确问题解决流程：规划和发现、构建、验证、修复。第二层是 deterministic context injection：用 `PreCompletionChecklistMiddleware` 在 agent 试图结束前拦截一次，提醒它对照任务 spec 重新做验证。

这里最值得借鉴的是 middleware 的位置。验证提示如果只写在系统提示里，模型可能在长任务中淡忘；放在退出前的 hook 里，就把“交付前检查”变成了运行时机制。它不保证正确，但能显著降低 agent 过早结束的概率。

## Context Engineering 是 harness 的职责

文章还强调了一个容易被低估的点：harness engineering 也是 context engineering 的交付机制。Terminal Bench 任务有目录结构、工具链和严格 timeout，agent 如果每次都自己摸索环境，就会浪费时间，还会因为搜索路径错误而做错判断。

LangChain 用 `LocalContextMiddleware` 在 agent 启动时注入当前目录、父子目录和可用工具信息，例如 Python 安装。这类信息并不是高深知识，但对 agent 来说很关键，因为它降低了环境发现的错误面。

他们还通过 prompt 告诉 agent：工作会被程序化测试衡量，任务中提到的文件路径要精确遵守，要关注 edge case，而不是只验证 happy path。再加上时间预算提醒，agent 更容易在 strict timeout 下从探索切换到实现和验证。

我的理解是，这里的 context engineering 不只是“把更多信息塞进上下文”，而是把那些 agent 本来容易漏掉、但对任务成败有决定性影响的环境约束提前摆到它面前。好的 harness 应该替 agent 完成一部分 onboarding。

## 推理预算也需要工程化

文章里另一个有意思的实验是 reasoning budget。直觉上，给 reasoning model 更多推理预算应该更好，但 Terminal Bench 有 timeout。LangChain 发现全程 `xhigh` 反而只有 53.9%，不如 `high` 的 63.6%，原因是高推理预算会消耗更多 token 和时间。

他们最后采用的是类似 “reasoning sandwich” 的启发式：前期规划用更高推理，中间实现阶段降低，最后验证再提高。这个策略不一定普适，但它提出了一个实际问题：agent harness 不应该把推理预算看成单一全局参数，而应该按任务阶段分配。

我的理解是，在真实产品里，这会继续扩展成多模型 harness：大模型负责规划，小模型负责局部实现，验证阶段再按风险选择更高推理预算，或者由模型自己做 adaptive reasoning。无论哪种方式，核心都是把推理计算当作稀缺资源调度，而不是简单开到最大。

## 我的判断：harness 的核心资产是失败样本

这篇文章给我的最大启发是，harness engineering 的核心资产不是 prompt 模板，而是失败样本和反馈回路。

如果没有 trace，只靠感觉改 prompt，很容易陷入局部优化：某个失败案例修好了，但你不知道它是否提升了整体表现。如果没有退出前验证、环境注入和推理预算控制，agent 的很多错误会反复出现，因为模型本身没有足够稳定的行为倾向。文章里提到的 `LoopDetectionMiddleware` 也属于同一类短期护栏：当 agent 对同一个文件反复编辑时，middleware 会提示它重新考虑方案，避免在错误路径上不断小修小补。

当然，这篇文章的边界也很清楚。Terminal Bench 2.0 是有固定任务、固定 timeout 和自动评分的环境，里面有效的 heuristics 不一定能直接迁移到所有真实软件开发场景。比如时间预算提醒在 benchmark 里很重要，但在长周期产品开发里可能需要换成里程碑、成本和风险控制。

但它提供了一个可复用的方向：不要把 agent 看成单次调用模型，而要把它看成一个可以被观测、被干预、被验证的执行系统。模型越强，harness 的价值越不是“弥补模型不会”，而是把强模型的能力稳定地导向任务目标。

## 原文

- [Improving Deep Agents with harness engineering | LangChain Blog](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/)
