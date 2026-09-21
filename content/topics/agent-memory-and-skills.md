---
title: "Agent 记忆与 Skill 阅读路径"
description: "从 Computer History、文件上下文和桌面演示，读到 Skill 的组织、复用与评估。"
summary: "围绕找回工作与复用方法，分清活动历史、当前上下文和 Skill 各自承担什么作用。"
hideMeta: true
showToc: true
isCJKLanguage: true
---

午饭后怎样接着做上午的工作？每周重复的操作，又怎样变成下次可以调用的方法？这条路径从两个桌面工作场景出发，先看 Agent 如何取得工作线索，再看方法怎样写成 Skill、怎样检查它是否有效。

## 先看工作线索怎样找回

- [从电脑活动到下一步行动：Computer History]({{< relref "/posts/from-activity-to-action.md" >}})：看获准活动怎样整理成 History，以及 Agent 为什么还要回到原始来源核对当前状态。
- [文件系统与 Agent 上下文：保存、检索和重新读取]({{< relref "/posts/filesystems-for-context-engineering.md" >}})：补上存储与读取机制，理解计划、材料和中间结果怎样留在文件中供 Agent 按需读取。

## 再看方法怎样保存和复用

- [从一次演示到可复用 Skill：Codex Record & Replay 与 Claude Record a Skill]({{< relref "/posts/from-demonstration-to-skill.md" >}})：用一次填报演示，理解录制证据、固定方法与每次变化的数据怎样分开。
- [Claude Code 团队的 Skills 实践：把反复踩坑的经验变成任务包]({{< relref "/posts/claude-code-how-we-use-skills.md" >}})：从团队使用经验看 Skill 的任务边界、按需加载与分发方式。

## 最后检查方法是否有效

- [GPT-6 Astra 的指令整理：Skill 触发、上下文与完成边界]({{< relref "/posts/rethinking-skills-and-prompts-for-gpt-6-astra.md" >}})：看模型升级后如何重新检查触发范围、材料加载时机与完成标准。
- [拆解 skill-creator：分别验证触发、产物与改进效果]({{< relref "/posts/anthropic-skill-creator-breakdown.md" >}})：继续追问 Skill 该触发时能否触发、执行后是否改善结果，以及怎样根据失败改进它。
- [Warp 如何把团队反馈变成 Agent 的 Skill 改进]({{< relref "/posts/how-warp-builds-self-improving-agents-on-claude.md" >}})：看 Issue 与 PR 中的反馈如何转成可审查的 Skill 修改，以及合并后还需要验证什么。

## 继续探索

- [Context Engineering 阅读路径]({{< relref "/topics/context-engineering.md" >}})：继续看信息选择、压缩、隔离与缓存。
- [Harness Engineering 阅读路径]({{< relref "/topics/harness-engineering.md" >}})：继续看工具、权限、验证与运行反馈。
