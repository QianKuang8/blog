---
title: "Harness Engineering 阅读路径"
description: "从工具、权限、反馈、评估和可观测性，串起 Qian's blog 中关于 Harness Engineering 的文章。"
summary: "模型周围的系统怎样影响结果：约束怎样被读到，工具和权限怎样设计，反馈怎样让 Harness 持续改进。"
lastmod: '2026-10-27T16:03:41+08:00'
hideMeta: true
showToc: true
isCJKLanguage: true
---

模型能读写代码、调用工具以后，结果好坏越来越取决于它周围的系统：能读到哪些约束，能调用哪些工具、在什么权限下调用，修改以后能拿到什么反馈。Harness Engineering 讨论的就是这部分。这条路径的 16 篇文章先看为什么要在 Harness 上投入，再看工具和权限怎样设计，最后看反馈、观测和自进化怎样让 Harness 持续改进。

## 先分清几篇相近的文章

第一段的四篇都在回答“Harness 为什么重要”，路径末尾的三篇讨论自我改进：

| 文章 | 原文 | 回答的问题 |
| --- | --- | --- |
| [Building Effective Agents]({{< relref "/posts/building-effective-agents.md" >}}) | Anthropic，2024-12 | 工作流和 Agent 怎样区分，什么时候值得增加调用次数和自主性，工具接口怎样设计 |
| [长任务 Harness]({{< relref "/posts/harness-design-long-running-apps.md" >}}) | Anthropic，2026-03 | 一组实验：用独立的评价器检查生成结果、驱动返工，以及模型升级后怎样逐个移除组件 |
| [让 Agent 读取约束并验证运行结果]({{< relref "/posts/harness-engineering-leveraging-codex-in-an-agent-first-world.md" >}}) | Ryan Lopopolo（OpenAI），2026-02 | 一个从空仓库开始、坚持由 Codex 写代码的五个月项目：怎样让 Agent 看到运行行为、找到长期约束 |
| [Harness 与 SDD]({{< relref "/posts/harness-engineering-vs-sdd.md" >}}) | 何艺萍，2026-03 | 执行环境和规范各管什么：工具再齐全，也补不上缺失的业务语义 |
| [Agent 自进化的三类路径]({{< relref "/posts/a-taxonomy-of-self-evolving-agents.md" >}}) | Shilong Liu，2026-07 | 按反馈改写的对象，区分产物搜索、Harness 改进和模型学习 |
| [Agent 如何通过 Harness Engineering 改进自身]({{< relref "/posts/harness-engineering-for-self-improvement.md" >}}) | Lilian Weng，2026-07 | 从上下文管理到 Harness 代码，看失败证据、候选提案和回归验证怎样支持系统改进 |
| [Agent 自进化与 RSI]({{< relref "/posts/self-evolving-agents-rsi.md" >}}) | 周星星，2026-07 | 沿相近的分类看具体研究，重点是预算对等、留出任务和递归改进的证据 |

第一段先讲概念、再看案例，最后转到规范：Building Effective Agents 发表最早，给出基本概念；Anthropic 的长任务实验和 OpenAI 的 Codex 项目是两个具体案例，前者侧重评价器和返工，后者侧重让运行环境可读、可验证；何艺萍的文章放在最后，把注意力转到规范，说明缺少契约时，执行环境再完善，Agent 仍可能实现错。三篇自我改进文章放在路径末尾，先读分类，再看 Harness 修改怎样生成和验证，最后检查预算、迁移与递归证据。

## 路径怎样展开

**先理解 Harness 为什么重要。** 四篇见上表。读的时候可以留意一个共同点：这些组件都根据观察到的失败调整，模型变化以后也要复查。长任务实验在模型升级后逐个移除组件，再观察结果有没有变差；OpenAI 的项目把反复出现的审查意见写成可以执行的检查，减少人重复指出同一个问题。

**再看工具和权限。** Seeing like an Agent 用 Claude Code 的几个演进案例说明，工具要按模型的实际行为调整：提问做成独立工具，待办改成支持依赖的 Task，代码搜索从向量索引改为 Grep。Auto Mode 一篇讨论怎样用分类器承接一部分权限确认：常规动作先按规则放行，其余动作交给只看用户消息和工具调用的动作分类器判断；原文公开的数据显示，第二阶段减少误拦的同时，也放过了更多危险动作。Meta Muse 一篇把执行、凭证和授权拆到不同组件：Agent 在受限容器里执行，凭证服务和授权服务 Sentinel 放在容器外，一次网络请求获得 Sentinel 授权以后，才在出网时把替身换成真实凭证。从演示到 Skill 一篇比较 Codex 和 Claude 的录制功能：一次演示怎样写成 Skill，下次执行时 Skill、当前任务和产品提供的工具与权限怎样共同决定执行，以及录制的内容可能超出任务需要。

**最后看反馈、观测与成本。** AI 研发度量和 Routa 可视化两篇讨论怎样看清协作过程：前者主张结合规约、过程指标和验收结果来观察协作，后者把规范、评审触发器和 CI 放进同一个生命周期视图。Deep Agents 一篇是一个完整的调整案例：固定模型，从失败轨迹中找出重复问题，用中间件补上退出前的验证、环境信息和循环检测，再按阶段分配推理预算，Terminal Bench 2.0 得分从 52.8 提高到 66.5；原文没有把增益分到每项改动上。行为评估一篇用针对工具调用等中间动作的断言，检查这类改动有没有带来回归，并与端到端评测互补。Devin Fusion 一篇讨论双 Agent 的交接和成本：委派说明和返回结果要足以支撑执行和审查；执行交给更便宜的配置以后，规划、审查和返工的开销也要算进去，并和分数一起看。最后三篇讨论自我改进：先区分产物、Harness 与模型等优化对象，再由 Lilian Weng 的综述看上下文机制演化、失败归因与回归检查，最后讨论报告提分时怎样排除额外搜索预算和挑选任务带来的偏差。

读完这条路径，应该能回答三个问题：一次失败该通过补信息、补工具、补反馈还是收紧权限来处理；模型升级以后，哪些 Harness 组件应该重新检查甚至移除；一项 Harness 改动带来的提分，怎样排除预算和任务选择带来的偏差。

{{% reading_path %}}

## 继续探索

- [harness-engineering 标签]({{< relref "/tags/harness-engineering" >}})
- [agent 标签]({{< relref "/tags/agent" >}})
- [Agent 评估阅读路径]({{< relref "/topics/agent-evals.md" >}})：继续看评分方法、公开基准的误差和回归检查。
