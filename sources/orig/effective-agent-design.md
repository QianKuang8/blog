---
title: "Effective Agent Design"
source_url: "https://x.com/RLanceMartin/status/2009683038272401719"
domain: "x.com"
description: "A Lance Martin thread synthesizing common design patterns for long-running autonomous agents and context management."
retrieved_at: "2026-06-05T21:16:57+08:00"
extractor: "defuddle"
---

![Cover image](https://pbs.twimg.com/media/G-LRQq9aoAABumF.jpg)

2025 ended with Meta buying Manus for [over $2b](https://manus.im/blog/manus-joins-meta-for-next-era-of-innovation) and Claude Code reaching a [$1B run rate](https://www.anthropic.com/news/anthropic-acquires-bun-as-claude-code-reaches-usd1b-milestone). Here I explore common design patterns across these and other popular agents based on many of my favorite blogs, papers, and posts.

We are getting closer to long-running autonomous agents. [@METR\_Eval](https://x.com/METR_Evals)s reports that agent task length [doubles every 7 months](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/). But one challenge is that models get worse as context grows. [@trychroma](https://x.com/trychroma) reported on [context rot](https://research.trychroma.com/context-rot\)), [@dbreunig](https://x.com/dbreunig) outlined [various failure modes](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html\)), and Anthropic [explains it here](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents\)):

Context must be treated as a finite resource with diminishing marginal returns. Like humans with limited working memory, LLMs have an "attention budget." Every new token depletes it.

With this in mind, [@karpathy](https://x.com/karpathy) framed the [need for context engineering](https://x.com/karpathy/status/1937902205765607626\)):

Context engineering is the delicate art and science of filling the context window with just the right information for the next step.

Effective agent design largely boils down to context management. Let's explore a few common ideas from my favorite blogs, papers, and posts.

## Give Agents A Computer

[@barry\_zyj](https://x.com/barry_zyj) and [@ErikSchluntz](https://x.com/ErikSchluntz) defined agents as [systems where LLMs direct their own actions](https://www.anthropic.com/engineering/building-effective-agents). It's become clear over the past year that agents benefit from access to a computer, giving them primitives like a filesystem and shell.

The filesystem gives agents access to persistent context. The shell lets agents run built-in utilities, CLIs, provided scripts, or code they write.

![](https://pbs.twimg.com/media/G-K_mcga0AA7_uA.png)

We've seen this across many popular agents. Claude Code broke out as an agent that ["lives on your computer"](https://x.com/karpathy/status/2002118205729562949). Manus uses a [virtual computer](https://e2b.dev/blog.how-manus-uses-e2b-to-provide-agents-with-virtual-computers). And both fundamentally use tools to control the computer, as [@rauchg](https://x.com/rauchg) [captured](https://x.com/rauchg/status/2006860649067065565):

The fundamental coding agent abstraction is the CLI ... rooted in the fact that agents need access to the OS layer. It’s more accurate to think of Claude Code as “AI for your operating system”.

## **Multi-Layer Action Space**

Agents perform actions by calling tools. It's become easier to give tools to agents (e.g., via [model context protocol](https://modelcontextprotocol.io/docs/getting-started/intro)). But, this can [cause problems](https://www.anthropic.com/engineering/code-execution-with-mcp):

As MCP usage scales ... tool definitions overload the context window and intermediate tool results consume additional tokens.

Tool definitions are typically loaded directly into context. The GitHub MCP server, as an example, has 35 tools with [~26K tokens of tool definitions](https://www.anthropic.com/engineering/advanced-tool-use). More tools can also [confuse models](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html\)) if they have overlapping functionality.

Many popular general purpose agents use a surprisingly small number of tools. [@bcherny](https://x.com/bcherny) [mentioned](https://every.to/podcast/how-to-use-claude-code-like-the-people-who-built-it\)) that Claude Code uses around a dozen tools. [@peakji](https://x.com/peakji) [said](https://www.youtube.com/watch?v=6_BcCthVvb8) that Manus uses fewer than 20 tools. [@beyang](https://x.com/beyang) from Amp Code talks about [how they curated](https://www.youtube.com/watch?v=gvIAkmZUEZY) the action space to include only a few tools.

![](https://pbs.twimg.com/media/G-LBsrfa0AIwPBy.png)

How can agents limit tools but still perform a wide range of actions? They can push actions from the tool calling layer to the computer. [@peakji](https://x.com/peakji) explained the Manus action space as a hierarchy: the agent uses a few atomic tools (e.g., a bash tool) to perform actions on the virtual computer. Its bash tool can use shell utilities, CLIs, or just write / execute code to perform actions.

The [CodeAct paper](https://arxiv.org/abs/2402.01030) showed that agents can chain many actions by writing and executing code. Anthropic wrote about this [here](https://www.anthropic.com/engineering/code-execution-with-mcp), highlighting the token savings benefit because the agent does not process the intermediate tool results. [@trq212](https://x.com/trq212) showed some practical examples of this using Claude.

## **Progressive Disclosure**

An agent needs to know what actions are available. One option is to push actions to the tool calling layer and load tool definitions upfront into context.

But, we've seen a trend towards progressive disclosure of actions for better context management. This is a design pattern that shows only essential information upfront and reveals more details only as the user needs them.

At the tool calling layer, some agents [index tool definitions](https://github.com/langchain-ai/langgraph-bigtool) and retrieve tools on demand, potentially using a [search tool](https://www.anthropic.com/engineering/advanced-tool-use) to encapsulate this process.

For shell utilities or installed CLIs, [@peakji](https://x.com/peakji) [said](https://drive.google.com/file/d/1QGJ-BrdiTGslS71sYH4OJoidsry3Ps9g/view) that Manus just provides a list of available utilities in the agent instructions. Then the agent uses its bash tool (e.g., via a --help flag) to learn about any one of them if needed.

![](https://pbs.twimg.com/media/G-LER8vaEAA206O.jpg)

MCP servers can be pushed from the tool calling layer to the computer, allowing them to be progressively disclosed. Cursor Agent [syncs MCP tool descriptions to a folder](https://cursor.com/blog/dynamic-context-discovery), gives the agent a short list of available tools, and allows the agent to read the full description only if needed based on the task. Both [Anthropic](https://www.anthropic.com/engineering/code-execution-with-mcp) and [Cloudflare](https://blog.cloudflare.com/code-mode/) discuss similar ideas for MCP management.

Anthropic's [skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills\)) [standard](https://agentskills.io/home\)) uses progressive disclosure. [@barry\_zyj](https://x.com/barry_zyj) and [@MaheshMurag](https://x.com/MaheshMurag) gave a [talk on it](https://www.youtube.com/watch?v=CEvIs9y1uog&t=1s), which explains that skills are folders containing [SKILL.md](https://x.com/RLanceMartin/status/SKILL.md) files. The YAML frontmatter of each file is loaded into agent instructions, letting the agent decide to read [SKILL.md](https://x.com/RLanceMartin/status/SKILL.md) only if needed.

## Offload Context

Another thing you can do with a computer is offload context from the agent context window to the filesystem. Manus [writes old tool results to files](https://rlancemartin.github.io/2025/10/15/manus/) and applies summarization once there are diminishing returns from offloading.

![](https://pbs.twimg.com/media/G-LGvgOa0AUCByT.jpg)

Cursor Agent [also offloads](https://cursor.com/blog/dynamic-context-discovery) tool results and agent trajectories to the filesystem, allowing the agent to read either back into context if needed.

![](https://pbs.twimg.com/media/G-LGzuca0AASCZ7.jpg)

Both of these examples help address the [valid](https://cognition.ai/blog/dont-build-multi-agents#a-theory-of-building-long-running-agents) concerns that compaction of context (aka summarization) can result in loss of useful information.

Offloading context to the filesystem can also be used to help steer long-running agents. Some agents write a plan to a file and read it back into context periodically to [reinforce objectives](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) and / or [verify their work](https://www.anthropic.com/engineering/multi-agent-research-system\)).

## Cache Context

Agents typically manage context as a list of messages. The context from each action is just appended to this list. [@irl\_danB](https://x.com/irl_danB) had an [interesting comment](https://x.com/irl_danB/status/2003223600195625356):

Agents (use a) linear chat history. Software engineers ... mental model resembles a call stack: pushing tasks on, popping them off (when done)

It is interesting to consider ways to mutate the session history by removing or adding context blocks. But, there is a consideration that informs how context might be mutated. Agents can become cost prohibitive without prompt [caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), which allows an agent to resume from a prompt prefix.

![](https://pbs.twimg.com/media/G-LIP_MXoAEGSzw.jpg)

Manus called out "cache hit rate" as the [most important metric](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) for production agents, and mentioned that a higher capacity ($/token) model with caching can actually be cheaper than a lower cost model without it. [@trq212](https://x.com/trq212) [notes that coding agents](https://x.com/trq212/status/2004026126889320668) (Claude Code) would be cost-prohibitive without caching.

## Isolate Context

Many agents delegate tasks to sub-agents with isolated context windows, tools, and / or instructions. A clear use for sub-agents is parallelizable tasks. [@bcherny](https://x.com/bcherny) [mentioned](https://every.to/podcast/how-to-use-claude-code-like-the-people-who-built-it) that the Claude Code team uses sub-agents in code review to independently check different possible issues. A similar map-reduce pattern can be used for tasks like updating lint rules or migrations.

![](https://pbs.twimg.com/media/G-LKQmLWYAE9KZJ.jpg)

Long-running agents also use context isolation. [@GeoffreyHuntley](https://x.com/GeoffreyHuntley) coined the "Ralph Wiggum", a loop that runs agents repeatedly until a plan is satisfied. It is often infeasible for a long-running task to fit into the context window of a single agent. Context lives in files and progress can be communicated across agents via git history (see [@ryancarson](https://x.com/ryancarson)'s [overview](https://x.com/ryancarson/status/2008548371712135632?s=20) and [@dexhorthy](https://x.com/dexhorthy)'s [post](https://www.humanlayer.dev/blog/brief-history-of-ralph)).

![Ralph Loop](https://pbs.twimg.com/media/G-LKwsgXYAAIC4o.jpg)

Ralph Loop

Anthropic [described](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) one version of the Ralph loop where an initializer agent sets up an environment (e.g., a plan file, a tracking file) and sub-agents tackle individual tasks from the plan file. [@bcherny](https://x.com/bcherny) mentioned this pattern with Claude Code, using [stop hooks](https://code.claude.com/docs/en/hooks) to verify work after each Ralph loop.

## Evolve Context

There's been a lot of interest in [continual learning for agents](https://www.dwarkesh.com/p/timelines-june-2025). We want agents to improve at tasks and learn from experience, like humans. Some [research](https://arxiv.org/pdf/2512.16301) has shown that agent deployments fail due to inability to adapt or learn.

[@Letta\_AI](https://x.com/Letta_AI) talks about [continual learning in token space](https://www.letta.com/blog/continual-learning\)), which just means updating agent context (rather than the model weights) with learnings over time. A common through line across approaches involves reflecting over past agent trajectories/sessions and using this as a basis for context updates.

![](https://pbs.twimg.com/media/G-LLxO_WgAEFHWN.jpg)

This pattern can be applied to task-specific prompts. As an example, [GEPA](https://arxiv.org/pdf/2507.19457) applies this idea: collect agent trajectories, score them, reflect on failures, and propose a mix of task-specific prompt variants for further testing.

This pattern can also be applied to open-ended memory learning. There are [many papers](https://arxiv.org/pdf/2510.04618\)) on this. I've [tested it](https://rlancemartin.github.io/2025/12/01/claude_diary/) with Claude Code, inspired by an interesting [insight](https://every.to/podcast/how-to-use-claude-code-like-the-people-who-built-it) from [@\_catwu](https://x.com/_catwu): distill Claude Code sessions into diary entries, reflect across diary entries, and use them to update \`[CLAUDE.md](https://x.com/RLanceMartin/status/CLAUDE.md)\`.

This can also be applied to skills. [@Letta\_AI](https://x.com/Letta_AI) has an [example of this](https://www.letta.com/blog/skill-learning), reflecting over trajectories to distill reusable procedures and then saving them to the filesystem as new skills. I've [tested similar ideas](https://www.youtube.com/watch?v=c5yDkwjZG80) with [Deepagents](https://github.com/langchain-ai/deepagents).

## Future Directions

A few patterns have emerged. Give agents a computer, and push actions from the tool calling layer to the computer. Use the filesystem to offload context and for progressive disclosure. Use sub-agents to isolate context. Evolve context over time to learn memories or skills. Cache to save cost / latency.

There are many open challenges that I'm excited to track over the next year.

**Learned Context Management**

Context management can include hand-crafted prompting for compression, spawning sub-agents, determining when / what context to offload, and how to evolve context for learning over time. [The Bitter Lesson](https://rlancemartin.github.io/2025/07/30/bitter_lesson/) predicts that compute / model scaling often overtakes such hand-crafted approaches.

For example, rather than compaction [@jeffreyhuber](https://x.com/jeffreyhuber) suggested an idea:

[Recursive Language Model](https://www.primeintellect.ai/blog/rlm) (RLM) [work](https://arxiv.org/html/2512.24601v1/) from [@lateinteraction](https://x.com/lateinteraction), [@a1zhang](https://x.com/a1zhang), [@primeintellect](https://x.com/primeintellect) is a generalization of this point, suggesting that LLMs can learn to perform their own context management. Much of the prompting or scaffolding packed into agent harnesses might get absorbed by models.

This seems particularly interesting for memories. It's a bit related to the [sleep-time compute](https://arxiv.org/abs/2504.13171) paper by [@Letta\_AI](https://x.com/Letta_AI), which shows that agents can think offline about their own context. Imagine if agents automatically reflect over their past sessions and use this to update their own memories or skills. Also, agents might directly reflect over their own memories accumulated over time to better consolidate them and / or prepare for future tasks, just as we do.

**Multi-Agent Coordination**

As agents take on larger tasks, we will likely see swarms of agents working concurrently. [@cognition](https://x.com/cognition) [noted](https://cognition.ai/blog/dont-build-multi-agents) that today's agents struggle with shared context: each action contains implicit decisions and parallel agents risk making conflicting decisions without visibility into each other's work. Agents can't engage in the proactive discourse that humans use to resolve conflicts.

Multi-agent projects like [Gas Town](https://github.com/steveyegge/gastown) by [@Steve\_Yegge](https://x.com/Steve_Yegge) are interesting: it uses a multi-agent orchestrator with git-backed work tracking, a "Mayor" agent with full context about the workspace, and coordinates dozens of concurrent Claude Code instances with a merge queue and role specialization. This and related multi-agent coordination efforts will be interesting to follow.

**Abstractions for Long-Running Agents**

Long-running agents need new infrastructure: observability into what agents are doing, hooks for human review, and graceful degradation when things go wrong. Today's patterns are still rough. Claude Code uses [stop hooks](https://docs.claude.com/en/docs/claude-code/hooks) to verify work after each iteration and the Ralph Loop tracks progress via git history. But there are no standards for agent observability, common debugging interfaces, or agreed-upon patterns for human-in-the-loop monitoring. As agents [run longer](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/), we'll probably need new abstractions to manage them.
