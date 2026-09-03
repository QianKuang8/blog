---
date: '2026-06-05T21:28:00+08:00'
lastmod: '2026-06-05T21:48:35+08:00'
title: 'LLM 架构比较：今天的创新更多是在效率边界上'
summary: "解读 Sebastian Raschka 的大模型架构比较：从 DeepSeek V3 到 GLM-5，现代 LLM 仍延续 Transformer 主干，真正的变化集中在注意力、MoE、归一化、位置编码和推理效率。"
description: "从 The Big LLM Architecture Comparison 看 MLA、MoE、GQA、滑动窗口注意力、QK-Norm、线性注意力和现代 LLM 架构演化"
tags: ["model-engineering", "行业动向"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Sebastian Raschka 这篇 [The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison) 很长，也很适合作为现代 LLM 架构的参考索引。它的核心问题是：从 GPT-2 到 DeepSeek V3、Llama 4、Qwen3、GLM-5，这些模型到底在架构上发生了什么变化？

文章开头的判断很克制：七年过去了，现代旗舰模型看起来仍然和原始 GPT 架构有很多相似之处。真正的变化不是推翻 Transformer，而是在多个局部做效率和稳定性改造。

## 架构创新主要围绕注意力和专家结构

文章讨论 DeepSeek V3/R1 时重点放在 MLA 和 MoE。MLA 解决的是 KV cache 和注意力计算效率问题；MoE 则通过稀疏激活扩大参数规模，同时控制每次推理的计算量。

这也是今天 LLM 架构创新的主线之一：模型要更大、上下文要更长、推理要更便宜，不能只靠堆 dense 参数。于是 GQA、MLA、sliding window attention、linear attention、partial RoPE、multi-token prediction、MoE sparsity 等技术不断出现。

它们共同回答的是一个问题：怎样在可承受的内存和延迟下，让模型拥有更强表达能力和更长上下文。

## 很多变化不是能力炫技，而是推理工程

我读这篇文章最大的感受是，现代 LLM 架构越来越像模型研究和推理工程的合谋。比如 GQA 减少 key/value 头，降低 KV cache 压力；滑动窗口注意力牺牲全局注意力换效率；MoE 的 expert 数量和大小直接影响服务端调度；multi-token prediction 又和 speculative decoding 接上。

这些设计不只是论文里的结构图，它们会直接影响部署成本、延迟、吞吐和长上下文可用性。对于应用开发者来说，理解这些概念，不是为了自己训练模型，而是为了理解为什么某些模型便宜、快、长上下文强，另一些模型在特定任务上更稳定。

## 我的判断：基础架构仍稳定，优化空间还很大

这篇文章让我更不相信“下一代架构马上完全替代 Transformer”这种说法。现实更像是：Transformer 主干继续存在，但周围的效率结构不断演化。

未来一段时间，大模型架构的竞争可能仍然集中在几个方向：更高效的 attention、更好的 sparse expert 设计、更长上下文的可控外推、更贴近推理服务的训练目标，以及更强的推理时计算利用。

所以这篇文章适合收藏。它不是一篇可以一口气完全消化的短评，而是一张现代 LLM 架构术语地图。读懂这些术语，会帮助我们更清楚地判断模型发布时哪些是营销话术，哪些是真正会改变成本和能力边界的结构变化。

## 原文

- [The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
