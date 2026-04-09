---
title: "Every CLI coding agent, compared"
source_url: "https://michaellivs.com/blog/cli-coding-agents-compared"
domain: "michaellivs.com"
description: "A landscape survey of CLI coding agents, comparing first-party and open-source tools across features, licensing, and developer workflows."
retrieved_at: "2026-04-09T23:03:58+08:00"
extractor: "defuddle"
---

/Actions

[Subscribe](https://michaellivs.com/subscribe)

The terminal is where agents got serious. Not IDE plugins. Not web chatbots. The CLI.

Claude Code, Codex CLI, Gemini CLI, OpenCode. These aren’t toys. They read your codebase, edit files, run tests, commit code. Some run for hours without human intervention. Some [spawn sub-agents](https://michaellivs.com/blog/anatomy-of-agentic-systems). Some sandbox themselves so thoroughly they can’t access the network.

There are now 36 CLI coding agents. I’ve mapped the entire landscape.

## The big four

The frontier labs all have terminal agents now. But an open-source project is outpacing them all.

| Agent | Stars | License | Local Models | Free Tier |
| --- | --- | --- | --- | --- |
| [OpenCode](https://github.com/anomalyco/opencode) | 97.5K | MIT | Yes (75+ providers) | Free (BYOK) |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | 93.6K | Apache-2.0 | No | 1000 req/day |
| [Claude Code](https://github.com/anthropics/claude-code) | 64K | Proprietary | No | None |
| [Codex CLI](https://github.com/openai/codex) | 59K | Apache-2.0 | Yes (Ollama, LM Studio) | None |

OpenCode exploded to 97.5K stars. It’s the free, open-source alternative to Claude Code with 650K monthly users.

Gemini CLI has the most generous free tier. 1000 requests per day with just a Google account. No API key required. But no local model support.

Claude Code is locked to Claude models but has the [richest feature set](https://michaellivs.com/blog/architecture-behind-claude-code). Jupyter notebook editing, sub-agent orchestration, the deepest permission system.

Codex CLI is the only one written in Rust. OpenAI rewrote it from TypeScript in mid-2025 for performance.

## The full landscape

Sorted by GitHub stars.

### First-party (major labs)

| Agent | Maker | Stars | Lang | License | Key Feature |
| --- | --- | --- | --- | --- | --- |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Google | 93.6K | TS | Apache-2.0 | 1M token context, generous free tier |
| [Claude Code](https://github.com/anthropics/claude-code) | Anthropic | 64K | TS | Proprietary | Created MCP, Jupyter editing, deepest features |
| [Codex CLI](https://github.com/openai/codex) | OpenAI | 59K | Rust | Apache-2.0 | Rust performance, model-native compaction |
| [Qwen Code](https://github.com/QwenLM/qwen-code) | Alibaba | 18.1K | TS | Apache-2.0 | Ships with open-weight Qwen3-Coder |
| [Trae Agent](https://github.com/bytedance/trae-agent) | ByteDance | 10.7K | Python | MIT | SOTA on SWE-bench Verified |
| [Copilot CLI](https://github.com/github/copilot-cli) | GitHub | 8K | Shell | Proprietary | GitHub ecosystem integration |
| [Kimi CLI](https://github.com/MoonshotAI/kimi-cli) | Moonshot AI | 5.9K | Python | Apache-2.0 | First Chinese lab with CLI agent |
| [Mistral Vibe](https://github.com/mistralai/mistral-vibe) | Mistral | 3K | Python | Apache-2.0 | Only European lab CLI agent |
| [Junie CLI](https://github.com/jetbrains-junie/junie) | JetBrains | 31 | TS | Proprietary | Deep JetBrains integration, CI/CD native |
| [Amazon Q CLI](https://github.com/aws/amazon-q-developer-cli) | AWS | 1.9K | Rust | Apache-2.0 | Deprecated, now Kiro (closed-source) |

### Community & independent

| Agent | Stars | Lang | License | Key Feature |
| --- | --- | --- | --- | --- |
| [OpenCode](https://github.com/anomalyco/opencode) | 97.5K | TS | MIT | 75+ providers, 650K users |
| [OpenHands](https://github.com/OpenHands/OpenHands) | 67.5K | Python | MIT | Full platform, Docker sandbox, $18.8M raised |
| [Open Interpreter](https://github.com/openinterpreter/open-interpreter) | 62K | Python | AGPL-3.0 | Runs any code, not just file edits |
| [Cline CLI](https://github.com/cline/cline) | 57.6K | TS | Apache-2.0 | IDE agent that added CLI mode |
| [Aider](https://github.com/Aider-AI/aider) | 40.3K | Python | Apache-2.0 | Pioneer, git-native, tree-sitter repo map |
| [Continue CLI](https://github.com/continuedev/continue) | 31.2K | TS | Apache-2.0 | JetBrains + CLI, headless CI mode |
| [Goose](https://github.com/block/goose) | 29.9K | Rust | Apache-2.0 | MCP-native architecture, Block-backed |
| [Warp](https://github.com/warpdotdev/Warp) | 25.9K | Rust | Proprietary | Full terminal replacement with agents |
| [Roo Code](https://github.com/RooCodeInc/Roo-Code) | 22.1K | TS | Apache-2.0 | Multi-agent orchestration (Boomerang) |
| [Crush](https://github.com/charmbracelet/crush) | 19.5K | Go | Custom | Beautiful TUI, from Bubble Tea team |
| [SWE-agent](https://github.com/SWE-agent/SWE-agent) | 18.4K | Python | MIT | Research-grade, NeurIPS paper |
| [Plandex](https://github.com/plandex-ai/plandex) | 15K | Go | MIT | Diff sandbox, git-like plan branching |
| [Kilo Code](https://github.com/Kilo-Org/kilocode) | 14.9K | TS | Apache-2.0 | 500+ models, zero markup |
| [Claude Engineer](https://github.com/Doriandarko/claude-engineer) | 11.2K | Python | MIT | Self-expanding tools |
| [AIChat](https://github.com/sigoden/aichat) | 9.2K | Rust | Apache-2.0 | Swiss Army knife CLI |
| [DeepAgents](https://github.com/langchain-ai/deepagents) | 8.9K | Python | MIT | LangChain’s agent harness |
| [Pi](https://github.com/badlogic/pi-mono) | 6.6K | TS | MIT | Only 4 tools, self-extending |
| [ForgeCode](https://github.com/antinomyhq/forge) | 4.6K | Rust | Apache-2.0 | 300+ models, Rust performance |
| [Kode CLI](https://github.com/shareAI-lab/Kode-cli) | 4.3K | TS | Apache-2.0 | Multi-model collaboration |
| [gptme](https://github.com/gptme/gptme) | 4.2K | Python | MIT | OG agent (2023), still active |
| [AutoCodeRover](https://github.com/AutoCodeRoverSG/auto-code-rover) | 3.1K | Python | Source-Available | $0.70/task on SWE-bench |
| [Codebuff](https://github.com/CodebuffAI/codebuff) | 2.8K | TS | Apache-2.0 | Multi-agent architecture |
| [Codel](https://github.com/semanser/codel) | 2.4K | TS | AGPL-3.0 | Docker sandbox built-in |
| [Grok CLI](https://github.com/superagent-ai/grok-cli) | 2.3K | TS | MIT | xAI/Grok in terminal |
| [Agentless](https://github.com/OpenAutoCoder/Agentless) | 2K | Python | MIT | No persistent agent loop |
| [Amp](https://ampcode.com/) | N/A | TS | Proprietary | Multi-model per-task (Sourcegraph) |

### Agent orchestrators

These don’t write code themselves. They run multiple CLI agents in parallel.

| Tool | Stars | What it does |
| --- | --- | --- |
| [Claude Squad](https://github.com/smtg-ai/claude-squad) | 5.9K | Parallel agents via tmux + git worktrees |
| [Toad](https://github.com/batrachianai/toad) | 2.1K | Unified TUI for multiple agents (by Rich creator) |
| [Superset](https://github.com/superset-sh/superset) | 1.2K | Terminal command center for agent teams |
| [Emdash](https://github.com/generalaction/emdash) | 1.2K | YC-backed, Linear/GitHub/Jira integration |

## Feature comparison

The features that actually differentiate them.

| Agent | MCP | Sandbox | Sub-agents | Headless | Plan Mode | Project Memory |
| --- | --- | --- | --- | --- | --- | --- |
| OpenCode | Yes | Docker | Yes | Yes | Yes | AGENTS.md |
| Claude Code | Yes | Seatbelt/Bubblewrap | Yes | Yes | Yes | CLAUDE.md |
| Codex CLI | Yes | Seatbelt/Landlock | Yes | Yes | Yes | AGENTS.md |
| Gemini CLI | Yes | Seatbelt/Docker | Yes | Yes | Yes | GEMINI.md |
| Qwen Code | Yes | Docker/Seatbelt | Yes | Yes | Yes | QWEN.md |
| Aider | No | None | No | Yes | No | None |
| Goose | Yes | Docker (MCP) | Yes | Yes | Yes | .goosehints |
| OpenHands | Yes | Docker | Yes | Yes | Yes | None |
| Continue CLI | Yes | None | Yes | Yes | No | .continue/rules |
| Cline CLI | Yes | Checkpoints | Yes | Yes | Yes | .clinerules |
| Warp | Yes | None | No | Yes | Yes | WARP.md (reads all) |

Warp reads everyone’s memory files: `WARP.md`, `CLAUDE.md`, `AGENTS.md`, and `GEMINI.md`. If you switch between agents, it just works.

## New features to watch

The latest wave of CLI agents added several differentiating features:

| Feature | Who has it | What it does |
| --- | --- | --- |
| **LSP Support** | Claude Code, OpenCode, Crush, Cline | Language Server Protocol for IDE-grade code intelligence |
| **Skills/Prompt Templates** | Claude Code, Gemini CLI, OpenCode, Pi, Kilo Code | Reusable capability packages loaded on-demand |
| **Hooks** | Claude Code, Gemini CLI, Goose, Mistral Vibe, Crush | Pre/post tool execution event handlers |
| **Voice Input** | Gemini CLI (experimental), Cline, Aider, Goose | Speech-to-text for hands-free coding |
| **Checkpoints/Branching** | Claude Code, Plandex, Gemini CLI, Kilo Code, Cline | Git-like state snapshots for plan exploration |
| **Multi-agent Orchestration** | Claude Code, Roo Code (Boomerang), Claude Squad, Emdash | Coordinate multiple specialized agents |
| **Tree-sitter** | Aider, Claude Code, Plandex, Cline, Kilo Code | AST-based code understanding |

## Sandboxing approaches

I wrote about [sandboxing strategies](https://michaellivs.com/blog/sandbox-comparison-2026) in detail, but here’s the CLI agent reality:

| Agent | Linux | macOS | Network |
| --- | --- | --- | --- |
| Claude Code | bubblewrap | Seatbelt | Proxy with allowlist |
| Codex CLI | Landlock + seccomp | Seatbelt | Disabled by default |
| Gemini CLI | Docker/Podman | Seatbelt | Proxy |
| Goose | Docker (optional) | None | Via MCP |
| OpenHands | Docker | Docker | Isolated |
| Codel | Docker | Docker | Isolated |

Claude Code and Codex CLI both use OS-level primitives. No Docker required. This matters for CLI tools — users won’t install Docker just to use an agent.

## How to pick

**You want the most features.** Claude Code or OpenCode. Sub-agents, hooks, skills, updated almost daily, LSP support. Claude Code has the deepest permission system. OpenCode is open-source with 75+ providers.

**You want free.** Gemini CLI. 1000 requests/day, no API key, 1M token context, skills, hooks, checkpoints. Hard to beat.

**You’re in the OpenAI ecosystem.** Codex CLI. OS-level sandboxing, Apache-2.0, written in Rust. Native GPT integration.

**You want local models.** OpenCode, Aider, or Kilo Code. All support Ollama. Kilo Code has 500+ models; Aider has tree-sitter repo maps.

**You’re building your own agent.** Pi. Four core tools, great component library, extensions, solid philosophy. A clean base to fork.

**You want plan branching.** Plandex. Git-like branching for plans, diff sandbox, tree-sitter repo maps.

**You love Charmbracelet.** Crush. From the Bubble Tea team, written in Go, LSP-aware.

**You’re on JetBrains.** Junie CLI. JetBrains’ own agent, deeply integrated, works headless in CI.

Thirty-six agents. Four that matter for most people: OpenCode for open-source, Claude Code for features, Gemini CLI for free, Codex CLI for performance.

The rest solve specific problems — browse the full list above.

A year ago, none of this existed. Now there’s a CLI agent for every workflow. Pick one and start shipping.

---

*Full dataset with all 36 agents, features, and metadata: [cli-agents.json](https://michaellivs.com/data/cli-agents.json)*
