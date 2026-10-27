---
date: '2026-06-05T21:20:00+08:00'
lastmod: '2026-10-26T12:21:49+08:00'
title: "Anthropic 长任务实验：先加评价器，模型升级后再拆编排"
summary: "Anthropic 用前端设计和全栈应用实验，展示独立 evaluator 如何提供可执行反馈，也展示模型升级后哪些编排可以移除。收益需要连同预算、任务范围和评价器盲点一起看。"
description: "分析长时间应用开发中的 evaluator 校准、sprint contract、上下文交接与 Harness 简化实验。"
tags: ["harness-engineering", "agentic-coding", "agent", "anthropic"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
learning_status: done
---

应用能打开，离用户能完成任务还有一段距离；页面整齐，离预期的视觉表达也还有一段距离。长时间自主开发如果只让生成者自己判断是否完成，这些差距往往会被藏进一份乐观的总结里。

Anthropic 的 [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) 记录了 Prithvi Rajasekaran 的实验：用独立 evaluator 检查生成结果，再把具体问题交回 generator 迭代。它分别用于主观的前端设计和可操作验证的全栈应用。原文报告的是作者的开发实验，本文没有复现。

## 先让评价器具备可重复的判断方式

前端实验把目标拆成四个维度：整体设计、原创性、实现细节和可用性。颜色、字体、布局是否协调，是否有针对任务的设计选择，以及用户能否找到主要动作，分别进入评价。

作者更重视整体设计和原创性，因为当时模型已经比较容易生成基本工整、可用的页面，却经常采用相似的模板。为了减少评价漂移，他还给 evaluator 提供带详细分数说明的少量示例，使它接近自己的偏好。

运行时，generator 先生成 HTML/CSS/JS，evaluator 通过 Playwright MCP 打开页面、截图并操作，再返回评分和批评。generator 根据反馈决定继续改进当前方向，或换一种设计。原文每次运行进行 5–15 轮，长的可达四小时。

博物馆页面在第十轮转成 CSS perspective 构建的三维展厅，是作者观察到的一个显著变化。但结果也显示评价指标会塑造风格：“museum quality”等措辞使不同设计趋向某种共同审美；后期实现更复杂，作者有时反而更喜欢中间版本。所以分数提高只说明结果更符合评价标准；标准本身是否合适、最终选哪个版本，仍要由人决定。

## 全栈任务用 contract 连接需求与验证

在全栈版本中，planner 将一到四句话扩成产品规格，generator 按功能阶段实现，evaluator 检查实际应用。planner 主要规定产品目标和高层设计，避免过早指定细节，把错误实现方案传给后续阶段。

高层需求仍不足以直接验收，因此每个 sprint 前，generator 与 evaluator 先协商 contract：这段工作交付什么、怎样验证完成。generator 提出计划和检查方式，evaluator 确认它覆盖需求，双方通过文件交换意见，达成一致后才实现。

QA 随后通过界面、API 和数据库状态检查行为。原文列出的反馈很具体：矩形填充只在拖拽起终点放置图块，删除实体的条件判断要求了不会同时设置的状态，以及 FastAPI 路由顺序把 `/frames/reorder` 当成整数 `frame_id`，返回 422。

这些反馈把“功能不对”缩到可修复的差异：期望是什么，实际做了什么，错误可能出现在哪里。它们比总分更直接地帮助下一轮执行。

独立 evaluator 起初也不是合格的 QA。作者观察到，它会发现问题后说服自己“影响不大”，或者只做浅层测试。团队通过阅读日志、找出与人工判断不一致的案例、调整 QA 提示，迭代了数轮。分开生成与评价，给了人一个校准评价器的入口，评价器自己的盲点仍然存在。

## 案例收益同时包含更大范围与更高预算

原文用同一个“二维复古游戏制作器”提示比较 Opus 4.5 的两种运行：

| 运行方式 | 时长 | token 成本 |
| --- | --- | --- |
| 单 Agent | 20 分钟 | 9 美元 |
| 完整 Harness | 6 小时 | 200 美元 |

单 Agent 产物中，实体可以显示，却不能响应输入。完整 Harness 的 planner 则扩展出 16 项功能、10 个 sprint，加入动画、声音、AI 辅助生成和分享导出等内容；最终核心 play mode 可以运行，但仍有流程提示不清、物理表现和关卡可通行性问题。

![单 Agent 运行生成的复古游戏制作器初始界面：深色背景上只有项目标题、空项目列表和新建按钮，大部分区域留空。](/images/harness-design-long-running-apps/solo-harness-app.png)

*图 1：原图，来源：[Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)。原文指出这一版布局浪费空间，固定高度的面板让大部分视口空着；截图只展示初始界面。*

![完整 Harness 生成的复古游戏制作器：新建游戏对话框中可以填写项目名称、描述、画布分辨率、图块大小和调色板。](/images/harness-design-long-running-apps/full-harness-app.png)

*图 2：原图，来源同上。同一提示下，完整 Harness 的版本在新建时就要求配置画布、图块和配色，对应正文所说 planner 扩展出的功能范围。*

在这个案例里，完整 Harness 做出了更完整的应用，但同时变化的还有多 Agent 分工、约 18 倍的时长、约 22 倍的费用和扩大的需求范围，原文没有把它们各自的贡献分开。另外，自动扩充功能是本实验刻意要求的；实际项目要先决定是否愿意承担扩出来的范围和维护成本。

## 模型升级后逐个移除组件

上下文处理体现了 Harness 随模型变化的过程。早期 Sonnet 4.5 在接近上下文上限时容易过早收尾，作者称之为 context anxiety。团队用清空窗口和结构化交接缓解，代价是额外编排、token 与延迟。到了 Opus 4.5，这种行为明显减轻，全栈实验便移除了 reset，改为连续会话配合 SDK 自动压缩。

随后，Opus 4.6 使作者继续检查原有脚手架。一次大幅删减无法复现效果，也难以判断删掉了哪项有效机制；之后改为每次移除一个组件，观察结果。

其中被移除的是 sprint 结构。planner 保留，因为没有它时实现范围容易偏小；evaluator 也保留，但检查从每个 sprint 后移到完整构建后。末尾检查同样可以触发返工，返工后再次接受 QA。

浏览器 DAW 案例就经过了三轮构建与 QA，总计 3 小时 50 分钟、124.70 美元。评价器先后发现时间线片段不能拖动、缺少乐器面板、录音按钮只是状态切换而没有采集麦克风、片段缩放和分割未实现等问题。最终具备基本编曲、混音与播放能力，但远非专业 DAW；原文还指出模型无法实际听到音乐，限制了音乐品味方面的评价。

这条实验路径给出一种具体的维护方法：从真实失败提出架构假设，为它增加可观察的反馈，再在模型或任务变化后逐项复查。原文的观察是：模型独自就能做好的任务，evaluator 只是额外开销；接近模型能力上限的部分，它仍能发现关键遗漏。是否保留它，应由同一质量标准下的结果、成本和剩余缺陷共同决定。

## 原文

- [Harness design for long-running application development — Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps)
