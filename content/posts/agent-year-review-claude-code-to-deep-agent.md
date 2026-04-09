---
date: '2026-04-06T11:00:00+08:00'
lastmod: '2026-04-09T20:11:36+08:00'
title: 'Agent 元年复盘：从 Claude Code 到 Deep Agent，架构之争已经结束'
summary: "解读周星星的 Agent 元年总结：Deep Agent 的两个特征（够垂+Long-Running）、Agent Skills 的渐进式披露设计、LangGraph 四大支柱（Planning/Sub-Agent/FileSystem/SystemPrompt）、架构收敛至主从模式，以及从 Workflow 升级为 Agent 的实践路径。"
description: "2025 Agent元年复盘与架构收敛分析"
tags: ["agent"]
origStatus: "available"
author: "Qian"
isCJKLanguage: true
showToc: true
---

解读周星星文章 [Agent 元年复盘：从 Claude Code 到 Deep Agent，Agent 的架构之争已经结束](https://zhuanlan.zhihu.com/p/1983512173549483912)。

## 核心判断：架构之争已定

Agent 架构收敛至以 Claude Code 和 Deep Agent 为代表的**通用型 Agent**形态。2025 年 10 月后基本定局（Manus 到 10 月已重构 5 次，LangChain 10 月才发 v1.0 和 DeepAgent）。

收敛后的架构特点：**Main Agent - Sub Agent 主从架构** + 自主规划能力 + 独立文件系统。

## 哲学转变：管理风险而非消除方差

> "We are managing risk, not eliminating variance."

这是文章提出的关键认知转变。Workflow 追求消除方差（硬编码路径），但面对现实世界的无限边缘情况必然触及"复杂性天花板"。Agent 用自然语言抽象来导航和管理风险，用绝对确定性的代价换取显著更高的能力上限。

更准确地说，复杂度并没有消失——Workflow 将复杂业务逻辑显式构建为"有向图"，Agent 将这些逻辑抽象为自然语言。**复杂度只是从"流程编排"转移到了"Prompt 设计"中**。无论 Workflow 还是 Agent，核心都在实践 **Test-Time Scaling Law**：通过良好的上下文工程让模型"合理"消耗更多 token，换取更高的任务准确率。

## Deep Agent 的两个特征

### 特征一：够"垂"（行业性）

Agent 的知识和能力必须源于行业的**深度实践和共识**，而非通用工具的泛泛输出：

- 招聘 Agent：输出达到高级招聘经理水准的专业背景报告
- 营销 Agent：筛选结果与市场部人工筛选高度重合（70%+），报价在合理区间

衡量标准：假如你的 Agent 输出与通用型工具（如 Manus）一样，那就是不合格的。

### 特征二：Long-Running（稳定性）

典型验证案例：
- Claude 3.7 Sonnet 发布时连续数小时玩宠物小精灵
- Gemini 3 跨应用多步骤旅行规划（查日历→重排会议→创建清单→发送邮件）
- 豆包手机 GUI Agent 完成比价-预订链路

两大维度：长时间运行不崩溃 + 连续保质执行多步骤任务（可能涉及 50+ tool/API 调用）。

## 维度一：用 Skills 融入业务知识

传统做法（硬写 Prompt / RAG）不够"丝滑"。Anthropic 2025 年 10 月提出的 **Agent Skills** 提供了一种优雅解法。

### 渐进式披露（Progressive Disclosure）

Skills 的核心设计原则——三级加载机制：

| 披露层级 | 内容类型 | 加载时机 |
|---------|---------|---------|
| **L1: 元数据** | Skill name + description | 启动时预加载到 System Prompt |
| **L2: 核心逻辑** | SKILL.md 全文 | Claude 判断与当前任务相关时 |
| **L3: 深度上下文** | 附加文件（如 forms.md、Python 脚本） | 特定子任务需要时才导航和加载 |

这个设计让 Agent 变得更轻快、更专注——从"把所有信息一次性塞进 Prompt"变为"按需分级加载"。上下文窗口的变化过程：启动时只含元数据 → 触发时读取 SKILL.md → 需要时读取附加文件。

Skills 还能包含代码（如提取 PDF 表单字段的 Python 脚本），利用代码的确定性保证工作流一致可重复。从这个角度看，Skills 部分取代了 tools/MCP 的作用——将外部不可控的工具调用转化为自主掌控的确定性代码。

### 为什么好

1. **更好的 Context 管理**：分级加载告别暴力全塞
2. **工程师进入"业务心流"**：编写 Skill 本质上是对业务做高内聚、低耦合的抽象——人做高层抽象，AI 完成具体执行
3. **高度可复用**：Skill 是独立文件夹，直接 Copy 即可
4. **Token 效率**：相比 50 个 tools 全部加载到 system prompt，Skill 按需加载

> 落地祛魅：Claude 模型能 98% 稳定触发 Skills，非 Claude 模型可能仅 80% 左右。

## 维度二：怎么做到 Long-Running

LangGraph 提出的四大支柱：

### 1. Planning（规划）

- 用 `write_todos` 等工具将复杂任务分解为离散步骤
- 在模型上下文中创建待办列表，保持执行焦点
- 根据新信息动态调整计划

### 2. Sub-Agents（子代理）

- **上下文隔离**：子任务不污染主 Agent 上下文
- **并行执行**：多个子任务同时进行
- **专业化分工**：不同子 Agent 配置专属工具和指令
- **Token 效率**：只将高度综合的结果返回给主 Agent

架构已收敛到**超强 main-agent + 按需调用 sub-agent**（Supervisor/Worker 模式），额外好处是 KV Cache 利用率高——同一主循环的请求路由到同一 worker，历史上下文可复用，省钱且跑得快。

### 3. File System（文件系统）

- **上下文卸载**：将大量观测数据卸载到文件，用指针替代，防止上下文窗口溢出
- **共享工作区**：所有 Agent（含子 Agent）协作的中介
- **长期记忆**：存储笔记、信息和可执行脚本，按需读回上下文

### 4. System Prompt（系统提示）

最优秀的 coding CLI 和 deep research 拥有**极其复杂详细的系统提示**（数百甚至数千行）。定义：
- 何时暂停执行进行规划
- 何时生成子 Agent vs 自己完成
- 所有工具的详细定义和最佳实践
- 文件命名和目录结构规范

## 工具调用的三层分层设计

解决"超过 100 个工具导致上下文混淆"的问题：

| 层级 | 核心思想 | 示例 |
|------|---------|------|
| **原子层** | ~20 个核心高频正交工具 | read_file, edit_file, bash, ls |
| **沙箱工具层（去工具化）** | 不为每个程序定义 tool，让 Agent 通过 bash 调用预装程序 | 不为 ffmpeg 定义 API，Agent 通过 bash 调用 |
| **代码/包层（逻辑封装）** | 复杂串行逻辑用 Python 脚本一次性执行 | 50 个国家的手机比价：不是 100 次 tool 调用，而是十几行代码的循环 |

底层仍是**渐进式披露**——原子层始终可见，沙箱层按需探索，代码层按需编写。

## 上下文自动压缩

长时间运行中 token 必然超限。当使用量达到上限（如 200k）的 80% 时，自动调用总结模型对前文进行摘要压缩，释放空间同时保留核心任务状态。

## 从 Workflow 升级为 Agent

模仿 Claude Deep Research 的 Prompt 架构——只有三个 prompt 的 main-agent/sub-agent 架构：
1. Main Agent（调度）
2. Sub Agent（执行）
3. 后处理 Agent（引用信息）

核心做法：将复杂的业务流程和决策逻辑，通过极度详尽的 System Prompt 沉淀到 Main Agent 的认知体系中。

> 前提：需要最 SOTA 的模型（Claude 4.5、Gemini 3、GPT 5.2）。没有的话，把任务难度降一级。

Agent 模式的开发路径跳过了 SFT 的数据准备环节，将迭代周期从"周级"压缩至"天级"。本质是通过**消耗 token** 换取效果的快速迭代。

## 垂直场景适配清单

1. **业务知识技能化**：将 SOP 抽象为 Skills，存储在 Agent 文件系统中按需加载
2. **业务接口 MCP 化**：将企业 API 封装为 MCP 服务，Agent 像连接外设一样按需调用
3. **提示词精细化**：分别针对 Main Agent（调度）和 Sub Agent（执行）编写极详细的 System Prompt

## 原文

- [Agent 元年复盘：从 Claude Code 到 Deep Agent，Agent 的架构之争已经结束 | 知乎](https://zhuanlan.zhihu.com/p/1983512173549483912)
