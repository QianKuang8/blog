---
date: '2026-04-06T10:30:00+08:00'
lastmod: '2026-04-07T22:43:56+08:00'
title: '深入解析 Codex 智能体循环'
summary: "解读 OpenAI Codex Agent Loop 的技术架构：推理-执行迭代机制、Responses API 集成、Prompt 构造与角色层级、无状态架构与 ZDR、以及 Prompt Caching 和上下文压缩策略。"
description: "Codex Agent Loop 技术架构深度解析"
tags: ["agent"]
origStatus: "missing"
author: "Qian"
isCJKLanguage: true
showToc: true
---

解读 OpenAI 官方博客 [深入解析 Codex 智能体循环](https://openai.com/zh-Hans-CN/index/unrolling-the-codex-agent-loop/)。

## Agent Loop：软件 Agent 的核心编排逻辑

Agent Loop 是 Codex 框架的核心编排逻辑，协调用户、LLM 和工具集之间的交互。关键概念：

- **交互轮次**：从用户输入到最终响应的完整旅程，通常包含多次内部迭代
- **推理 vs 执行**：模型推理（消费 prompt 生成 token）与工具执行（shell 命令等）交替进行
- **主要输出**：不是聊天消息，而是对**本地文件系统或环境的直接修改**

## 推理-执行迭代机制

通过 SSE (Server-Sent Events) 处理流式数据和工具生命周期：

1. **输入与 Token 化**：用户输入和环境上下文聚合并转换为 token
2. **推理与 SSE 处理**：模型生成响应流，Codex 处理特定 SSE 事件：
   - `response.output_text.delta`：实时 UI 流式展示
   - `response.output_item.added`：转换为内部对象追加到下次输入
   - `response.output_item.done`：标记推理或工具调用项完成
3. **迭代子循环**：如果生成 `function_call`，执行工具 → 将输出追加到输入列表 → 重新推理
4. **终止**：模型返回不含工具请求的 assistant message 时循环结束

## Responses API：可配置的后端抽象

Codex 可通过 `~/.codex/config.toml` 中的 `responses_api_endpoint` 指向不同后端：

| 端点类型 | URL |
|---------|-----|
| ChatGPT 后端 | `chatgpt.com/backend-api/codex/responses` |
| OpenAI API | `api.openai.com/v1/responses` |
| 本地/OSS (gpt-oss) | `localhost:11434/v1/responses`（支持 Ollama/LM Studio） |
| 云厂商 | Azure 托管的 Responses API |

请求 payload 三个参数：
- `instructions`：核心行为定义（未指定则用模型特定文件如 `gpt-5.2-codex_prompt.md`）
- `tools`：包含内部工具、API 工具和 MCP 工具的函数列表
- `input`：包含 `type`、`role`、`content` 的对话历史

## Prompt 构造与角色层级

角色权重由层级决定，控制权分布是关键设计：

| 角色 | 优先级 | 控制方 |
|------|--------|--------|
| `system` | 最高 | 服务端（核心安全和对齐） |
| `developer` | 高 | 客户端（沙盒权限和工程约束） |
| `user` | 标准 | 具体任务请求和环境数据 |
| `assistant` | 信息性 | 历史推理和工具结果 |

### 初始化序列（构建静态缓存前缀）

1. **沙盒权限**（`role=developer`）：定义 shell 工具限制（仅适用于 Codex 工具，MCP 工具需自行实现安全）
2. **开发者指令**（`role=developer`）：来自本地 `config.toml`
3. **项目上下文**（`role=user`）：来自 `AGENTS.md`，有 32 KiB 限制，从 CWD 向上扫描到 Git root
4. **环境上下文**（`role=user`）：声明 CWD 和活跃 Shell 类型

## 无状态架构与 Zero Data Retention

Codex 刻意避免使用 `previous_response_id`：

- **代价**：每次请求传输完整对话历史，JSON payload "二次增长"
- **理由**：确保**无状态架构**，对 ZDR 合规至关重要——服务器可能持有解密密钥，但不存储对话数据
- **可接受性**：网络开销远低于模型采样成本

## Prompt Caching 与 Append-Only 策略

为维持线性采样复杂度，依赖**精确前缀匹配**缓存：

- **缓存未命中的陷阱**：动态工具枚举（MCP server 排序变化）、对话中换模型、环境配置变更
- **Append-Only**：配置变更（如目录切换）时，不修改原始环境消息，而是在 input 末尾**追加**新消息，保留所有前序 token 的缓存前缀

## 上下文压缩（Compaction）

防止超出 token 限制：

- **手动**：`/compact` 命令生成摘要替代历史
- **自动**：达到 `auto_compact_limit` 后调用 `/responses/compact` 端点
- **技术细节**：返回 `type=compaction` 项和 opaque `encrypted_content`，模型以压缩无状态格式保留"理解"，同时释放上下文窗口

## 工程实践要点

- **确定性工具枚举**：MCP 工具列表必须保持一致排序
- **静态指令优先**：核心指令和项目文档放在 payload 开头
- **客户端侧 MCP 安全**：不假设 Codex 沙盒覆盖第三方 MCP 工具
- **Append-Only 状态更新**：环境变量或 CWD 变更时追加而非编辑历史
- **关注压缩阈值**：关键项目指令放在 `instructions` 或早期 `input` 项中

## 原文

- [深入解析 Codex 智能体循环 | OpenAI](https://openai.com/zh-Hans-CN/index/unrolling-the-codex-agent-loop/)
