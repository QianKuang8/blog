---
title: 自进化（Self-evolving／RSI），一篇就够了
source_url: https://zhuanlan.zhihu.com/p/2065227313973825752
domain: zhuanlan.zhihu.com
author: "周星星"
published_at: "2026-07"
description: 梳理 Artifacts、Harness 与 Model 三类自进化路径，以及递归自我改进的机制和评测边界。
retrieved_at: '2026-10-15T14:07:13+08:00'
extractor: defuddle
archived_from: https://www.qingkeai.online/blog/Self-evolving
archive_title: 什么是 Self-evolving / self-improving / RSI ？一篇文章搞懂自进化
extraction_note: 知乎原文 defuddle 抓取返回 403；经用户指定，改用青稞社区同文转载抓取归档，保留原作者和知乎原文 URL。已与用户提供的知乎 Markdown 核对主要章节、核心案例和结尾；转载保留 15 张原文图片，缺失的一张三层分类图由用户版补齐并注明；移除导航、阅读数、上一篇/下一篇、报名二维码和相关推荐，将一条损坏的站内推荐链接保留为文字。转载页缺少文末参考资料列表，由用户提供的知乎版补齐并注明，解开跳转、修复两条混入日期的链接。原文概念冲突和指标歧义未擅改，公开解读另作区分。
image_sources:
  - title: "RSI 三层分类：Harness / Models / Artifacts"
    path: "/images/self-evolving-agents-rsi/rsi-three-layers.jpg"
    source_url: "https://pic2.zhimg.com/v2-f097a603306561d44f811a9f21388d47_1440w.jpg"
    method: "原图文件，未改动"
    retrieved_at: "2026-10-19T10:55:03+08:00"
  - title: "Recursive Harness Self-Improvement 循环"
    path: "/images/self-evolving-agents-rsi/rhi-loop.jpg"
    source_url: "https://pic3.zhimg.com/v2-1669fcf924692e343c4d693231c12f44_1440w.jpg"
    method: "原图文件，未改动；原文转引 Sakana RHI 论文 Figure 2"
    retrieved_at: "2026-10-19T10:55:03+08:00"
  - title: "Terminal-Bench 2.1 预算对等对照"
    path: "/images/self-evolving-agents-rsi/terminal-bench-budget-matched.jpg"
    source_url: "https://pic1.zhimg.com/v2-9b9082f68a8a94ac728f6d43d17f9636_1440w.jpg"
    method: "原图文件，未改动"
    retrieved_at: "2026-10-19T10:55:03+08:00"
---
