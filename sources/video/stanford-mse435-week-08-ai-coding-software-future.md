---
title: "Applications, Coding AI"
source_url: "https://www.youtube.com/watch?v=HA7lZd7zk3M"
source_type: "video"
channel: "Stanford Online"
speaker: "Guillermo Rauch (Vercel CEO)"
published_at: "2026-06-23"
duration: "49:22"
retrieved_at: "2026-08-31T16:15:56+08:00"
series: "Stanford MS&E 435: Economics of the AI Supercycle"
pdf_path: "stanford-mse435/week-08-ai-coding-software-future.pdf"
---

## 来源范围

- 视频 ID：`HA7lZd7zk3M`
- 原始语言：英语
- 字幕：1,091 条人工英文 CC
- 视频分辨率：1920×1080
- 课堂日期：2026-05-22；上传日期：2026-06-23
- 主持人：Apoorv Agrawal
- 嘉宾：Guillermo Rauch（Vercel 创始人兼 CEO）
- 配套材料：Stanford MS&E 435 Course Materials，Week 8 材料页

本记录没有提交完整字幕、视频、音频、抽帧目录或生成日志。关键论点由视频元数据、带时间戳人工 CC、PDF 笔记和课程材料交叉整理。

## 章节（依据字幕话题转折重建）

PDF 九章结构：

1. 从个人经历到软件民主化 (00:00:36–00:06:50)
2. 写代码不等于交付：部署才启动学习 (00:06:50–00:10:29)
3. 从 Pixels 到 Tokens：智能体基础设施的总体框架 (00:10:50–00:13:47)
4. 智能体云的核心原语：网关、沙箱、安全与自动运维 (00:17:09–00:24:01)
5. SaaS 的分层可塑化：呈现层可生成，系统记录继续复用 (00:24:07–00:28:29)
6. 一次性软件与新的开发、支持闭环 (00:29:09–00:32:09)
7. 局部推理、可组合性与全栈复用 (00:32:09–00:40:08)
8. 价值归属、开放商业与「token 速度」(00:40:10–00:48:05)
9. 总结与延伸：可靠性、能源与未决问题 (00:48:05–00:49:22)

## 核心论点与证据边界

| 论点 | 时间范围 | 来源属性 | 发布边界 |
|---|---|---|---|
| 编程史可理解为访问权扩张史，每次抽象把稀缺性推向下一层 | 00:06:10–00:06:50 | Rauch 的判断 | 不扩写为行业共识 |
| 部署才启动学习：源码库是中间态，可运行版本才产生真实信号 | 00:07:19–00:08:06 | Rauch 的核心论点 | 不等于所有代码都必须立即部署 |
| 云的部署对象从 Page 扩展到 Agent，长时任务改写基础设施需求 | 00:08:27–00:10:29 | Rauch 设想 + Vercel 产品映射 | Amazon Agent Services 是反事实命名 |
| 智能体基础设施三角：给智能体运行、用基础设施造智能体、让智能体运行基础设施 | 00:13:47–00:14:48 | Rauch 框架 | 三者权限模型不同 |
| 积木经济：开放、可组合的构件比从头重建更经济 | 00:15:45–00:17:09 | Rauch 借用 Mitchell Hashimoto 说法 | 选择率数字只属于演讲所示测试口径 |
| SaaS 不是整体死亡，而是分层可塑化：呈现层可生成，记录系统复用 | 00:24:07–00:28:29 | Rauch 拆层判断 | 停车和销售案例只证明局部定制 |
| 一次性软件作为高保真沟通媒介，AI 反身性增加生成频率 | 00:29:09–00:30:30 | Rauch + Shopify Tobi 说法 | 不是正式数学模型 |
| 局部推理使可组合性成为规模化前提 | 00:33:27–00:36:39 | Rauch 以 Tailwind 和 React 说明 | 局部性不保证完美迁移 |
| 面向智能体的商业接口：原始信号、即时进入、按量消费 | 00:45:22–00:46:21 | Rauch 预测 | 即时不意味绕过合规 |
| "No more rate limits" 是挑衅，真实目标是动态容量控制 | 00:46:21–00:47:40 | Rauch 自述为 provocation | 仍需身份、KYC、滥用检测、系统健康 |

## 重要不确定项

- shadcn 90.1%、Vercel 100% 选择率只属于演讲展示的特定测试，缺少完整报告方法和模型版本。
- Meta 和 Notion 案例来自 Vercel 创始人客户讲述，证据强度低于客户公开技术报告。
- "约 95% 的火箭发动机" 底座复用比喻无代码或成本口径。
- 计算量数月约增三倍、每日部署数翻倍是公司自述，基期和绝对量未知。
- Amazon 页面每慢 100ms 转化率下降 1% 被标为"Rauch 在演讲中引用"，未追溯原始实验。

## 发布映射与文件校验

- 博客文章：`content/posts/stanford-mse435-week-08-ai-coding-software-future.md`
- 站点 PDF：`/blog/pdfs/stanford-mse435/week-08-ai-coding-software-future.pdf`
- GitHub 源文件：`https://github.com/QianKuang8/blog-pdfs/blob/a0d1ded/stanford-mse435/week-08-ai-coding-software-future.pdf`
- 源 PDF 与公开仓库文件已经通过 `cmp` 验证，字节一致，没有压缩或重新编码。
