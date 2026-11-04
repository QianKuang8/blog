---
title: "OpenAI 如何扩展 Git"
source_url: "https://openai.com/zh-Hans-CN/index/scaling-git-at-openai/"
domain: "openai.com"
author: "Aaron Friel, Taylor Blau, Ted Nyman"
published_at: "2026-11-02"
description: "了解 OpenAI 如何构建兼容 Git 的后端 Pando，以支持 Codex 带来的开发规模。"
retrieved_at: "2026-11-04T16:33:29+08:00"
extractor: "defuddle"
related_sources: ["scaling-git-git-update-ref", "scaling-git-gitprotocol-v2"]
extraction_note: "defuddle 提取中文原站，浏览器核对从导语至未来方向的正文和全部 11 张图。补回提取器遗漏的 4 张静态 SVG 原图 URL，并附动态数据图的文字记录；保留模拟统计口径。删除页尾推荐与交互控件噪声，动态状态以原页面为准。"
image_note: "已逐张查看原页面全部 11 张图：季度提交量、对象关系、packfile 原理、主干与侧分支包、三方案教学模拟、push/fetch、通告 refs、fetch planning、compaction、合并成功率、数据分发量。本文用自绘假设例子集中说明共同基线与重复传输；不复用原图，不用教学模拟或动态初始状态表示生产性能。"
image_sources:
  - title: "共同基线与可复用包的假设示例"
    path: "/images/scaling-git-at-openai/shared-pack-example.svg"
    source_url: "https://git-scm.com/docs/gitprotocol-v2"
    method: "本文绘制：假设的对象集合与客户端状态，不是 Pando 实测或实现规格"
    retrieved_at: "2026-11-04T16:40:31+08:00"
---
