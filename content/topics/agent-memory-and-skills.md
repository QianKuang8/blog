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
- [How agents can use filesystems for context engineering：文件系统如何成为 Agent 的外部记忆]({{< relref "/posts/filesystems-for-context-engineering.md" >}})：补上存储与读取机制，理解计划、材料和中间结果怎样留在文件中供 Agent 按需读取。

## 再看方法怎样保存和复用

- [从一次演示到可复用 Skill：Codex Record & Replay 与 Claude Record a Skill]({{< relref "/posts/from-demonstration-to-skill.md" >}})：用一次填报演示，理解录制证据、固定方法与每次变化的数据怎样分开。
- [Claude Code 怎么用 Skills：扩展点要按工作类型分层]({{< relref "/posts/claude-code-how-we-use-skills.md" >}})：从团队使用经验看 Skill 的任务边界、按需加载与分发方式。

## 最后检查方法是否有效

- [skill-creator 的真正变化：从脚手架变成评估闭环]({{< relref "/posts/anthropic-skill-creator-breakdown.md" >}})：继续追问 Skill 该触发时能否触发、执行后是否改善结果，以及怎样根据失败改进它。

## 继续探索

- [Context Engineering 阅读路径]({{< relref "/topics/context-engineering.md" >}})：继续看信息选择、压缩、隔离与缓存。
- [Harness Engineering 阅读路径]({{< relref "/topics/harness-engineering.md" >}})：继续看工具、权限、验证与运行反馈。
