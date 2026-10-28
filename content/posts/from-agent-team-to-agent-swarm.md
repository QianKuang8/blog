---
date: '2026-10-28T15:21:49+08:00'
lastmod: '2026-10-28T15:25:00+08:00'
title: "周星星谈 Agent Swarm：并行之后，怎样可靠地整合结果"
summary: "多 Agent 能同时展开工作，但交付质量还取决于结果交接、共享决策和验收。结合原文与 MiniMax、Cursor、Kimi、Apodex 的一手材料，解释运行时管理、上下文分工和编排训练分别解决什么问题。"
description: "从任务产物、上下文分工、状态机、关键路径与独立验证，解读 Agent Team 到 Agent Swarm 的工程取舍。"
tags: ["agent", "harness-engineering", "context-engineering"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

多个 Agent 同时查资料容易理解；同时写一篇文章、修改一个代码库，最后怎样得到一致的结果？周星星的《Multi-Agent 的新趋势：从 Agent Team 到 Agent Swarm》围绕这个问题梳理了不同系统的尝试。本文依据[青稞社区转载](https://qingkeai.online/blog/%20Multi-Agent-form-Agent-to-Swarm)，并回查其中四份一手材料，重点讨论并行产出之后的交付。

这里不把 Team 与 Swarm 当作严格的技术分界。判断一套方案时，更有用的是问：哪些工作可以独立进行，哪些决定必须共享，谁负责确认最终结果。

## 拆任务时，一并设计交付物

原文用 EvoMap 的实验提醒读者：子任务中得到的正确结果，也可能在报告和汇总时丢失。这项对照同时改变了任务粒度与汇总方式，适合提示信息传递风险，不能把全部收益归因于某一个环节。

由此可以提出一个设计原则：先区分需要原样保留的数据，与需要重新组织的解释。假设任务是核对一批 API，每个子任务可以交付接口标识、字段、证据链接与未确认项。程序负责按标识收集、检查缺项；模型再解释差异。这里的 API 场景是说明性例子，并非原文实验。

如果交付物是一篇文章，事实一致、论证顺序与语气仍需要编辑判断。结构化保存能减少中途改写，却不能自动完成内容整合。因此拆分方案要同时说明“交什么”和“谁来整合”，只规定角色名称还不够。

## 上下文隔离以后，共享什么

[Cursor 的复盘](https://cursor.com/blog/agent-swarm-model-economics)采用任务树：planner 负责拆解，worker 聚焦局部实现。每个角色只保留自己负责范围的上下文。Cursor 将上下文效率视为系统能够扩展的一种可能解释。

![单 Agent 遍历整棵任务树并累积上下文；分层方案中，planner 保留目标与子任务，subplanner 保留负责的子树，worker 聚焦一个任务切片。](/images/from-agent-team-to-agent-swarm/decomposing-work.png)

*图 1：原图，来源：[Cursor](https://cursor.com/blog/agent-swarm-model-economics)。对照左右两侧的上下文范围：职责拆分也在减少每个角色需要持续携带的信息。这是机制示意图。*

隔离之后仍要传递全局约束。Cursor 描述过两个 planner 对同一概念作出不同设计的情况，并要求委派的子树避免重复决定同一个问题。对工程实现而言，可以据此先检查接口约定由谁决定，再安排各模块的实现；否则各模块单独完成，也可能无法共同工作。

交接材料还应保留回查入口。摘要用于快速定位，文件和来源用于核对细节。这与[文件系统承接上下文]({{< relref "filesystems-for-context-engineering.md" >}})讨论的是同一个问题：保存材料之后，还要让下一位执行者知道何时、去哪里读取。

## 调度状态交给运行时

[MiniMax 的设计说明](https://www.minimax.io/blog/minimax-agent-team-long-running-1779893953)将工作分给 Leader、Worker 和 Verifier，并用 Team Engine 状态机管理任务。任务经过 producing、verifying、done；验证失败会重新唤醒产出节点继续修改。运行中的节点也可以接收补充信息。

这个区分很实用：Worker 返回一段文字，表示它停止了当前执行；系统还需要单独记录结果是否通过验收。模型可以解释失败和提出修订，运行时负责保存状态并按规则推进，减少仅凭一句“已完成”就结束任务的情况。

代价也要计入计划。MiniMax 将交接、共享和汇总分别列为成本。我的归纳是，扩大并发前应先观察结果接收与验收是否已经积压；增加产出者会进一步放大这些环节的工作量。

## 学习编排，优化最慢的分支

[Kimi K2.5 技术报告第 3 节](https://arxiv.org/html/2602.02276v1)介绍了 PARL：冻结子 Agent，只训练编排器。训练初期用辅助奖励鼓励尝试并行并完成子任务，再逐渐将这些奖励的权重降到零，让最终策略围绕任务结果优化。

报告还以 critical steps 衡量关键路径：每一阶段计入主 Agent 的步数，再加上并行子任务中最长的分支。它是时间成本的代理指标，不是实际耗时或总 token 数。

用一个假设例子理解：主 Agent 派活用 1 步，三个分支分别用 5、8、20 步，该阶段记 21 个关键步。继续增加几个很快的分支，并不会缩短那条 20 步的路径。工程上需要同时记录等待时间、总消耗和最终质量，才能判断并行带来的收益。

训练可以改善“何时拆、怎样拆”的判断，任务状态、产物保存和失败恢复仍需要执行环境承接。这也是[自进化分类]({{< relref "a-taxonomy-of-self-evolving-agents.md" >}})中区分执行方法与模型学习的意义：两种改进作用于不同对象。

## 探索可以分叉，验收需要证据

[Apodex 的 heavy-duty 模式](https://www.apodex.com/blog/apodex-1.0)让专门的 Agent 异步提交报告，汇入共享报告池；出现冲突时交给验证角色，探索结束后由 global verifier 检查汇集的证据。它强调以证据支持程度作判断，避免仅靠答案票数决定结果。

这对开放研究尤其有启发。多个答案可能引用同一份材料，重复出现并没有增加独立证据；保留来源和推导过程，才便于检查分歧出在哪里。

验收手段也应按产物选择。LLM reviewer 可以查找遗漏与矛盾，但仍可能误判；测试检查既定用例，形式验证检查形式化命题。这里是对验证方式的区分，不把某一种通过信号扩展为对所有结论的保证。

据此搭建一个小规模系统时，可以先固定子任务交付格式、共享决策和验收条件，再观察失败发生在执行、交接还是整合阶段。只有这些失败能够定位，并发规模的增加才有明确的改进依据。

## 延伸阅读

- 周星星：[知乎原文](https://zhuanlan.zhihu.com/p/2069524382196691517) · [青稞社区转载：Multi-Agent 的新趋势：从 Agent Team 到 Agent Swarm](https://qingkeai.online/blog/%20Multi-Agent-form-Agent-to-Swarm)。本文读取的是 2026 年 8 月 15 日的转载页。
- [MiniMax Agent Team: Built for Long-Running Tasks and Continuous Evolution](https://www.minimax.io/blog/minimax-agent-team-long-running-1779893953)
- [Cursor: Agent swarms and the new model economics](https://cursor.com/blog/agent-swarm-model-economics)
- [Kimi K2.5: Visual Agentic Intelligence，v1，第 3 节](https://arxiv.org/html/2602.02276v1)
- [Apodex-1.0：Heavy-duty mode 与 global verification](https://www.apodex.com/blog/apodex-1.0)
