---
date: '2025-04-13T13:58:21+08:00'
title: '技术好文记录'
summary: "一些技术好文的记录"
description: "一些技术好文的记录"
tags: ["technical", "default"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

## 将服务从x86架构迁移到arm架构上

思考：这两篇文章讲述了uber如何将服务从x86架构的服务器迁移到arm架构的服务器上，主要出发点是节约成本。
- 第一篇文章重点在如何从0到1，包括如何启动这个项目，在刚开始搭建CI/CD的过程中做了什么事情，最后直到完成单个服务的迁移
- 第二篇文章重点在如何从1到100，包括如何将单个服务迁移成功的经验推广到其它服务，如何平滑地进行大规模的迁移

[Adopting Arm at Scale: Bootstrapping Infrastructure](https://www.uber.com/en-KR/blog/adopting-arm-at-scale-bootstrapping-infrastructure/)

本文讨论了 Uber 的战略性举措，将基于 Arm 的计算机与现有的基于 x86 的系统集成到其云基础设施中，以降低成本、提高性能并确保硬件灵活性。过渡过程涉及一个复杂的多阶段过程，包括确保主机、构建和平台就绪。

[Adopting Arm at Scale: Transitioning to a Multi-Architecture Environment](https://www.uber.com/en-KR/blog/adopting-arm-at-scale-transitioning-to-a-multi-architecture-environment/)

本文讨论了 Uber 通过大规模采用基于 Arm 的主机向多架构环境的过渡。它描述了从在基于 Arm 的主机上运行单个服务到扩展到数千个服务的旅程。