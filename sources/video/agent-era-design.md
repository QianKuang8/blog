---
title: "How To Design In The Agent Era"
source_url: "https://www.youtube.com/watch?v=P06RgnUKX_I"
source_type: "video"
channel: "Y Combinator"
speaker: "Stephen Haney (Paper 创始人)"
published_at: "2026-08-07"
duration: "56:01"
retrieved_at: "2026-08-31T16:15:56+08:00"
series: ""
pdf_path: "standalone/agent-era-design.pdf"
---

## 来源范围

- 视频 ID：`P06RgnUKX_I`
- 原始语言：英语
- 字幕：英文自动字幕（发布时应明确标注）
- 视频分辨率：3840×2160
- 发布日期：2026-08-07
- 主持人：Aaron Epstein
- 受访者：Stephen Haney（Paper 创始人）
- 内容性质：YC Design Review，含访谈、产品演示和三个网站现场评审

本记录没有提交完整字幕、视频、音频、抽帧目录或生成日志。关键论点由视频元数据、带时间戳自动字幕、官方章节和 PDF 笔记交叉整理。

## 官方章节

| # | 章节 | 时间 |
|---:|---|---|
| 1 | Great companies have great design | 00:00:00–00:01:04 |
| 2 | What is Paper and why build it? | 00:01:04–00:03:17 |
| 3 | What makes Paper agent-native | 00:03:17–00:05:11 |
| 4 | Demo: Shaders, image generation, and brand design | 00:05:11–00:11:32 |
| 5 | Design-to-code and the new agent stack | 00:11:32–00:16:48 |
| 6 | Design Review: Legion Health | 00:16:48–00:24:11 |
| 7 | How to avoid AI design slop | 00:24:11–00:28:26 |
| 8 | Design Review: Sytex | 00:28:26–00:32:42 |
| 9 | The biggest tells of AI-generated design | 00:32:42–00:37:39 |
| 10 | Design Review: Moreta | 00:37:39–00:41:11 |
| 11 | Can AI learn taste? | 00:41:11–00:43:56 |
| 12 | How Paper uses agents internally | 00:43:56–00:46:52 |
| 13 | Building a community around Paper | 00:46:52–00:49:15 |
| 14 | Lessons from Stephen's first startup | 00:49:15–00:53:30 |
| 15 | What's next for design and Paper | 00:53:30–00:56:01 |

## 核心论点与证据边界

| 论点 | 时间范围 | 来源属性 | 发布边界 |
|---|---|---|---|
| 代理降低执行成本，判断仍然稀缺；设计更重要而非更不重要 | 00:00:00–00:01:04 | Haney 开场核心判断 | 经验判断，不是数据证明的因果 |
| 代理原生的核心是 HTML/CSS 共享表示，不是聊天框 | 00:03:17–00:05:11 | Haney 的工程经验 | 性能差异未提供基准测试 |
| 语言与画布是两种互补输入：自然语言表达目标，画布表达空间关系 | 00:03:45–00:05:08 | Haney 的设计哲学 | 不等于所有任务都需要画布 |
| 新代理栈：编码代理 + 视觉画布 + 审查合并 | 00:12:28–00:16:48 | Haney 概括 + 演示 | 三类能力组合，不是固定产品清单 |
| 设计与代码共享事实源，双向流动减少交接漂移 | 00:15:30–00:16:48 | Haney + Paper 演示 | 事实源主张需要代码库保持更新 |
| 策展式设计过程：代理扩展候选，人负责筛选、组合与验收 | 00:19:11–00:24:11 | Legion Health 案例演示 | 视频也展示了选区错误和文字重叠等现场失败 |
| AI 设计俗套是可诊断和可修正的：字重过重、字号过多、对比度不当 | 00:24:11–00:28:26 | Haney 演示 + 启发式 | 启发式针对具体案例，不是固定数值规范 |
| 首屏先回答"用户得到什么"，再展示细节 | 00:28:26–00:32:42 | Sytex 案例评审 | 适用于落地页评审场景 |
| 金融产品需要信任，专业化不应压平品牌个性 | 00:37:39–00:41:11 | Moreta 案例评审 | 品味判断不等于通用规则 |
| AI 品味 = 偏好 × 语境 × 权衡链 | 00:41:11–00:43:56 | Haney 推测 | 视频只给出方向，未给出实现方案 |
| 代理放大高水平小团队，不是降低人才标准 | 00:43:56–00:46:52 | Haney 团队经验 | Paper 约 12 人团队的个案 |

## 重要不确定项

- 自动字幕把 MCP 识别为 "MTP"，但画面后续明确显示 via MCP。
- Paper 录制时约 12 人，团队规模和能力范围为受访者自述。
- 停车管理 CEO 替代既有软件的故事没有数据迁移、安全、异常处理或成本基线。
- "有人让代理跑一整夜，早上看到几百个变体" 是 Haney 的间接转述。
- 演示中的模型名（OpenAI Image 2、Nano Banana 2、Flux 2 Pro、Grok）来自画面，非正式产品公告。

## 发布映射与文件校验

- 博客文章：`content/posts/agent-era-design.md`
- 站点 PDF：`/blog/pdfs/standalone/agent-era-design.pdf`
- GitHub 源文件：`https://github.com/QianKuang8/blog-pdfs/blob/a0d1ded/standalone/agent-era-design.pdf`
- 源 PDF 与公开仓库文件已经通过 `cmp` 验证，字节一致，没有压缩或重新编码。
