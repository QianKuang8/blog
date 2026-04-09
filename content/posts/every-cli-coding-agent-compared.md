---
date: '2026-04-09T23:16:00+08:00'
lastmod: '2026-04-09T23:16:00+08:00'
title: 'Every CLI coding agent, compared：终端已经成为 coding agent 的主战场'
summary: "解读 Michael Livs 的《Every CLI coding agent, compared》：这篇文章最有意思的地方，不是罗列 30 多个产品，而是说明 coding agent 的主战场已经从 IDE 辅助转向终端运行时，差异开始落在协议、沙箱、上下文管理和可扩展性上。"
description: "从 30 多个 CLI coding agent 的横向比较看终端为何成为 agent 工程的默认载体"
tags: ["agentic-coding", "行业动向"]
origStatus: "available"
author: "Qian"
isCJKLanguage: true
showToc: true
---

这篇 [Every CLI coding agent, compared](https://michaellivs.com/blog/cli-coding-agents-compared) 很适合当作一份行业横截面来看。它表面上是在盘点 30 多个 CLI coding agent，真正更重要的结论其实是：**终端已经不再只是一个交互界面，而逐渐变成 coding agent 的默认运行时。**

这和早期 AI 编程工具的逻辑不太一样。过去大家更容易把 AI 编程理解成 IDE 补全、聊天问答或者侧边栏助手，但现在越来越多核心能力都在 CLI 里先成熟：读写文件、跑测试、调 git、开子代理、接 MCP、接系统沙箱。这不是产品偏好变化，而是能力边界在变化。

## 为什么主战场会从 IDE 移到 CLI

文章一开始就讲得很直白：不是 IDE 不重要了，而是 CLI 更接近真实系统接口。

只要 agent 要开始做多文件修改、执行 shell、跑构建、管理版本控制和调用外部工具，终端天然就是更低摩擦的入口。相比之下，IDE 插件形态虽然更容易被接受，但它本质上还是一个受限容器，很多能力最终都得绕回终端。

所以我觉得这篇文章真正点穿的一件事是，CLI coding agent 的崛起，并不是“极客审美获胜”，而是**agent 要真正参与工程闭环，就必须更深入地进入操作系统和工具链。**

## 真正能拉开差距的，已经不是“会不会改代码”

盘点这么多产品之后，一个很明显的感觉是：大家都已经不只是“会改文件”的工具了。差异越来越多地出现在底层工程设计上。

比如有的产品重押 LSP 和 Tree-sitter，强调代码理解精度；有的重押 MCP 和 hooks，强调工具扩展与自动化；有的选择 Rust 重写来降低资源开销，有的坚持 TypeScript 以换取迭代速度和生态协作；有的主打本地模型和 BYOK，有的则围绕企业合规和深权限体系构建壁垒。

也就是说，今天看 CLI coding agent，已经不能只看模型接得多不多，而要看它的 runtime、上下文管理、沙箱、安全边界和扩展接口做得怎么样。

## 沙箱和记忆文件，说明这个市场已经进入工程层竞争

文章里我特别喜欢两个观察：一是各种沙箱策略的分化，二是记忆文件的收敛。

前者说明大家都接受了一件事：agent 可以改代码、跑命令以后，权限和隔离就不再是附属功能，而是产品本体的一部分。Docker 隔离、OS 原语、网络代理、总断网策略，各有各的权衡，但都说明这个行业已经从 demo 工具进入了需要认真治理风险的阶段。

后者则体现在 `CLAUDE.md`、`AGENTS.md`、`GEMINI.md`、`WARP.md` 这类仓库级记忆文件上。命名不统一，但思想越来越统一：agent 需要一个可持久发现的项目上下文层。这个变化很重要，因为它说明 coding agent 正从“会话工具”变成“长期协作者”。

## “大四强”之外，真正有意思的是生态分叉

文章当然提到了 OpenCode、Gemini CLI、Claude Code、Codex CLI 这些大玩家，但我觉得更值得看的是生态分叉本身。

你能明显看到几条不同路线在并行发展：

- 第一方实验室工具，重在模型协同、权限和体验闭环
- 开源工具，重在模型中立、成本优化和可 fork 能力
- 编排层工具，重在多 agent 协作和工作树管理

这意味着 CLI coding agent 不会收敛成一个单点市场，而更像一个多层栈。有人做底层 runtime，有人做产品入口，有人做 orchestration，有人做企业安全。这和过去“找一个最强聊天框”已经完全不是一个行业结构了。

## 我的看法：终端不是最终形态，但它会是 agent 工程的默认底座

我读完这篇文章之后最大的感受是，终端未必会是所有开发者最后停留的 UI，但它很可能会成为 agent 系统真正的默认底座。

因为只要问题进入真实软件工程，最终就要处理文件系统、命令执行、权限、沙箱、跨进程协作和上下文持久化。这些都更接近 runtime 问题，而不是界面问题。IDE、Web、云端面板都可以是上层入口，但底层越来越像是一个终端原生的 agent harness。

所以如果要总结这篇文章，我会说：它最有价值的地方，不是帮你选“哪一个 CLI 最强”，而是让人更清楚地看到一件事。**coding agent 的竞争已经明显从前端交互层，转向终端运行时和工程基础设施层。**

## 原文

- [Every CLI coding agent, compared](https://michaellivs.com/blog/cli-coding-agents-compared)
