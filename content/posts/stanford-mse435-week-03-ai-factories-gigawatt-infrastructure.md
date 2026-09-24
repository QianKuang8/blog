---
date: '2026-08-31T17:10:00+08:00'
lastmod: '2026-09-23T14:27:57+08:00'
title: '从电子到 Token：吉瓦级 AI 工厂的物理约束与经济回报'
summary: "AI 产品看起来是聊天框或 API，但每次训练与推理都要经过芯片、电力、冷却、建筑和网络。这场 Stanford 课堂用 Crusoe 的 Abilene 项目，把数据中心从抽象 CapEx 数字拆成能源选址、设备堆叠、互联集群和 token 服务的完整物理链。"
description: "解读 Stanford MS&E 435 Week 3：吉瓦级 AI 工厂的能源选址、CapEx 堆叠、算力经济寿命与从基础设施出租到 token 服务的商业模式演进"
tags: ["model-engineering", "行业动向"]
categories: ["视频笔记"]
author: "Qian"
isCJKLanguage: true
showToc: true
learning_status: pending
---

AI 服务背后需要多大的电力、冷却和建设投入？[Stanford MS&E 435 Week 3](https://www.youtube.com/watch?v=GcCGzfKdCd0) 以 Crusoe 的数据中心项目为例，把抽象的资本开支拆成选址、建筑、设备与服务收入，讨论这些环节怎样约束 token 生产。

嘉宾是 Chase Lochmiller，Crusoe 创始人兼 CEO。视频由 Stanford Online 发布于 2026 年 6 月 17 日，时长 49 分 47 秒。本文依据 1147 条人工英文字幕及 2026 年 9 月 23 日修订的 32 页课程笔记整理。需要特别注意：MW/GW 是功率而非年度能量；所有"每 MW 成本"是当场粗算；四年和两年回收期是按收入计算的静态估计，不是利润或 IRR。

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

Abilene（得克萨斯）项目是主要案例：该地区可再生能源供给过剩、电价一度为负，Crusoe 从 200 MW 起步，按讲者当时介绍的规划扩展到 2.1 GW。[00:13:16–00:18:32](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=796s) 八栋建筑通过高速互联形成一个统一集群，而不是八个独立机房。

## 配电、冷却与可靠性各自解决什么

在算成本之前，先要分清设备职责。PDC（配电中心）组织配电，变压器改变电压，开关设备控制和保护回路，UPS 在中断时短时支撑关键负载。字幕先出现 34.5 kV，后续又出现 345 kV，课件没有足够的电压标注消解冲突，因此只能保留设备分工，不能据此画出已确认的完整电压拓扑。[00:19:35–00:20:28](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=1175s)

冷却则是另一条循环：水进入 GPU 机架吸热，经管路流向冷机，把热排到空气后再返回；CDU 负责冷却液向机架的分配。这里要区分系统首次充水与每年新增用水。讲者称每栋建筑首次约需 100 万加仑水，闭环运行后的年度补水很低；这不能缩写为数据中心“零用水”。[00:20:28–00:22:37](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=1228s)

备电也有优先级。讲者描述部分备电优先保护存储和网络，使计算暂停后仍能读取 checkpoint、迁移和恢复工作负载。它说明如何按恢复价值配置可靠性，没有给出整个园区经过测量的可用率。[00:22:04–00:23:45](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=1324s)

## CapEx 堆叠：19.2M 美元/MW 的构成

讲者把基础设施 CapEx 拆成详细的逐项堆叠，总计约 19.2M 美元/MW。[00:23:45–00:30:20](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=1425s) 其中劳务约 4.7M 美元/MW，占比约四分之一——这在传统软件讨论中几乎不会出现，却是物理基础设施的硬约束。设备布局页还列了若干每 MW 的示例成本，但这些项目并非完整、互斥预算，不能再加到 19.2M 的堆叠总额上。

IT CapEx 是另一大块。标题与口述为约 40M 美元/MW，图中 GPU 30M、网络 4M、CPU 与存储 3M、机房内 CapEx 3M、部署劳务与运输 1M，相加却为 41M。讲者还怀疑机房内 CapEx 与前页存在双计。[00:30:27–00:32:54](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=1827s) 这组数只能描述量级，既不能把 41M 升格为精确预算，也不能自行删项凑成 40M。

互联架构分两级：机架内 NVLink，跨机架 InfiniBand 或 RoCE。网络与 CPU、存储共同把 GPU 组织成可调度的服务，不能在比较硬件价格时忽略。[00:31:11–00:32:35](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=1871s)

算力的经济寿命也容易被误判。课堂中的 H100 与 B200 租赁价格曲线呈现先降后升，但这不能证明设备应采用更长的折旧期；主持人追问是否应超过五六年时，讲者明确回答不知道。[00:34:55–00:37:26](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=2095s) 两页图标题写“since Dec ’26”，横轴却只到 2026 年 3 月，存在日期冲突。这里只保留可见价格走势，不自行改写起始日期，也不把租赁价格当作二手硬件成交价。

## 从基础设施出租到 Token 服务

Lochmiller 描述了一条商业模式演进链：最基础是出租电力和机房空间（infrastructure-as-a-service）；往上是出租 GPU 算力（compute-as-a-service）；最高是直接卖 token（intelligence-as-a-service）。[00:37:26–00:40:49](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=2246s)

越靠近 token，收入上限越高——因为客户付费的依据从"用了多少电"变成"完成了什么任务"。但成本和风险也越未知：基础设施出租的利润率相对可预测，token 服务则要承担模型效率、利用率波动和客户需求变化。

合并到总账时，差异仍然存在：标题写 58M 美元/MW，分项 19 + 30 + 10 合计 59M，讲者口述约 60M。[00:37:26–00:38:09](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=2246s) 这些是同一组粗算的不同口径，不能当作三个独立报价。年度 OpEx 图示约 1.1M 美元/MW，但讲者承认工程团队等费用尚未全部纳入。

讲者用约 60M 前期投入除以约 15M 年收入，得到约四年；若 token 服务把年收入提高到约 30M，则约为两年。[00:38:09–00:40:49](https://www.youtube.com/watch?v=GcCGzfKdCd0&t=2289s) 分母是收入，尚未扣除完整运营费用，也没有把利用率、融资、税费和更新投入纳入现金流。这两个结果是按收入计算的静态年数，不能解释为利润回收期或 IRR。

## 选址收益还要经过运行与收入验证

Energy-first 让选址从可获得的能源出发，但便宜电力只是条件之一。建设、冷却、网络和客户负载必须同时配合，设施才能持续交付计算。仅凭当地有剩余电力，不能推断所有 AI 工作负载都能灵活吸收它的波动。

从机房出租走向 token 服务，则改变了企业承担的风险：收益更接近应用需求，也更依赖模型效率、利用率与客户付费。课程中的两年、四年估算没有扣除全部成本，适合帮助拆解收入口径，不能据此宣布某种商业模式回报更高或风险更低。

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
- [完整课程笔记 PDF：32 页](/blog/pdfs/stanford-mse435/week-03-ai-factories-gigawatt-infrastructure.pdf)
- [在 GitHub 查看发布源文件](https://github.com/QianKuang8/blog-pdfs/blob/5fe326dc06c33ec0577f6b9c92becabf01412eec/stanford-mse435/week-03-ai-factories-gigawatt-infrastructure.pdf)
