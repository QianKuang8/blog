---
title: "深入解析 Codex 智能体循环"
source_url: "https://openai.com/zh-Hans-CN/index/unrolling-the-codex-agent-loop/"
domain: "openai.com"
author: "Michael Bolin"
published_at: "2026-01-23"
description: "本文将对 Codex 智能体循环进行深度技术剖析，阐述 Codex CLI 如何利用 Responses API 来协调模型、工具、提示，并优化整体性能。"
retrieved_at: "2026-04-09T00:00:00+08:00"
extractor: "clippings"
tags:
  - "clippings"
image_sources:
  - title: "请求随工具调用增长与压缩（重绘）"
    path: "/images/unrolling-codex-agent-loop/request-prefix-growth.svg"
    source_url: "https://openai.com/zh-Hans-CN/index/unrolling-the-codex-agent-loop/"
    method: "重绘：依据原文对 input 构造、追加更新与 compaction 的文字说明绘制，原文无对应示意图"
    retrieved_at: "2026-10-16T18:19:14+08:00"
---
