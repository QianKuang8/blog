---
date: '2026-04-05T10:00:00+08:00'
lastmod: '2026-04-05T10:00:00+08:00'
title: 'Zed Edit Prediction：从代码补全到"编辑预测"'
summary: "解读 Zed 的 Next Edit Prediction 技术方案——基于 Qwen2.5-Coder-7B 的 Editing by Rewriting 方法，以及训练、评估和延迟优化的工程实践。"
description: "解读 Zed 的 Next Edit Prediction 技术方案——基于 Qwen2.5-Coder-7B 的 Editing by Rewriting 方法"
tags: ["code-editing", "next-edit"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

解读 Zed 博客 [Edit Prediction](https://zed.dev/blog/edit-prediction) 的技术方案。

## 问题定义：为什么需要 Next Edit Prediction

传统的代码补全基于 **Fill-In-The-Middle (FIM)**——给模型前缀和后缀，让它补中间的文本。FIM 能处理光标处的线性补全，但无法做到"预测开发者下一步要在哪里编辑"。

Next Edit Prediction 的目标是：

- **预测意图**：在开发者主动操作之前预判下一步
- **即时响应**：p50 延迟 < 200ms
- **非线性编辑**：支持文件内任意位置的编辑预测，而非仅限光标所在行
- **无缝集成**：Tab 键确认，Alt/Option 键预览（避免与 LSP 补全冲突）

## 核心方案：Editing by Rewriting

Zed 的 Zeta 模型基于 **Qwen2.5-Coder-7B** 微调，采用了 **"Editing by Rewriting"** 方法：

不再把编辑当作"在空隙中填文本"的问题，而是把光标周围的代码片段视为一个可重写的块——模型接收这段代码，直接输出包含预测修改的完整重写版本。

模型输入三个信息：
1. **Recent Edits**：开发者最近的编辑历史
2. **Cursor Position**：当前光标位置
3. **Contextual Excerpt**：光标周围的代码片段

这种方案让模型能进行复杂的结构化变换，而不仅仅是逐 token 的 diff。

## 训练流程：SFT + DPO

### 第一阶段：SFT（监督微调）

面临"鸡生蛋"问题——训练需要真实的编辑历史数据，但公开数据集里没有这种数据。解决方法：

1. **合成引导**：用 Claude 生成 50 个初始样本，定义任务结构
2. **内部 Dogfooding**：在 Zed 内部发布早期版本，收集约 400 个高质量真实开发场景样本

SFT 的目标：
- **意图逻辑**：让模型学会从编辑模式推断下一步操作
- **语法完整性**：确保重写后的代码片段无语法错误

### 第二阶段：DPO（直接偏好优化）

SFT 之后模型仍有问题——在大文件中偶尔会触发随机删除或插入。通过约 150 个正负样本对进行 DPO，教会模型识别并避免"幻觉"行为（如破坏性插入）。

## 评估：LLM-as-a-Judge

传统单元测试对生成式代码任务不适用——即使输出逻辑正确，也可能和参考字符串差几个 token。即使使用 temperature 0 + 固定 seed 也无法消除生成式模型固有的输出方差。

Zed 的解决方案是用 **Claude 作为评判者**：用自然语言描述预期逻辑，让 Claude 判断 Zeta 的输出是否满足意图。从"文本一致性"转向"功能正确性"的评估。

## 延迟优化

目标：p50 < 200ms，p90 < 500ms。

### Speculative Decoding

Rewriting 的 token 生成量比 FIM 大，但有一个关键特征：输出和输入 90%+ 相同。利用这个相似性，通过 **n-gram 搜索** 匹配输入输出中的相同片段，找到"跳跃点"并行生成 token，绕过自回归解码的顺序限制。

### 部署架构

- **Baseten**：GPU 推理基础设施
- **Cloudflare Workers**：边缘路由降低网络开销
- **地理分片**：北美和欧洲部署 GPU 集群，缩短物理距离

## FIM vs Rewriting 对比

| 特性 | FIM | Zeta Rewriting |
|------|-----|---------------|
| 任务类型 | 线性文本补全 | 结构化编辑预测 |
| 编辑位置 | 仅光标处 | 片段内任意位置 |
| 模型输出 | 在空隙中填文本 | 重写整个片段 |
| 上下文输入 | 静态前缀+后缀 | 编辑历史+光标+片段 |
| 历史感知 | 无 | 高（基于最近编辑记录） |

## 关键设计决策

- **模型大小 vs 延迟**：32B 模型性能更好但无法满足延迟要求，最终选择 7B
- **Rewriting vs 粒度编辑**：Rewriting token 开销更大，但提供了多位置编辑的结构灵活性，通过 speculative decoding 弥补
- **Prompt Engineering 的局限**：早期用 prompt engineering 调优容易回归（修一个 case 坏另一个），最终转向正式的 SFT/DPO 训练流程才稳定

## 原文

- [Zed Edit Prediction](https://zed.dev/blog/edit-prediction)
