---
title: "How the Claude Code team uses Claude Code"
source_url: "https://www.youtube.com/watch?v=S-sYlFiGFv8"
source_type: "video"
channel: "Claude"
speaker: "Thariq Shihipar、Sid Bidasaria、Robert Boyce"
published_at: "2026-09-02"
duration: "22:23"
retrieved_at: "2026-09-08T15:32:54+08:00"
series: ""
pdf_path: "standalone/how-claude-code-team-uses-claude-code.pdf"
---

## 来源范围

- 视频 ID：`S-sYlFiGFv8`，标题、频道、讲者、发布日期及章节来自原视频元数据和说明。
- 本次读取材料：已保存的原视频元数据、人工英文字幕 `en`（657 条有效时间记录）、中文讲义及最终 14 页 PDF；读取日期为 2026-09-08。
- 实质讨论范围：`00:00:20–00:22:17`。开场预告与片尾不另作论据。
- PDF 是根据视频整理的中文学习讲义，包含 6 章和 6 张矢量关系图；重绘图与编者综合不作为讲者原话。
- 视频画面为桌边访谈。博客采用一张根据讨论重绘的机制图，不把访谈人像当作技术证据。

本记录只保存元信息、论点索引和发布映射；原视频、音频、完整字幕、候选帧及生成日志不纳入博客仓库。本文记录团队在这次访谈中描述的工作方式，不据此断言 Claude Tag、workflows 或 routines 的公开可用范围。

## 官方章节

| 章节 | 时间 | 内容 |
|---|---|---|
| Intro | `00:00:00–00:00:35` | 开场与工作方式变化 |
| Working through Claude Tag: from tool calls to goals | `00:00:35–00:02:17` | Slack 上下文与目标委派 |
| Building on technology that evolves every two months | `00:02:17–00:04:48` | 模型演进与工具取舍 |
| How the Claude Code team uses Claude Code: AskUserQuestion, artifacts, and Claude Tag | `00:04:48–00:06:41` | 交互工具与可视化产物 |
| Running loops and routines remotely | `00:06:41–00:08:52` | 从笔记本转向远端持续工作 |
| How code review inspired dynamic workflows | `00:08:52–00:14:04` | 并行查找、对抗复核、动态编排 |
| Building Claude Tag with Claude Tag: verification and feedback loops in Slack | `00:14:04–00:18:37` | 开发环境、消息界面、验证与反馈 |
| What they miss about the old way of software engineering | `00:18:37–00:22:23` | 工程师的手艺、创造与角色变化 |

## 关键论点与证据边界

| 论点 | 证据时间 | 来源属性与发布边界 |
|---|---|---|
| Slack 中的产品讨论和团队决策帮助代理理解更大的目标 | `00:00:35–00:02:17` | 团队成员的使用经验；70%–80% 是成员对个人工作比例的口述，不是全团队统计 |
| 待办列表曾弥补模型做五件事只完成三件的失效；模型变强后需要重新评估旧支撑 | `00:03:19–00:04:48` | 访谈中的历史回顾；Sonnet 3.5 带有“maybe”限定，不据此确定版本或产品移除日期；更大任务仍会需要新工具 |
| AskUserQuestion 从规划后的步骤变为可调用工具，成员又开始使用带图和 mockup 的 HTML artifact 提问 | `00:05:39–00:06:41` | 工具设计及个人使用历程；不表示提问工具已经被产品弃用 |
| 远端环境解除笔记本在线限制，接入开发环境后才能承担持续工作 | `00:06:48–00:08:14` | 使用经历；“10x”是个人生产力感受，没有测量基线，正文不将其写为效果数据 |
| routines 可以每天汇集反馈、按重要性归类并处理高把握的修复 | `00:08:14–00:08:52` | 讲者举例；不扩写成所有反馈都可自动修复或生产环境自动部署 |
| 人工审查应关注 API 设计和服务边界等背景判断，代理帮助准备相关信息 | `00:09:16–00:10:42` | 讲者对注意力分配的判断；不表示人不再审查代码 |
| 并行查找后，对候选问题从不同视角复核，过滤后呈现给人 | `00:10:42–00:11:48` | 讲者描述审查机制；“三种视角”指候选问题复核，不是固定三个搜索代理；没有准确率、漏报率或成本数据 |
| 代理按问题组织子代理，并用代码串联查找、筛选、验证和汇总 | `00:11:48–00:14:04` | workflow 的设计说明；推理阶段计算与确定性代码相结合，循环遍历本身不保证语义判断正确 |
| Claude Tag 的主要消息界面与详细执行记录分开，代理通过工具选择沟通时机和内容 | `00:14:51–00:16:13` | 产品使用描述；消息工具负责发送，决策由代理作出；transcripts 不等于可读取模型原始内部思维 |
| 工具开发案例覆盖寻找同事、mockup、实现、内部试用、事件监测、反馈和改进使用漏斗 | `00:16:13–00:17:26` | 单个使用案例；将这些活动连成闭环属于整理者归纳，不是团队固定发布流程 |
| 验证、代码审查与获取反馈相互补充；测试、截图和录屏帮助验收，成员仍亲自试用 | `00:17:26–00:18:32` | 讲者明确区分的三类活动；不能据此写成已取消人工验收 |
| 成员怀念性能优化和 UI 细节打磨，同时把更多精力转向快速实现新想法 | `00:19:26–00:22:17` | 个人感受；不泛化为所有工程师的体验或能力比较 |

## 图示与整理者判断

- 博客图示：`static/images/how-claude-code-team-uses-claude-code/review-workflow.svg`，根据视频 `00:09:16–00:14:04` 重绘，展示并行搜索、逐项复核和汇总给人的关系；分支数量只为示意。
- 博客围绕目标与上下文、工具演进、持续执行、审查及反馈组织主题；这不是原视频的逐章转写。
- “把监督从每次工具调用转向目标和证据”“扩大委派前先打通验证与反馈”等表述属于整理者基于案例的判断，不是访谈给出的量化结论。

## 发布映射与文件校验

- 博客文章：`content/posts/how-claude-code-team-uses-claude-code.md`
- 站点 PDF：`/blog/pdfs/standalone/how-claude-code-team-uses-claude-code.pdf`
- GitHub 源文件：`https://github.com/QianKuang8/blog-pdfs/blob/e71c1c8252555b885aa1797408fe1784c4ad048a/standalone/how-claude-code-team-uses-claude-code.pdf`
- 选定源文件：`Claude_Code团队的AI协作实践_notes.pdf`（源目录根部最终交付版）。
- PDF 页数：14 页
- PDF 字节数：566,836
- SHA-256：`8a6237e3c9aba84fe69253baf7a1947696d135fc1592b4cc0c004aa3916cd172`
- 发布时以 `cmp` 校验选定源文件、公开 PDF 仓库文件和 Hugo 产物；保留源 PDF 字节，不压缩、不重新编码。
