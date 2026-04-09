---
title: "We've completely rebuilt the Kilo Code extension for VS Code. Join the beta test."
source_url: "https://blog.kilo.ai/p/we-completely-rebuilt-the-kilo-vs-code-extension"
domain: "blog.kilo.ai"
description: "Kilo announces a rebuilt VS Code extension with a portable core, subagent delegation, parallel execution, and improved agent management."
retrieved_at: "2026-04-09T23:03:58+08:00"
extractor: "defuddle"
---

### Subagent delegation, parallel execution, and the full power of the CLI—now inside your editor

Last month, [we shipped a renewed Kilo CLI](https://blog.kilo.ai/p/kilo-cli) built on OpenCode server—a portable, open-source core that isn’t tied to any single editor. The VS Code extension was always going to be next. Today it’s here.

**The completely rebuilt Kilo Code for VS Code is available now as a pre-release**, and we’re looking for developers to help us test it. Same portable engine as the CLI. No more VS Code internals weighing down every surface. And with the new foundation comes a set of capabilities developers have been asking for: subagent delegation and parallel execution, the Agent Manager, and improved latency.

This isn’t an incremental update. It’s a new extension—architected to grow with us as we expand to every surface where developers work. We’re putting it out as a pre-release because we want real feedback from real workflows before we push it to production. Some things aren’t migrated yet (more on that below), and that’s the point—we’d rather ship early and build the rest with your input than polish in private.

If you find bugs and help fix them, we want to reward you for it. More on that below too.

## Why We Rebuilt

Our original VS Code extension served over 800,000 developers and worked well on its home turf. But under the hood, every surface—CLI, JetBrains, Cloud Agents—was still running VS Code internals, whether it needed them or not. The clearest example was JetBrains, where we were running VS Code internals inside a JetBrains IDE. Developers felt it.

When we rebuilt the CLI on [OpenCode](https://github.com/anomalyco/opencode) server—an MIT-licensed, open-source foundation for agentic coding—we saw the opportunity to fix this at the root. Instead of patching around VS Code dependencies, we built a portable core that runs natively on every surface. The new VS Code extension shares the same engine as Kilo CLI. One foundation. One set of capabilities. One experience that follows you from terminal to editor and back.

## What’s New

![](https://www.youtube.com/watch?v=tbbzsBysg9M)

### Subagent Delegation and Parallel Execution

The new extension is fundamentally more responsive—and the reason is parallelism at every level.

![](https://substackcdn.com/image/fetch/$s_!0bb9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F530e6411-6919-43ce-b4cd-9874751ea034_972x855.png)

Kilo now supports parallel tool calls, meaning the agent can execute multiple actions at the same time instead of waiting for each one to finish before starting the next. Files read, terminal commands, searches—they run concurrently, and you feel the difference immediately. Tasks that used to block on sequential tool execution now resolve faster without any change to how you prompt.

On top of that, the extension supports parallel subagents. When a task is too complex for a single prompt, Kilo can spin up **multiple subagents that work simultaneously** —an implementation agent, a test-writing agent, and a documentation agent—each performing its piece of the work in parallel, then condensing the results back to the parent agent. Orchestrator mode coordinates the delegation and merges everything intelligently.

And subagents aren’t a black box. You can define your own. If your workflow calls for a security review agent, a migration agent, or a linting pass, create it. **Custom subagents let you shape the delegation pattern to match how your team actually works**, rather than relying on a one-size-fits-all orchestration.

The result is an agent that doesn’t just think faster—it works faster, doing more in the same amount of wall-clock time.

### The Agent Manager

![](https://substackcdn.com/image/fetch/$s_!TaRS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69ea6d92-52c4-42db-bb39-7068c8c3f348_1600x1002.png)

The Agent Manager has been part of Kilo Code for a while, but in the previous extension it sat on top of a separate mechanism from the rest of the stack. In the rebuilt extension, the **Agent Manager runs on the same portable core** as everything else. That means it inherits all the new capabilities natively— [git worktrees](https://git-scm.com/docs/git-worktree), parallel sessions, inline code review—without the workarounds that were needed before.

Spin up new agents through tabs. Monitor what each one is doing. Switch context instantly. Whether you’re running two agents or eight, the Agent Manager gives you one place to see everything that’s happening and step in when you need to.

#### Inline Code Review

When agents make changes across your codebase, you need a way to review the work and push back when something isn’t right. The Agent Manager includes a built-in diff reviewer that shows every change an agent has made, file by file, in either unified or split view. Toggle it open for a side panel, or expand into a full-screen review tab with a file tree sidebar for navigating large changesets.

But viewing diffs is just the starting point. You can leave line-level review comments directly on the diff, the same way you would on a pull request. Click a line, type your feedback, and when you’re done reviewing, hit “Send all to chat.” Every comment, with its file path, line number, and the code in question, is sent straight to Kilo as structured context. Point at the line, say what’s wrong, and let Kilo handle the rest.

This turns agent-assisted development into something closer to a real code review workflow. Instead of approving or reworking an entire changeset, you’re having a targeted conversation with the agent about specific lines of code, the same way you’d review a pull request from a teammate.

![](https://substackcdn.com/image/fetch/$s_!H2JX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a99f66c-3e26-4cce-980e-4591195caae0_1600x470.png)

#### Parallel Agents with Worktrees

This is where it gets powerful. Open as many Kilo tabs as you need—each one is a fully independent agent. But running multiple agents on the same codebase creates conflicts. So the Agent Manager lets you create **git-worktrees**: separate copies of your repository where each agent operates independently, like giving each developer their workspace.

![](https://substackcdn.com/image/fetch/$s_!Enbl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F332bdd9b-5bfe-495e-b2bb-678ed52afa7a_1036x816.png)

Click the plus button, and Kilo creates a new worktree in a subdirectory of your repo. One agent adds a new API endpoint. Another refactors the auth module. A third writes tests. They all work simultaneously without stepping on each other’s code.

When they’re done, you merge the results—apply changes directly, commit them, or create a PR, the same way you’d handle branches from different developers on your team.

For engineers working on large codebases, this is a multiplier. Instead of feeding one task at a time to a single agent and waiting for completion, you orchestrate multiple streams of work in parallel. What used to take hours finishes in minutes.

**Running parallel agents on the same worktree** is also supported for read-heavy workflows. A common pattern: one agent makes code changes while a second agent reviews the current diff or investigates how a specific feature is implemented elsewhere in the codebase. No merge overhead, just faster feedback loops.

#### Multi-Model Comparisons

This one’s useful more often than you’d think. The Agent Manager lets you start multiple agents on the same prompt using different models—Claude Opus 4.6 and GPT-5.3, for example. Both work the task independently, and you compare the results side by side.

![](https://substackcdn.com/image/fetch/$s_!TkAV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b0ff7f2-59ee-41c5-a02b-33a49d94e31e_1266x986.png)

It’s not just for trying out new models. Any time you’re doing something complex or open-ended—a tricky refactor, a page layout, an architecture decision—it helps to have a few versions to compare. Run two or three models on the same problem, see which one got closest, and go with that. Sometimes Opus nails it, sometimes GPT does. Having both means you don’t have to guess.

### Cross-Platform Sessions

Start a coding session in the CLI while being SSHed into a production server. Pick it up in VS Code when you’re back at your desk. Share the context with a teammate via Slack. Because the extension and CLI now share the same portable core, session continuity isn’t a bolt-on feature—it’s built into how the system works.

![](https://substackcdn.com/image/fetch/$s_!ohMf!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0aaf2f73-3ce2-4505-8051-482d0a215c45_745x757.png)

## Get Started

Here’s how to get started with the pre-release:

1. Search for **“Kilo Code”** in the VS Code Extensions panel, or install directly from the [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=kilocode.Kilo-Code).
2. Switch to the **pre-release version** in the extension panel.
3. Open multiple Kilo tabs and go parallel.

**A few things to know before you dive in.** This is a pre-release, and not everything has been migrated yet. Provider configuration isn’t available in the extension UI right now—if you configure your providers via the [Kilo CLI](https://www.npmjs.com/package/@kilocode/cli), those settings will carry over and work in the extension. We’re building native provider setup into the extension as a priority for GA.

If you want to test the pre-release without touching your current setup, install it on [VS Code Insiders](https://code.visualstudio.com/insiders/) —it runs as a separate instance, so you can try the new extension side by side with your existing one.

If you’re already a [Kilo CLI](https://kilo.ai/cli) user, your settings and sessions sync automatically. That’s the whole point.

We’d love your feedback—what works, what doesn’t, what’s missing. Drop it in [Discord](https://discord.gg/kilocode).

## What’s Next

The pre-release is stable and ready for daily use. Here’s what we’re focused on as we move toward general availability:

- **Smoother migration.** We’re building a migration experience that automatically carries your provider settings, API keys, and configurations like Memory Bank over to the new extension. You shouldn’t have to reconfigure anything.
- **Bug bounty for PRs.** This is open source, and we want the community involved from day one. Find a bug in the pre-release, submit a PR to fix it, and if it gets merged, we'll give you **$100 in Kilo Credits**.
- **Production release.** Once we’ve incorporated feedback from the pre-release and stabilized the remaining rough edges, we’ll push the full general release to all users.

---

[Install the extension.](https://kilo.ai/install) [Try the CLI.](https://kilo.ai/cli) [Tell us what you think.](https://kilo.ai/discord)

Move at Kilo Speed.
