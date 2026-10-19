---
title: "拆解 Anthropic 的 skill-creator：AI Agent 的技能工厂是怎么运转的"
source_url: "https://blog.riba2534.cn/blog/2026/%E6%8B%86%E8%A7%A3anthropic%E7%9A%84skill-creator-ai-agent%E7%9A%84%E6%8A%80%E8%83%BD%E5%B7%A5%E5%8E%82%E6%98%AF%E6%80%8E%E4%B9%88%E8%BF%90%E8%BD%AC%E7%9A%84/"
domain: "blog.riba2534.cn"
description: "A Chinese deep dive into Anthropic's updated skill-creator workflow, evaluators, benchmarks, and description optimization loop."
retrieved_at: "2026-06-05T21:16:57+08:00"
extractor: "defuddle"
image_sources:
  - title: "skill-creator 核心工作流（Draft → Test → Evaluate → Improve）"
    path: "/images/anthropic-skill-creator-breakdown/skill-creator-workflow.png"
    source_url: "https://blog.riba2534.cn/blog/2026/%E6%8B%86%E8%A7%A3anthropic%E7%9A%84skill-creator-ai-agent%E7%9A%84%E6%8A%80%E8%83%BD%E5%B7%A5%E5%8E%82%E6%98%AF%E6%80%8E%E4%B9%88%E8%BF%90%E8%BD%AC%E7%9A%84/"
    method: "原页面图表截图：用 Chromium 以 2 倍像素比截取原文第二节的 Mermaid 渲染结果，未改动"
    retrieved_at: "2026-10-19T20:20:27+08:00"
---
