---
title: "Stanford MS&E435 Economics of the AI Supercycle | Spring 2026 | Enterprise Internal Knowledge"
source_url: "https://www.youtube.com/watch?v=LRGX-gTegVA"
source_type: "video"
channel: "Stanford Online"
speaker: "Apoorv Agrawal（主持）; Yash Patil（嘉宾，Applied Compute）"
published_at: "2026-05-22"
duration: "48:10"
retrieved_at: "2026-08-31T20:00:00+08:00"
series: "Stanford MS&E 435: Economics of the AI Supercycle"
pdf_path: "stanford-mse435/week-06-enterprise-knowledge-intelligence.pdf"
---

## 来源范围

- 视频 ID：`LRGX-gTegVA`
- 原始语言：英语
- 字幕：1511 条英文自动字幕
- 视频分辨率：1080p
- 发布日期：2026-05-22
- 课程日期：2026-05-08
- 主持人：Apoorv Agrawal
- 嘉宾：Yash Patil（Applied Compute；曾参与 OpenAI 模型评测）
- 内容性质：Stanford MS&E 435 Week 6 讲座，含模型能力史回顾、企业专用化闭环和持续学习
- 配套阅读：Karpathy《2025 LLM Year in Review》、Silver & Sutton《Welcome to the Era of Experience》

本记录没有提交完整字幕、视频、音频、抽帧目录或生成日志。关键论点由视频元数据、带时间戳自动字幕和 PDF 笔记交叉整理。

## 章节结构（基于语义转折）

| # | 章节 | 时间 | 核心问题 |
|---:|---|---|---|
| 1 | 通用模型为何不懂企业 | 00:00–05:43 | 通用能力与企业适配是两个不同问题 |
| 2 | 从表征学习到推理模型 | 05:44–17:22 | AlexNet → Transformer → 扩展定律 → RLHF → 推理模型 |
| 3 | 从预训练到后训练 | 17:22–23:57 | 数据墙之后训练信号从哪里来 |
| 4 | Eval 定义山峰 | 23:57–35:42 | 企业用 eval、纠错和系统编排形成专用化闭环 |
| 5 | 持续学习 | 35:43–40:08 | 生产中的稀疏延迟反馈如何转成持续改进 |
| 6 | 技术与商业边界 | 40:08–47:55 | 架构、算力与数据市场限制下一轮扩展 |
| 7 | 总结与延伸 | 47:55–48:05 | 企业经验闭环 |

## 核心论点与证据边界

| 论点 | 时间范围 | 来源属性 | 发布边界 |
|---|---|---|---|
| 通用模型像不了解业务的天才，企业知识沉淀在内部 | 00:05:07–00:05:40 | Patil 核心比喻 | 经验判断，不是数据证明 |
| 瓶颈逐步迁移：算力→架构→数据→对齐→RL环境→持续学习 | 00:11:53–00:14:16 | Patil 历史梳理 | 不等于旧资源不再重要 |
| 代码和数学因可验证而成为 RLVR 第一前沿 | 00:14:42–00:15:24 | Patil 机制判断 | 通过测试不保证所有情形正确 |
| DoorDash 菜单：人工纠错→ground truth→训练信号 | 00:27:21–00:29:17 | Patil 案例 | 据讲者介绍，未独立核验 |
| 不能只等下一代通用模型：时间价值+私有标准在通用训练分布之外 | 00:29:16–00:31:04 | Patil 战略判断 | 不是"永远不可能"的定理 |
| 企业系统由 model+context+harness 三层共同交付 | 00:34:08–00:35:42 | Patil 架构概括 | 视频未展示具体产品架构 |
| Cursor Composer 用接受/撤销作为隐式奖励做在线更新 | 00:37:16–00:38:04 | Patil 案例 | 接受不等于业务成功 |
| 持续学习更新面：weights、context、harness | 00:39:17–00:40:08 | Patil 总结 | 视频未给出实现细节 |

## 重要不确定项

- 嘉宾姓名以视频简介 Yash Patil 为准，自动字幕写作 "Patel" 是听写误差。
- 视频简介与发言使用 Applied Compute，课程材料页却把本讲列作 "Applied Intelligence"。
- DeepSeek V3 预训练约 240–250 万 H800 GPU 小时、R1 约 15 万小时，讲者口头概括为"约 5%"，按数字直接算约 6.0%–6.25%。
- 自动字幕把 benchmark 名首次记作 SWE-bench、后一次写成 "TreeBench"，关键帧未显示专名。
- 结尾视觉产品名无法由自动字幕可靠还原。

## 发布映射与文件校验

- 博客文章：`content/posts/stanford-mse435-week-06-enterprise-knowledge-intelligence.md`
- 站点 PDF：`/blog/pdfs/stanford-mse435/week-06-enterprise-knowledge-intelligence.pdf`
- GitHub 源文件：`https://github.com/QianKuang8/blog-pdfs/blob/409d269/stanford-mse435/week-06-enterprise-knowledge-intelligence.pdf`
- 源 PDF 与公开仓库文件已通过 `cmp` 验证，字节一致。
