---
date: '2026-06-05T21:30:00+08:00'
lastmod: '2026-06-05T21:48:35+08:00'
title: 'skill-creator 的真正变化：从脚手架变成评估闭环'
summary: "解读 Riba 对 Anthropic skill-creator 的拆解：更新后的 skill-creator 不只是生成 SKILL.md，而是把意图捕获、测试、评估、描述优化和基准比较连成了一个自我改进系统。"
description: "从 skill-creator 的 Draft-Test-Evaluate-Improve 流程看 Agent Skills 的触发、评估、description 优化和元技能设计"
tags: ["agent", "harness-engineering"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Riba 这篇 [拆解 Anthropic 的 skill-creator](https://blog.riba2534.cn/blog/2026/%E6%8B%86%E8%A7%A3anthropic%E7%9A%84skill-creator-ai-agent%E7%9A%84%E6%8A%80%E8%83%BD%E5%B7%A5%E5%8E%82%E6%98%AF%E6%80%8E%E4%B9%88%E8%BF%90%E8%BD%AC%E7%9A%84/) 很值得读，因为它不是泛泛介绍 Skills，而是把 skill-creator 这个“造 Skill 的 Skill”拆成了一个评估系统来看。

文章最重要的判断是：新版 skill-creator 已经不只是模板生成器。它从“问几个问题，生成 SKILL.md 初稿”，变成了 Draft-Test-Evaluate-Improve 的闭环，有评估 agent、基准测试、description 优化循环和交互式审查仪表盘。

## Skill 的难点不在写，而在是否稳定触发和有效完成

写一份 SKILL.md 并不难。难的是它该触发时会不会触发，不该触发时会不会乱触发，触发后是否真的改善任务结果。文章说得很实在：这些问题靠手动调试很难回答。

这也是 skill-creator 改版的核心动机。一个 skill 如果只是 markdown，它很容易变成“看起来有用”的文档；但如果没有测试和评估，你不知道它在真实任务中到底有没有发挥作用。

## Draft-Test-Evaluate-Improve 是元技能的关键

文章拆出的工作流包括 Capture Intent、Draft、Test、Evaluate、Improve。Capture Intent 先问清楚 skill 做什么、什么 prompt 应该触发、输出格式是什么、是否需要测试。Draft 阶段强调 description 要稍微积极一点，因为 Claude 有 undertrigger skills 的倾向。

Test 和 Evaluate 是新版真正强的地方。评估不只是看输出有没有生成，而是读取 transcript、检查输出文件、逐条验证断言，还会提取隐含声明。文章举的例子很好：如果断言只是“文件包含公司名称”，但整个文件是乱码，不能因为碰巧包含了公司名就算通过。

Improve 阶段也强调不要针对测试样例过拟合，而要从失败里泛化规律。这个原则很重要，因为 skill 面对的是未来任务分布，不是当前几个例子。

## 三个评估 Agent 把“好不好”拆开了

文章详细讲了 Grader、Comparator、Analyzer 三个 agent。Grader 做断言评级和证据检查；Comparator 做盲测 A/B，对比 with_skill 和 without_skill；Analyzer 识别跨运行模式。

这套设计的价值在于把不同评价问题拆开。一个输出是否满足断言、两个输出哪个更好、多次运行暴露了什么模式，本来就是不同层次的问题。混在一个评审 prompt 里，很容易变成主观印象。

我尤其喜欢文章提到的“评估评估本身”。弱断言上的 PASS 会制造虚假信心。很多 AI 工作流失败，不是因为没有评估，而是因为评估标准太弱。

## description 优化是 Skill 触发的核心工程

Skill 的 description 是给模型看的，它决定什么时候加载这个 skill。文章提到优化循环会分 train/test，改进模型看不到 test 结果，最终选 test 得分最高的 iteration，而不是最后一轮。这已经很接近机器学习式的调参方法。

我的理解是，description 不是说明书，而是路由器。写得太窄会 undertrigger，写得太宽会乱触发；写太多具体例子可能过拟合，写得太抽象又可能不落地。用评估循环优化 description，比凭感觉改 prompt 靠谱得多。

## 我的判断：skill-creator 是 harness engineering 的缩影

这篇文章真正有意思的地方在于自我参考性：Agent 用 skill-creator 创建 skill，再用评估 agent 测试 skill，再用优化循环改进 description。它展示的是一种更一般的模式：把 Agent 的经验资产纳入可测试、可比较、可迭代的工程循环。

所以 skill-creator 不只是“技能工厂”，更像是一个小型 harness：有输入意图、有生成器、有评估器、有基准、有反馈、有版本选择。未来真正可靠的 Agent 扩展，应该都会往这个方向走，从一次性 prompt 变成持续演化的系统资产。

## 原文

- [拆解 Anthropic 的 skill-creator：AI Agent 的技能工厂是怎么运转的](https://blog.riba2534.cn/blog/2026/%E6%8B%86%E8%A7%A3anthropic%E7%9A%84skill-creator-ai-agent%E7%9A%84%E6%8A%80%E8%83%BD%E5%B7%A5%E5%8E%82%E6%98%AF%E6%80%8E%E4%B9%88%E8%BF%90%E8%BD%AC%E7%9A%84/)
