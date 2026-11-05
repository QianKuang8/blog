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
image_sources:
  - title: "Representing branches in Pando（主干与侧分支的包）"
    path: "/images/scaling-git-at-openai/pando-branch-packs.svg"
    source_url: "https://images.ctfassets.net/kftzwdyauwt9/5wDkqDPp9fjzOjtAQRDRzw/117b2f107fd11818f7e9154c958b0878/representing-branches-in-pando-diagram-desktop-light.svg"
    method: "原图文件，未改动"
    retrieved_at: "2026-11-05T16:25:28+08:00"
  - title: "How advertised refs affect packfile size（通告引用与包大小）"
    path: "/images/scaling-git-at-openai/advertised-refs-pack-size.svg"
    source_url: "https://images.ctfassets.net/kftzwdyauwt9/3H8EcvD2zWlkO6LDnf4Zzy/90597498322b48ae7215638f012fe716/how-advertised-refs-affect-packfile-size-diagram-desktop-light.svg"
    method: "原图文件，未改动"
    retrieved_at: "2026-11-05T16:25:28+08:00"
---
