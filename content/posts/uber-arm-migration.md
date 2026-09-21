---
date: '2025-04-13T13:58:21+08:00'
lastmod: '2026-09-21T10:14:01+08:00'
title: "Uber 的 Arm 迁移：先打通构建，再推广到多架构运行"
summary: "Uber 先解决构建系统的循环依赖，再通过双架构验证、分阶段迁移和自动回退推广 Arm。两篇实践说明了从单个服务跑通到平台持续支持之间的工程距离。"
description: "解读 Uber 的 Arm 构建引导、多架构镜像、测试与渐进迁移机制。"
tags: ["arm", "架构迁移", "uber"]
categories: ["好文分享"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

把一个服务编译成 Arm 版本，只解决了架构迁移的一小部分。运行它的主机代理、构建器、发布平台和依赖库，也可能默认世界里只有 x86。Uber 在 2025 年发布的两篇 [Arm 迁移文章](https://www.uber.com/kr/en/blog/adopting-arm-at-scale-bootstrapping-infrastructure/)，展示了如何先打通一条部署路径，再把它扩展为可持续运行的多架构平台。

## 先打破构建系统的循环依赖

第一阶段的目标很具体：用既有发布平台，在 Arm 主机上构建并运行一个服务。困难在于，原来的构建器 Makisu 依赖 Buildkite，Buildkite 又运行在 Odin 平台上，而底层主机代理也由 Makisu 构建。要让构建器迁移，先得让支撑它的系统能够迁移。

Uber 用 Bazel 逐层完成这段引导，随后在 x86 与 Arm 主机上分别原生构建，再用多架构 manifest 组织镜像。这样保留了大量既有构建流程，但也增加了双份构建的成本。这个选择体现了迁移范围的控制：先为无法绕开的依赖提供新路径，再让已有系统接手常规工作。

## 把兼容性检查放进日常交付

[第二篇文章](https://www.uber.com/kr/en/blog/adopting-arm-at-scale-transitioning-to-a-multi-architecture-environment/) 讨论规模推广。团队清理基础镜像和依赖，在两种架构上运行测试，并比较线上延迟、错误率和资源使用情况。构建成功、测试通过和生产表现稳定，分别回答不同的问题。

例如，浮点计算的差异可能只有在执行测试时才暴露；硬件的持续性能与短时突发性能，也可能影响真实负载。这里值得借鉴的是验证安排：把差异尽量提前到开发和 CI 中发现，再用生产观察检查测试没有覆盖的情况。

## 自动化迁移也要有停止条件

推广按服务重要性、非生产与生产环境、可用区分阶段推进。自动化系统读取目标状态，以小批次协调迁移；告警或 SLA 下降触发回退。原文报告迁移了超过 2800 个无状态 Go 服务，这是当时已完成的范围，不能推成所有语言和有状态服务都已迁移。

从这段实践可以归纳出三项验收：目标架构是否具备完整构建路径，服务是否保持预期行为，以及运行收益是否覆盖新增的构建和维护成本。迁移平台若能持续回答这三个问题，新增一种硬件才会成为可维护的能力。单次跑通的样例，则只是进入下一阶段的起点。

## 延伸阅读

- [Adopting Arm at Scale: Bootstrapping Infrastructure — Uber](https://www.uber.com/kr/en/blog/adopting-arm-at-scale-bootstrapping-infrastructure/)
- [Adopting Arm at Scale: Transitioning to a Multi-Architecture Environment — Uber](https://www.uber.com/kr/en/blog/adopting-arm-at-scale-transitioning-to-a-multi-architecture-environment/)
