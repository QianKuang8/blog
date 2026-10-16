---
title: "Scaling Pain of Coding Agent  Serving: Lessons from Debugging GLM-5 at Scale"
source_url: "https://z.ai/blog/scaling-pain"
domain: "z.ai"
description: "An engineering post about debugging GLM-5 Coding Agent serving anomalies under high-concurrency, long-context inference workloads."
retrieved_at: "2026-06-05T21:34:06+08:00"
extractor: "manual-local-markdown"
image_sources:
  - title: "Figure 2: KV Cache Race Condition under PD Disaggregation"
    path: "/images/scaling-pain-coding-agent-serving/pd-kv-cache-race.png"
    source_url: "https://z-cdn-media.chatglm.cn/prompts-rich-media-resources/scaling-pain-blog/BkevbCk0Wx.png"
    method: "原图文件，未改动"
    retrieved_at: "2026-10-16T18:19:14+08:00"
  - title: "Figure 3: Fixing Missing Load-Time Synchronization in HiCache"
    path: "/images/scaling-pain-coding-agent-serving/hicache-load-sync.png"
    source_url: "https://z-cdn-media.chatglm.cn/prompts-rich-media-resources/scaling-pain-blog/HyaPZ0yAWe.png"
    method: "原图文件，未改动"
    retrieved_at: "2026-10-16T18:19:14+08:00"
---
