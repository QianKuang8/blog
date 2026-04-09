---
date: '2026-04-09T23:24:00+08:00'
lastmod: '2026-04-09T23:24:00+08:00'
title: 'How to Kill the Code Review：AI 时代的人类审查应从 diff 前移到规范'
summary: "解读《How to Kill the Code Review》：这篇文章最有刺激性的地方，不是喊“代码评审已死”，而是提出一个更值得讨论的判断：当 agent 成为主要产码者之后，人类最有价值的审核点会从 PR diff 前移到 specs、约束和验证规则。"
description: "从 Latent Space 这篇文章看 AI 时代代码审查为何需要从读 diff 转向定义规范与验证"
tags: ["agentic-coding"]
origStatus: "available"
author: "Qian"
isCJKLanguage: true
showToc: true
---

这篇 [How to Kill the Code Review](https://www.latent.space/p/reviews-dead) 标题很激进，但我觉得它真正值得看的地方，不是“代码评审会不会死”这个口号，而是它试图重新定义：**在人和 agent 协作的软件生产线上，人类最该在哪个节点介入。**

文章的核心判断很明确。既然 AI 已经显著放大了产码速度，而人工 review 的吞吐没有同步增长，那么继续把人类主要时间花在线性读 diff 上，很可能会越来越不划算。

## 这篇文章真正攻击的，不是 review 本身，而是 review 所在的位置

我觉得这点很关键。很多人看到标题会本能地反对，觉得作者是不是要取消质量保障。但如果仔细看，会发现它并不是说不要验证，而是说不要把“人类逐行审 PR”当成默认主防线。

因为在 agent 时代，PR 数量、变更规模和修改速度都在上涨，而人的注意力仍然是线性的。你当然还能坚持人工 review，但结果往往会变成：大家越来越疲惫，review 越来越表面，真正的质量控制却没有同步变强。

所以作者的矛头其实是指向一个更根本的问题：**质量门到底应该放在哪。**

## 从 review code 转向 review intent，是这篇文章最重要的提议

文章最有启发的一点，是把人类的审核职责前移到 spec、constraints 和 acceptance criteria。

也就是说，人更应该审查的是：

- 我们到底要解决什么问题
- 哪些边界不能碰
- 什么结果算通过
- 哪些验证脚本和测试必须成立

而不是等 agent 写完几百行 diff 之后，再靠人肉逐段解释“这段是不是看起来还行”。这个转向我认为非常有价值，因为它更符合人类和 agent 的能力分工。人更擅长判断目标和约束，机器更擅长在约束内高频迭代。

## 真正可行的替代物，不是“让另一个 AI 再看一遍”，而是分层验证

文章里提出的 Swiss-cheese 模型我很认同。没有任何单一措施能保证 agent 输出总是可靠，所以更现实的做法是堆叠多层验证：

- 多 agent 竞争，比较不同方案
- 确定性 guardrails，比如 tests、type checks、linters
- 人类事先定义 acceptance criteria
- 权限系统限制 agent 触达范围
- 用独立 agent 做 adversarial verification

这背后的思想非常重要：不要再把“判断代码好不好”寄托在一次 review 上，而是要把可靠性拆成多个可执行的验证层。某种意义上，这和现代线上系统靠 feature flag、rollback、监控而不是单点审批来保证稳定性，是同一种工程哲学。

## 这篇文章的风险点也很明显：它默认组织已经有了更强的 spec 能力

我同意文章的大方向，但也觉得它隐含了一个前提：团队必须先学会写更好的 spec，定义更强的测试和 guardrails。

否则，“把 review 前移”很容易退化成另一种形式的口号。因为如果 specs 很模糊、验收标准也不清楚，那最后你还是只能靠人去看 diff、凭经验兜底。换句话说，代码评审不会自动消失，它只会在上游能力不足时重新回来。

所以这篇文章真正提出的，不只是一个结论，而是一套对组织能力的要求：如果你想减少人工读代码，就得先把规范、测试、权限和验证层建设起来。

## 我的看法：代码评审不会马上消失，但它的重心一定会前移

我读完之后的感觉是，文章虽然故意把话说得很重，但它抓住的趋势是对的。

AI 时代最稀缺的人类劳动，不再应该是“慢慢读每一行 agent 产出的代码”，而更应该是“定义正确的问题、边界和验证方式”。在这套新分工里，review 当然不会彻底消失，但它会越来越少地停留在 diff 上，越来越多地转向 spec、policy 和 verification artifacts。

所以如果要总结这篇文章，我会说：它最重要的价值，不是宣布 code review 已死，而是逼我们重新思考质量门的位置。**真正适合 agent 时代的人类审核，不该主要发生在代码产出之后，而应该尽可能发生在代码生成之前。**

## 原文

- [How to Kill the Code Review](https://www.latent.space/p/reviews-dead)
