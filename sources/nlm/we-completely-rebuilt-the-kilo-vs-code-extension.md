# Technical Report: The Re-Architecture of Kilo Code for VS Code

### 1. Problem Definition: The Architectural Debt of VS Code Internals
The legacy Kilo Code architecture suffered from a fundamental dependency on VS Code internals, which served as a primary bottleneck for multi-platform expansion. While functional within its native environment, this "editor-first" design created severe technical frictions when ported to other surfaces:

*   **Inappropriate Abstraction Leakage:** Every deployment—including the Kilo CLI, Cloud Agents, and the JetBrains extension—was forced to package and execute VS Code internal components.
*   **Cross-IDE Performance Degradation:** In the JetBrains ecosystem, the system was effectively running VS Code internals inside a competitor IDE. This resulted in significant latency and resource overhead, as developers were forced to operate through a fragmented "IDE-within-an-IDE" stack.
*   **Sequential Bottlenecks:** The legacy architecture was optimized for single-threaded, sequential tool execution, which constrained agent throughput to the latency of the slowest individual tool call.
*   **Infrastructure Rigidity:** Patching around editor-specific dependencies prevented the realization of a truly portable agentic core, complicating maintenance and slowing the deployment of new capabilities to non-VS Code surfaces.

### 2. Technical Solution and Core Architecture
The re-architecture centers on the **OpenCode server**, a portable, MIT-licensed engine designed specifically for agentic engineering. By decoupling the core logic from the VS Code runtime, we have established a platform-agnostic system that allows the VS Code extension to share the exact same foundation as the Kilo CLI.

**The "One Foundation" Approach: Architectural Benefits**
*   **Engine Portability:** The OpenCode server acts as a standalone core, enabling native performance across CLI, IDE, and cloud environments without the weight of unnecessary editor internals.
*   **Unified Logic Layer:** New features and performance optimizations are implemented once at the core level and immediately propagated across all supported interfaces.
*   **Native Throughput:** By removing the shim layers required for VS Code internal compatibility, the extension achieves lower latency in file I/O and terminal operations.
*   **Extensibility:** The MIT-licensed foundation encourages community-driven improvements to the agentic core, independent of specific editor APIs.

### 3. Advanced Parallelism and Subagent Delegation

**Parallel Tool Execution**
The re-architecture shifts the performance bottleneck from sequential tool-chain latency to parallel subagent throughput. Kilo now handles concurrent tool calls natively. Rather than waiting for a file read to complete before initiating a codebase search or a terminal command, the OpenCode engine executes these actions simultaneously. This multi-threaded orchestration significantly reduces the "wall-clock time" required for complex, multi-step engineering tasks.

**Subagent Orchestration**
For high-complexity workflows, the system utilizes **Orchestrator mode** to implement a delegation pattern. A primary agent can spin up multiple specialized subagents to work on independent components of a project:
*   **Specialized Subagents:** Simultaneous execution of Implementation, Test-writing, and Documentation agents.
*   **Custom Subagents:** Developers can define specialized subagents for bespoke workflows, such as security auditing, migration passes, or linting.
*   **Intelligent Aggregation:** The Orchestrator manages these parallel work streams, intelligently merging their outputs into the parent context to maintain project cohesion.

### 4. The Agent Manager: Git-Worktrees and Code Review Integration
The Agent Manager has been re-engineered to run natively on the OpenCode core, facilitating sophisticated "Agent-assisted development" workflows.

**Git-Worktrees and Read-Heavy Workflows**
To eliminate file conflicts during parallel execution, the Agent Manager utilizes **git-worktrees**. This allows multiple agents to operate in isolated subdirectories of the same repository. Furthermore, the system supports a "read-heavy" pattern where one agent executes code changes while a secondary agent simultaneously reviews the diff or analyzes codebase patterns without merge overhead.

| Feature | Single Agent Workflow | Parallel Agent-Worktree Workflow |
| :--- | :--- | :--- |
| **Concurrency** | Sequential; tool calls must resolve linearly. | Multi-threaded; simultaneous execution of subtasks. |
| **Conflict Management** | High; agents risk overwriting shared buffers. | Low; isolation via independent git-worktrees. |
| **Throughput** | Limited by individual LLM response times. | Multiplier effect; hours of work compressed into minutes. |
| **State Resolution** | Single-branch dependence. | Managed merge via PR or direct worktree application. |

**Multi-Model Comparison**
The Agent Manager enables simultaneous execution of the same prompt across disparate LLMs. This is critical for evaluating complex architectural decisions or UI layouts. For example, a developer can run **Claude Opus 4.6** and **GPT-5.3** on a single refactoring task to compare outputs side-by-side, selecting the implementation that best aligns with project requirements.

**Inline Code Review and Diff Reviewer**
To maintain code quality during autonomous execution, the Agent Manager includes a built-in **diff reviewer**. 
*   **Visualization:** Supports unified or split views with a file tree sidebar for navigating large changesets.
*   **Line-Level Feedback:** Developers can leave comments directly on specific lines of the diff, identical to a standard PR workflow.
*   **Context Injection:** Upon hitting "Send all to chat," these comments—including file paths and line numbers—are fed back to the agent as structured context for iterative refinement.

### 5. Integration and Cross-Platform Session Continuity
The shared OpenCode core ensures that session state, including **Memory Bank configurations**, remains synchronized across all environments. The technical flow of a cross-platform session is as follows:

1.  **Initiation:** A session is initialized via the Kilo CLI (e.g., while a developer is SSHed into a production server).
2.  **Context Synchronization:** Active session state, provider settings, and Memory Bank configurations are stored within the shared core.
3.  **Transition:** The developer opens VS Code on a local workstation; the extension detects and synchronizes the remote session state.
4.  **Resumption:** The developer resumes the workflow in the IDE with full access to the history and context generated in the CLI environment.

### 6. Design Decisions and Critical Trade-offs
The transition toward "Agentic Engineering" necessitates a shift from deterministic IDE control to autonomous agentic workflows. This creates specific architectural trade-offs:

| Feature | Technical Trade-off |
| :--- | :--- |
| **Autonomous Parallelism** | **Loss of Granular Transparency:** Parallel tool lists can operate as a "black box," executing multiple steps without the step-by-step confirmation found in sequential IDE assistants. |
| **Agent Autonomy** | **Workflow Displacement:** Agents may prioritize task completion over real-time developer feedback, occasionally ignoring instructions to "wait for confirmation" in favor of autonomous execution. |
| **Git-Worktree Isolation** | **Branch Visibility Gap:** Changes made in isolated worktrees are not visible in the primary editor branch until the merge phase, potentially disrupting developers who prefer to "micro-manage" file states during development. |
| **Shared Core Migration** | **UI Lag:** Initial pre-release versions may lack native UI for provider configuration, requiring temporary reliance on CLI-based setup. |

### 7. Future Roadmap and Community Engagement
The path toward General Availability (GA) focuses on stabilizing the portable core and incentivizing community contributions:

1.  **Automated Migration Experience:** Implementation of a seamless transfer for provider settings, API keys, and Memory Bank configurations from legacy extensions to the OpenCode-based system.
2.  **Open-Source Bug Bounty:** A community incentive program offering $100 in Kilo Credits for merged pull requests that resolve bugs in the pre-release core.
3.  **Native Provider UI:** Integration of provider setup directly into the VS Code extension interface, removing the current requirement for CLI-based configuration.
4.  **Production Stabilization:** Finalizing the migration of all remaining legacy features and optimizing the Orchestrator for large-scale enterprise codebases.