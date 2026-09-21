---
title: "Adopting Arm at Scale: Bootstrapping Infrastructure"
source_url: "https://www.uber.com/kr/en/blog/adopting-arm-at-scale-bootstrapping-infrastructure/"
domain: "www.uber.com"
description: "In February 2023, Uber embarked on a strategic journey: migrating from on-premise data centers to the cloud with Oracle® Cloud Infrastructure and Google Cloud Platform™. While the scale of such a migration was already daunting, Uber added another ambitious goal: integrating Arm-based computers into a fleet dominated by x86. Why? To reduce costs, improve price-performance, and secure hardware flexibility in an unpredictable supply chain environment."
retrieved_at: "2026-09-21T10:14:01+08:00"
extractor: "defuddle"
---

## Arm: A New Era for Cloud

In February 2023, Uber embarked on a strategic journey: migrating from on-premise data centers to the cloud with Oracle <sup>®</sup> Cloud Infrastructure and Google Cloud Platform <sup>™</sup>. While the scale of such a migration was already daunting, Uber added another ambitious goal: integrating Arm-based computers into a fleet dominated by x86. Why? To reduce costs, improve price-performance, and secure hardware flexibility in an unpredictable supply chain environment.

What followed was a journey of technical challenges and cross-team collaboration as Uber adopted Arm-based hosts into the fleet. This blog is the first in a two-part series that describes that journey and focuses on the technical challenges we faced when transitioning into a multi-architecture environment.

---

## OCI Strategy

To understand our motivations for moving to Arm-based hosts, it’s important first to understand OCI’s (Oracle Cloud Infrastructure) motivation for adopting Ampere <sup>®</sup> Computing processors in their data centers. Energy efficiency is a key factor driving all hyperscale cloud service providers to use Arm processors. Arm’s reputation for low-power designs in mobile devices has extended to data center products, with Ampere processors setting a new benchmark for performance per watt. This efficiency reduces energy costs and provides OCI with significant savings. Another less obvious benefit is space densification. Ampere processors enable higher compute density within a smaller data center footprint, delivering superior performance at the rack level while minimizing real estate and infrastructure costs.

So, what motivates Uber? Our decision is rooted in the pursuit of hardware and capacity diversity. As part of our commitment to becoming a zero-emissions company, adopting high-performing, energy-efficient hosts is a critical step toward reducing our environmental footprint. The energy and space savings realized by OCI translate directly into better price-performance and cost optimizations for Uber, helping us achieve our goals of sustainability and operational efficiency.

---

## Adoption Phases

Uber’s adoption of a multi-architecture environment was a complex process requiring multiple layers of bootstrapping, careful planning, and execution across many teams. The effort was divided roughly into seven phases, as shown in Figure 1.

![](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/02/overviewwithoutlogos-17394207847479.svg)

Figure 1: Arm adoption phases.

- **Host Readiness:** Ensuring host-level software is compatible with Arm.
- **Build Readiness:** Updating the build pipeline to support multi-architecture container images.
- **Platform Readiness:** Enhancing deployment systems with architecture-specific placement constraints and safeguards.
- **SKU Qualification:** Assessing hardware reliability and performance to determine if the SKU is feasible.
- **Workload Readiness:** Making code repositories and container images compatible with Arm.
- **Adoption Readiness:** Establishing testing and monitoring protocols to validate workload performance on Arm.
- **Adoption:** Executing the migration, workload by workload, to Arm-based environments.

While adoption primarily followed a sequential process, certain phases were conducted concurrently, enabling us to accelerate progress where possible. The following sections explore the challenges of bootstrapping our infrastructure on Arm-based hosts.

---

## Initial Goal

It started with a simple goal: build a single service for Arm and deploy it to our Arm-based hosts using our existing deployment platform. However, this seemingly simple goal unraveled into a more profound challenge, as every layer of our infrastructure, from the hosts to the build pipeline responsible for creating container images, was deeply tied to x86.

---

## Host Readiness

Before building and deploying services, we had to ensure our hosts were ready to support Arm. This meant starting from the ground up. The first step was to create an Arm-compatible host image, which includes the operating system, kernel, and all the essential host-level software that powers Uber’s most foundational infrastructure components.

Every component had to be rebuilt carefully, tested, and validated to ensure it’d work correctly with Arm-based hardware. Once the host image was in place, we could begin integrating Arm hosts into our fleet and bootstrap our build platform to support the next step in the journey: building services for Arm.

---

## Building Services for Arm

At first, the task sounded straightforward, but as we began to pull on that thread, it quickly became a more complex challenge due to the many layers of our build infrastructure that were strongly tied to a single architecture.

