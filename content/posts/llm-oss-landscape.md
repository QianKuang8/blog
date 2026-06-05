---
date: '2026-06-05T21:28:00+08:00'
lastmod: '2026-06-05T21:28:00+08:00'
title: 'Agentic AI Landscape：看生态图要先看分层'
summary: "解读 antgroup/llm-oss-landscape：这个仓库的价值不只是收集项目，而是把 Agentic AI 生态拆成 Agent Infra、Model Infra 和 Large Models 三层，方便判断项目所在位置。"
description: "从 Agentic AI Landscape and Trends 看开源项目生态、Agent Infra、Model Infra 和大模型基础层"
tags: ["行业动向", "agent"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

[antgroup/llm-oss-landscape](https://github.com/antgroup/llm-oss-landscape) 这个仓库适合当作 AI 开源生态的导航页。它的价值不只是列项目，而是用分层方式组织项目：Agent Infra、Model Infra、Large Models。

这三个层次很重要。Agent Infra 组织应用、框架、运行时和工具生态；Model Infra 覆盖数据、训练、服务和部署栈；Large Models 则是上层能力的基础。看清一个项目属于哪一层，比单纯看 stars 更有意义。

## 生态图不是百科全书，而是代表性项目索引

仓库 README 说，它强调当前生态中有代表性的项目，而不是试图覆盖所有项目。这是合理的。AI 生态变化太快，如果追求全量，维护成本会很高，也容易变成噪音。

一个好的 landscape 应该帮助读者回答几个问题：当前生态分成哪些层，每层有哪些代表项目，项目之间大概如何关联，哪些方向正在变热或变稳。它不是最终答案，而是进入生态的地图。

## 分层能帮助判断项目风险

我觉得这个仓库最有用的地方，是强迫我们从系统位置看项目。比如一个 Agent 应用可能非常火，但如果它缺乏稳定使用场景，很容易被新模型或新产品替代。一个 Model Serving 或数据基础设施项目增长没那么戏剧化，但可能更容易成为依赖链的一部分。

Agentic AI 生态尤其需要这种分层视角，因为 Agent 不是单层产品。一个可用 Agent 背后有模型、工具协议、运行环境、记忆、评估、可观测性、部署和安全边界。项目越能嵌入这些基础链路，越值得长期关注。

## 我的判断：生态导航的核心是减少盲目追热点

这类 landscape 最大的作用，是让我们少被单个项目热度带着跑。看到一个新项目时，先问它在三层结构里属于哪一层，再问它替代的是哪类旧能力，依赖哪些上游，又为哪些下游提供价值。

如果只是看项目名，很容易把应用、框架、基础设施和模型混成一团。分层之后，很多争论会变清楚：有些项目是在抢用户入口，有些是在做开发者工具，有些是在做算力和部署效率，有些是在提供基础模型能力。

所以这份仓库我更愿意当作“生态坐标系”，而不是排行榜。

## 原文

- [Agentic AI Landscape and Trends](https://github.com/antgroup/llm-oss-landscape)
