---
title: "The Anatomy of Harness Engineering: How to Evaluate, Iterate, and Guard AI Coding Agents"
source_url: "https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/"
domain: "developers.googleblog.com"
author: "Taylor Mullen, Christian Gunderman"
published_at: "2026-09-09"
description: "Learn how to build a robust evaluation harness for AI agents using behavioral evals. Test specific tool calls, automate prompt engineering, and ship with confidence."
retrieved_at: "2026-09-10T16:36:43+08:00"
extractor: "defuddle"
---

## The Anatomy of Harness Engineering: How to Evaluate, Iterate, and Guard AI Coding Agents

SEPT. 9, 2026

[Taylor Mullen](https://developers.googleblog.com/search/?author=Taylor+Mullen) Principal Engineer

[Christian Gunderman](https://developers.googleblog.com/search/?author=Christian+Gunderman) Staff Software Engineer

![BlogBanner_990x556_x2](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/BlogBanner_990x556_x2.original.png)

When developers first work on harness engineering for agentic coding systems, they often fall into the same trap: they run common end-to-end benchmarks like Terminal-Bench and DeepSWE, watch a composite score move by a few percentage points, and have no idea why it changed.

End-to-end benchmarks are the de facto for evaluating model performance and determining what needs deeper investigation, but the challenge is that those investigations come at a high cost.

**Behavioral evaluations are often a better measure of confidence** on whether the behaviors you expect actually do happen and whether you’re moving in the right direction instead of backsliding when it comes to regressions or new model changes. They can serve as your iteration partner and help give insight into why certain changes move the needle in one way or another.

Here’s our take on behavioral evaluation, including approaches that have helped us keep agent systems reliable as models evolve.

## The paradigm shift: Report cards vs. behavioral guideposts

Most teams evaluate AI agents like they would evaluate a student taking an exam. They hand the agent a large codebase, give it a time limit, and measure its success based on how many tests pass or fail.

When that score drops, what went wrong?

- Did the model get overconfident on ambiguous prompts?
- Did it forget to verify the test suite before submitting?
- Did it hallucinate a CLI flag?

End-to-end benchmarks don’t typically directly answer these questions.

**Behavioral evaluations** function like integration tests for improving agent harness operation. When you have a rich enough behavioral eval set, you have a baseline for the behavior you're targeting from your agent, and you're able to iteratively improve the prompt to get there.

Instead of measuring whether the agent solved an entire multi-file refactor, a behavioral eval measures discrete, observable actions:

- When given an underspecified prompt, does the agent ask a clarifying question instead of guessing?
- When modifying a build file, does it run the local validator before declaring it complete?
- When generating documentation, does it provide canonical repository links?

![Screenshot 2026-09-09 at 9.34.40 AM](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/Screenshot_2026-09-09_at_9.34.40AM.original.png)

## When to evaluate: The dogfooding precedent

Instead of setting up a complex evaluation harness on day one, use this time to follow your hunches and run experiments.

When bootstrapping an agent from scratch, **you start with developer instinct and dogfooding**. Until you have built an agent capable of dogfooding its own codebase, handling boilerplate, writing its own markdown renderer, and executing routine developer tasks, it doesn’t make sense to run evaluations.

Evals belong to the second phase of development: **ensuring forward progress** and **guarding against regressions**.

The primary purpose of an evaluation suite is not to celebrate when you make the agent 2% better; it is to give you unshakeable confidence that a new prompt tweak, tool schema change, or model upgrade **did not make the agent holistically worse**.

## How a behavioral evaluation architecture works

A robust harness evaluation framework separates behavioral assertions into fast, deterministic, unit-style checks that run locally.

Shifting your focus to these smaller, observable actions creates a reliable safety net. You can confidently iterate on your system prompts or switch to a different model, because you’ll know immediately if you've accidentally broken a core behavior.

### Writing a behavioral eval

Behavioral evals assert on intermediate execution steps, like specific tool calls or file modifications, instead of final string equality:

```python
import pytest
from google.antigravity import Agent, LocalAgentConfig, types

@pytest.mark.asyncio
async def test_agent_uses_web_search_for_live_weather():
  """Assert that the agent consults ground truth rather than guessing."""
  config = LocalAgentConfig()

  async with Agent(config) as agent:
    response = await agent.chat("What's the weather like in Mountain View, California?")
    tools = [call.name async for call in response.tool_calls]

  # Assert behavior, not output prose
  assert types.BuiltinTools.SEARCH_WEB in tools, (
      "Agent answered from memory without consulting live search."
  )
```
[Example written for the Antigravity SDK. Explore the full repo.](https://github.com/google-antigravity/antigravity-sdk-python)

With a rich suite of behavioral evals, you can automate your prompt engineering. For example, you can set up a loop where an LLM tweaks its own system prompt, iterating until a failing test finally passes, all while the rest of your test suite acts similar to how a CI/CD-style guardrail operates. This helps you ensure that the changes don’t break any existing features.

## What to consider when building a behavioral suite

There are a few things you can do from the start to make this process repeatable. I suggest you start small with a three-step behavioral testing loop:

1. **Pick one failure mode**: Find a recent mistake your agent made, like forgetting to run unit tests before marking a task as done. Find a single, obvious action that slipped, and make that your target.
2. **Write flexible assertions based on task complexity:** For simple tasks with one optimal solution, build a strict single-turn assertion checking if the agent hit a specific milestone (e.g., verifying it called the test-runner). However, for more complex tasks, the model may take an unexpected but entirely correct path. In those scenarios, avoid enforcing a rigid tool sequence. Instead, use fuzzier, outcome-based checks, such as an LLM-as-a-judge, to evaluate whether the agent's chosen steps successfully and safely solved the problem.
3. **Automate batch evaluations to monitor stability:** Rather than blocking PRs on single eval runs that can be noisy due to nondeterminism of AI models, automate batch evaluations to pull a larger volume of data. Tracking aggregate pass rates over time ensures the model's behavior is trending correctly. Relying on this directional signal gives you the flexibility to tweak prompts and upgrade models safely without halting development for expected variance.

```shell
# Run local behavioral suite in under 5 seconds
pytest evals/behavioral/ -v
```

Your agent doesn't need a higher benchmark score to get started. It needs an evaluation harness that keeps it honest.

To build a stable, resilient harness, you have to stop treating your model like a black box passing a final exam, and start treating your harness like standard software that requires unit and integration testing.

## Final thoughts

While behavioral evaluations are a core pillar of harness engineering, they aren’t a replacement for larger, end-to-end evaluation suites. They’re actually complementary. Macro benchmarks verify the final destination and micro behavioral evals serve as a partner that enables safe, rapid iteration. When you adopt both, you'll have higher confidence levels when iterating, like when making prompt changes, building out new features, or even deploying brand-new models.
