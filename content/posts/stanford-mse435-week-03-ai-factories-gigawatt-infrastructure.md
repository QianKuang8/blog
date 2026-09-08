---
date: '2026-08-31T17:10:00+08:00'
lastmod: '2026-09-08T15:38:17+08:00'
title: '从电子到 Token：吉瓦级 AI 工厂的物理约束与经济回报'
summary: "AI 产品看起来是聊天框或 API，但每次训练与推理都要经过芯片、电力、冷却、建筑和网络。这场 Stanford 课堂用 Crusoe 的 Abilene 项目，把数据中心从抽象 CapEx 数字拆成能源选址、设备堆叠、互联集群和 token 服务的完整物理链。"
description: "解读 Stanford MS&E 435 Week 3：吉瓦级 AI 工厂的能源选址、CapEx 堆叠、算力经济寿命与从基础设施出租到 token 服务的商业模式演进"
tags: ["视频笔记", "model-engineering", "行业动向"]
categories: ["视频笔记"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

[Stanford MS&E 435 Week 3](https://www.youtube.com/watch?v=GcCGzfKdCd0) 真正回答的不是"数据中心长什么样"，而是"从一度电到一个 token，中间经过哪些物理环节，每个环节的成本结构和约束是什么，最终能否产生足以覆盖巨额 CapEx 的经济回报"。

嘉宾是 Chase Lochmiller，Crusoe 创始人兼 CEO。视频由 Stanford Online 发布于 2026 年 6 月 17 日，时长 49 分 47 秒。本文依据 1147 条人工英文字幕和 30 页课程笔记整理。需要特别注意：MW/GW 是功率而非年度能量；所有"每 MW 成本"是当场粗算；四年和两年回收期是按收入计算的静态估计，不是利润或 IRR。

## 三个核心判断

1. AI 数据中心是宏观基础设施，不是模型之外的附属机房。软件需求最终落在物理约束上。
2. 瓶颈会移动：今天可能是 GPU 供给，明天可能是电力、冷却、互联或劳动力。垂直整合的价值在于协调多个约束。
3. 越靠近 token 服务，收入上限越高，但成本和风险也越未知。从基础设施出租到 token 服务是一条商业模式演进链。

## 从 CapEx 图进入物理世界

主持人用五家超大规模云厂商的 AI 资本开支图开场：曲线快速向右上方延伸，他把本轮投入与太空计划和美国高速公路体系比较，称其规模仅次于美国国防预算。[00:00:14–00:00:48](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=14s) 这些宏大类比建立量级直觉，但在缺少统计口径时不能改写为经审计的历史排名。

问题随后被落到一条物理链：训练、微调和大规模推理都要让 GPU 真正获得电力、冷却和互联，并持续向用户交付 token。主持人把数据中心相关投入概括为约 6500 亿美元。[00:02:39–00:03:07](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=159s)

Lochmiller 把 AI 生产拆成五类要素：数据、算法、算力、能源和数据中心。Crusoe 聚焦后三项物理层——算力、能源与数据中心如何建设、运营和提高利用率。[00:03:08–00:04:59](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=188s) 他用"从电子到 token"描述完整链条：把电子变成计算，把计算变成训练和推理，把推理变成"数字劳动力"（digital workforce），后者的服务价值可以类比人类知识工作者的时薪。[00:05:00–00:07:30](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=300s)

## Energy-first：为什么搬数据而不是搬电

Crusoe 的垂直整合覆盖能源获取、电力基础设施、数据中心建设和 GPU 云服务，但明确不做芯片设计和模型训练。[00:07:30–00:10:00](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=450s)

Lochmiller 的核心选址逻辑是 energy-first：不是先选城市再拉电力，而是先找到电力供给过剩、价格低甚至出现负价的地方，再把数据中心建在那里。[00:10:00–00:13:16](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=600s) 他的原话是"搬数据比搬电便宜"——光纤传输数据的成本远低于输电线传输电力的损耗和建设成本。

Abilene（得克萨斯）项目是主要案例：该地区可再生能源供给过剩、电价一度为负，Crusoe 从 200 MW 起步，当前规划扩展到 2.1 GW。[00:13:16–00:18:32](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=796s) 八栋建筑通过高速互联形成一个统一集群，而不是八个独立机房。

## CapEx 堆叠：19.2M 美元/MW 的构成

讲者把基础设施 CapEx 拆成详细的逐项堆叠，总计约 19.2M 美元/MW。[00:23:45–00:30:20](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=1425s) 其中劳务约 4.7M 美元/MW，占比约四分之一——这在传统软件讨论中几乎不会出现，却是物理基础设施的硬约束。

IT CapEx（GPU、网络、存储）则是另一大块，约 40M 美元/MW 量级。[00:30:20–00:37:26](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=1820s) 互联架构分两级：机架内 NVLink，跨机架 InfiniBand 或 RoCE。这两级网络的带宽和延迟决定了集群能否真正作为一个系统工作。

算力的经济寿命是一个容易误判的问题。GPU 二手市场出现价格反弹不能证明更长的折旧期——商品化、规模效应和前沿需求可以同时成立。[00:34:00–00:37:26](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=2040s)

## 从基础设施出租到 Token 服务

Lochmiller 描述了一条商业模式演进链：最基础是出租电力和机房空间（infrastructure-as-a-service）；往上是出租 GPU 算力（compute-as-a-service）；最高是直接卖 token（intelligence-as-a-service）。[00:37:26–00:40:49](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=2246s)

越靠近 token，收入上限越高——因为客户付费的依据从"用了多少电"变成"完成了什么任务"。但成本和风险也越未知：基础设施出租的利润率相对可预测，token 服务则要承担模型效率、利用率波动和客户需求变化。

讲者给出的粗算是按收入约四年回收基础设施投入，如果卖 token 则可能缩短到约两年。[00:38:00–00:40:49](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=2280s) 但这两个数字都是静态回收期（revenue-basis payback），不是利润或 IRR——它们没有扣除运营成本、折旧或资金成本。

## 我的判断：物理约束是 AI 的隐性税

这场讲座最值得带走的认知是：AI 的物理层不是一个可以抽象掉的实现细节，而是决定成本下限和扩展上限的硬约束。每一度电、每一立方米冷却水、每一条互联带宽、每一个劳动力工时，都是 token 成本的组成部分。

我认为 Lochmiller 的 energy-first 思路代表了一种有意思的逆向逻辑：不是从需求出发找供给，而是从供给过剩出发创造需求。这在能源转型背景下特别有价值——可再生能源的间歇性和地理集中性恰好可以被 AI 工作负载的灵活性和可迁移性吸收。

但风险也很明确：垂直整合意味着同时承担能源、建设、运营和客户需求的波动。如果 AI 需求增速放缓或算力效率跳升导致单位需求下降，已建成的吉瓦级基础设施就变成沉没成本。这也是为什么从基础设施出租向 token 服务演进不只是商业选择，更是风险对冲。

## 关键时间索引

- [00:00:00–00:07:30：AI 工厂为何成为宏观基础设施](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=0s)
- [00:07:30–00:13:16：垂直整合与 energy-first 选址](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=450s)
- [00:13:16–00:18:32：Abilene 吉瓦级项目](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=796s)
- [00:23:45–00:30:20：基础设施 CapEx 堆叠](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=1425s)
- [00:30:20–00:37:26：IT CapEx 与算力经济寿命](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=1820s)
- [00:37:26–00:40:49：从基础设施出租到 token 服务](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=2246s)
- [00:40:49–00:49:47：模块化降本与未来电力栈](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=2449s)

## 继续阅读

- [Stanford MS&E 435 系列目录]({{< relref "/topics/stanford-mse435.md" >}})：查看 Week 1–9 的主题与阅读顺序。
- [原视频：Building AI Factories](https://www.youtube.com/watch?v=GcCGzfKdCd0)
- [完整课程笔记 PDF：30 页](/blog/pdfs/stanford-mse435/week-03-ai-factories-gigawatt-infrastructure.pdf)
- [在 GitHub 查看发布源文件](https://github.com/QianKuang8/blog-pdfs/blob/2eaabbb/stanford-mse435/week-03-ai-factories-gigawatt-infrastructure.pdf)
