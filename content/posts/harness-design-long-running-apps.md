---
date: '2026-06-05T21:20:00+08:00'
lastmod: '2026-06-05T21:20:00+08:00'
title: 'Long-running Harness 的关键，不是多 Agent，而是把判断外置'
summary: "解读 Anthropic 的 long-running application harness 实验：文章真正值得看的不是三 agent 架构本身，而是它如何把生成、评价、规划和上下文交接拆成可调试的工程系统。"
description: "从 Anthropic 的 generator-evaluator harness 看长时间自主编码、前端设计评价和 agent QA 的工程取舍"
tags: ["harness-engineering", "agentic-coding", "agent"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Anthropic 这篇 [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) 很值得读，因为它讨论的不是“多 agent 是否更强”这种抽象问题，而是更具体的工程问题：当模型要连续几个小时构建完整应用时，哪些脚手架真的能提高质量，哪些又只是成本。

文章作者从两个问题出发：让 Claude 生成更好的前端设计，以及让 Claude 在没有人类持续干预的情况下完成完整应用开发。最后形成的是一个 planner、generator、evaluator 组成的 harness。我的理解是，这套架构最核心的不是 agent 数量，而是把“做事”和“判断做得好不好”分开。

## 长任务的两个主要失败点

文章先指出 naive implementation 的两个问题。第一个是长任务里的上下文退化。随着上下文窗口被文件、分支探索和中间想法填满，模型会逐渐失去连贯性。有些模型还会出现作者称为 context anxiety 的现象，也就是接近自认为的上下文边界时过早收尾。

Anthropic 早期 harness 用 context reset 来处理这个问题：清空上下文，启动新 agent，再通过结构化 handoff artifact 把状态和下一步传过去。它和 compaction 的区别在于，compaction 只是压缩原会话，仍然保留连续性和残留压力；reset 给模型一个干净起点，但要求 handoff 足够完整。

第二个问题是 self-evaluation。模型评价自己产物时经常过于宽容，尤其是前端设计这类没有二元测试结果的任务。文章的判断很直接：让生成者自己变得足够挑剔很难，但调一个独立 evaluator 变得更怀疑、更稳定，反而可行。

## 把审美变成可评分标准

前端设计实验是这篇文章最有意思的部分。作者把“好不好看”拆成四个评价维度：design quality、originality、craft、functionality。前两个权重更高，因为 Claude 默认已经能做出基本可用、工整的界面，但容易落进模板化、库默认和典型 AI slop。

这个设计很关键。审美当然不能完全被分数覆盖，但如果没有可评价语言，evaluator 只能说“看起来不错”。一旦标准里明确写出颜色、字体、布局、图像是否形成整体气质，是否有定制化决策，是否只是白卡片加紫色渐变，模型就有了可以反复优化的靶子。

实际流程里，generator 先基于用户 prompt 生成 HTML/CSS/JS 前端，evaluator 通过 Playwright MCP 打开页面、截图、交互，然后按标准打分和写 critique。每次反馈再回到 generator，通常跑 5 到 15 轮，完整过程最长到 4 小时。文章提到一个荷兰艺术博物馆页面例子，第 10 轮从常规深色落地页转向一个 CSS perspective 渲染的 3D 房间体验，这说明外部评价有时确实能逼出单次生成看不到的方向变化。

## 全栈 harness 的价值在于可验收的迭代

迁移到全栈应用后，文章使用 planner、generator、evaluator 三类 agent。planner 把 1 到 4 句话的需求扩展成产品规格，generator 按 sprint 实现功能，evaluator 用 Playwright 点击 UI、测 API、看数据库状态。每个 sprint 前，generator 和 evaluator 会先协商 sprint contract，明确这个阶段完成的定义和可测试行为。

这个 contract 我觉得是重点。它把高层产品 spec 和具体实现之间的缝补上了。否则 generator 很容易按自己的理解开工，evaluator 事后也只能泛泛说“还不错”。有了 contract，QA 就能针对明确标准验收。

文章里的 retro game maker 对比很说明问题。单 agent 版本跑了 20 分钟，成本 9 美元；完整 harness 跑了 6 小时，成本 200 美元。后者贵了 20 多倍，但输出质量明显更高。solo 版本界面看起来符合预期，却存在空间浪费、流程僵硬、实体无法响应输入等核心问题。harness 版本由 planner 扩展成 16 个 feature、10 个 sprint，还包括 sprite animation、behavior templates、音效音乐、AI-assisted sprite generator 和分享导出等能力。它仍有交互直觉不足和物理细节问题，但 play mode 的核心链路是通的。

更重要的是，evaluator 不是只看表面。文章列出的失败包括矩形填充工具只在拖拽起止点放 tile、删除 entity spawn point 的条件判断错误、FastAPI 路由顺序导致 `/frames/reorder` 被当成 frame_id 解析。这些都是具体、可修的工程反馈。

## Harness 会随着模型能力重新洗牌

文章后半段对我最有启发：harness 不是一劳永逸的架构。作者在 Opus 4.6 发布后重新审视原有设计，因为新模型更擅长规划、长任务、代码审查和调试，于是开始移除 sprint construct，只保留 planner 和 evaluator，让 QA 不再按 sprint 逐段验收，而是在完整 build 之后集中检查。

这不是说 evaluator 不重要了，而是它的价值边界移动了。对于模型已经能稳定独立完成的任务，evaluator 可能只是额外成本；对于仍处在模型能力边界之外的复杂应用，它还能抓住 stub feature、交互缺口和最后一公里问题。

DAW 例子里，更新后的 harness 仍然跑了 3 小时 50 分钟，成本 124.70 美元。QA 第一轮指出核心 DAW 功能有些只是展示而不可交互，例如 clip 不能拖动、没有 instrument UI panels、没有视觉化 effect editors。第二轮又指出录音仍是 stub、clip resize 和 split 没实现、effect visualization 只是数字滑杆。这些都说明，即使模型变强，外部评价仍然在能力边界附近有用。

## 我的判断：harness 是对模型短板的可执行假设

我读完最大的感受是，harness engineering 不是把流程搞复杂，而是把你对模型短板的判断写成可执行结构。你认为模型会低估需求，就加 planner。你认为模型会自我宽容，就加 evaluator。你认为长上下文会污染，就加 reset 和 handoff。你认为阶段目标不清，就加 contract。

但这些结构都不是永久真理。模型升级后，某些短板会变轻，原本 load-bearing 的组件可能变成纯成本。好的 harness 需要经常拆开检查，而不是因为一次实验有效就固化成仪式。

所以这篇文章的价值不在于复制三 agent 架构，而在于它展示了一种思路：读模型在真实任务里的 trace，找到失败模式，把失败模式转成可评价、可交接、可迭代的工程机制。对长时间 autonomous coding 来说，这比“多开几个 agent”重要得多。

## 原文

- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
