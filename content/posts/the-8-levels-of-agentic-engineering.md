---
date: '2026-04-09T23:20:00+08:00'
lastmod: '2026-04-09T23:20:00+08:00'
title: 'The 8 Levels of Agentic Engineering：从补全到后台代理团队的能力阶梯'
summary: "解读《The 8 Levels of Agentic Engineering》：这篇文章最有价值的地方，不是发明了一个新术语，而是把 agentic coding 的成熟度差异拆成了一条很具体的升级路径，从上下文工程一路走到 harness、后台代理和多智能体协作。"
description: "从 8 个层级看 agentic engineering 如何从个人辅助工具演进成团队级生产系统"
tags: ["agent", "agentic-coding"]
origStatus: "available"
author: "Qian"
isCJKLanguage: true
showToc: true
---

这篇 [The 8 Levels of Agentic Engineering](https://www.bassimeledath.com/blog/levels-of-agentic-engineering) 我觉得很有意思，因为它没有停留在“AI 编程越来越强”这种大而化之的描述，而是试图把差距落到实践层。

作者真正想说的是：同样的模型，为什么有的团队已经能把 agent 当成全天候产能，有的团队却还停留在 plan mode 和手动兜底？答案不是模型差一个版本，而是**你有没有把 agentic engineering 真正做成一套分层升级的工程体系。**

## 这篇文章最好的地方，是把“能力差距”翻译成“实践层级”

文章把路径拆成八级：从 tab complete、AI IDE、context engineering、compounding engineering，一路走到 MCP/skills、harness engineering、background agents，再到 autonomous agent teams。

我很认同这种拆法，因为它揭示了一个容易被忽略的事实：AI 编程的提升并不是线性的。你不是从“会补全”平滑长到“会自己做项目”，而是每跨过一个层级，工作方式都会发生一次质变。

比如 Level 3 的重点还是“给模型更好的上下文”；到了 Level 4，重点已经变成把经验 codify 回系统；再到 Level 6，主战场则彻底转向 harness、反馈回路和 trust boundary。也就是说，越往后越不像 prompt 技巧，越像系统工程。

## Level 3 到 Level 5，其实在解决同一个问题：怎么让无状态模型持续积累能力

文章前半段我最有共鸣的是 Context Engineering、Compounding Engineering、MCP and Skills 这三层。

它们表面上是三件事，实际上在共同回答一个问题：模型本身没有长期记忆、也不天然理解你的项目，那你怎么让它越来越像一个熟悉环境的协作者？

- Context engineering 解决当前回合“该看什么”
- Compounding engineering 解决历史经验“怎么留下来”
- MCP/skills 解决能力边界“怎么扩出去”

我觉得这三层的连贯性非常强。很多团队只做第一层，努力优化 prompt 和规则文件；但如果没有后两层，agent 还是很难真正复利。因为它今天学会的东西，明天还会忘；今天能做的事情，明天也未必能接上外部系统。

## 从 Level 6 开始，问题不再是“上下文够不够好”，而是“系统能不能自我纠偏”

Level 6 的 harness engineering 我觉得是全文真正的分水岭。

到了这一步，作者已经不再强调人怎么给模型喂上下文，而是强调环境本身如何给 agent 形成 backpressure。测试、类型系统、lint、预提交检查、运行日志、浏览器录制、权限边界，这些东西共同构成了 agent 的外部反馈系统。没有这些，agent 再聪明也只能靠自我感觉继续前进。

这也是为什么我越来越认同一个判断：真正成熟的 coding agent，首先是一个能持续接收负反馈并修正自己的 runtime，而不是一个会写长代码的聊天机器人。

## Background Agents 和 Team 模式，本质上是在讨论组织形态

文章后半段讲到 background agents 和 autonomous agent teams，这一点也很有启发。

因为到了这个阶段，你讨论的已经不是“一个人怎么更高效地用 AI”，而是团队如何重新组织并行工作。后台代理意味着任务可以异步持续推进，review 和 implement 解耦；多 agent 团队则意味着任务可以像分布式系统一样被拆分、领取、协商和汇总。

虽然作者也承认 Level 8 还很实验性，但这条演进路径已经足够说明问题：agentic engineering 的终点并不是“更厉害的 IDE 插件”，而是更接近一种新的工程生产组织。

## 我的看法：这篇文章最大的价值，是让“高阶用法”不再显得玄学

我读完之后最大的感受是，这篇文章把很多原本容易被神秘化的高阶实践拆开了。

它让你看到，从 context engineering 到 harness engineering，再到 background agents，其实不是一堆松散 buzzword，而是一条逐级抬高自动化上限的路径。前一层做不好，后一层只会放大混乱；前一层做扎实了，后一层才会开始真正复利。

所以如果要总结这篇文章，我会说：它最有价值的地方，不是给 agentic engineering 贴了八个标签，而是给团队提供了一张很实用的能力阶梯图。**这张图的意义在于，它把“为什么别人比你用 AI 更猛”这件事，解释成了一系列可以逐步补齐的工程实践。**

## 原文

- [The 8 Levels of Agentic Engineering](https://www.bassimeledath.com/blog/levels-of-agentic-engineering)
