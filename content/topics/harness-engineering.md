---
title: "Harness Engineering 阅读路径"
description: "从工具、权限、反馈、评估和可观测性，串起 Qian's blog 中关于 Harness Engineering 的文章。"
summary: "从工具、权限、反馈、评估和可观测性，串起 Qian's blog 中关于 Harness Engineering 的文章。"
hideMeta: true
showToc: true
isCJKLanguage: true
---

这条路径关注一个更工程化的问题：当模型已经能做很多事之后，怎样把它放进一个可观察、可约束、可迭代的系统里。

## 先理解 Harness 为什么重要

- [长任务 Harness：把生成、验收与返工连成循环]({{< relref "/posts/harness-design-long-running-apps.md" >}})：从长时间运行任务理解 harness 的控制面。
- [Harness Engineering：让 Agent 读取约束并验证运行结果]({{< relref "/posts/harness-engineering-leveraging-codex-in-an-agent-first-world.md" >}})：看 harness 如何改变团队协作和交付方式。
- [Harness 与 SDD：让任务约束能被找到、执行和验证]({{< relref "/posts/harness-engineering-vs-sdd.md" >}})：把 harness 和规格驱动开发放在同一张图里看。

## 再看工具和权限

- [Seeing Like an Agent：工具如何随模型能力调整]({{< relref "/posts/claude-code-seeing-like-an-agent.md" >}})：理解 action space 为什么要贴着模型的实际使用方式设计。
- [Claude Code Auto Mode：如何判断动作是否越过授权]({{< relref "/posts/claude-code-auto-mode.md" >}})：从权限分类器看 agent 控制系统。
- [从一次演示到可复用 Skill：Codex Record & Replay 与 Claude Record a Skill]({{< relref "/posts/from-demonstration-to-skill.md" >}})：看录制证据怎样写成方法，以及 Skill、当前任务、工具与权限怎样共同决定执行。

## 最后看反馈、观测与成本

- [AI 研发度量：把规约、执行过程与验收结果连起来]({{< relref "/posts/ai-native-software-engineering-observability-control.md" >}})：把 trace、可控性和组织转型放在一起看。
- [Deep Agents 提分：从失败轨迹调整 Harness]({{< relref "/posts/improving-deep-agents-with-harness-engineering.md" >}})：理解失败分析和评估闭环。
- [Harness Engineering：用行为评估守住 Agent 的关键动作]({{< relref "/posts/harness-engineering-behavioral-evaluations.md" >}})：理解行为断言能证明什么，以及它怎样与端到端评测共同检查回归。
- [Uber 软件工厂：围绕有效交付优化 Agent 成本]({{< relref "/posts/uber-efficient-software-factory.md" >}})：看模型分工与工具流程的改进，怎样用同一组真实任务检查质量和成本。
- [Devin Fusion：双 Agent 的分工与成本]({{< relref "/posts/cognition-local-fusion.md" >}})：聚焦规划与执行的交接，理解上下文分工、审查证据和任务成本之间的关系。

## 继续探索

- [harness-engineering 标签]({{< relref "/tags/harness-engineering" >}})
- [agent 标签]({{< relref "/tags/agent" >}})
