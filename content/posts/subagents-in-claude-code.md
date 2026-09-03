---
date: '2026-06-05T21:20:00+08:00'
lastmod: '2026-06-05T21:20:00+08:00'
title: 'Subagents 的价值：为 Claude Code 保留主线程的清醒'
summary: "解读 Claude Code subagents 指南：subagent 的核心价值不是“多开几个模型”，而是在研究、并行修改和独立 review 中隔离上下文、减少主线程污染。"
description: "从 Claude Code 官方文章看 subagents 的适用场景、调用方式、自动化路径和不该使用的边界"
tags: ["agentic-coding", "agent", "context-engineering"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Claude 官方这篇 [How and when to use subagents in Claude Code](https://claude.com/blog/subagents-in-claude-code) 讲的是一个看似简单、实际很容易误用的能力：什么时候应该把任务交给 subagent，什么时候留在主会话里做。

文章开头的判断很准确：Claude Code 能处理复杂的多步骤项目，但长会话会变重。每次读文件、每个旁支探索、每段半成品思路都会留在上下文里，增加 token 成本，也让主线程更吵。Subagent 的价值，就是给这些旁支开一个独立上下文，最后只把结果带回来。

## Subagent 本质上是上下文隔离工具

文章对 subagent 的定义很清楚：它是一个拥有自己上下文窗口的独立 Claude instance。它接收任务，独立读文件、探索代码或修改文件，完成后只把相关结果返回主会话。

这意味着 subagent 不继承主会话里的全部历史、假设和噪音。多个 subagents 可以并行运行，也可以有不同权限。比如研究型 subagent 可以只读，实施型 subagent 可以有编辑权限。

所以我不太愿意把 subagent 理解成“更多算力”。它更像 context engineering 里的隔离机制：把会污染主上下文的探索、验证和旁支工作挪出去，让主线程继续保持决策清醒。

## 最适合 subagent 的几类任务

文章列了几个很明确的信号。

第一类是 research-heavy task。比如你要改一个陌生系统，先要理解认证、数据库、API routes、前端组件。让主会话直接读几十个文件，后面就会背着很多无关上下文继续实现。让 subagent 先探索并返回摘要，主会话只接收结论。

第二类是多个独立任务。比如不同包里的 TypeScript 错误、多个文件里同一模式的改造、彼此没有依赖的并行修改。文章的判断很直接：三个 subagents 同时做，通常会接近一个任务的耗时完成。

第三类是 fresh perspective。独立 review 很适合 subagent，因为它没有参与实现过程，不会继承主会话里的解释、取舍和盲点。文章也把 verification before committing 单独列出来：提交前让一个没看过实现旅程的 subagent 检查边界情况和错误处理，往往更容易发现熟悉感遮住的问题。

第四类是 pipeline workflow。设计 API contract、实现后端、写集成测试，这类阶段清楚的流程可以用明确 handoff 串起来，让每个阶段专注自己的问题。

## 从自然语言开始，不要一上来就自动化

文章推荐从 conversational invocation 开始，也就是直接要求 Claude 使用 subagents。有效 prompt 的关键是把 scope、并行性和返回格式说清楚。

比如“Use subagents to explore this codebase in parallel: find API endpoints, identify database schema, map authentication flow. Return summaries, not full file contents.”这个结构好在它明确了三个独立任务、要求并行、说明返回摘要而不是原始文件。

当同一种任务反复出现时，再考虑 custom subagents。它们可以放在 `.claude/agents/` 或 `~/.claude/agents/`，定义自己的 system prompt、工具权限和模型。文章给的 security-reviewer 例子很典型：只允许读工具，专门检查 SQL injection、XSS、auth、敏感数据泄漏等问题，并要求返回按优先级排序的 findings。

再往上，可以用 CLAUDE.md 描述项目级规则，例如每次 code review 都必须用 read-only subagent，检查安全、性能和架构约定。Skills 则适合复杂但按需触发的多步工作流，比如 staged changes 上同时跑 security、performance、style 三类 review。Hooks 是更自动的一层，可以在 Stop、提交等生命周期事件里触发检查。

这条路径很健康：先用自然语言找到真实重复模式，再把稳定模式固化到 custom agent、CLAUDE.md、skills 或 hooks。反过来，如果一开始就为所有事情建 specialist，很容易把系统搞得难以路由。

## Subagent 不适合所有事情

文章最后专门讲了什么时候不该用 subagent，这部分很重要。

如果任务是强顺序依赖，第二步必须完整继承第一步细节，主会话通常更简单。如果两个 subagents 会同时编辑同一个文件，那就是制造冲突。小任务也不值得 delegation，因为启动上下文和沟通结果本身有成本。

还有一个很现实的边界：不要定义太多 specialist agents。选项太多会让自动 delegation 变得不可靠。大多数团队最后应该只有少数几个边界清楚的 agent，而不是为每种想象场景都建一个角色。

如果 subagents 之间需要互相沟通，也不适合普通 subagent 模式。文章建议这种情况使用 agent teams，因为普通 subagent 是向主会话汇报结果，不是彼此协作。

## 我的判断：subagent 的关键不是并行，而是主线程卫生

并行当然是 subagent 的显性收益，但我觉得更大的收益是主线程卫生。Coding agent 的上下文很容易被探索痕迹污染：读过的无关文件、失败的假设、临时推理、被否掉的方向，都会影响后面的判断。Subagent 给了一个低成本的隔离方式，让探索发生在旁路，只把整理后的结论带回来。

这也是为什么 fresh review 特别适合 subagent。很多 review 失败不是因为模型能力不够，而是因为它知道实现过程，于是会替自己的取舍找理由。干净上下文能减少这种路径依赖。

所以使用 subagent 的好问题不是“能不能多开几个 agent 加速”，而是“这段工作会不会污染主会话，或者是否需要独立视角”。如果答案是是，subagent 很值；如果只是一个小而连续的改动，主会话做完更省心。

## 原文

- [How and when to use subagents in Claude Code](https://claude.com/blog/subagents-in-claude-code)
