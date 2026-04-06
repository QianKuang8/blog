# Technical Report: Instinct - Open Next Edit Model for Intelligent Code Refactoring

### 1. Problem Definition: Beyond Cursor-Based Autocomplete

The "Next Edit" task represents a fundamental departure from standard predictive text in software engineering. While traditional autocomplete is restricted to character-stream insertion at the current cursor position, Next Edit models must predict the developer's next logical modification—including deletions, multi-line replacements, and structural refactoring—across a defined code window.

| Aspect | Traditional Autocomplete | Next Edit |
| :--- | :--- | :--- |
| **Scope of Change** | Inserts text only at the cursor | Rewrites code windows (deletions, insertions, replacements) |
| **Complex Changes** | Requires multiple acceptances | Handles complex refactoring in a single operation |
| **Code Restructuring** | Cannot delete or restructure code | Understands editing trajectories and developer intent |
| **Developer Flow** | Frequent interruptions break flow | Maintains flow with fewer interruptions |

#### Technical Efficiency Gap
Function refactoring serves as a primary benchmark for this task. A standard operation—such as modifying parameter lists, updating return types, and adjusting the function body—typically requires over **40 manual operations**, even when accounting for optimized cursor jumps and bulk deletions. Instinct collapses this operational sequence into a single **tab-to-accept** decision. As detailed in the Keystroke-Distance Evaluation (Section 6), transforming these ~40 DP-optimal operations into a single action is the primary driver of the measured 6.4x workflow acceleration.

### 2. Technical Architecture and Foundation

Instinct is architected on the **Qwen2.5-Coder-7B** base, selecting a 7-billion parameter count to ensure high-fidelity reasoning while remaining viable for local deployment.

*   **Deployment Characteristics:** The model is optimized for local GPU execution via **Ollama** or **SGLang** endpoints, addressing enterprise requirements for data privacy and low-latency inference.
*   **Input Context Specification:** To effectively infer developer intentions, the model ingests a multi-faceted prompt structure:
    *   **Edit Trajectory:** The five most recent edits in the session.
    *   **Codebase Context:** RAG-retrieved segments from external files.
    *   **Current File State:** The full content of the active file.
    *   **Editable Region:** The specific span designated for rewriting.
    *   **Architectural Rationale:** This holistic context is required to move beyond pattern matching toward intention inference, allowing the model to anticipate the "next step" in a non-linear editing sequence.

### 3. Data Engineering and Pipeline

Model performance is predicated on high-fidelity interaction logs rather than synthetic git-commit data, which often lacks the granular "trajectory" of a live session.

#### Data Sourcing and Heuristics
The dataset comprises over **4,000 real-world edits** collected from active developer sessions.
*   **Chunking Logic:** Raw keypress streams were processed using line- and timing-based heuristics to aggregate individual characters into well-formed, self-contained diffs.
*   **Efficiency Filtering:** To ensure the model predicts direct refactoring paths, sequences involving repetitive or "ping-pong" editing behavior (jumping between lines without progress) were discarded.

#### Multilingual Synthesis and Mixture Tuning
To maintain performance across the polyglot requirements of modern IDEs, the TypeScript-heavy source data was expanded via a "bootstrap" translation method:
*   **Synthetic Translation:** A self-hosted **Qwen3-Coder-30B** translated TypeScript trajectories and contexts into Java, C, Python, and Rust.
*   **Data Mixture Optimization:** Precise data correctors were applied to maintain quality. Critically, the final data mixture was tuned by ablating **CodeBLEU** scores across languages, ensuring balanced validation performance and high-quality synthetic-to-real-world distribution.

### 4. Training Methodology: Selective Knowledge Transfer (SeleKT)

Supervised Fine-Tuning (SFT) was conducted using the **SeleKT** algorithm, originally utilized in the **NextCoder** instructed editing models. 

*   **Mechanism vs. LoRA:** Unlike LoRA, which updates a predefined set of low-rank adapters, SeleKT performs a full backward pass to compute dense gradients for all parameters. It then identifies and extracts the **top-k gradients** by magnitude, applying only those sparse updates. 
*   **Technical Advantage:** This "discovery" process ensures that only the parameters most critical to the Next Edit task are modified. Zero-ing out smaller updates prevents the "erosion" of the model’s pre-trained coding knowledge and mitigates overfitting.
*   **Training Specs:**
    *   **Fine-tuning Scope:** 5% of parameters updated.
    *   **Schedule:** Log warmup and cosine decay over 5 epochs.
    *   **Proxy Evaluation:** CodeBLEU was monitored to ensure high similarity between predicted rewrites and human ground truth.

### 5. Engineering Trade-offs

*   **Editable Region Constriction:** The rewrite span was fixed at **one line above and five lines below the cursor**. This configuration was selected based on the natural features and mean size of diffs in the interaction dataset, balancing model focus with contextual awareness.
*   **Sparse Update Selection:** The choice of SeleKT over full fine-tuning was a strategic decision to maintain the model's general-purpose programming logic while injecting the specific "intent-to-diff" mapping required for Next Edit.
*   **Diff-Centric Definition:** Moving from raw keypresses to self-contained diffs was essential. Training on fragmented character sequences results in incoherent "flickering" suggestions; training on logical diff units produces stable, expert-level refactors.

### 6. Comparative Performance and Evaluation

#### LLM Judge Framework (Quality)
Evaluation utilized a **Claude-based judge** on a 0-5 scale. This represents a methodological shift away from binary or assertion-based evaluations.
*   **The "Expert Edit" Benchmark:** A score of **3** is assigned to edits that do not match the ground truth but are logically valid actions an expert developer would take. This allows for the evaluation of intent and alternative valid refactors.
*   **Results:** Instinct achieved an average score of **3.877**, surpassing the previous open-source state-of-the-art, Zeta (3.735).

#### Keystroke-Distance Evaluation (Speed)
The efficiency gain was quantified by determining the absolute lower bound of manual editing time.
*   **Methodology:** The system backtracks through the **dynamic programming (DP) table of a Levenshtein distance calculator** to extract the character-level diff. This diff is then resolved into a **DP-optimal sequence** of keypresses and cursor jumps.
*   **Speed Benchmark:** Assuming a developer at 90 WPM executing this DP-optimal sequence, Instinct—running on an **8xH100 cluster**—is **6.4x faster** than manual editing.

### 7. Future Directions and Ecosystem

Instinct is released with open weights to provide the community with a robust foundation for local AI-assisted development. Assets available for immediate integration include:
*   **Open Weights & HuggingFace Model Card:** Full access to the 7B parameter model and the underlying 4,000+ edit dataset.
*   **KTO Integration:** The released assets are compatible with **Kahneman-Tversky Optimization (KTO)**, enabling teams to further refine the model using their own internal accept/reject interaction data.
*   **GitHub Repository:** Source code for training pipelines and evaluation frameworks.