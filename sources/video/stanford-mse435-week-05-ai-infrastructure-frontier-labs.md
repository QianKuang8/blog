---
title: "Stanford MS&E435 Economics of the AI Supercycle | Spring 2026 | Infrastructure, Capstone Case"
source_url: "https://www.youtube.com/watch?v=4k53z3Ysjg0"
source_type: "video"
channel: "Stanford Online"
speaker: "Sachin Katti（OpenAI）; Apoorv Agrawal（主持）"
published_at: "2026-05-27"
duration: "46:06"
retrieved_at: "2026-08-31T17:30:00+08:00"
series: "Stanford MS&E 435: Economics of the AI Supercycle"
pdf_path: "stanford-mse435/week-05-ai-infrastructure-frontier-labs.pdf"
---

## 来源范围

- 视频 ID：`4k53z3Ysjg0`
- 字幕：957 条人工英文字幕
- 嘉宾：Sachin Katti（OpenAI，负责 industrial compute，前 Intel CTO）
- 内容性质：Stanford MS&E 435 Week 5，讨论算力交付、吉瓦级供应链同步、智能体计算图、TTFT 与全栈瓶颈迁移

## 核心论点与证据边界

| 论点 | 时间范围 | 发布边界 |
|---|---|---|
| RL 后训练采样、合成数据生成和产品服务都会大量使用推理 | 00:06:01–00:07:00 | 并列用途，不规定串行顺序；未来推理占比为讲者预测 |
| 合同容量须经过上线、稳定运行与调度才形成可用算力 | 00:09:26–00:11:44 | 容量乘可用率和条件利用率是笔记的教学近似，非讲者原公式 |
| 智能体把模型、工具、搜索和外部执行编成任务图 | 00:17:36–00:27:29 | 节点资源分类为整理，不是产品硬件规格 |
| 400–500 ms 主要描述上下文处理，外围延迟需另加 | 00:29:02–00:31:43 | 口头量级，不是完整端到端 TTFT 或 p50/p95 测量 |
| Cerebras 加快 token 生成后，应用/API 延迟显现 | 00:31:43–00:33:13 | 支持 decode 加快，不据此外推 prefill 倍数或 TTFT 降幅 |

## 2026-09-23 理解复核

依据当日修订的 22 页课程笔记、对应 LaTeX 与修订记录复核正文，并直接查看新版 TTFT 阶段图。页码均按 PDF 物理页计算，包含封面与目录。

- 第 6 页：RL 后训练、合成数据与产品服务为并列推理用途。
- 第 8 页：简化关系中的利用率指设备可用期间的利用率；若已把停机算入利用率分母，不再乘可用率。该关系还未单列降频、通信和任务质量损失。
- 第 15–16 页：区分完整 TTFT、prefill 与 decode，保留 400–500 ms 的口述范围及外围延迟；用课堂实际 API 瓶颈例子替代固定的跨层迁移顺序。
- 30 GW 为愿景目标，约 100 GW 为即席估算，7 TW 为思想实验，状态与范围不同，不能相加为已规划容量。

本次复核不等于对 OpenAI 容量、收入、内部性能或项目计划的独立审计。讲者的规模、推理占比与远期判断保留现场口径。

## 发布映射

- 博客文章：`content/posts/stanford-mse435-week-05-ai-infrastructure-frontier-labs.md`
- 站点 PDF：`/blog/pdfs/stanford-mse435/week-05-ai-infrastructure-frontier-labs.pdf`
- GitHub 源文件：`https://github.com/QianKuang8/blog-pdfs/blob/5fe326dc06c33ec0577f6b9c92becabf01412eec/stanford-mse435/week-05-ai-infrastructure-frontier-labs.pdf`
