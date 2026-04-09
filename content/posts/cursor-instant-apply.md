---
date: '2026-04-05T14:00:00+08:00'
lastmod: '2026-04-09T20:11:36+08:00'
title: 'Cursor Instant Apply：Speculative Edits 实现极速全文件编辑'
summary: "解读 Cursor 的 Speculative Edits 方案——无需 draft model，利用代码编辑的强先验实现 1000 tokens/s 的全文件重写，9 倍加速。"
description: "解读 Cursor Instant Apply 的 Speculative Edits 技术方案"
tags: ["code-editing", "apply"]
origStatus: "available"
author: "Qian"
isCJKLanguage: true
showToc: true
---

解读 Cursor 博客 [Near-Instant Full-File Edits](https://www.cursor.com/blog/instant-apply)（web archive）的技术方案。

## 问题：前沿模型的"编辑差距"

GPT-4、Claude 等前沿模型擅长高层推理，但在全文件代码编辑的机械执行上存在三个核心问题：

- **懒惰和省略**：RLHF 训练倾向简洁，模型常用 `// ...` 省略代码
- **语法不准确**：即使单次编辑也会引入 bug，Agent 常陷入无限循环反复修同一个错误
- **高延迟**：标准自回归生成对大文件太慢，打断开发者心流

## 两阶段架构：Plan and Apply

将编辑过程解耦为两个阶段：

1. **Planning**：高能力前沿模型（Claude 3 Opus / GPT-4o）通过对话确定需要什么修改
2. **Applying**：专用 "fast-apply" 模型执行重写，基于当前文件上下文、对话历史和 Planning 阶段产出的 "sketch"

## 核心技术：Speculative Edits

传统的 Speculative Decoding 需要一个小型 draft model 来猜测 token。Cursor 的创新在于：**不需要 draft model**。

**关键洞察**：代码编辑有"强先验"——原文件中已有的 token。用确定性算法基于当前文件状态推测未来 token，而非依赖第二个模型。

这消除了 VRAM 开销和计算成本，同时保持 70B 参数模型的精度。

**性能指标：**
- 吞吐量：**~1000 tokens/s**（约 3500 字符/s）
- 相比 vanilla Llama-3-70b **13 倍加速**
- 相比之前 GPT-4 speculative edits 部署 **9 倍加速**

## 训练方法

fast-apply 模型基于 **Llama-3-70b** 微调，数据策略：

- **合成/真实数据比 80/20**
- Loss 用 **bits-per-byte** 归一化（跨 tokenizer 可比）
- 三项关键过滤：下采样小文件（<100 LOC）、按文件名封顶、下采样无变更样本

模型选择：评估了 Deepseek Coder 33b，最终选 Llama-3-70b-ft，因为它接近 Claude-3-Opus-diff 的准确度，主观"手感"也更好。

## 全文件重写 vs Diff 格式

| 维度 | 全文件重写 | Search/Replace Diff |
|------|-----------|-------------------|
| Token 效率 | 低（输出更多 token） | 高 |
| 前向传播 | 多（更多"思考"时间） | 少 |
| 分布对齐 | 高（匹配预训练数据） | 低（分布外） |
| 鲁棒性 | 高（避免行号计算） | 不稳定（数字出错） |

**行号问题**：tokenizer 常把 "123" 合并为一个 token，迫使模型在处理足够上下文前就"提交"到特定行号。

## 设计权衡

- **Compute-over-Time**：全文件重写虽然 token 效率低，但更多前向传播给模型更多"思考"空间，确保语法完整性
- **速度定义**：`(重写字符数) / (延迟秒数)`，除以 4（字符/token 比）得到保守的 tokens/s 下界

## 未来方向

- **长上下文训练**：扩展到 2500 行文件，修改 RoPE position ID
- **知识蒸馏**：将 70B 的 fast-apply 能力蒸馏到 Llama-3-8b
- **在线 RL**：用当前部署数据迭代改进编辑准确性

## 原文

- [Near-Instant Full-File Edits](https://web.archive.org/web/20240823050616/https://www.cursor.com/blog/instant-apply)（Web Archive）
