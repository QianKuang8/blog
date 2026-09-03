---
date: '2026-06-05T21:34:00+08:00'
lastmod: '2026-06-05T21:48:35+08:00'
title: 'Coding Agent Serving 的 Scaling Pain：质量问题也可能是系统一致性问题'
summary: "解读 z.ai 关于 GLM-5 Coding Agent Serving 的排障文章：长上下文、高并发和 KV Cache 复用会把底层竞态条件表现成乱码、重复和罕见字符等模型质量问题。"
description: "从 GLM-5 大规模 Coding Agent 推理实践看 PD 分离、KV Cache 竞态、HiCache 同步、Speculative Decoding 监控和 LayerSplit 优化"
tags: ["model-engineering", "agentic-coding"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

z.ai 这篇 [Scaling Pain of Coding Agent Serving](https://z.ai/blog/scaling-pain) 很值得读，因为它讲的不是模型评测，也不是 Agent 产品体验，而是大规模 Coding Agent 推理系统里最容易被忽略的一层：底层状态一致性。

文章的起点很具体。GLM-5 系列在复杂 Coding Agent 任务里出现了乱码、重复、罕见字符生成等异常输出。这些问题在标准推理设置下不会出现，只在高并发、长上下文的 Coding Agent 工作负载里暴露。也就是说，用户看到的是“模型质量问题”，工程上真正要查的却可能是请求调度、KV Cache、异步写入和缓存复用。

## 异常输出不一定来自模型本体

文章先把问题拆成两类假设：如果是模型本身导致，异常通常会在特定输入上稳定复现；如果异常和系统压力、运行时状态相关，就更像推理基础设施的 bug。

团队最初反复重放用户 bad case，没有复现问题。后来他们匿名化生产日志，尽量保留并发分布和请求时序，再通过调整 prefill-decode disaggregation 比例、增加 Prefill backlog 和 Decode 侧 KV Cache 压力，才在离线环境里复现出每 10000 个请求约 3 到 5 个异常输出。

这个细节很重要。Coding Agent 的推理工作负载和普通聊天不同：输入更长、上下文复用更多、请求持续时间更长、并发压力也更复杂。模型没有变，系统状态一旦变复杂，质量问题就可能从基础设施层冒出来。

## Speculative Decoding 变成了质量监控信号

文章里我最喜欢的部分，是他们把 speculative decoding 指标用于异常检测。Speculative decoding 原本是性能优化：draft model 先提出候选 token，target model 再验证接受哪些 token。

但团队发现，异常输出时这组指标会出现稳定模式：乱码和罕见字符通常伴随极低的 `spec_accept_length`，重复通常伴随极高的 `spec_accept_rate`。前者暗示 target model 和 draft model 的 KV Cache 状态严重不匹配，后者暗示被污染的 KV Cache 可能让注意力退化成高置信重复循环。

于是他们做了在线监控：生成超过 128 tokens 后，如果 `spec_accept_length` 持续低于 1.4，或 `spec_accept_rate` 超过 0.96，就主动终止当前生成并交给负载均衡重试。

这让我想到一个更一般的工程原则：推理优化指标不只是优化指标，也可以是模型状态健康度信号。随着 Agent serving 越来越复杂，系统需要的不只是 latency、throughput、availability，还需要能捕捉“模型状态是否仍然可信”的指标。

## 真正的故障来自 KV Cache 生命周期错位

第一类 bug 发生在 PD disaggregation 下的 KV Cache 复用。为了控制尾延迟，系统会在 Prefill 阶段超时时让 Decode abort 请求并回收 KV Cache。问题是 abort 信号没有正确同步到 Prefill 侧。Decode 以为内存可以复用，Prefill 侧之前发出的 RDMA writes 却还在路上。

结果就是，新请求拿到了旧请求的 KV Cache 地址，而旧请求的写入随后覆盖了新请求的缓存。Decode 读到被污染的 KV Cache，自然可能生成乱码、重复或异常 token。

修复方式也很典型：不能只看 Decode 侧是否 abort，还要建立 request termination 和 KV Cache write completion 之间的显式同步。Prefill 只有在没有发起 RDMA 写入，或所有写入都完成后，才返回 safe-to-reclaim 信号。文章说这个修复把异常输出率从约 0.1% 降到 0.03% 以下。

第二类 bug 是 HiCache 的 load-use ordering。Coding Agent 平均输入长度超过 70K tokens，前缀复用率又高，层级 KV 缓存非常关键。但如果 cache swap-in 和计算重叠，却没有保证数据加载完成再使用，就会出现 read-before-ready。团队通过在 Indexer kernel 前加入显式同步，消除了这类异常。

## 我的判断：Agent 时代的推理系统要把 correctness 当一等指标

文章最后的 LayerSplit 优化也很有意思：在 90% cache hit rate、40K 到 120K 请求长度下，吞吐提升 10% 到 132%。但对我来说，这篇文章真正的价值不是某个优化数字，而是它展示了 Coding Agent serving 的新压力模型。

普通聊天系统里，延迟、吞吐、成本已经很难；Coding Agent 又把问题推高一层。长上下文让 KV Cache 成为核心状态，prefix cache 让复用更复杂，高并发让竞态条件更容易暴露，而用户最终看到的不是“缓存错了”，而是“模型胡说了”。

所以我会把这篇文章读成一个提醒：未来 Agent 基础设施不能只追求更快、更便宜，还要证明每一次 generation 背后的模型状态是正确的。否则系统层面的微小竞态，会被包装成模型层面的质量退化，排障成本会非常高。

Coding Agent 的 Scaling Pain，本质上是模型能力扩张之后，基础设施假设开始被真实负载审判。

## 原文

- [Scaling Pain of Coding Agent Serving: Lessons from Debugging GLM-5 at Scale](https://z.ai/blog/scaling-pain)
