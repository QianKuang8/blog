# Technical Summary: Deep Dive into the Codex Agent Loop

## 1. Core Problem Definition: The Software Agent Loop

The **Agent Loop** is the central orchestration logic of the Codex framework, coordinating the interaction between users, Large Language Models (LLMs), and the toolset required to execute tasks. The primary challenge for any software agent is maintaining reliability and state while performing iterative reasoning and executing modifications within a local environment.

### The Interaction Turn
An "interaction turn" (or "dialogue thread") encompasses the complete journey from user input to the final agent response. A single turn is rarely a linear exchange; it often involves multiple internal iterations where the agent must decide whether to provide a textual answer or invoke a tool.

### Inference vs. Tool Execution
*   **Model Inference:** The process where the model consumes a prompt (context) to generate tokens. This is the reasoning phase.
*   **Tool Execution:** When the model issues a functional request (e.g., a shell command), the agent pauses generation, executes the action locally, and appends the result back into the dialogue history.

### Primary Output
Unlike standard chat assistants, the primary output of a software agent is the **direct modification of the local file system or environment**. The "Assistant Message" serves as a termination signal, indicating the loop has reached a completion state or requires further user clarification.

---

## 2. Technical Architecture and Inference Flow

### The Iterative Mechanism
Codex processes inference and execution through a strict sequential flow, utilizing Server-Sent Events (SSE) to handle streaming data and tool lifecycle:

1.  **Input & Tokenization:** User input and environment context are aggregated and converted into integer-based tokens.
2.  **Inference & SSE Handling:** The model generates a response stream. Codex handles specific SSE event types:
    *   `response.output_text.delta`: Used for real-time UI streaming.
    *   `response.output_item.added`: Converted into internal objects to be appended to the next **input** payload.
    *   `response.output_item.done`: Signals the completion of a reasoning or tool-call item.
3.  **The Iteration Sub-loop:**
    *   **Tool Call:** If a `function_call` item is generated, the agent executes the tool.
    *   **Context Update:** The tool's output is appended to the **input** list.
    *   **Re-inference:** The updated history is sent back to the Responses API for the next step.
4.  **Final Response:** The loop terminates when the model returns an assistant message without further tool requests.

### Responses API Integration
The Responses API acts as a standardized abstraction layer. Codex CLI can be configured to point to various backends via the `responses_api_endpoint` in **~/.codex/config.toml**:

| Endpoint Type | Implementation / URL |
| :--- | :--- |
| **ChatGPT Backend** | `https://chatgpt.com/backend-api/codex/responses` |
| **OpenAI API** | `https://api.openai.com/v1/responses` |
| **Local/OSS (gpt-oss)** | `http://localhost:11434/v1/responses` (supports Ollama/LM Studio) |
| **Cloud Providers** | Support for **Azure**-hosted Responses API implementations |

### Data Payload Structure
The JSON payload for a Responses API request is defined by three parameters:
*   **`instructions`**: Client-provided messages defining core behavior. If not specified in **config.toml**, Codex defaults to model-specific files like **gpt-5.2-codex_prompt.md**.
*   **`tools`**: A schema-compliant list of functions including internal Codex tools, API-exposed tools, and MCP (Model Context Protocol) tools.
*   **`input`**: A structured list of objects containing `type`, `role`, and `content` representing the conversation history.

---

## 3. Prompt Construction and Message Prioritization

### Role Hierarchy and Control
Content weighting is determined by a role hierarchy. A critical distinction in the Codex architecture is the locus of control for these roles:
*   **system**: Highest priority. Content is typically controlled by the **server**, ensuring core safety and alignment.
*   **developer**: High priority. Controlled by the **client** to define sandbox permissions and specific engineering constraints.
*   **user**: Standard priority. Contains specific task requests and local environment data.
*   **assistant**: Informational priority. Previous reasoning and tool results.

### Initialization Sequence
Codex populates the **input** field in a strict order before the first user message to establish a consistent "Static Prefix" for caching:
1.  **Sandbox Permissions (`role=developer`):** Defines shell tool limitations using fragments like **workspace_write.md** or **on_request.md**. **Note:** This sandbox applies *only* to Codex-provided shell tools; MCP tools must implement their own safety protocols.
2.  **Developer Instructions (`role=developer`):** Custom instructions from the user's local **config.toml**.
3.  **Project Context (`role=user`):** Aggregated instructions from **AGENTS.md** or **AGENTS.override.md**. This is subject to a 32 KiB limit, scanning upward from the Current Working Directory (CWD) to the Git root.
4.  **Environment Context (`role=user`):** Explicitly states the CWD and active Shell type to orient the model.

---

## 4. Key Design Decisions and Engineering Trade-offs

### Statelessness and Zero Data Retention (ZDR)
Codex intentionally avoids using the `previous_response_id` parameter.
*   **The Trade-off:** This results in "quadratic growth" of the JSON payload, as the entire conversation history is transmitted with every request.
*   **Architectural Justification:** This ensures a **stateless architecture**, which is critical for ZDR compliance. In ZDR configurations, the server may store the decryption key for `encrypted_content`, but it does not store the conversation data itself. The network overhead is considered acceptable as it is significantly lower than the cost of model sampling.

### Performance via Prompt Caching
To maintain linear complexity (O(n)) in sampling costs despite quadratic growth in payload size, Codex relies on **Exact Prefix Matching** for prompt caching.
*   **Cache Miss Pitfalls:** Dynamic tool enumeration (ordering changes in MCP servers), mid-conversation model swaps, or changing environment configurations.
*   **The Append-Only Strategy:** When a configuration change occurs (e.g., a directory change), Codex does not modify the original environment message. Instead, it **appends** a new `role=user` message to the end of the input, preserving the existing cache prefix for all preceding tokens.

### Context Window Management (Compaction)
To prevent exceeding the model's token limit, Codex manages context through compaction:
*   **Manual:** The `/compact` command generates a summary to replace the history.
*   **Automated:** Once the `auto_compact_limit` is reached, Codex calls the `/responses/compact` endpoint.
*   **Technical Detail:** This endpoint returns a `type=compaction` item with an opaque `encrypted_content` field. This allows the model to retain context "understanding" in a compressed, stateless format while freeing the context window for new tokens.

---

## 5. Operational Best Practices for AI Engineering

*   **Enforce Deterministic Tool Enumeration:** Tool lists, especially those from dynamic MCP servers, must be provided in a consistent order to ensure cache hits.
*   **Prioritize Static Instruction Placement:** Keep core instructions and project documentation at the beginning of the payload to maximize the "Static Prefix."
*   **Implement Client-Side MCP Safety:** Do not assume the Codex sandbox covers third-party MCP tools. Engineers must verify that MCP tools include their own execution guards.
*   **Adhere to Append-Only State Updates:** When modifying environment variables or CWD mid-turn, always append new messages rather than editing historical items to avoid breaking the cache prefix.
*   **Monitor Compaction Thresholds:** Ensure that critical project-level instructions are placed in the `instructions` or early `input` items so they are preserved or prioritized during automated compaction.