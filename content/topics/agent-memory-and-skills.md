---
title: "Agent 记忆与 Skill 阅读路径"
description: "从 Computer History、文件上下文和桌面演示，读到 Skill 的组织、复用与评估。"
summary: "围绕找回工作与复用方法，分清活动历史、当前上下文和 Skill 各自承担什么作用。"
lastmod: "2026-10-26T16:46:44+08:00"
hideMeta: true
showToc: true
isCJKLanguage: true
---

午饭后怎样接着做上午的工作？每周重复的操作，又怎样变成下次可以调用的方法？这条路径的 10 篇文章先看 Agent 怎样找回工作线索，再看方法怎样写成 Skill、组织和复用，最后看怎样检查一份 Skill 是否有效。

## 先分清几篇相近的文章

第一段的三篇都在讲怎样保存之前的工作、需要时再找回，保存的东西和找回的方式各不相同：

| 文章 | 原文 | 回答的问题 |
| --- | --- | --- |
| [从电脑活动到下一步行动]({{< relref "/posts/from-activity-to-action.md" >}}) | 原创，2026-09 | Computer History 怎样把获准的电脑活动整理成可读的摘要，作为找回工作的索引 |
| [文件系统与 Agent 上下文]({{< relref "/posts/filesystems-for-context-engineering.md" >}}) | LangChain，2025-11 | 工具结果、计划和中间产物存进文件以后，怎样按需搜索和读取 |
| [从压缩历史到按需恢复]({{< relref "/posts/from-compaction-to-context-recovery.md" >}}) | 原创，2026-09 | Codex 的切窗实验和传统压缩有何不同：换窗以后先读笔记接上进度，需要细节时再查询历史 |

三篇都把保存和找回分开处理：Computer History 用 History 摘要指路，再回到原始文档核对当前状态；文件系统一篇把完整材料留在文件里，并指出写进文件只解决了信息可用性的一部分，还要能找到位置、把合适的内容读回当前上下文；压缩实验一篇用笔记记下目标、约束和进度，帮模型接上任务，缺少细节时再沿笔记中的引用查历史。

后两段的 Skill 文章可以按一份 Skill 的生命周期来读：从哪里来、怎样组织和复用、改了以后怎样确认有效。

## 路径怎样展开

**先看工作线索怎样找回。** 三篇见上表。Computer History 和压缩实验都是站内原创：前者整理用户在多个 app 里的获准活动，用户提问以后，由 Agent 读取 History 并打开原始来源；后者处理 Agent 在同一个 session 里积累的对话和工具记录，切换上下文窗口以后按需读回。

**再看方法怎样保存和复用。** 从演示到 Skill 一篇讲 Skill 的来源，比较 Codex Record & Replay 与 Claude Record a Skill：用户演示一次，两边分别留下结构化事件或图文关键帧，Agent 再区分固定的方法和本次的数据，写成 `SKILL.md`，下次执行时重新规划，不回放旧坐标；文章也提醒，录制下来的材料可能包含任务以外的信息。Claude Code 团队的实践讲 Skill 的组织和分发：按工作类型划分，description 写明什么时候使用，需要跨运行保留的数据放在稳定的目录，不放在升级时可能被清理的技能目录里；小团队把 Skill 放进仓库，规模大了用插件市场分发。Matt Pocock 的五个 Skill 依次负责追问需求、写 PRD、拆分任务、TDD 和架构改进，解读按各步的交接产物把它们串起来，也提醒小修复不必走完整套流程。按任务选择 Skill 是一份个人清单：前三项是现成的 Skill（Skill Creator、Superpowers、Grill Me），第四项是自建本地仓库索引 Skill 的需求记录。

**最后检查方法是否有效。** Astra 一篇讨论换模型以后怎样审查已有指令：触发范围是否过宽，规则是否出现在需要它的地方，完成标准是否写清。skill-creator 一篇把触发评估和产物评估分开，产物评估把用了 Skill 的运行和基线比较：新建时是不用 Skill 的运行，修改旧 Skill 时也可以是旧版。Warp 一篇展示反馈怎样变成 Skill 的修改：一个 Skill 执行任务，另一个定期归纳反馈、提出修改，经人审核后合并；原文没有给出改进前后的量化对照。

读完这条路径，应该能回答三个问题：找回工作时，哪些信息可以直接用，哪些必须回到原始来源核对；把一次操作经验写成 Skill 时，哪些是固定的方法，哪些是每次都要确认的变量；一份 Skill 改了以后，怎样确认它在该触发时触发，并且改善了结果。

{{% reading_path %}}

## 继续探索

- [Context Engineering 阅读路径]({{< relref "/topics/context-engineering.md" >}})：继续看信息选择、压缩、隔离与缓存。
- [Harness Engineering 阅读路径]({{< relref "/topics/harness-engineering.md" >}})：继续看工具、权限、验证与运行反馈。
- [Agent 评估阅读路径]({{< relref "/topics/agent-evals.md" >}})：继续看 Skill 之外的评估方法与回归检查。
