# Technical Summary: Zeta — Next Edit Prediction via Generative Rewriting

### 1. Problem Definition: Transitioning from Code Completion to Next Edit Prediction
Standard industry models primarily utilize **Fill-In-The-Middle (FIM)**, a task-specific architecture where a model is provided a prefix and a suffix to generate the intervening text. While FIM is effective for linear code completion at the current cursor position, it is fundamentally ill-equipped for "Next Edit Prediction." FIM lacks the structural awareness to predict edits at arbitrary locations based on non-linear edit histories.

In the Zed editor, our goal was to move beyond simple completion toward a tool that anticipates the developer's next logical move. This required a paradigm shift in user experience:
*   **Predictive Intent:** Anticipating the developer's next move before it is manually initiated.
*   **Instant Interaction:** Achieving an "instant" feel through sub-200ms p50 latency.
*   **Non-Linearity:** Supporting multi-location edits across a file rather than being tethered to the cursor's current line.
*   **Seamless UI Integration:** The "Tab" key serves as the primary confirmation mechanism. To resolve conflicts with Language Server Protocol (LSP) menus, we implemented an **Alt/Option modifier** (or **Alt-L** on Linux) to preview predictions without obstructing completions.

### 2. Technical Solution: The Zeta Model & "Editing by Rewriting"
The Zeta model is a fine-tuned derivative of **Qwen2.5-Coder-7B**, chosen for its optimal balance between reasoning capabilities and inference-time performance. 

To move beyond the limitations of FIM, we adopted an **"Editing by Rewriting"** methodology. Instead of treating the edit as a simple string-gap problem, Zeta treats a code excerpt as a mutable block. The model receives a snippet of text surrounding the cursor and generates a full rewrite of that excerpt, incorporating the predicted changes directly into the structure. This approach allows the model to perform complex, structural transformations that granular, token-level diff models often fail to execute cleanly.

**Input Parameters for the Model:**
*   **Recent Edits:** A chronologically ordered history of the developer's recent changes.
*   **Cursor Position:** High-resolution telemetry of the user's current focal point.
*   **Contextual Excerpt:** A surrounding window of code that serves as the basis for the rewrite.

### 3. Training Methodology: A Three-Stage Pipeline
Moving from a general-purpose model to a production-grade edit predictor required a specialized fine-tuning pipeline using **Unsloth** and **LoRA** to maintain high training throughput.

#### Supervised Fine-Tuning (SFT)
We initially faced a "chicken-and-egg" data scarcity: training required real-world edit history that didn't exist in open datasets. We resolved this by:
1.  **Synthetic Bootstrapping:** Generating 50 initial examples via Claude to define the basic task structure.
2.  **Internal Dogfooding:** Shipping an early version of Zeta behind a feature flag to our internal team. This allowed us to collect ~400 high-quality, real-world examples of professional development workflows.

> **SFT Strategic Objectives**
> *   **Intent Logic:** Teaching the model to correlate recent edit patterns with the next logical structural change.
> *   **Syntactic Integrity:** Ensuring that the rewritten snippet integrates seamlessly without introducing side effects or syntax regressions.

#### Direct Preference Optimization (DPO)
SFT alone left the model vulnerable to specific failure modes, particularly in larger files where it would occasionally trigger random deletions or insertions. To address this, we used **DPO** with ~150 curated pairs of positive and negative examples. This taught Zeta not just what a "good" edit looks like, but specifically which "hallucinated" behaviors—such as destructive insertions—to avoid.

### 4. Evaluation Strategy: LLM-as-a-Judge
Traditional unit testing and "strict assertions" are insufficient for generative code tasks. Even when Zeta’s output is logically correct, it may differ from a reference string by a few tokens, causing brittle tests to fail. Furthermore, while we attempted to mitigate non-deterministic output variance using `temperature 0` and RNG `seeds`, these measures did not eliminate the inherent variability of generative rewriting.

Our solution was an **LLM-as-a-Judge** framework using Claude. We replaced brittle token-based assertions with plain English descriptions of the intended logic. Claude evaluates Zeta’s output against these assertions, validating that the intent was met even if the exact string differs. This shift allowed us to move from measuring "textual identity" to measuring "functional correctness."

### 5. Latency Optimization: Speculative Decoding & Infrastructure
To maintain Zed’s "instant" performance standards, we established strict targets: a **p50 of <200ms** and a **p90 of <500ms**.

#### Speculative Decoding
Rewriting an entire excerpt is more token-intensive than FIM. However, we identified a critical mathematical prerequisite for optimization: the output rewrite is typically 90%+ identical to the input. We leverage this similarity via **speculative decoding**, using an **n-gram search** to identify matching segments between the input and output. This allows the system to find "jumping-off points" to parallelize token generation, effectively bypassing the sequential nature of autoregressive decoding.

#### Serving Architecture
*   **Baseten Infrastructure:** We worked with Baseten engineers to optimize the model for flexible GPU deployments.
*   **Cloudflare Workers:** Requests are routed at the edge to ensure the lowest possible network overhead.
*   **Geographic Sharding:** To mitigate the laws of physics regarding latency, we deployed GPU clusters in both North America and Europe, minimizing the physical distance between the developer and the inference engine.

### 6. Comparative Analysis: Zeta vs. Industry Standard (FIM)

| Feature | Standard FIM (Fill-In-The-Middle) | Zeta (Editing by Rewriting) |
| :--- | :--- | :--- |
| **Task Type** | Linear text completion | Structural next edit prediction |
| **Edit Location** | Constrained to the current cursor gap | Arbitrary/Multiple locations within snippet |
| **Model Output** | Appends new text to a static gap | Rewrites the mutable excerpt block |
| **Contextual Input** | Static Prefix and Suffix | Recent edit history, cursor, and excerpt |
| **History Awareness**| None (Stateless regarding edits) | High (Driven by recent edit telemetry) |

### 7. Key Design Decisions & Trade-offs
*   **Model Size vs. Latency:** Initial testing with 32B models showed high performance but failed to meet the sub-500ms p90 latency budget. We successfully transitioned to the **7B Zeta model** to ensure the inference-time latency stayed within the limits required for a "live" feel.
*   **Rewriting vs. Granular Edits:** While rewriting requires higher token generation than granular diffs, it provides the model the structural flexibility needed for multi-location edits. We mitigated the token cost through our speculative decoding implementation.
*   **Regression Management:** Early prompt engineering was highly susceptible to regressions—fixing one edge case frequently caused existing test cases to fail. This lack of robustness necessitated the shift to a formal SFT/DPO fine-tuning pipeline, which provided the stability required for production deployment.