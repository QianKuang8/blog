---
title: "Introducing Instinct: the world's best open Next Edit model, built by Continue"
source_url: "https://blog.continue.dev/instinct/"
domain: "x.com"
description: "Meet Instinct, Continue's open Next Edit model that's built to predict your next edit and keep you in flow"
retrieved_at: "2026-04-09T14:23:57+08:00"
extractor: "defuddle"
---

[← Back to blog](https://blog.continue.dev/) ![Introducing Instinct: the world's best open Next Edit model, built by Continue](/_next/image?url=%2Fimages%2Fblog%2Finstinct-hero.png&w=3840&q=75&dpl=dpl_6u6eiWY42vZnTSTmEC7bhAWcx2vv)

We're thrilled to share [Instinct](https://huggingface.co/continuedev/instinct?ref=blog.continue.dev), our open Next Edit model, which intelligently predicts your next move to keep you in flow.

When we launched [Next Edit](https://blog.continue.dev/next-edit-powered-by-mercury-coder/), we premiered it with [Mercury Coder](https://hub.continue.dev/inceptionlabs/mercury-coder?ref=blog.continue.dev) from Inception. Today, we're expanding the possibilities with Instinct: an open, in-house–trained model that developers can run locally on their own GPUs.

As you code, Instinct sees your edit trajectory and carries out the next step automatically—an estimated 6.4x faster than manual editing.

> 💡 [Try it today](https://docs.continue.dev/guides/instinct?ref=blog.continue.dev) with Ollama and Continue in VS Code

## Why Train an Open Model?

While open models for agentic coding tasks have advanced rapidly in recent months, work on Next Edit remains nascent. Most progress had been made by Zed on their model Zeta and we are glad to be able to build upon what they learned. One of our goals is to highlight the open opportunity and lay the groundwork for future efforts that will benefit not only our team, but also our community and the broader developer ecosystem.

And while existing models like Mercury Coder have shown excellent performance, Instinct enables developers to run or customize a Next Edit model on their own GPUs, addressing privacy and customization needs.

| Aspect | Traditional Autocomplete | Next Edit |
| --- | --- | --- |
| Scope of Change | Inserts text only at the cursor | Rewrites code windows (deletions, insertions, replacements) |
| Complex Changes | Requires multiple acceptances | Handles complex refactoring in a single operation |
| Code Restructuring | Cannot delete or restructure code | Understands editing trajectories and developer intent |
| Developer Flow | Frequent interruptions break flow | Maintains flow with fewer interruptions |

Traditional tab autocomplete can only *insert* code at the cursor as you type. This is helpful when ripping through boilerplate code, but most of the time developers are refactoring, maintaining, iterating on— *editing* —code.

As an example, refactoring a function might require: deleting old parameters (5 keystrokes), moving to the return statement (2 cursor jumps), changing the return type (8 keystrokes), and updating the function body (20+ keystrokes and 5+ cursor jumps). With Instinct, this entire sequence becomes a single tab-to-accept action, transforming what would be 40+ manual operations into one.

## Training the Model

### Real World Training Data

To create our Next Edit model, we needed high quality training data. Instead of synthetically generating examples, we automatically collected over 4,000 real-world edits from the Continue team as they worked on our open-source code. This is an order of magnitude more than the Zeta dataset released earlier this year, and represents real world development patterns better than the purely synthetic data that could be constructed from git commits.

Each data example includes:

- The five most recent edits the developer made
- Relevant context from other files
- The region of code to rewrite
- The ground-truth change the developer made to that region

A fundamental question we ran into was what constituted an "edit." Every keypress? Every time the user hit save? All keypresses made within some time window? After many iterations, we defined a set of line- and timing-based heuristics that "chunked" individual keypresses into well-formed and self-contained diffs.

When we examined sequences of such diffs, we noticed that developers sometimes jumped back and forth, iterating on the same one or two lines repetitively. We defined filters to throw out such examples since we wanted Instinct to make efficient, non-repetitive edits.

Continue's [autocomplete context pipelines](https://blog.continue.dev/root-path-context-the-secret-ingredient-in-continues-autocomplete-prompt/) provided relevant information about the codebase, with content from the current file included in the prompt as well. We define the editable region (the span of code to be rewritten by the model) as starting one line above the cursor and ending five lines below. This decision was made based on the natural features of the diffs we saw in our dataset.

Taken together, the edit sequence, context, current file content, and editable region provide the necessary information to infer the developer's intentions and predict the next step in the edit sequence.

### Maintaining Multilingual Support

One problem we ran into was that the Continue team works mostly with Typescript code. However, we wanted our model to preserve support for multiple languages. In addition to training the model in a robust way (more on this later), we used a self-hosted Qwen3-Coder-30B model to synthetically "translate" diffs, context, and file contents into Java, C, Python, and Rust—thus bootstrapping a multilingual dataset off of the Typescript data. A set of precise data correctors and filters ensured high quality and a similar distribution of edits among the 4,000+ synthetic examples.

With a multilingual dataset ready to go, it was time to move on to supervised fine-tuning (SFT). SFT for specific tasks like Next Edit is typically done using Low-Rank Adaptation (LoRA), since although [it learns less, it also forgets less](https://arxiv.org/abs/2405.09673?ref=blog.continue.dev) of the pre-trained model's general coding abilities.

The central problem with using LoRA, however, is that it fixes the parameters to be fine-tuned before training even begins. A preferable approach is to *discover* which parameters' weight updates are most important, and update only those. Rather than treating Next Edit as learning new *knowledge* at the expense of forgetting previous coding ability, the model can ideally adapt to the *task* of Next Editing while retaining its pre-trained coding knowledge.

We found exactly such a solution in the Selective Knowledge Transfer (SeleKT) algorithm used to train the [NextCoder](https://www.microsoft.com/en-us/research/publication/nextcoder-robust-adaptation-of-code-lms-to-diverse-code-edits/?ref=blog.continue.dev) instructed code-editing models. SeleKT computes dense gradients (as in full fine-tuning), extracts the top- *k* gradients by magnitude, and then applies only those sparse weight updates. It discovers through practice what actually needs to change, rather than guessing beforehand, and as a result, only the most important weights for the Next Edit *task* are updated. Moreover, zero-ing out small weight updates helps prevent overfitting and erosion of previous coding knowledge, problems that full fine-tuning would suffer from.

We fine-tuned 5% of [Qwen2.5-Coder-7B](https://arxiv.org/abs/2409.12186?ref=blog.continue.dev) 's parameters using SeleKT. After initial hyperparameter sweeps, the training process was standard, using a log warmup and cosine decay learning rate schedule for 5 epochs. We used the [CodeBLEU](https://arxiv.org/abs/2009.10297?ref=blog.continue.dev) score as a quick proxy eval between predicted and ground truth rewrites during training. Ablating CodeBLEU scores across different languages in the dataset allowed us to adjust the data mixture, resulting in high validation performance across languages. Due to the robust training, only a small number of multilingual examples were needed.

## Performance Results: Evals for Quality and Speed

| 3.877 | 6.4x faster\* |
| --- | --- |
| Average LLM Judge Score (new open-source state-of-the-art) | than manually typing out edits *\* on our 8xH100 cluster* |

It's nontrivial to evaluate the quality of a Next Edit suggestion formally, since there are often many ways to accomplish the same coding goal. Accordingly, we deployed Claude as an LLM judge with instructions to assess the quality of Next Edit suggestions on a five-point scale, where:

- A score of five corresponds to a functional match with the developer's ground-truth edit,
- A score of four corresponds to a similar edit to the developer's ground truth edit, although not an exact functional match,
- A score of three corresponds to an edit that does not match the ground truth but would reasonably be made by an expert developer in such a scenario,
- A score of two corresponds to an edit that does not logically follow from the previous edits and context,
- A score of one corresponds to an edit that is likely to hinder developer progress, such as large deletions or complete irrelevance, and
- A score of zero corresponds to a malformed rewrite that does not line up with the editable region.

This evaluation method is similar to the one Zed uses for Zeta. We noticed that their judge prompt caused the LLM to output scores of only zero or five, and that it relied on handcrafted assertions about the next edit. We created a different system prompt that helps represent the full spectrum of scores and compares the model's edit to the developer's ground truth change instead of relying on assertions. With just minor adjustments to account for our different Next Edit prompt structures, Instinct's average score of 3.877 outperforms Zeta's score of 3.735 on the held-out eval set. We're excited to see further work continuing to improve on this benchmark.

Not only does Instinct provide high-quality suggestions, our keystroke-distance eval, loosely based on that of [Coeditor](https://arxiv.org/abs/2305.18584?ref=blog.continue.dev), demonstrates that it also massively speeds up your workflow. By backtracking through the dynamic programming (DP) table of a Levenshtein distance calculator, it's possible to extract a character-level diff between the editable region and the suggested rewrite. That character-level diff can be "chunked" into edit operations, *e.g.*, adding three characters at one location, deleting five characters at another location, and such.

The minimum time to carry out the full edit is given by the optimal combination of keypresses and cursor jumps that accomplish all the edit operations. This can be posed as another DP problem. We assume the developer types at an average of 90 WPM, simulate the ability to highlight and delete as opposed to repeatedly hitting the backspace key, allow for small arrow movements instead of more time-intensive cursor jumps, and use the spatial distance between cursor locations (*i.e.* line and character) instead of just the index within the whole string. This lower bound on manual editing time is compared to average model inference time on our internal SGLang endpoint plus the time for one keypress (tab-to-accept).

The result is that even if you immediately knew exactly what edit to make, *and* took the DP-optimal sequence of actions to carry it out at 90 WPM, using the model would still provide the high-quality edit 6.4 times faster.

## Now what?

First, we encourage you to try it out! Instinct is a 7B model so you should expect it to be slow on most laptops, but with sufficient hardware it is a great option for self-hosting. Read [our guide](https://docs.continue.dev/guides/instinct?ref=blog.continue.dev) to learn more.

If you want to build upon our dataset, training pipelines, or open weights (for example to run [KTO](https://arxiv.org/abs/2402.01306?ref=blog.continue.dev) on your own accept/reject data) we'd recommend exploring our [GitHub repository](https://github.com/continuedev/instinct?ref=blog.continue.dev), [HuggingFace model card](https://huggingface.co/continuedev/instinct?ref=blog.continue.dev), and dataset.

Most importantly, if you are interested in furthering the state of the art, either as part of the community or the Continue team, please [reach out](mailto:nate@continue.dev)!
