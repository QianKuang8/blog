---
title: "代码编辑阅读路径"
description: "从编辑格式、快速应用到下一处编辑预测，串起 Qian's blog 中关于 AI 代码编辑的文章。"
summary: "模型想好怎样改代码以后，修改怎样准确写回文件、怎样快速应用，下一处编辑又怎样预测。"
lastmod: "2026-10-26T16:46:44+08:00"
hideMeta: true
showToc: true
isCJKLanguage: true
---

模型想清楚怎样改代码以后，还要把修改写回文件：找到要改的位置，保留不该动的内容，并在开发者愿意等待的时间内完成。这条路径的 8 篇文章先看编辑格式和应用失败，再看专用模型与推测解码怎样加速完整修改，最后看编辑器怎样根据刚做的修改预测下一处编辑。

## 先分清几篇相近的文章

最后一段的四篇都在讲 Next Edit，也就是根据近期修改预测下一处编辑，各篇的侧重不同：

| 文章 | 原文 | 侧重 |
| --- | --- | --- |
| [Copilot Next Edit Suggestions]({{< relref "/posts/copilot-next-edit-suggestions.md" >}}) | GitHub Next，2023-11 | 原型阶段的交互问题：建议粒度、展示顺序和延迟怎样影响开发者逐步接受 |
| [Zed Edit Prediction]({{< relref "/posts/zed-edit-prediction.md" >}}) | Antonio Scandurra（Zed），2025-02 | 一个开放模型的完整做法：重写光标附近的片段，监督微调之后再用偏好训练（DPO）抑制误改，靠推测解码和就近部署压低延迟 |
| [Augment Next Edit]({{< relref "/posts/augment-next-edit.md" >}}) | Jiayi Wei（Augment），2025-02 | 大型代码库里的跨文件建议：意图推断、专用检索器定位、紧凑 diff 生成三段处理 |
| [Continue Instinct]({{< relref "/posts/continue-instinct.md" >}}) | Adarsh Iyer（Continue），2025-09 | 训练数据从哪里来：把真实编辑序列整理成样本，再用多语言转换和稀疏微调训练 7B 模型 |

四篇按发布时间排列：Copilot 是提出问题的原型，Zed 和 Continue 公开了模型，Augment 介绍的是产品内部的处理链。Continue 的评估直接拿 Zed 的 Zeta 作对照，两者都基于 Qwen2.5-Coder-7B，可以对照着读。

另一组容易混淆的是 Cursor Instant Apply 和 Zed：两者都让模型输出整段代码，再用原文本作推测候选来加速。区别在于修改从哪里来：Cursor 的修改已经由聊天模型以草图给出，Apply 模型负责把它合并进完整文件；Zed 要根据近期编辑自己推测下一处修改，只重写光标附近的片段。

## 路径怎样展开

**先看修改怎样落到文件里。** Code Surgery 比较了五个 coding assistant 的编辑工具，包括上下文补丁、搜索替换和交给另一个模型应用，重点是怎样定位、怎样保留缩进，以及部分修改成功时怎样把结果告诉下一轮。Aider 一篇用实验比较编辑格式：在 89 个 Python 重构任务上，从 SEARCH/REPLACE 换成去掉行号、按完整代码块组织并配合容错应用的 unified diff 以后，GPT-4 Turbo 留下省略注释的任务从 12 个降到 4 个；作者也说明，这项基准不是严格的重构正确性证明。

**再看完整修改怎样快速应用。** 输出整个文件，工具拿到的就是新文件，不必再解析补丁；代价是只改几行也可能要生成几百行。Assisted Generation 一篇先说明推测解码的原理：用便宜的方式提出候选 token，目标模型一次前向计算验证多个位置。Cursor Instant Apply 把这个思路用在编辑上：原文件就是现成的候选，专门训练的 Apply 模型只在发生变化的地方正常生成。原文报告约 1,000 tokens/s，比 Llama-3-70B 普通推理快约 13 倍，比此前的 GPT-4 speculative edits 部署快约 9 倍；两个倍数的基线不同，不能相乘。

**最后看下一处编辑怎样预测。** 四篇见上表。它们面对同一组风险：模型从近期编辑推测意图，可能猜错方向、误改无关代码，或者建议来得太慢。各篇的处理不同：Copilot 讨论怎样展示建议，Zed 用偏好训练抑制副作用，Augment 把定位和生成拆开，Continue 限定模型只改光标附近几行，并用允许合理替代编辑的评分衡量质量。

读完这条路径，应该能回答三个问题：一种编辑格式把定位的负担放在模型还是工具上；整文件输出为什么还能快，收益取决于什么；评价一个 Next Edit 系统时，除了离线分数，还要看哪些交互成本。

{{% reading_path %}}

## 继续探索

- [code-editing 标签]({{< relref "/tags/code-editing" >}})
- [Coding Agent 阅读路径]({{< relref "/topics/coding-agent.md" >}})：继续看编辑之外的执行循环、产品工作流与验收。
