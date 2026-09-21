---
title: "Adopting Arm at Scale: Transitioning to a Multi-Architecture Environment"
source_url: "https://www.uber.com/kr/en/blog/adopting-arm-at-scale-transitioning-to-a-multi-architecture-environment/"
domain: "www.uber.com"
description: "This is the second blog in a two-part series that describes how Uber adopted Arm at scale. In the first part, we described the foundational work of introducing Arm-based hosts into an extensive x86 infrastructure. We covered how we untangled multiple layers of infrastructure tailored to a single architecture environment and reached the initial milestone of building and deploying a simple service to Arm-based hosts through our deployment platform. In this blog, we describe the journey from a single service running on Arm-based hosts to scaling the adoption of thousands of services. Each service brought its own dependencies, build nuances, and performance considerations. We had to address hidden issues that hadn’t surfaced in years and refine our operational strategies to ensure that we could run both x86 and Arm with confidence."
retrieved_at: "2026-09-21T10:14:01+08:00"
extractor: "defuddle"
---

## Beyond Bootstrapping

This is the second blog in a two-part series that describes how Uber adopted Arm at scale. In the [first part](https://www.uber.com/kr/en/blog/adopting-arm-at-scale-bootstrapping-infrastructure/), we described the foundational work of introducing Arm-based hosts into an extensive x86 infrastructure. We covered how we untangled multiple layers of infrastructure tailored to a single architecture environment and reached the initial milestone of building and deploying a simple service to Arm-based hosts through our deployment platform.

In this blog, we describe the journey from a single service running on Arm-based hosts to scaling the adoption of thousands of services. Each service brought its own dependencies, build nuances, and performance considerations. We had to address hidden issues that hadn’t surfaced in years and refine our operational strategies to ensure that we could run both x86 and Arm with confidence.

A new mindset emerged that viewed multi-architecture as an integral aspect of our production environment. As we dig deeper, you’ll see how we prepared our codebases, revised our container images, and gradually introduced more services into this multi-architecture environment.

---

## Addressing Technical Debt

After proving a handful of services could run successfully on Arm-based hosts, we faced a new challenge of extending the adoption of our entire platform, which includes more than 5,000 services. Achieving this would mean revisiting and refining multiple code repositories, untangling years of legacy dependencies, and ensuring nothing would break when we switched architectures at scale.

Uber’s services are mostly built from three language-specific monorepos with the following CPU allocation distribution: 60% Go, 20% Java, and 10% Web. The rest are scattered across numerous micro-repositories. This distribution mattered as our monorepos, built with Google <sup>®</sup> Bazel <sup>™</sup>, are relatively uniform and more straightforward to transition to Arm. In contrast, the micro-repositories have custom toolchains, making it more time-consuming to make them compatible with Arm. We focused first on monorepos to avoid getting stuck, making rare exceptions only for critical micro-repository services.

### Preparing the Source Code

The goal was to ensure all services could be built in a multi-architecture variant, which meant that all dependencies in the language monorepos had to be available in a Linux <sup>®</sup> Arm-compatible variant. Bazel’s repository dependencies, retrieved from our internal instance of JFrog <sup>®</sup> Artifactory <sup>®</sup>, had to be prepared. In addition, our monorepos included C++ dependencies, for which we use the [Zig CC compiler](https://www.uber.com/en-DK/blog/bootstrapping-ubers-infrastructure-on-arm64-with-zig/), as it excels at cross-compiling. As part of this work, we developed a [Bazel wrapper](https://github.com/uber/hermetic_cc_toolchain), so the compiler could be integrated into our build toolchain. With this in place, building for Arm was no longer a special case—it became another supported target in our build ecosystem.

### Fixing Container Images

With the source code prepared, we turned our attention to container images. Our new multi-architecture build pipeline, introduced in the first [Bootstrapping Infrastructure blog](https://www.uber.com/kr/en/blog/adopting-arm-at-scale-bootstrapping-infrastructure/), allowed us to produce images compatible with x86 and Arm. However, as soon as we started mass-building services, we encountered old container image dependencies and other incompatibilities that needed to be fixed on Arm.

Some of the more common issues included legacy base images and outdated Debian <sup>®</sup> packages. Some services depended on outdated, single-architecture base images. We replaced these with updated, multi-architecture versions. Others relied on Debian packages that had never been built for Arm. We tackled these one by one, rebuilding or replacing them wherever possible, which was quite time-consuming.

This cleanup wasn’t glamorous work, but it was undeniably essential. Each replaced base image, each rebuilt package, and each dependency sorted out brought us closer to a world where multi-architecture builds were the default and not the exception.

---

## Ensuring a Reliable Transition

With most services enabled in a multi-architecture version, the next goal was establishing a reliable adoption process for the new Arm-based hosts. Adopting thousands of services onto Arm-based hosts involved more than updating code and container images. It also required ensuring that every service functions correctly in terms of correctness and performance. To achieve this, we’ve introduced several initiatives, described below.

### Unit Test Compatibility

We updated our CI setup to trigger tests on both architectures to ensure our services would function correctly on both x86 and Arm. This approach helped us spot subtle, architecture-specific issues such as floating-point behavioral discrepancies before they could affect production. Interestingly, [Go allows implementors](https://go.dev/ref/spec#Arithmetic_operators) to use fused floating-point operations despite rounding differences. We maintained consistent business logic across both architectures by catching these differences early.

### Extensive Monitoring

After services had been adopted to Arm, we needed a reliable way to spot problems if the adoption introduced regressions. To capture that, we built an extensive monitoring tool that tracked latency, error rates, CPU utilization, and resource throttling and conducted A/B testing across both architectures and the different failure domains to better identify issues. By closely watching these metrics, we could detect if a service behaved unexpectedly on Arm before minor discrepancies turned into major incidents.

### Dev Pod Compatibility

Our developers rely heavily on Dev Pods, remote development environments tailored with Uber’s internal tools. Previously, these environments were limited to x86, making it hard to anticipate architecture-specific issues. Extending Dev Pods to support Arm gave engineers the power to run, build, and debug services on either x86 or Arm. This early exposure to multi-architecture conditions gave our teams the context they needed to write architecture-agnostic code.

### SKU Qualification and Benchmarking

To validate the suitability of the Ampere <sup>®</sup> Computing A1 and A2 instances, we conducted comprehensive benchmarking and compared their performance against our existing x86 fleet. Automated performance tests, designed to simulate production conditions, provided valuable insights. Furthermore, we partnered with product teams to run synthetic load tests on Arm. These tests exposed nuances that didn’t appear in controlled benchmarks. For instance, the Ampere A1 instances we use offered predictable, steady performance rather than opportunistic bursts typical of some x86 hosts. While initially surprising, these insights underscored that different architectures follow different design philosophies. Understanding these philosophies helped us plan more effectively. Furthermore, these benchmarking results helped us understand where Arm fits into our overall performance spectrum and guided how networking traffic should be balanced between x86 and Arm hosts.

These initiatives formed the groundwork for our multi-architecture adoption strategy. By combining rigorous testing, benchmarking, monitoring, and hands-on developer experience, we ensured that moving thousands of services onto Arm wouldn’t require a leap of faith.

---

## Adoption Strategy

We implemented a gradual adoption strategy for migrating services to Arm-based infrastructure to minimize impact and ensure a smooth transition. Our adoption and qualification of services was done across the following dimensions.

- **Tier-by-tier:** Each service at Uber is assigned a tier that represents how critical the service is to the core business flows. We used a tiered adoption strategy to ensure a reliable adoption, allowing us to prioritize services based on criticality and impact. After each large cohort of a tier was adopted, a production readiness review gate was conducted to assess stability and performance, determining whether the tier was ready to be fully adopted and whether the next tier could proceed. This structured approach allowed us to identify and address potential issues in lower-criticality services before advancing to more critical tiers.
- **Non-production** **before** **production:** We first migrated the services’ non-production environments, which serve as testing grounds. If everything looked good, we proceeded to the production environments.
- **Zone-by-zone:** To further mitigate risk, we adopted a zone-by-zone migration approach. This strategy allowed us to initiate failovers in the event of a major incident or drain network traffic from an availability zone.

Throughout the migration process, testing was automatically triggered whenever a service was deployed. Additionally, continuous monitoring ensured that adopted services performed as expected. The process was automatically reverted if any alerts were triggered or SLA degradation occurred so that it could be hands-free.

---

## Automating the Adoption

Manual adoption quickly becomes time-consuming and error-prone when faced with thousands of services. To streamline this process, we built a goal-state-driven system that automates and manages the entire process. It starts by reading a high-level plan, defining which services should be adopted and in which zones. Then, it relies on a reconciliation loop, implemented as a [Cadence](https://cadenceworkflow.io/) workflow, to determine the right services to move at each step.

It handles these migrations in small, controlled batches rather than attempting one massive “big bang” to minimize risk and keep any potential issues manageable. This automated approach ensures every transition adheres to the original plan and that services are migrated predictably, resulting in a more reliable adoption process.

![](https://cn-geo1.uber.com/image-proc/resize/udam/format=auto/quality=0/width=2160/srcb64=aHR0cHM6Ly90Yi1zdGF0aWMudWJlci5jb20vcHJvZC91ZGFtLWFzc2V0cy81OGU3YzI2Ni1kNjlkLTU4ZGItYTRhNi0wNWRlYzgzYTgzMmQucG5n)

Figure 1: Goal state driven system for automating the adoption process.

---

## Results

We have successfully adopted over 2,800 stateless Go-based services to Arm-based hosts and transformed nearly 20% of our Oracle <sup>®</sup> Cloud Infrastructure capacity from x86 to Ampere A1 and A2 CPUs without a serious incident. We’ve reevaluated old assumptions, upgraded legacy dependencies, and learned how to run an efficient and reliable multi-architecture environment.

This transformation demonstrated the benefits of better price-performance, a more flexible platform, and a meaningful step toward reducing our carbon footprint. We proved that Arm could coexist with x86 at Uber’s scale and enhance our overall platform.

---

## Conclusion

Looking ahead, our multi-architecture environment is poised for even more diversity. While we’ve already seen success with stateless, Go-based services, Java services will join the fold in the coming year. We’re also preparing to tackle more complex territory: stateful workloads like Redis <sup>®</sup>, etcd <sup>®</sup>, Apache Cassandra *<sup>®</sup>*, and MySQL *<sup>®</sup>*, and M3, batch processing, and machine learning jobs.

This isn’t the end of our story. As we continue exploring this evolving landscape, we’ll keep pushing the limits of what’s possible in a heterogeneous world. Our goal remains the same: to build an environment where every architecture thrives, and every workload finds its best fit.

---

## Acknowledgments

The successful adoption of Arm-based hosts at Uber was made possible through the collective efforts of numerous internal and external contributors, including our partners at Oracle Cloud Infrastructure and Ampere. The authors would like to thank all who worked on this initiative and helped make it a success.

Cover Photo Attribution: The cover photo was generated using OpenAI ChatGPT Enterprise*.*

*Apache* *<sup>®</sup>**, Apache Cassandra* *<sup>®</sup>**, and Cassandra* *<sup>®</sup>**, are either registered trademarks or trademarks of the Apache Software Foundation in the United States and/or other countries. No endorsement by The Apache Software Foundation is implied by the use of these marks.*

[*bazel-zig-cc*](https://github.com/ajbouh/bazel-zig-cc/)*, which we cloned and was the foundation for the cross-compiler tooling, was originally created by Adam Bouhenguel.*

*Google Cloud Platform <sup>™</sup> and Bazel are trademarks of Google LLC and this blog post is not endorsed by or affiliated with Google in any way.*

*JFrog <sup>®</sup> ”, “Artifactory <sup>®</sup> ”, “Bintray <sup>®</sup> ”,. “JFrog Mission Control <sup>®</sup> ” and the logos of JFrog, and other marks are Marks of JFrog or its affiliates.*

*Redis is a registered trademark of Redis Ltd. Any rights therein are reserved to Redis Ltd. Any use by Uber is for referential purposes only and does not indicate any sponsorship, endorsement or affiliation between Redis and Uber.*
