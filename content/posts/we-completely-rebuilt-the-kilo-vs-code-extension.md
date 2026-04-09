---
date: '2026-04-09T23:28:00+08:00'
lastmod: '2026-04-09T23:28:00+08:00'
title: 'Kilo 重构 VS Code 扩展：把子智能体和并行执行带回编辑器'
summary: "解读 Kilo 的重构文章：它最有意思的点，不是又加了几个功能，而是说明 IDE 里的 agent 产品正在把底层核心从编辑器内部实现中抽出来，转向一个可在 CLI、IDE 和云端复用的便携 runtime。"
description: "从 Kilo 重构 VS Code 扩展看 agent 产品如何以便携核心承载并行执行、子智能体与 worktree"
tags: ["agentic-coding", "行业动向"]
origStatus: "available"
author: "Qian"
isCJKLanguage: true
showToc: true
---

这篇 [We've completely rebuilt the Kilo Code extension for VS Code. Join the beta test.](https://blog.kilo.ai/p/we-completely-rebuilt-the-kilo-vs-code-extension) 我觉得很值得看，因为它讨论的不是“编辑器里又多了一个 AI 功能”，而是更底层的问题：**agent 产品的核心到底应该长在 IDE 里，还是应该长成一个可跨表面复用的 runtime。**

Kilo 这次给出的答案很明确。他们把 VS Code 扩展重构到 OpenCode 这个便携核心之上，让 CLI、IDE 和其他表面共享同一套引擎。这背后反映的是一个越来越明显的行业方向：agent 能力正在从“编辑器插件功能”升级成“跨环境运行时”。

## 这次重构真正解决的，是“编辑器内部依赖外溢”问题

文章里提到的原始痛点其实很典型：以前 Kilo 的很多表面都依赖 VS Code 内部实现，甚至 JetBrains 这类环境也要背着 VS Code internals 跑。

这类设计在产品早期很常见，因为起步快、离用户近，但它的副作用也很明显：跨平台能力会变得沉重，性能被编辑器内部抽象拖住，很多能力只能在特定入口里生长。Kilo 这次重构，本质上就是把这些历史包袱从核心里剥出去。

这一步很重要，因为它说明 agent 产品已经到了要认真处理“核心和表面分离”的阶段。否则你很难同时把 CLI、IDE、Cloud Agent 和多工作区能力都做扎实。

## 真正的新能力，不只是并行，而是可组织的并行

文章里最吸引人的当然是 parallel tool calls、subagent delegation、Agent Manager、git worktrees 这些功能。但我觉得这些功能最重要的意义，不在于“更快”，而在于它们把并行执行组织成了一套可以管理的工作流。

一个 agent 改代码、另一个 agent 写测试、第三个 agent 做 review，彼此跑在不同 worktree 里，再由 orchestrator 汇总结果。这里的关键不是同时开了几个线程，而是系统开始有能力把多 agent 的并发工作组织起来，而不是让用户自己在聊天窗口里硬调度。

这也是我对这篇文章最有感触的地方：它展示的已经不是“AI 助手”，而是更接近一个轻量级的软件生产调度系统。

## Agent Manager 的价值，在于把多 agent 工作从黑箱拉回可控界面

另一点我比较认同的是它对 Agent Manager 的定位。多 agent 协作如果只有后台执行，很容易变成不可见黑箱；而如果完全回到人工手工切换，又失去了效率优势。

Kilo 想做的是中间态：你可以开多个 agent tab，看它们各自状态，用 diff reviewer 审查修改，再把行级评论回注给 agent 继续修。这样一来，多 agent 并发不再只是“让系统自己跑”，而是变成“人仍然能在高杠杆节点介入”。

我觉得这类设计会越来越重要，因为随着 agent 数量增长，真正稀缺的不是生成能力，而是可见性和协调能力。

## 这篇文章透露出的趋势，是 IDE 正在变成 agent runtime 的一个前端

如果把整篇文章抽象一下，它最重要的信号其实是：IDE 在 agent 时代的角色正在变化。

过去 IDE 是核心容器，CLI 是补充入口；现在越来越像反过来，核心能力长在一个独立 runtime 上，IDE 只是其中一个更适合可视化和人工介入的前端。CLI、VS Code、远程会话、工作树管理、模型对比，都是同一核心在不同表面的投影。

这意味着未来的编辑器竞争，可能不再只是“谁的插件 API 更强”，而更取决于谁能承接一个成熟 agent runtime 的展示、控制和协作层。

## 我的看法：这篇文章真正讲清楚的是 agent 产品的下一阶段形态

我读完之后最大的感受是，Kilo 这篇文章真正有意思的地方，并不只是某个产品加了 subagent 或 parallel execution，而是它把 agent 产品的下一阶段形态讲得更清楚了。

当核心能力足够复杂之后，你迟早要把它从单一编辑器里拆出来，变成一个可跨界面、可跨会话、可跨工作区运行的系统。IDE 仍然重要，但它的重要性越来越像可视化控制台，而不是能力本体。

所以如果要总结这篇文章，我会说：它最有价值的地方，不是展示 Kilo 新版多炫，而是说明了一个更大的趋势。**未来成熟的 coding agent 产品，很可能都会走向“便携核心 + 多表面入口 + 可组织的并行协作”这条路线。**

## 原文

- [We've completely rebuilt the Kilo Code extension for VS Code. Join the beta test.](https://blog.kilo.ai/p/we-completely-rebuilt-the-kilo-vs-code-extension)
