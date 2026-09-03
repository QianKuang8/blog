---
date: '2026-08-31T15:30:00+08:00'
lastmod: '2026-08-31T15:30:00+08:00'
title: '用 HTML 替代 Markdown：Coding Agent 的输出格式该升级了'
summary: "Claude Code 团队提出用 HTML 替代 Markdown 作为 agent 输出格式。核心不是技术炫技，而是信息密度、可读性和双向交互三个维度上，Markdown 已经跟不上 agent 的能力增长。"
description: "从 Claude Code 团队的 HTML 实践看 coding agent 输出格式的演进方向"
tags: ["agentic-coding", "context-engineering"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Thariq Shihipar（Anthropic Claude Code 团队）最近写了一篇 [Using Claude Code: The Unreasonable Effectiveness of HTML](https://claude.com/blog/using-claude-code-the-unreasonable-effectiveness-of-html)，主张用 HTML 替代 Markdown 作为 coding agent 的默认输出格式。这篇文章表面上是工具技巧分享，实际上触及了一个更根本的问题：当 agent 能力增长快于人类消化能力时，人机协作的瓶颈可能出在输出格式上。

## Markdown 的瓶颈不是语法，是信息密度

作者的核心观察是：Markdown 作为 agent 输出格式已经力不从心了。不是因为 Markdown 语法不好，而是 agent 生成的内容越来越复杂，spec、plan、code review 动辄上百行，纯文本格式下人的阅读意愿急剧下降。

> "I find it difficult to read a markdown file of more than a hundred lines. I certainly am not able to get anyone else in my organization to read it."

这个判断值得认真对待。很多团队在用 agent 生成 spec 或 plan 时都遇到过类似问题：agent 输出了详尽的方案，但没人真的从头到尾读完。问题不在内容质量，而在呈现形式。

HTML 在信息密度上的优势是结构性的：表格、CSS 布局、SVG 图表、可折叠区块、tab 导航，这些都是 Markdown 做不到或做得很别扭的事。作者举了一个有趣的例子——Claude Code 在 Markdown 里用 Unicode 字符来"模拟"颜色展示，这恰恰说明模型已经在试图突破格式限制。

## 双向交互是真正的差异化能力

文章列举了几个 HTML 的优势——信息密度、视觉清晰度、易于分享——但我认为最有价值的是**双向交互**。

传统的 agent 输出是单向的：agent 生成一个文件，人类阅读并决定下一步。但 HTML 可以嵌入滑块、旋钮、拖拽界面，让人类在 agent 的输出上直接操作，然后把调整结果导出为 prompt 或配置喂回 agent。

作者举的几个用例很有代表性：

- 用拖拽卡片界面重排 30 个 Linear ticket 的优先级，比在文本框里描述排序高效得多
- 为 system prompt 做一个左右分栏编辑器，左侧编辑 prompt 模板，右侧实时预览三组 sample input 的填充结果
- 调一个按钮动画参数时，用滑块实时调整，满意后一键复制参数

这些场景的共同点是：有些信息用文字描述效率极低，但用可视化交互表达很自然。HTML 在这里不只是更好的展示格式，而是开辟了一种新的人机协作模式。

## 这不是什么新发现，但时机对了

用 HTML 做 agent 输出并不新鲜。Claude Artifacts、v0 早就在做类似的事。但这篇文章有两个背景让它更有说服力：

第一，Claude Code 把 context window 扩到了 1M tokens。作者提到 HTML 比 Markdown 生成时间长 2-4x，token 用量也更高，但在百万 token 的 context window 下，这个代价变得可以接受。格式升级需要基础设施先到位。

第二，作者的使用场景不是一次性 demo，而是日常工作流。他把 HTML 用在 spec 探索、code review、PR 说明、研究报告等所有环节，甚至说自己"几乎不再使用 Markdown"。这种全面替代的实践比单点 demo 有更强的说服力。

## 务实的 trade-off

作者没有回避 HTML 的缺点。最实际的问题是**版本控制**：HTML diff 远比 Markdown 嘈杂，code review 时很难看出实际内容变化。这对任何需要在 git 里管理这些文件的团队都是真实的痛点。

另一个隐含的 trade-off 是**可编辑性**。作者自己也承认，他越来越少亲手编辑这些文件，而是让 Claude 来编辑。HTML 对人类手工编辑不友好，这意味着一旦走上 HTML 路线，你对 agent 的依赖会进一步加深。这不一定是坏事，但值得意识到。

生成时间也是现实约束。HTML 需要 2-4 倍的生成时间，在快速迭代场景下这个延迟可能不可忽略。不过随着模型推理速度持续提升，这个问题可能会自然缓解。

## 我的看法

这篇文章让我重新思考了一个问题：我们给 agent 的输出格式约束，是不是无意中限制了 agent 的表达能力？

在实际使用 coding agent 的过程中，我经常遇到 agent 输出了一大段 plan 或 analysis，但阅读体验很差的情况。以前我归因于 agent 的写作能力，现在想来可能是格式限制。同样的内容如果用带导航、带图表的 HTML 呈现，消化效率会高很多。

不过，HTML 作为通用 agent 输出格式还有一段路要走。最大的障碍不是技术，而是生态：IDE 里的 agent 输出、CI 报告、PR description 这些场景目前都假设输出是纯文本或 Markdown。HTML 目前更适合作为独立文档格式（spec、report、explainer），而不是嵌入现有工作流的通用输出。

作者给的起步建议很实在：不需要写 skill 或做模板，直接在 prompt 里说"make a HTML file"就行。从 spec 和 plan 开始试，先感受信息密度和可读性的差异，再决定要不要扩大使用范围。

## 原文

- [Using Claude Code: The Unreasonable Effectiveness of HTML](https://claude.com/blog/using-claude-code-the-unreasonable-effectiveness-of-html)
