---
title: "Agent 评估阅读路径"
description: "从评分方法、公开基准到开发流程中的回归检查，串起 Qian's blog 中关于 Agent 评估的文章。"
summary: "分数来自什么任务、依据什么证据判分、能支持什么结论，以及评估怎样进入日常修改。"
lastmod: "2026-10-26T16:30:41+08:00"
hideMeta: true
showToc: true
isCJKLanguage: true
---

改了一条提示，Agent 的任务成功率提高了，这个改动能不能上线？要回答这个问题，需要知道分数来自哪些任务、评分器检查了什么证据、重复运行时结果是否稳定。这条路径的 7 篇文章先看评估方法，再看公开基准和产品自建评测各自能测出什么，最后看评估怎样进入开发流程：复查线上失败、守住关键行为、改进 Skill。

{{% reading_path %}}

## 继续探索

- [evals 标签]({{< relref "/tags/evals" >}})
- [Harness Engineering 阅读路径]({{< relref "/topics/harness-engineering.md" >}})：继续看评估结果怎样用来调整工具、反馈与执行流程。
