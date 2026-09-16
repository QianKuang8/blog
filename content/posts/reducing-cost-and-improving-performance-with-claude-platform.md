---
date: '2026-09-16T11:17:00+08:00'
lastmod: '2026-09-16T11:22:05+08:00'
title: 'Claude Platform 成本优化：缓存、指令与 effort 如何配合'
summary: "从 Anthropic 的成本优化文章出发，理解缓存复用、提示词审计和 effort 调整分别改变什么，以及怎样判断节省是否来自有效优化。"
description: "围绕 Claude Platform 的缓存、指令与 effort，梳理任务成本的来源、评估方法和适用边界。"
tags: ["context-engineering", "prompt-engineering", "anthropic"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Agent 的账单变高时，直接换便宜模型很容易想到；更难回答的是，现有流程到底在哪些地方多做了工作。输入反复处理、重复查证、失败重试，都可能让单次调用的价格失去解释力。

Lance Martin 在 Anthropic 的[这篇文章](https://claude.com/blog/reducing-cost-and-improving-performance-with-claude-platform)中，把优化归纳为缓存、指令和 effort 三个方向。它值得关注的地方，是把成本问题落到了请求构造和执行行为上。下面结合官方文档解释这些机制，再给出一套用于实际评估的整理思路；涉及的产品行为以 2026 年 9 月 16 日查阅的文档为准。

## 先看一次任务的钱花在哪里

排查时，可以先把一轮请求的 token 费用拆开：

```text
本轮 token 费用
  = 未缓存输入费用 + 缓存写入费用
  + 缓存读取费用 + 输出费用

任务费用
  = 各轮请求费用之和
  + 另行计费的工具等费用
```

这是一个记账框架，不是完整的供应商报价公式。它的作用是提醒我们：相同长度的输入可能按不同方式计费；较低的单轮费用也可能被更多轮次抵消。因此，后续每项改动都应同时观察请求和整个任务。

例如，在一个假设的工单流程中，减少一次无用查询会同时减少工具调用和后续上下文。反过来，如果精简提示词后漏掉了必要信息，增加的返工也要算进优化结果。

## 缓存收益来自可复用的前缀

Claude 的缓存按 `tools → system → messages` 的顺序覆盖前缀。文档明确区分缓存写入、缓存读取和普通输入；在响应的 `usage` 中，`input_tokens` 只表示未进入前两类的输入，不能单独当作全部输入量。评估缓存时，应一起记录这三部分。[缓存文档](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#tracking-cache-performance)

稳定内容放在前面之后，还要确认它确实被写入过缓存。显式断点标记写入的位置；自动缓存则随对话增长移动断点。一个容易忽略的边界是：缓存查找寻找此前写入的前缀，不会因为某段文字保持稳定，就自动替它建立可命中的缓存。[断点机制](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#structuring-your-prompt)

时间同样影响复用。默认缓存有效期为 5 分钟，命中会刷新有效期，计时从请求开始算起。生成回复和等待工具都会消耗这段时间；1 小时缓存可以覆盖更长间隔，但写入更贵。[缓存有效期](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

据此，工程上可以把“请求内容改变”和“请求间隔过长”分开排查。前者需要检查构造逻辑，后者需要看执行时间线。只盯着命中率这个汇总数字，很难知道该改哪一层。

## 升级模型时，重新审查旧指令

原文给出的客服实验，是在干净提示词中分别植入六类旧指令问题，再比较模型迁移前后的表现。清理后，作者报告平均成本下降 14.6%，准确率提高 5.3%。这个结果来自特定实验，不能直接当作其他应用的收益预期。[原文实验](https://claude.com/blog/reducing-cost-and-improving-performance-with-claude-platform)

官方成本指南解释了背后的机制：为旧模型补弱项而加入的固定检查、强制步骤和过度详尽要求，可能被新模型严格执行，带来额外工具轮次与输出。[提示词审计](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence#audit-prompts-against-the-current-model)

这里需要区分业务约束和实现习惯。以一个假设的退款流程为例，“退款前核对金额与权限”有明确的业务目的；“不论情况如何都重复查询两次”则需要证明第二次查询增加了什么证据。审计时可以保留前者，再通过失败样例判断后者是否仍然必要。

这种审查也让提示词更容易维护：每条规则都能对应到一个风险或验收要求，模型升级后便有依据决定保留、修改还是删除。

## effort 要放进任务评估中比较

Effort 控制模型投入多少工作，会影响推理和工具使用，不能简单理解为最终回答的字数限制。例如，当前文档特别说明，Opus 5 的 effort 调整并不可靠地缩短可见回复；需要短答案时，仍应明确长度要求。[Effort 文档](https://platform.claude.com/docs/en/build-with-claude/effort)

比较不同档位时，还要控制缓存条件。官方指南建议用不同会话测试，因为会话中修改顶层 effort 会干扰缓存，进而扭曲比较。部分模型支持通过消息调整 effort 并保留前缀，但有具体的模型与 beta 接口条件，不能推广为任意配置切换都不影响缓存。[评估建议](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort)；[会话中调整 effort](https://platform.claude.com/docs/en/build-with-claude/effort#change-effort-mid-conversation)

一个可操作的评估表，可以为每个任务记录以下项目：

| 观察项 | 要回答的问题 |
|---|---|
| 成功与失败原因 | 任务是否完成，遗漏了什么？ |
| 总费用与重试次数 | 节省是否被返工抵消？ |
| 工具调用轨迹 | 减少的是重复工作，还是必要取证？ |
| 完成时间 | 交互体验有没有改善？ |

这张表是本文的工程整理。关键在于让质量判断先于成本排序：先排除不满足验收条件的配置，再比较剩余方案。若只统计“返回了答案”的请求，提前结束的失败也可能看起来很便宜。

## 把优化结果变成可检查的证据

原文提供了三个入口：`/claude-api prompt-audit` 检查旧指令问题，`/claude-api cost-optimize` 审计成本，`/claude-api hillclimb` 借助评估迭代配置。后者区分用于调整的训练集和保留测试集。[工具说明](https://claude.com/blog/reducing-cost-and-improving-performance-with-claude-platform)

这些工具给出的修改仍需要在自己的任务上验收。实践中可以先保存基线，再一次改变一类因素，保留请求用量与失败轨迹；选定方案后，用未参与调参的样例复核。这样才能解释账单为什么下降，以及哪些任务仍然需要更多计算。

缓存让已有输入更便宜，指令审计改变执行路径，effort 调整工作投入。把三者放回同一条任务轨迹，优化结果才有可追溯的原因。

## 延伸阅读

- [原文：Reducing cost and improving performance with Claude Platform](https://claude.com/blog/reducing-cost-and-improving-performance-with-claude-platform)
- [官方文档：Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [官方文档：Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [官方文档：Optimizing for cost and intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- [站内：Prompt Caching 是 Claude Code Harness 的隐形地基]({{< relref "/posts/claude-code-prompt-caching-is-everything.md" >}})：继续理解缓存约束如何影响上下文布局。
