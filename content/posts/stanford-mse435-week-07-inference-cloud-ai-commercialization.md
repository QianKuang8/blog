---
date: '2026-08-31T17:30:00+08:00'
lastmod: '2026-08-31T17:30:00+08:00'
title: '从定制模型到推理云：为什么离开前沿 API 可能是正确的商业决策'
summary: "推理量将增长'十亿倍'只是问题设置，真正的问题是：当 AI 从回答问题变成交付服务，推理基础设施的经济学、定制化路径和算力稀缺如何共同决定应用的毛利和防御性。"
description: "解读 Stanford MS&E 435 Week 7：Baseten 的推理云、后训练闭环、定制模型经济学、多云推理、算力稀缺与垂直整合"
tags: ["视频笔记", "model-engineering", "行业动向"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

[Stanford MS&E 435 Week 7](https://www.youtube.com/watch?v=Qh7Oxvo5sJI) 把注意力从"模型如何训练"移到"训练好的模型如何在线上反复交付价值"。当 AI 功能渗入更多工作流，且单个应用又调用更多模型时，推理就从一项事后运维工作变成产品本身的交付层。

嘉宾是 Tuhin Srivastava（Baseten 联合创始人兼 CEO），由 Apoorv Agrawal 主持。视频由 Stanford Online 发布于 2026 年 6 月 5 日，时长 49 分 15 秒。本文依据完整英文字幕和 26 页课程笔记整理。

## 四个核心判断

1. 推理不只是部署——它是 AI 应用的交付层，延迟和可靠性直接等于用户体验。
2. 离开前沿 API 转向定制模型有两个理由：可生存性（成本差进入毛利）和防御性（把独特工作流留在自己控制的系统里）。
3. 算力稀缺推动垂直整合：软件粘性和 GPU 稀缺是两种相反的押注，当前市场同时存在。
4. 开放模型是产业战略变量，不只是技术选择。

## 推理如何成为应用的交付层

Tuhin 用两个客户案例说明推理平台的价值不只是"提供 GPU"。Wispr Flow 需要极低延迟的语音转文字——延迟就是界面体验。Abridge 需要在医疗工作流中保持高可靠性——一次推理故障就是产品故障。[00:03:03–00:08:00](https://www.youtube.com/watch?v=Qh7Oxvo5sJI&t=183s)

裸 GPU 不等于推理平台。从裸机到可靠的 token 交付，中间需要自动扩缩容、模型版本管理、故障切换、延迟优化和成本核算。这些系统工程才是推理平台的真正价值。

## 定制模型的经济学：可生存性与防御性

Tuhin 提出了一个重要的反方：为什么要离开"自动升级"的前沿 API？每次 OpenAI 或 Anthropic 发布新模型，你的产品就自动变好——这是一个很强的论点。[00:08:00–00:10:30](https://www.youtube.com/watch?v=Qh7Oxvo5sJI&t=480s)

但他给出两个离开的理由。第一是可生存性：前沿 API 的价格让很多应用无法实现正毛利；定制模型（通过后训练优化的小模型）可能在特定任务上接近前沿性能，但成本低一个量级。[00:08:00–00:10:30](https://www.youtube.com/watch?v=Qh7Oxvo5sJI&t=480s)

第二是防御性：如果你的独特工作流全部运行在别人的 API 上，你的核心竞争力可以被任何使用同一 API 的竞争者复制。把独特数据和后训练过程留在自己控制的系统里，形成的护城河更深。[00:10:30–00:13:00](https://www.youtube.com/watch?v=Qh7Oxvo5sJI&t=630s)

## 后训练闭环与数据信任

Baseten 的商业模式从"算力加价"演进为"每 token 价值"：不只是卖 GPU 时间，而是帮客户完成从数据到基础模型选择、后训练、部署到线上推理的完整闭环。[00:13:00–00:19:00](https://www.youtube.com/watch?v=Qh7Oxvo5sJI&t=780s)

Tuhin 把数据托管称为"王国的钥匙"——这首先是信任问题，不是技术问题。客户把训练数据交给平台，意味着平台必须在安全、隔离和合规上达到企业标准。这种信任一旦建立，切换成本就很高。

## 开放模型与多云推理

Baseten 的两项基础假设是：开放模型会持续存在且持续改进；推理需求会远超任何单一云厂商的供给。[00:19:00–00:25:00](https://www.youtube.com/watch?v=Qh7Oxvo5sJI&t=1140s)

多云聚合把分散在不同云厂商的 GPU 变成统一交付面。这对客户的价值是减少对单一供应商的依赖；对 Baseten 的价值是在算力稀缺时有更多供给选择。

Tuhin 还讨论了算力稀缺为何推动垂直整合：当 GPU 提前期长达 12-15 个月，推理平台必须提前锁定容量。这不是简单的软件问题，而是需要资本投入和供应链管理的基础设施问题。[00:25:00–00:35:00](https://www.youtube.com/watch?v=Qh7Oxvo5sJI&t=1500s)

## 我的判断：推理是 AI 的"最后一英里"

这场课堂最值得带走的认知是：推理之于 AI，就像配送之于电商——它是价值链中最接近用户的环节，也是成本最难压缩、体验最直接可感的环节。

我认为定制模型的经济学论证特别有启发。很多 AI 创业公司被困在一个三难困境中：用前沿 API 成本太高（毛利为负），用开源模型能力不够（用户体验差），用定制模型需要数据和后训练能力（技术门槛高）。Baseten 试图做的是降低第三条路的门槛。这条路是否走得通，取决于后训练能否真正接近前沿性能——这仍然是一个开放问题。

## 关键时间索引

- [00:00:09–00:03:03：推理增长与创业路径](https://www.youtube.com/watch?v=Qh7Oxvo5sJI&t=9s)
- [00:03:03–00:08:00：推理作为应用交付层](https://www.youtube.com/watch?v=Qh7Oxvo5sJI&t=183s)
- [00:08:00–00:13:00：定制模型的经济学](https://www.youtube.com/watch?v=Qh7Oxvo5sJI&t=480s)
- [00:13:00–00:19:00：后训练闭环与数据信任](https://www.youtube.com/watch?v=Qh7Oxvo5sJI&t=780s)
- [00:19:00–00:35:00：开放模型、多云推理与算力稀缺](https://www.youtube.com/watch?v=Qh7Oxvo5sJI&t=1140s)
- [00:35:00–00:49:15：供给侧创业与全栈优化](https://www.youtube.com/watch?v=Qh7Oxvo5sJI&t=2100s)

## 继续阅读

- [原视频：Applications, Applied AI](https://www.youtube.com/watch?v=Qh7Oxvo5sJI)
- [完整课程笔记 PDF：26 页](/blog/pdfs/stanford-mse435/week-07-inference-cloud-ai-commercialization.pdf)
- [在 GitHub 查看发布源文件](https://github.com/QianKuang8/blog-pdfs/blob/85c8d5d/stanford-mse435/week-07-inference-cloud-ai-commercialization.pdf)
