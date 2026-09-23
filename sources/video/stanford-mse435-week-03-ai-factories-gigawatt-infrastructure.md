---
title: "Stanford MS&E435 Economics of the AI Supercycle | Spring 2026 | Building AI Factories"
source_url: "https://www.youtube.com/watch?v=GcCGzfKdCd0"
source_type: "video"
channel: "Stanford Online"
speaker: "Chase Lochmiller（Crusoe 创始人兼 CEO）; Apoorv Agrawal（主持）"
published_at: "2026-06-17"
duration: "49:47"
retrieved_at: "2026-08-31T17:00:00+08:00"
series: "Stanford MS&E 435: Economics of the AI Supercycle"
pdf_path: "stanford-mse435/week-03-ai-factories-gigawatt-infrastructure.pdf"
---

## 来源范围

- 视频 ID：`GcCGzfKdCd0`
- 原始语言：英语
- 字幕：1147 条人工英文字幕
- 视频分辨率：1080p
- 发布日期：2026-06-17
- 嘉宾：Chase Lochmiller（Crusoe 创始人兼 CEO）
- 内容性质：Stanford MS&E 435 Week 3，讨论吉瓦级 AI 工厂的能源选址、数据中心全栈 CapEx、算力经济寿命与 token 服务回报

本记录没有提交完整字幕、视频、音频或生成日志。

## 核心论点与证据边界

| 论点 | 时间范围 | 发布边界 |
|---|---|---|
| AI 数据中心是宏观基础设施，CapEx 约 6500 亿美元 | 00:00:14–00:03:07 | 主持人口述，待复核 |
| Crusoe 垂直整合算力+能源+数据中心，energy-first 选址 | 00:07:30–00:13:16 | Lochmiller 公司描述 |
| Abilene 从 200 MW 到 2.1 GW，利用受困能源 | 00:13:16–00:18:32 | Lochmiller 案例 |
| 基础设施 CapEx 约 19.2M 美元/MW，含劳务 4.7M | 00:23:45–00:30:20 | 讲者粗算，非审计 |
| 从基础设施出租到 token 服务：越靠近 token 收入上限越高 | 00:37:26–00:40:49 | 商业模式判断 |

## 重要不确定项

- MW/GW 是功率而非年度能量；所有"每 MW 成本"是当场粗算
- 四年和两年都是按收入计算的静态回收期，不是利润或 IRR
- IT 标题约 40M、分项 41M；总账标题 58M、分项 59M、口述约 60M，且可能双计，不能只归结为取整
- 34.5/345 kV 电压口径仍有冲突，课件不足以确认完整电气拓扑

## 2026-09-23 理解复核

依据当日修订的 32 页课程笔记、对应 LaTeX 与修订记录复核正文，并直接查看原始 Cost Anatomy 课件和新版设备局部图。页码均按 PDF 物理页计算，包含封面与目录。

- 第 11–13 页、视频 00:19:35–00:23:45：区分 PDC、变压器、开关设备、UPS 与冷却循环；34.5/345 kV 冲突仍未解决，不据此补出电压拓扑。冷却初始充水与年度补水不能混用，备电分级也不等于园区 SLA。
- 原 Cost Anatomy 全图右侧存在两处倒置标签；新版 PDF 展示清晰设备局部，并将可见成本单独重排。重排没有改变来源数字，示例成本不能再次加到建设堆叠上。
- 第 18–19 页、视频 00:30:27–00:32:54：IT 标题与口述约 40M 美元/MW，五项合计 41M；讲者承认机房内 CapEx 可能双计，未删项凑整。
- 第 20–21 页、视频 00:34:55–00:37:26：H100/B200 图反映租赁价格而非二手成交；标题“since Dec ’26”与横轴至 2026 年 3 月冲突，只保留可见走势，不自行订正日期。
- 第 22–23 页、视频 00:37:26–00:39:20：总账标题 58M、分项 59M、口述约 60M 是同一粗算的内部差异；工程团队等 OpEx 尚未全部纳入。两年与四年只按收入计算，不能当作现金流回本或 IRR。

本次只复核课程材料、设备说明与成本口径；未独立验证工程拓扑、实际合同、建设预算或项目回报。

## 发布映射

- 博客文章：`content/posts/stanford-mse435-week-03-ai-factories-gigawatt-infrastructure.md`
- 站点 PDF：`/blog/pdfs/stanford-mse435/week-03-ai-factories-gigawatt-infrastructure.pdf`
- GitHub 源文件：`https://github.com/QianKuang8/blog-pdfs/blob/5fe326dc06c33ec0577f6b9c92becabf01412eec/stanford-mse435/week-03-ai-factories-gigawatt-infrastructure.pdf`
- 源 PDF 与公开仓库文件已通过 `cmp` 验证，字节一致。