For years, Uber’s container image stack relied on a centralized Buildkite <sup>™</sup> pipeline powered by [Makisu](https://www.uber.com/en-DK/blog/makisu/), which is an efficient and lightning-fast container image builder optimized for single-architecture builds. While Makisu served us well, it had a critical limitation: it couldn’t cross-compile for Arm. This meant we couldn’t just flip a switch to produce Arm-compatible container images. Instead, we had to rethink how container images were built across the fleet.

To make things worse, we have more than 5,000 services whose build processes are tightly coupled to Makisu, and many of them have several custom build steps tightly coupled to Makisu’s build flow. So, migrating away from Makisu was a substantial undertaking.

---

## Evolving the Build Pipeline

Instead of attempting to migrate away from Makisu, we decided to evolve our build pipeline by introducing a new container image builder capable of building for Arm. The plan was to use the new container image builder to create an Arm-compatible version of Makisu. Once we had that, Makisu could be used to build Arm versions of all other services. However, as we’ll see, bootstrapping Makisu on Arm started a chain reaction of bootstrapping other components.

We chose Google <sup>®</sup> Bazel <sup>™</sup> as the container image builder to address the bootstrap challenge of building Makisu for Arm. This decision was driven by Bazel’s ability to build container images for architectures different from the host it runs on by leveraging the [OCI container image rules](https://github.com/bazel-contrib/rules_oci). Additionally, since our language monorepos already rely on Bazel, this choice allowed us to leverage existing expertise and tooling.

---

## Breaking the Circular Dependency

With Bazel integrated into the container image build pipeline, we could now build Makisu for Arm. However, Makisu runs on Buildkite, our primary CI system, and Buildkite runs on our Stateful Platform, [Odin](https://www.uber.com/en-DK/blog/odin-stateful-platform/).

In addition, Odin relied on a collection of foundational host agents for logging, metrics, networking, and more. These critical foundation components are deployed to every host in our fleet, and all these components were built using Makisu.

This meant that before we could fully bootstrap Makisu for Arm, we had to untangle and rebuild every piece of this puzzle. Each component had to be migrated from being built with Makisu to being built with Bazel instead. It was a cascade of dependencies that required a lot of coordination. First, the host agents were migrated, then the components of the stateful platform, then our Buildkite stack, and finally, Makisu itself. It was a significant effort, but we tackled each layer systematically using Bazel’s multi-architecture capabilities, transforming our infrastructure one piece at a time.

![](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/02/buildstack-17394210019516.svg)

Figure 2: Components for bootstrapping the build stack.

---

## Distributing the Build Process

Once Makisu and the entire Buildkite stack were up and running on Arm-based hosts, we took the next big step: advancing our build setup by setting up a distributed build pipeline for container images.

This new pipeline multiplexes the build process across Arm and x86 hosts, running Makisu natively on each architecture. Once images have been built, the pipeline triggers a last step that merges the x86 and Arm images into a unified multi-architecture container image using a multi-architecture container manifest.

![](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/02/distributedbuildpipeline-17394210469874.svg)

Figure 3: Distributed build pipeline for container images.

Adopting the multi-architecture build pipeline provided significant advantages. It allowed us to avoid the extensive effort of migrating every container image build process from Makisu to Bazel, which had been deemed a substantial undertaking. Additionally, building images natively for both x86 and Arm enables us to support workloads that can’t cross-compile. Moreover, native builds eliminated the overhead associated with cross-compilation, reducing build times and helping us stay within our build latency SLAs.

However, adopting multi-architecture builds wasn’t without its trade-offs. One significant downside was the doubling of build costs, as container images needed to be built for both architectures. With more than 400,000 container image builds per week (at the time of writing), this additional cost quickly became substantial. However, despite the increase in build costs, the unit economics of transitioning to Arm still made it worthwhile. Furthermore, multi-architecture builds enable us to perform a gradual adoption as it allows the same image tag to be deployed across both Arm and x86 hosts.

---

## Deploying the First Services

Now that we could build images with multiple architectures, the next challenge was to ensure that our [stateless](https://www.uber.com/en-DK/blog/up-portable-microservices-ready-for-the-cloud/) and [stateful](https://www.uber.com/en-DK/blog/odin-stateful-platform/) platforms could leverage other architectures.

At Uber, we take great care in gradually introducing changes to our production environment, gradually increasing the scope of changes. This applies to image upgrades and hardware changes alike. For Arm, we had to extend these systems to support architecture-specific placement. This enabled fine-grained control over which architecture a service runs on, allowing us to transition from x86 to Arm with great care. Furthermore, we built a safety mechanism into our platforms that’d automatically revert the Arm placement constraint and fall back to x86 if a single architecture image was deployed for a service.

With these placement constraints and safety mechanisms in place, we reached a significant milestone: the first services were successfully built, scheduled, and running on Arm-based hosts. It was a moment of joy, proof that Arm could coexist alongside x86 in our infrastructure.

---

## Conclusion

Our work was far from over. The initial success of bootstrapping the infrastructure was only the start of a larger journey. Adapting 5,000 services to run on a multi-architecture platform would require more effort and ingenuity.

In the [next part of this blog series](https://www.uber.com/kr/en/blog/adopting-arm-at-scale-transitioning-to-a-multi-architecture-environment/), we’ll dive into the adoption process in greater detail and explain the initiatives and strategies implemented to support a transition of this scale.

---

## Acknowledgments

The successful adoption of Arm-based hosts at Uber was made possible through the collective efforts of numerous internal and external contributors, including our partners at Oracle Cloud Infrastructure (OCI), Google (GCP), Ampere, and Arm. The authors would like to thank all who worked on this initiative and helped make it a success.

Cover Photo Attribution: The cover photo was generated using OpenAI ChatGPT Enterprise*.*

*Buildkite <sup>™</sup> is a trademark of Buildkite Pty. Ltd.*

*Google Cloud Platform <sup>™</sup> and Bazel <sup>™</sup> are trademarks of Google LLC and this blog post is not endorsed by or affiliated with Google in any way.*
