---
date: '2026-06-05T21:20:00+08:00'
lastmod: '2026-06-05T21:20:00+08:00'
title: 'Prompt Engineering 不是咒语，而是把意图说清楚的工程接口'
summary: "解读 Claude 官方的 prompt engineering 最佳实践：这篇文章真正有价值的地方，是把提示词从技巧清单拉回到“清晰表达意图、约束和验收标准”的工程问题。"
description: "从 Claude 官方指南看 prompt engineering 在 context engineering 和 agentic workflow 中的基础作用"
tags: ["prompt-engineering", "context-engineering"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Claude 官方这篇 [Prompt engineering best practices](https://claude.com/blog/best-practices-for-prompt-engineering) 值得读，不是因为里面有某个神奇句式，而是因为它把 prompt engineering 讲回了一个很朴素的问题：你到底有没有把任务、背景、约束和成功标准讲清楚。

这点在今天反而更重要。现在大家更常讨论 context engineering、agent harness、multi-agent，prompt engineering 容易被看成上一代模型时代的技巧。但文章开头就把两者关系说清楚了：prompt engineering 是 context engineering 的基本构件。一个 agent 的上下文里有系统指令、工具结果、文件、历史轨迹，但每一次让模型采取行动的语言接口，仍然是 prompt。

## 好 prompt 首先是减少歧义

文章最基础的建议其实很硬：be explicit and clear、provide context and motivation、be specific、use examples、allow uncertainty。翻译成工程语言，就是不要假设模型会读懂你的隐含意图。

比如“Create an analytics dashboard”只是说了任务对象，没有说功能密度、交互深度和质量预期。文章给出的改写会明确要求包含尽可能多的相关功能和交互，并要求超过基础实现。这个例子好在它不是加花活，而是补上了验收标准。

同样，“不要用 bullet points”这种负面约束也不如解释偏好的原因。文章的例子是说明自己更喜欢自然段，因为阅读起来更连贯、更像对话。我的理解是，模型不是简单执行正则规则，它会根据上下文推断一类相邻选择。解释动机能让它在没有完全覆盖到的场景里做更接近用户意图的判断。

“允许不确定”也是一个容易被低估的建议。文章建议在任务里明确写出如果数据不足就说不足，不要猜。它对应的不是文风问题，而是可靠性问题：很多幻觉不是模型不知道，而是任务接口默认鼓励它把答案补齐。

## 高级技巧应该是按需升级，不是默认堆料

文章后半部分讲 prefill、chain of thought、输出格式控制、prompt chaining、XML tags 和 role prompting。这里我觉得最重要的判断是：这些技巧不是越多越好，而是每一种都解决一个具体失败模式。

需要严格 JSON 时，prefill 可以让模型从 `{` 开始，减少“Here is the JSON”这种前言。需要多步分析时，可以用 extended thinking 或手写 chain of thought。任务太复杂、单次输出不稳定时，prompt chaining 把一个大任务拆成多个小阶段，并在中间加入检查和反馈。

但文章也提醒，XML tags 和重度 role prompting 在现代模型里没有以前那么必要。结构清楚的标题、空行和直白语言，很多时候已经足够。角色设定也不该把模型绑死成“世界级专家且永不犯错”这种戏剧化人格；更好的方式通常是直接说明分析视角，比如“关注风险承受能力和长期增长潜力”。

这背后的原则是：prompt engineering 的目标不是展示技巧，而是降低任务失败率。每增加一层格式、示例或角色，都应该能解释它解决了什么问题。

## 真正的取舍在上下文成本和任务聚焦

文章有一节专门谈长内容，这部分和 context engineering 连接得最紧。示例、详细约束、多轮 chaining 都会占上下文，它们不是免费的。现代模型的长上下文能力确实更强，但文章仍然建议把复杂任务拆成更聚焦的小块。

这不是因为模型“装不下”，而是因为边界清楚的任务更容易做出高质量结果。一个 prompt 同时要求研究、判断、写作、校对、格式化，模型当然可能完成，但每个阶段的目标会互相干扰。拆开之后，每一步的输入和输出都更明确，也更容易验收。

我觉得这是这篇文章最有工程味的地方。它没有把 prompt 当作一次性的魔法文本，而是把它放进一个可迭代系统里：先写清楚，观察输出，定位失败模式，再决定是补背景、给例子、控制格式，还是拆成链式流程。

## 我的判断：prompt 是人和 agent 之间的 API

如果只把 prompt engineering 理解成“怎么问模型”，它会显得很轻。但如果把 prompt 看成人和 agent 之间的 API，事情就不一样了。

一个好 API 需要清楚的输入、输出、约束、错误处理和调用语义。一个好 prompt 也是一样：它要说明任务是什么，为什么做，输出长什么样，遇到不确定怎么办，哪些质量标准不能妥协。

所以我不觉得 prompt engineering 会因为模型变强而消失。相反，agent 越能执行真实任务，prompt 越像权限边界、验收标准和协作协议。真正会过时的是那些玄学化的固定咒语，不是清楚表达意图这件事。

这篇文章可以当作一个提醒：在追逐更复杂的 harness 之前，先把最基础的人机接口写清楚。很多失败并不需要新架构，可能只是 prompt 里缺了一句“如果证据不足，请停下来说明不足”。

## 原文

- [Prompt engineering best practices](https://claude.com/blog/best-practices-for-prompt-engineering)
