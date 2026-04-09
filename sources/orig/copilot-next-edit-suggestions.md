---
title: "Copilot Next Edit Suggestions"
source_url: "https://githubnext.com/projects/copilot-next-edit-suggestions/"
domain: "next.github.com"
description: "GitHub Next Project: Can we improve Copilot code completion by suggesting the next logical change, wherever it is in your project?"
retrieved_at: "2026-04-09T14:23:58+08:00"
extractor: "defuddle"
---

We *love* GitHub Copilot code completion. It provides helpful suggestions as we type, without causing us to lose focus on our main task. This is great for writing new code but what about when we need to edit existing code? When we're editing code we need to make a set of changes, additions and deletions all over our program and we'd like to have ghost text suggestions for those too. We're calling our new feature Next Edit Suggestions, or NES for short. With NES you make a change and then Copilot predicts the changes that follow and presents them to you in sequence.

Here's another way to look at it. Currently, Copilot only refers to the current version of your code to suggest a completion, but to make a next edit suggestion Copilot looks at the history of edits you have made to your program and predicts the next one. NES is a harder task since we have to consider changes anywhere in the whole file but we also have more information since we're looking at a historical sequence of edits rather than just a single snapshot in time. Copilot already tries to understand the intent behind the keystrokes, and by looking at a history of edits we're expanding that understanding so Copilot can be even more magical.

This is a tradeoff between how in-flow the suggestions appear and the breadth of suggestions we can make. Completions are naturally in-flow by being under your cursor, but limited in breadth. NES has much more scope but we also have to work harder to make sure the suggestions remain unobtrusive. [GitHub's research](https://github.blog/2022-09-07-research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/) has shown how good completions are with 73% of developers reporting it helps them stay in the flow and 87% highlighting how it reduces mental effort during repetitive tasks but now that models have improved, and we've learned a lot from our users, we think it's now worth exploring the other side of the balance.

Here are some examples from our prototype implementation.

#### Adding a field to a dataclass

We're adding a new field to a dataclass in Python. Let's look at the tradeoff. Copilot can complete a default value for the new field. It's got the task right, we're looking to complete the changes implied by adding this field, and the suggestion is not disruptive to the developer's work. Whereas, for NES the scope is broader and Copilot proposes a sequence of edits throughout the file. Copilot tries to predict how the programmer would make these changes so that the suggestions are natural even though they are not under the cursor.

<video controls=""><source src="https://githubnext.com/assets/projects/copilot-next-edit-suggestions/pointsint-nes-crop.mp4" type="video/mp4"></video>

#### Adding a new configuration option

Here we see the programmer adding a configuration option `remoteName` to their project. They copy-and-paste the block above and change the name, before NES automatically detects their intent, and handles the rest.

<video controls=""><source src="https://githubnext.com/assets/projects/copilot-next-edit-suggestions/remoteName-nes-crop.mp4" type="video/mp4"></video>

#### Adding a parameter to a method

As a final example let's look at adding a parameter to a method signature. We think this one is interesting because this operation is already provided as a standard refactoring by many IDEs. However, when you add a parameter then NES can provide a sensible value to use as the extra argument at each call-site, as well as relevant changes to the method itself.

<video controls=""><source src="https://githubnext.com/assets/projects/copilot-next-edit-suggestions/logging-nes-crop.mp4" type="video/mp4"></video>

### Open questions

We are pretty convinced that NES will be helpful for developers. However, based on our experience with Copilot we know how critical it is to get the user experience right and so we're spending our time investigating these big questions.

#### What's the best size of edit to suggest to the developer?

There are lots of options about how to show a predicted edit to the developer. Here are three examples where we consider showing either a character-level change, a line-level change, or a multiline-level change.

![Single-edit sized suggestions](https://githubnext.com/assets/projects/copilot-next-edit-suggestions/singleedit.png) ![Single-line sized suggestions](https://githubnext.com/assets/projects/copilot-next-edit-suggestions/singleline.png) ![Multiple-line sized suggestions](https://githubnext.com/assets/projects/copilot-next-edit-suggestions/multiline.png)

#### How do we show where we are going?

Copilot has a plan but its not always clear what it is.

<video controls=""><source src="https://githubnext.com/assets/projects/copilot-next-edit-suggestions/whichway-nes-crop.mp4" type="video/mp4"></video>

In this example the final product was pretty good, but the steps we took to get there were pretty odd---including deleting a line of code which we added back again later. Part of this is consideration of the size of change to show, part is the order in which to show them, and part is how we communicate a high-level plan to the developer.

You might have seen that we're pretty excited about [Copilot Workspace](https://githubnext.com/projects/copilot-workspace). We're thinking about how these two projects come together. Copilot Workspace presents a set of repository-wide changes to the developer, perhaps we can use the concepts here to work through them? Another idea is to get involved when the developer hands-off from Copilot Workspace to a development environment. Can we make NES more magical by feeding Copilot the information about the plan that's been built in the workspace?

#### How do we get the best performance/quality tradeoff from our models?

We're trying different models, prompts and fine-tuning. At the moment our large models produce good quality suggestions but at high latency, whereas our smaller models lean in the other direction. We know what we need here and we're experimenting with how to get there!

### What’s Next?

Watch this space. We have a prototype we're using on a daily basis. Our next step will be some internal user trials, and, if they go well, we'll be making it available more widely.

Update: Copilot Next Edit Suggestions is now available in [Visual Studio Code](https://code.visualstudio.com/blogs/2025/02/12/next-edit-suggestions) and [Visual Studio](https://learn.microsoft.com/en-us/visualstudio/ide/copilot-next-edit-suggestions?view=vs-2022).
