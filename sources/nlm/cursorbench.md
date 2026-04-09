# Technical Summary: Model Quality Evaluation Framework at Cursor

### 1. Core Problem: The Failure of Public Benchmarks for Frontier Agents
Current public coding benchmarks struggle to distinguish between frontier models because they fail to align with real-world developer experiences and the requirements of modern agentic workflows. Cursor identified three primary failure modes in existing frameworks:

*   **Alignment Issues:** Static benchmarks often measure irrelevant capabilities. For example, **Terminal-Bench** emphasizes broad, puzzle-style tasks, such as determining a chess move, which fails to reflect the actual repository-level coding work developers perform.
*   **Grading Rigidness:** Many public benchmarks assume a narrow set of "correct" solutions. While developer requests are often underspecified and allow for multiple valid architectural paths, traditional benchmarks either penalize alternative correct approaches or append synthetic requirements to force a specific outcome. This fails to assess a model's ability to navigate ambiguity.
*   **Data Contamination and Saturation:** Benchmarks like **SWE-bench (Verified, Pro, and Multilingual)** draw from public repositories that are frequently included in model training data. This leads to "saturation," where models can reproduce "gold patches" from memory. Evidence of this saturation is seen when low-tier models like **Haiku** can match or exceed the performance of frontier models like **GPT-5** on these benchmarks, rendering them useless for distinguishing true utility.

### 2. The Hybrid Evaluation Architecture: Online-Offline Loop
To maintain model quality, Cursor utilizes a dual-layer evaluation system that ensures model performance remains grounded in actual production usage through a continuous feedback loop.

*   **CursorBench (Offline):** The internal suite for measuring solution correctness, code quality, efficiency, and interaction behavior. This acts as the primary gate for benchmarking models before production deployment.
*   **Online Evaluations:** Controlled analysis on live traffic used to track high-level proxies of agent outcomes. By monitoring **interaction and output quality signals**, Cursor catches regressions where an agent’s output may look correct to a static grader but creates a friction-heavy experience for the developer.
*   **The Loop in Practice (Case Study):** To attribute impact accurately, Cursor uses controlled online experiments. For instance, when iterating on retrieval systems, the team ran an **ablation removing the semantic search tool entirely**. This experiment pinpointed exactly where the tool was critical—specifically for repository-grounded question-answering on larger codebases—allowing for more targeted offline benchmark refinements.

### 3. Data Sourcing and Methodology for CursorBench
CursorBench is engineered to provide a high-signal environment by utilizing real-world data and advanced grading techniques.

*   **The "Cursor Blame" Mechanism:** Tasks are sourced by tracing committed code back to the specific agent request that generated it. This provides a natural pairing of a real-world developer query and a ground-truth solution.
*   **Contamination Defense:** Many tasks are sourced from internal codebases and controlled private environments. This makes it physically impossible for public models to have encountered the tasks during pre-training, ensuring the benchmark measures reasoning rather than retrieval.
*   **Evolution to CursorBench-3:** The suite has scaled to match the complexity of frontier agents. **CursorBench-3** features tasks with **substantially more lines of code (LoC)** than those found in SWE-bench Verified, Pro, or Multilingual. The suite incorporates multi-workspace environments, monorepos, production log investigations, and long-running experiments.
*   **Agentic Graders:** Because developer queries are intentionally short and realistic, they are often underspecified. Cursor employs agentic graders to handle this ambiguity, allowing the system to reliably identify and reward valid alternative approaches that traditional, rigid scripts would fail to recognize.

### 4. Comparative Analysis: CursorBench vs. Public Benchmarks

| Dimension | Public Benchmarks (e.g., SWE-bench) | CursorBench |
| :--- | :--- | :--- |
| **Task Sourcing** | Public GitHub repositories; high contamination risk. | Internal sessions via "Cursor Blame"; low contamination risk. |
| **Task Specification** | Detailed, long-form GitHub issues. | Short, realistic, and underspecified developer queries. |
| **Grading Approach** | Narrow solutions or synthetic requirements to force a "gold patch." | Agentic graders that recognize multiple valid architectural paths. |
| **Model Separation** | **High Saturation:** Low-tier models (Haiku) can match/exceed frontier models (GPT-5). | **High Distinction:** Reliably separates models that developers experience as meaningfully different. |

### 5. Key Design Decisions and Engineering Trade-offs
Developing a production-grade evaluation framework requires navigating critical technical trade-offs to ensure the results translate to product excellence.

*   **Correctness vs. Efficiency:** Cursor utilizes correctness-vs-latency plots to visualize the compute/latency trade-off. The engineering objective is to optimize for the **"top right corner"** of the plot—achieving the highest solution correctness at the lowest completion token count.
*   **Specificity vs. Realism:** Cursor prioritizes realism by using short, ambiguous tasks over the hyper-specific prompts found in public benchmarks. While this increases grading complexity, it ensures the model is tested on how developers actually interact with the product.
*   **Reproducibility vs. Scalability:** As agents evolve to perform long-running tasks across external services, maintaining a reproducible environment becomes difficult. Furthermore, the use of agentic graders introduces significant compute costs, creating a trade-off between the depth of the evaluation and the frequency of the runs.

### 6. Future Directions in Agent Evaluation
As development work shifts toward long-running agents that operate independently over hours or days, Cursor is evolving its evaluation suite to meet three specific goals:

1.  **Cost Reduction in Grading:** Developing more efficient methodologies to make the agentic grading of complex, multi-step tasks financially sustainable at scale.
2.  **External Environment Reproducibility:** Solving the technical hurdles of creating deterministic environments for tasks that require interaction with live external services.
3.  **Closing the Offline-Online Gap:** Refining offline metrics to more perfectly predict shifts in "interaction and output quality signals" observed in the IDE, ensuring that every benchmark improvement translates to a better developer experience.