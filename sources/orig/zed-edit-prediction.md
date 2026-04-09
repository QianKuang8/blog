---
title: "Zed now predicts your next edit with Zeta, our new open model - Zed Blog"
source_url: "https://zed.dev/blog/edit-prediction"
domain: "zed.dev"
description: "From the Zed Blog: A tool that predicts your next move. Powered by Zeta, our new open-source, open-data language model."
retrieved_at: "2026-04-09T14:24:06+08:00"
extractor: "defuddle"
---

Zed is built for speed. We've always strived for an editing experience that feels *instant*. But what's faster than instant? A tool that anticipates your next move. That's why we're introducing [edit prediction](https://zed.dev/edit-prediction) in Zed, powered by [Zeta](https://huggingface.co/zed-industries/zeta), our new open source model.

Here's a quick walkthrough:

As you work, Zed now predicts your next edit, so you can apply it just by hitting `tab`. Once you accept a prediction, you can perform multiple follow-up edits by pressing `tab` repeatedly, saving you time and keystrokes. We've received *a ton* of requests for this functionality, and we've poured our hearts into making it feel like a natural extension of the Zed experience.

You can use Zeta for free during this public beta by [downloading Zed](https://zed.dev/download) and signing in with your GitHub account. Edit prediction won't be free forever, but right now we're just excited to share and learn.

## Thoughtful Integration

Edit prediction transforms `tab` into a magical, universal key. But what about the existing uses of `tab`, such as indenting lines? And what happens when there's both an edit prediction *and* suggestions from your language server? We didn't want a powerful new feature to come at the expense of the existing editing experience in Zed.

<video controls=""></video>

Zeta predictions together with language server completions.

When language server completions are visible, Zed won't preview the predicted edit until you press `option` or `alt`. As soon as you press the modifier, Zed previews the edit and hides the menu to enable an unobstructed review. On macOS, you can just hit `tab` to confirm, or back out by releasing `option` to restore the language server completions menu.

On Linux, `alt-tab` is often reserved by the window manager, so we offer `alt-l` as an alternative default. We chose `l` because it's on the QWERTY home row and represents rightward movement in Vim. If your Linux window manager doesn't claim `alt-tab`, you're free to use that binding as well.

## Introducing Zeta: Zed's Open Source Edit Prediction Model

[Zeta](https://huggingface.co/zed-industries/zeta) is derived from Qwen2.5-Coder-7B, and is fully open source, including [an open dataset](https://huggingface.co/datasets/zed-industries/zeta). If you're working in an open source repository, we'd love your help improving Zeta by contributing to its dataset. Please bear with us initially, as we will be reviewing the submitted data before publishing to ensure everyone's safety and privacy. We're excited to figure this out and see a community effort form to make edit prediction better everywhere, most especially in Zed!

Companion Video

How Zed's Open-Source Edit Predictions Work

Richard Feldman and Antonio Scandurra talk about how Zed's new Edit Prediction feature works under the hood. This includes how the Zed team developed and open-sourced both the code and the dataset behind the fine-tuned Zeta language model that powers it!

[Watch the video here →](https://youtu.be/r1A268kA1uM)

[![How Zed's Open-Source Edit Predictions Work](https://zed.dev/img/edit-prediction/decoded-banner.webp)](https://youtu.be/r1A268kA1uM)

### Editing By Rewriting

Most coding models are trained on a "fill in the middle" task. You give them a prefix and a suffix, and they generate what goes in between.

```rs
<|fim_prefix|>fn quicksort(array: &mut [T]) {
    if array.len() <= 1 {
        return;
    }
    let pivot = partition(array);
    <|fim_suffix|>
    quicksort(&mut array[pivot + 1..]);
}<|fim_middle|>
```

This works for completing text at the cursor, but we wanted Zeta to predict edits at arbitrary locations, which doesn't fit into this structure.

In our experience, models aren't very good at producing granular edits, but they do excel at rewriting larger chunks of code. So that's where we started: given a list of recent edits and the cursor position, we asked the model to rewrite a snippet of text around the cursor, incorporating one or more edit predictions in the rewritten text.

### Evaluating Predictions

Before writing a single line of code, we created a set of tests to check if our idea worked. Testing the output of a large language model is tricky because, on every run, you can get slightly different results even when feeding it the exact same input. This can be mitigated by using a temperature of `0` and, for providers that support it, providing a seed for the RNG.

That said, code can often be written in many different but equally valid ways. So even when Zeta's output differs from our expected answer, it might still be doing exactly what we want—just taking a different path to get there. This makes traditional unit testing approaches particularly challenging when working with LLMs.

This led us to take a different approach—instead of strict assertions, we used a larger LLM to evaluate Zeta's edits. By writing our test assertions in plain English and having Claude check if the results matched our intent, we could validate that Zeta was making sensible edits, even when its exact output differed between runs. This ended up being much more practical than trying to make brittle assertions about specific tokens.

Here's an example taken from our eval suite:

```rs
// Input:
pub fn quicksort<T: Ord>(arr: &mut [T]) {
    let len = arr.len();
    if len <= 1 {
        return;
    }
 
    let pivot_index = partition(arr);
    <|user_cursor_is_here|>
}
 
// Assertion: Ensure that the quicksort function recurses to the left and to the right of the pivot.
```

### Prompt Engineering

We took our first stab at making those tests pass by using Qwen2.5-Coder-32B and giving it clear instructions for which types of edits we wanted it to predict. [Here's the initial system prompt](https://github.com/zed-industries/zed/blob/79a70b72b3968d102c6171f8bd2738ec7be8e94f/crates/zeta/src/complete_prompt.md) we used and you can look through the history to see how we kept changing it to pass the eval suite.

This worked out surprisingly well for the first 4-5 evals. However, as soon as we introduced more, we started noticing that it got harder and harder to pass them all consistently. Changing the prompt caused the new evals to pass, but made the old ones fail. Overall, it felt like a flaky process and we didn't feel confident this would lead to the system being robust enough to be used in production.

Moreover, using a 32b model wasn't really compatible with our strict latency requirements (more on that later).

### Supervised Fine-Tuning

After playing around with different approaches, we decided to go with supervised fine-tuning using [Unsloth](https://unsloth.ai/) and LoRA. The idea was to teach Zeta two key things: figuring out what changes a developer might want next based on their recent edits, and then actually applying those changes cleanly to the code without introducing weird side effects.

But we had a classic chicken-and-egg problem—we needed data to train the model, but we didn't have any real examples yet. So we started by having Claude generate about 50 synthetic examples that we added to [our dataset](https://huggingface.co/datasets/zed-industries/zeta-dataset). We then used that initial fine-tune to ship an early version of Zeta behind a feature flag and started collecting examples from our own team's usage.

This approach let us quickly build up a solid dataset of around 400 high-quality examples, which improved the model a lot! However, we kept running into edge cases that would trip the model up. The most annoying ones were when Zeta was working with a small piece of code in a larger file—it would sometimes get confused and make random deletions or insertions that had nothing to do with what the user was trying to do, and it didn't seem like adding more examples steered the model away from those mistakes.

### Direct Preference Optimization

To handle these edge cases, we conducted another pass using direct preference optimization (DPO). This technique let us go beyond simply showing the model what good edits look like—we could also teach it what edits *to avoid*. With DPO, we could fine-tune Zeta by providing both positive and negative examples, helping it learn the subtle differences between helpful and problematic edits.

We found that just ~150 carefully selected examples were enough to significantly improve Zeta's behavior on tricky cases. Of course, we think we can make it even better by expanding our training data with more diverse examples, and we're excited to keep pushing the boundaries here.

### Minimizing Latency: Speculative Decoding

Like every feature in Zed, latency was a critical factor for edit prediction. When we started, we set aggressive performance targets: predictions should be delivered in under 200ms for the median case (p50) and under 500ms for the 90th percentile (p90). The challenge was that rewriting complete excerpts, while enabling multi-location edits, requires generating significantly more tokens than simple fill-in-middle approaches. Initially, this put us way over our latency budget.

However, there's a fascinating insight about how edit predictions work. When we rewrite a text snippet, the output often mirrors the input closely, with changes concentrated in specific spots. This pattern lets us parallelize token generation by using the input as a reference—a technique known as speculative decoding. We use n-gram search to identify promising jumping-off points in the input where we can start parallel token generation, giving us a significant speedup without sacrificing quality.

### Minimizing Latency: Serving The Model

For edit predictions to feel responsive, we needed to solve multiple latency challenges in parallel. As discussed above, we tackled the model execution time through speculative decoding, but serving the model at scale presented its own set of hurdles. This was by far the most compute-intensive problem our team has ever tackled.

A few weeks out from launch, we ran a brief competitive process, and we ended up being really impressed with [Baseten](https://www.baseten.co/). Their performance engineers quickly optimized our open source model to run on their flexible infrastructure, achieving our target latencies while letting us retain full visibility into the details of the deployment, both for the Zed team and the entire Zed community. We plan to follow up with a guest post about what they learned optimizing [our model](https://huggingface.co/zed-industries/zeta).

Latency is not just a function of compute; network transit time is a key driver of perceived speed. To cooperate with the laws of physics, we're launching with GPUs in both North America and Europe, and we hope to add more regions soon. We're also using [Cloudflare Workers](https://workers.cloudflare.com/) to handle your requests in a data center located as close to you as possible.

## Conclusion

There's plenty more to explore to make edit predictions more powerful. We'll be fast-following with more experiments. We plan on sending more kinds of context to the model and continuing our experiments with fine-tuning, and we'll share updates as we grow and evolve the Zeta dataset.

We've learned a lot since we launched Zed AI last fall. The world is changing fast, and we're having a blast exploring and learning to build features that developers love. We're also excited to build with AI the Zed way. From our early days, we've been proponents of an open approach to building software, even when hard, and we see no reason to change that approach when it comes to working with AI. We hope you'll join us as a user, a contributor, or an employee, as we hustle to ship a golden future.
