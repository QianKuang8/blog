# Technical Report: The Convergence of Agentic Architectures (2025 Year-in-Review)

## 1. Problem Definition: The Evolution of "Deep Agents"

The AI industry has undergone a decisive shift from generic "Smart Assistants" to **Deep Agents**. This transition reflects the move from simple chat interfaces to autonomous systems capable of handling high-complexity, high-stakes professional labor. A Deep Agent is defined by two non-negotiable characteristics:

*   **Verticality (Domain-Specific Expertise):** To be effective, an agent must deliver results indistinguishable from senior human professionals.
    *   **Recruitment:** Generating candidate reports for specialized roles (e.g., AI chip architects) that include rigorous project histories and professional backgrounds with zero factual errors.
    *   **Marketing:** Selecting influencers (KOLs) and calculating market rates that align with **internal department benchmarks** by 70% or more, reflecting specific industry "secrets" and pricing norms.
*   **Long-Running Capabilities:** Agents must maintain stability and coherence over multi-hour or multi-day execution windows.
    *   **Persistence:** The ability to run continuously without system failure, exemplified by the "Claude Plays Pokemon" multi-hour live stream.
    *   **Multi-Step Planning:** Executing complex, cross-application tasks. For example, **Gemini 3**’s ability to plan trips involves checking Google Calendars, rescheduling "important" meetings to the nearest free slot, generating packing lists in Google Keep based on destination weather, and emailing the final itinerary.

This evolution represents a fundamental philosophical pivot: moving from **eliminating variance** to **managing risk**. Legacy **Workflows** are designed to eliminate variance through rigid, hard-coded paths. However, they inevitably hit a "complexity ceiling" when faced with the infinite edge cases of the real world. Modern **Agents** use natural language abstraction to navigate and manage these risks, trading absolute certainty for a significantly higher capability ceiling.

## 2. The Convergent Technical Architecture: Main-Sub Agent Framework

By late 2025, technical architectures for high-end agents converged on the **Main Agent - Sub Agent (Supervisor/Worker)** model. This industry-standard framework utilizes a central "Supervisor" for high-level logic and delegation to specialized "Workers."

This architecture is sustained by four technical pillars designed for long-running stability:

*   **Planning:** Utilizing task decomposition tools (e.g., `write_todos`) to break objectives into discrete steps, track progress, and adjust strategies in real-time.
*   **Sub-Agents (Supervisor/Worker):** This mechanism provides **context isolation**, ensuring sub-task noise does not pollute the Supervisor’s context window. This model leverages **KV Cache** optimizations, allowing for faster and significantly cheaper execution by reusing historical context across parallel workers.
*   **File System:** Agents utilize specialized tools (`ls`, `read_file`, `edit_file`) to offload context to a persistent storage layer. This acts as a shared workspace and long-term memory, preventing context window overflow.
*   **System Prompts:** Application complexity has shifted from rigid code into dense, thousand-line system instructions. These prompts define protocol standards for when to pause for planning, how to manage the workspace, and when to spawn sub-agents.

The pivotal driver of this shift was the release of the **Claude Agent SDK** (formerly the Claude Code SDK). Anthropic recognized that planning, context compression, and file-system access were universal agentic requirements, not just coding needs. This transitioned the development focus from code-centric logic to **Agent Engineering**.

## 3. Key Design Decisions: Context Engineering & Progressive Disclosure

### Agent Skills Mechanism
The "Agent Skills" framework replaces traditional, heavy prompt-filling and passive RAG indexing with a multi-level file system. This allows the agent to dynamically discover and load expertise as needed.

**The Three Levels of Progressive Disclosure**

| Disclosure Level | Content Type | Loading Trigger |
| :--- | :--- | :--- |
| **Level 1: Metadata** | Skill Name & Description | Preloaded in the System Prompt at startup to inform the agent of available capabilities. |
| **Level 2: Core Logic** | `SKILL.md` (YAML + Instructions) | Loaded into context only when the agent identifies a specific task relevance. |
| **Level 3: Deep Context** | Supplemental files (e.g., `forms.md`, Python scripts) | Navigated and read only if the specific sub-task requires deep technical detail. |

### Context Compression
To sustain performance during multi-hour sessions, automated mechanisms handle token limits. When context usage reaches a threshold (typically 80% of 200k tokens), a summary model is triggered to compress the preceding history, freeing space while retaining the essential task state.

### Layered Tool Calling & "De-toolification"
To prevent **Context Confusion** caused by overwhelming an LLM with tool definitions, a three-tier design is employed:

1.  **Atomic Layer:** A minimal set (~20) of high-frequency core tools (e.g., `bash`, `read_file`, `browser_navigate`) to ensure foundational stability.
2.  **Sandbox Utilities (De-toolification):** Instead of creating individual JSON definitions for every possible library (e.g., FFmpeg), architects provide a single **Bash/CLI** tool. This allows the agent to navigate the environment autonomously, keeping tool definitions out of the system prompt and saving significant token overhead.
3.  **Code/Package Layer:** For complex serial logic, the agent writes and executes dynamic Python scripts. This reduces **LLM Roundtrips** from dozens to a single execution. For instance, comparing phone prices across 50 countries is executed via one script rather than 50 individual tool calls, drastically increasing reliability.

## 4. Technical Trade-offs and Comparative Analysis

Architects must prioritize "Test-Time Scaling"—the principle that spending more tokens at inference time through sophisticated context engineering buys higher task accuracy.

**Architectural Comparison: Workflow vs. Autonomous Agent**

| Feature | Workflow (Directed Graph) | Autonomous Agent (Natural Language) |
| :--- | :--- | :--- |
| **Complexity Management** | Explicitly mapped in code/graphs; rigid. | Abstracted into System Prompts and Skills. |
| **Scaling Strategy** | Fixed paths; manual updates required. | **Test-Time Scaling Law** (Scaling Context Engineering). |
| **Reliability** | 100% stability; low capability "ceiling." | High "upper-bound" capability; manages risk. |
| **Knowledge Integration** | Traditional RAG (Passive retrieval). | **Agent Skills** (Hierarchical, on-demand loading). |

Unlike traditional RAG, which often retrieves fragmented text, **Agent Skills** allow for the seamless, hierarchical loading of both instructions and executable code, making the agent more "lightweight" and focused.

## 5. Strategic Implementation for Vertical Businesses

To adapt general-purpose agents to vertical scenarios, the following technical checklist is required:

*   **SOP Digitalization:** Convert Standard Operating Procedures (SOPs) into "Skills" stored in the agent’s file system for **Load on Demand** execution.
*   **Infrastructure Encapsulation:** Utilize the **Model Context Protocol (MCP)** to wrap internal business APIs, allowing the agent to connect to enterprise data as a peripheral device.
*   **Boundary Control:** Implement fine-grained System Prompts to distinguish between the **Main Agent** (responsible for orchestration/routing) and **Sub-Agents** (responsible for execution), ensuring adherence to business constraints.

**Conclusion: The Path for 2026**
The emergence of **Agent-native models**—such as **Claude 3.7/4.5**, **DeepSeek V3.2**, and **Gemini 3**—has fundamentally compressed the development cycle. By leveraging Agent Engineering, developers can now skip the weeks of intensive data preparation required for **Supervised Fine-Tuning (SFT)**. The new path for 2026 favors **token consumption** as a strategic trade-off for development velocity, reducing time-to-market for complex vertical agents from weeks to days.