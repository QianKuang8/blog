---
date: '2026-06-05T21:28:00+08:00'
lastmod: "2026-09-21T10:20:14+08:00"
title: "Harrison Chase 谈长程 Agent：上下文、交接与可审查结果"
summary: "长程 Agent 每一步都可能改变后续输入。Harrison Chase 从文件系统、子任务交接和 trace 说明如何维持任务连续性，并将可审查初稿与异步、同步交互作为产品边界。"
description: "基于 Harrison Chase 访谈转录，解读长程 Agent 的上下文管理、评估反馈和工作区交互。"
tags: ["agent", "context-engineering", "harness-engineering"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

长程 Agent 的第十四步会看到什么，开发者很难仅凭启动时的提示回答。前十三步可能读过文件、调用工具，也可能引入错误结论。任务越长，后续行为越依赖这些不断变化的输入。

在 Training Data 的 [Harrison Chase 访谈](https://www.youtube.com/watch?v=vtugjs2chdA) 中，这个例子说明了 trace 的用途：记录每一步实际可见的上下文和执行结果。本文依据归档中的带时间戳转录整理；转录有少量专名误识别，以下只采用含义明确的片段，不把口头判断写成普遍实验结论。

## 先让长时间工作产出可审查初稿

Harrison 在 [3:25](https://www.youtube.com/watch?v=vtugjs2chdA&t=205s) 提出，适合长程 Agent 的工作常有“初稿”概念：代码进入 PR，调查形成报告，客服升级前先汇总背景。这些任务允许 Agent 做大量探索，再把结果交给人继续判断。

这个产品边界使任务有明确交接点。运行很久不等于可以直接发布；报告完成也不等于其中结论都已成立。用户应能检查产物、指出缺漏，并让 Agent 根据反馈继续工作。

访谈对可靠性的口头评价说明了讲者为何偏好这种模式，没有给出统一测量协议。因此，不宜将其中提到的百分比当成所有 Agent 的可靠性上限。

## Harness 把上下文管理变成默认行为

在 [5:14](https://www.youtube.com/watch?v=vtugjs2chdA&t=314s)，Harrison 区分模型、framework 与 harness：模型接收和输出消息，framework 提供模型、工具和记忆等抽象，harness 则带有更多具体选择，例如默认规划工具、上下文压缩和文件系统操作。

这种差异影响开发者需要自己决定多少事情。长任务必然遇到历史增长，harness 可以规定何时整理历史、哪些内容保留在外部、哪些工具供模型按需读取。讲者同时强调，模型训练与这些工具形态共同演化，不能把系统收益完全分配给其中一方。

文件系统提供了一种实用的外部状态。在 [17:09](https://www.youtube.com/watch?v=vtugjs2chdA&t=1029s) 附近，他举出两个用途：压缩后仍保存原始消息，方便回查；把大型工具输出写到文件中，由模型只读取所需部分。存储接口也可以由数据库支持的虚拟文件系统实现，但虚拟文件存储本身并不等于代码执行环境。

## 子 Agent 完成工作，还需要把结果交回来

访谈在 [11:13](https://www.youtube.com/watch?v=vtugjs2chdA&t=673s) 给出一个具体失败：子 Agent 做了很多工作，最终只回复“见上文”；主 Agent 实际只收到最后这句话，看不到子任务的中间历史。

这里的问题发生在交接协议。委派时要给足完成任务的材料，返回时也要提供能独立理解的结论和依据。只隔离上下文，却没有定义传回什么，就可能把有价值的探索留在主负责人看不到的地方。

从这个例子可以归纳，任务连续性需要保存可用状态，而不只是让进程继续运行。文件记录、压缩摘要和子任务结果都应回答同一个问题：接手者凭这些材料能否决定下一步？

## Trace 提供材料，评价标准仍需校准

在 [20:19](https://www.youtube.com/watch?v=vtugjs2chdA&t=1219s) 之后，访谈把 trace 视为调试和测试材料：团队先看实际发生的步骤，再提取问题案例。工具接口代码可以说明允许的行为，但只有运行记录能显示这次输入实际引发了什么。

对于需要人类判断的任务，讲者在 [27:43](https://www.youtube.com/watch?v=vtugjs2chdA&t=1663s) 讨论人工标注与 LLM judge。代理评分器需要用人工判断校准，否则自动化只是规模化一个偏离目标的评分标准。

在 [31:06](https://www.youtube.com/watch?v=vtugjs2chdA&t=1866s)，他还描述让 coding agent 获取 trace、诊断失败并提出代码或提示修改的模式。修改仍可作为初稿交人审查。稍后的“每晚分析轨迹并更新指令”则是希望增加的能力，不能与当时已支持的交互反馈写入指令混为一谈。

## 异步运行之后，需要同步讨论与状态查看

长任务运行时，人通常会去做其他工作，因此需要任务列表和状态管理；结果返回后，又可能进入连续讨论。Harrison 在 [34:37](https://www.youtube.com/watch?v=vtugjs2chdA&t=2077s) 将两种模式放在同一产品中考虑。

聊天帮助表达修订意见，工作区则让人检查 Agent 已经改变的文件、报告或其他状态。只显示一句完成通知，无法替代产物查看；只有异步收件箱，也可能让几轮简短纠正变得低效。

这条讨论最后落在一个清楚的系统要求上：长期工作要有可持续保存的状态，关键过程要有可回看的记录，交接时要有可审查的结果。上下文、工具和界面围绕这些要求组织，才让“运行更久”转化为可继续协作的工作。

## 原文

- [Context Engineering Our Way to Long-Horizon Agents: LangChain's Harrison Chase — Training Data](https://www.youtube.com/watch?v=vtugjs2chdA)
