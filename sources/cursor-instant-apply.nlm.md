# Technical Summary: Scaling Full-File Code Edits via Speculative Edits and Specialized Models

## 1. Problem Definition: The Frontier Model "Edit Gap"

While frontier models like GPT-4 and GPT-4o excel at high-level reasoning, they struggle with the mechanical requirements of full-file code edits. This "Edit Gap" manifests in three primary failure modes that break the programmer’s flow and hinder agentic workflows (e.g., SWE-Agent):

*   **Laziness and Omission:** Often an artifact of RLHF training for conciseness, models frequently omit code using placeholders like `// ...` or comments.
*   **Syntactic Inaccuracy:** Even on isolated edits, models introduce bugs or consistent syntactic errors. Agents often fall into infinite loops attempting to correct the same simple edit multiple times.
*   **High Latency:** Standard autoregressive generation is too slow for large files. The delay between planning a change and seeing it applied disrupts the developer's cognitive state.

## 2. System Architecture: The Two-Stage "Plan and Apply" Framework

To optimize for both reasoning and speed, the system decouples the editing process into two distinct phases:

1.  **Planning Phase:** A high-capacity frontier model (e.g., Claude 3 Opus or GPT-4o) interacts with the user via a chat interface to determine the necessary changes.
2.  **Applying Phase:** A specialized "fast-apply" model executes the rewrite. This model is conditioned on the current file context, the conversation history, and the "sketch" or target code block produced during the planning phase.

## 3. Inference Optimization: Speculative Edits Algorithm

The core technical breakthrough in achieving high-speed edits is the **Speculative Edits** algorithm. Unlike standard speculative decoding, which requires a smaller "draft model," this approach leverages the unique nature of code editing.

**Technical Innovation:**
The algorithm utilizes a **deterministic algorithm** for speculation rather than a draft model. Because code edits typically involve a "strong prior"—the existing tokens in the original file—the system can speculate on future tokens based on the current file state. This **eliminates the need for a secondary draft model**, significantly reducing VRAM overhead and compute costs while maintaining the accuracy of a 70B parameter model.

**Performance Metrics:**
*   **Throughput:** Achieves **~1000 tokens/s** (approximately 3500 characters/s).
*   **Speedup:** Represents a **13x speedup** over vanilla Llama-3-70b and a **9x speedup** over the previous GPT-4 speculative edits deployment.
*   **Infrastructure:** Developed in collaboration with Fireworks, utilizing their specialized inference engine and custom speculation logic API.

## 4. Training Methodology and Data Engineering

The "fast-apply" model (Llama-3-70b-ft) was fine-tuned using a sophisticated data pipeline focused on "cmd-k" prompts (edit instructions within a selected region).

**Synthetic Data and Filtering:**
The training set utilized an **80/20 ratio** of synthetic to real data. To ensure quality, loss was normalized across different tokenizers using a **bits-per-byte** metric. Three critical filtering strategies were applied:
1.  **Downsampling small files:** Reducing representation of files <100 LOC.
2.  **Filename capping:** Limiting the number of examples per specific filename to avoid overfitting.
3.  **No-op downsampling:** Reducing data points where no changes were made to the file.

**Model Selection:**
While Deepseek Coder 33b was evaluated, **Llama-3-70b-ft** was chosen because it almost matched **Claude-3-Opus-diff** and outperformed GPT-4 variants in accuracy. Subjectively, it provided a superior "feel," whereas smaller or un-tuned models often required manual correction of "lazy" omissions.

## 5. Comparative Analysis: Full Rewrites vs. Diff-Based Formats

A significant design decision involved choosing between full-file rewrites and search/replace diffs (Aider-style).

| Dimension | Full-File Rewrites | Search/Replace Diffs |
| :--- | :--- | :--- |
| **Token Efficiency** | Lower (More output tokens) | Higher (Fewer output tokens) |
| **Forward Passes** | High (Increased "thinking" time) | Low (Compensated by brevity) |
| **Distribution Alignment**| High (Matches pre-training data) | Low (Out of Distribution) |
| **Robustness** | High (Avoids line counting) | Variable (Prone to number errors) |

**The Line Number Problem:**
Models struggle with standard diffs because tokenizers often merge digits (e.g., "123" as one token). This forces the model to "commit" to a specific line number before it has processed enough context to be accurate. To mitigate this, search/replace blocks were implemented using **redundant `-` and `+` lines**, making the parsing system robust to minor model failures.

**Evaluation Framework:**
Evaluations were conducted using the **Priompt** framework. **Claude-3 Opus** served as the primary grader because its assessments showed the highest correlation with human qualitative ratings compared to GPT-4 variants.

## 6. Key Design Decisions and Trade-offs

*   **Compute-over-Time:** While full rewrites are token-inefficient, the increased number of forward passes provides the model with more "compute-over-time." This effectively allows the model more "thinking" tokens to ensure syntactic integrity and avoid reasoning errors inherent in shorter diff formats.
*   **Speed Metric:** Speed is defined as `(Num Rewritten Chars) / (Latency in seconds)`. This normalizes performance across tokenizers and accounts for Time To First Token (TTFT). Dividing this metric by 4 (the typical char-to-token ratio) provides a conservative **tokens/s** lower bound.

## 7. Future Engineering Directions

To push the performance frontier further, three initiatives are underway:

1.  **Long-Context Training:** Expanding the context window to handle files up to 2,500 lines by modifying RoPE position IDs, as standard linear scaling has proven insufficient.
2.  **Knowledge Distillation:** Distilling the "fast-apply" capabilities of the 70B model into a smaller **Llama-3-8b** model to further reduce latency for massive files.
3.  **On-Policy Reinforcement Learning (RL):** Implementing RL using data from current deployments to iteratively improve edit accuracy and reliability.