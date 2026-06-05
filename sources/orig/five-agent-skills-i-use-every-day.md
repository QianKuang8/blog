---
title: "5 Agent Skills I Use Every Day"
source_url: "https://www.aihero.dev/5-agent-skills-i-use-every-day"
domain: "aihero.dev"
description: "Matt Pocock's practical list of agent skills for turning repeatable engineering process into reusable AI workflows."
retrieved_at: "2026-06-05T21:16:57+08:00"
extractor: "defuddle"
---

![Matt Pocock](https://res.cloudinary.com/total-typescript/image/upload/c_limit,w_96/f_auto/q_auto/v1728059672/matt-pocock_eyjjli?_a=BAVMn6DY0)

Matt Pocock

I've been an engineer for nearly a decade. Right now, process has never been more important.

You have access to a fleet of middling to good engineers that you can deploy at any time. But these engineers have a critical flaw: they have no memory. They don't remember things they've done before.

This means you need extremely strict and well-defined processes to get them to do useful work. As a developer, you're constantly steering your agents, keeping them on the right track.

My way of fixing this has been to create a LOT of agent skills. Each skill I've designed helps me encode my process so that AI has a strict path to follow every single time:

![Repository of engineer skills and processes](https://res.cloudinary.com/total-typescript/image/upload/c_limit,w_3840/f_auto/q_auto/v1773675111/ai-hero-images/pgyy6kr82bhjliy774jx?_a=BAVMn6DY0)

Repository of engineer skills and processes

The result? The code quality that AI produces has shot up dramatically.

**The kit:** [grill-me](https://www.aihero.dev/skills-grill-me) · [to-prd](https://www.aihero.dev/skills-to-prd) · [to-issues](https://www.aihero.dev/skills-to-issues) · [tdd](https://www.aihero.dev/skills-tdd) · improve-codebase-architecture · [see all skills →](https://www.aihero.dev/skills)

## 1\. /grill-me: Flesh Out an Idea

[Read the guide](https://www.aihero.dev/skills-grill-me) · [GitHub](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me)

```shellscript
npx skills@latest add mattpocock/skills
```

This is my favorite skill. It's only three sentences long, but it's incredibly impactful.

**The Grill Me Skill:**

> Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one by one. And finally, if a question can be answered by exploring the code base, explore the code base instead.

The concept of a "design tree" comes from *The Design of Design* by Frederick P. Brooks. It's the idea that as you're designing something, you need to walk down all of the branches of a design tree.

For example, you might be designing a search page and need to decide between an advanced search interface or a simple text box. If you choose advanced search, you need to figure out all the filters and sorting methods. You keep walking down the tree until you've fully understood your design before committing to code.

![Claude asking clarifying questions about a feature](https://res.cloudinary.com/total-typescript/image/upload/c_limit,w_3840/f_auto/q_auto/v1773675112/ai-hero-images/p1coswbfzivaglbxkose?_a=BAVMn6DY0)

Claude asking clarifying questions about a feature

When I invoke this skill, I want to reach a shared understanding with the LLM. Claude Code tends to spit out a plan really early when in plan mode, creating a document before we've truly understood each other. But the grill me skill forces that conversation.

In one conversation about adding a feature to my course video editor, Claude asked me 16 questions. And that was a relatively short grilling session. I've had sessions lasting nearly half an hour with 30, 40, or even 50 questions on really complex features.

![16 interview questions displayed in the conversation](https://res.cloudinary.com/total-typescript/image/upload/c_limit,w_3840/f_auto/q_auto/v1773675113/ai-hero-images/a0vvhui4lkubi5b2aqq9?_a=BAVMn6DY0)

16 interview questions displayed in the conversation

**The key takeaway: Skills don't have to be long to be impactful. You just need to choose the right words at the right time.**

## 2\. /to-prd: From Conversation to Document

[Read the guide](https://www.aihero.dev/skills-to-prd) · [GitHub](https://github.com/mattpocock/skills/tree/main/skills/engineering/to-prd)

```shellscript
npx skills@latest add mattpocock/skills
```

Once I've reached a shared understanding with the LLM, I invoke my next skill: `/write-a-prd`.

This skill asks the LLM to create a Product Requirements Document. It may skip steps if they're not necessary. For example, if you've already done a deep interview, it moves straight to step four.

The workflow includes:

- Ask the user for a detailed description
- Explore the repo to verify assertions
- Interview the user relentlessly (using the grill me skill)
- Sketch out major modules needed
- Write the PRD using a template and submit as a GitHub issue

The important part of any PRD is the user stories. These describe the desired behavior of your system in language, drawing from Agile methodology.

![User stories section of a PRD](https://res.cloudinary.com/total-typescript/image/upload/c_limit,w_3840/f_auto/q_auto/v1773675114/ai-hero-images/mpombfwy8uz2rr1xy1yi?_a=BAVMn6DY0)

User stories section of a PRD

## 3\. /to-issues: Breaking Down the Destination into a Journey

[Read the guide](https://www.aihero.dev/skills-to-issues) · [GitHub](https://github.com/mattpocock/skills/tree/main/skills/engineering/to-issues)

```shellscript
npx skills@latest add mattpocock/skills
```

The PRD describes your destination. But what you really need is the journey to get there.

That's what the PRD to Issues skill does. It takes a PRD and turns it into a Kanban board of independently grabbable issues.

The process:

1. Locate the PRD (fetch it if needed)
2. Explore the code base
3. **Draft vertical slices** - break the PRD into tasks that flush out unknown unknowns quickly

The [tracer bullet](https://www.aihero.dev/tracer-bullets) analogy applies here. Each issue is a thin vertical slice cutting through all integration layers, not a horizontal slice of one layer.

The skill also establishes blocking relationships between tasks. For instance, one issue might not be blocked by anything, so it can be picked up independently. This is useful if you have parallel agent setups where multiple agents can work simultaneously.

![Four GitHub issues created as vertical slices](https://res.cloudinary.com/total-typescript/image/upload/c_limit,w_3840/f_auto/q_auto/v1773675116/ai-hero-images/qaodyngpkcdpfwdvi1do?_a=BAVMn6DY0)

Four GitHub issues created as vertical slices

[

AI Hero · Skill System

### There are more where these came from

grill-with-docs, domain-model, and triage round out the kit — plus a changelog of updates as it evolves.

See the skill set](https://www.aihero.dev/skills)

## 4\. /tdd: Increasing Code Quality

[Read the guide](https://www.aihero.dev/skills-tdd) · [GitHub](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)

```shellscript
npx skills@latest add mattpocock/skills
```

How do you execute on a skill? How do you make the implementation rock solid and increase code quality?

You use a TDD skill. TDD stands for Test-Driven Development, and it forces (or rather, encourages) the agent to follow a red-green-refactor loop.

This skill is substantial. It includes philosophy on refactoring, mocking, and what deep modules are. **Doing really good TDD has been the most consistent way to improve agent outputs.**

The workflow starts with confirming what interface changes are needed. When an AI looks at a bad codebase, it sees many tiny, undifferentiated modules. But if you restructure it into larger modules with thin interfaces on top, the AI can navigate it much more easily.

The skill then:

- Confirm which behaviors to test
- Design interfaces for testability
- Write one test at a time (test first)
- Implement code to make the test pass
- Look for refactoring candidates

Red-green-refactor with agents is incredible. It creates a loop that continues until complete.

![TDD workflow diagram showing the red-green-refactor cycle](https://res.cloudinary.com/total-typescript/image/upload/c_limit,w_3840/f_auto/q_auto/v1773675117/ai-hero-images/lz08tqnibbua15wpkq2n?_a=BAVMn6DY0)

TDD workflow diagram showing the red-green-refactor cycle

## 5\. /improve-codebase-architecture: Making Your Code Agent-Friendly

[View on GitHub](https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture)

```shellscript
npx skills@latest add mattpocock/skills
```

TDD demands a lot of your codebase. In a badly structured code base, test boundaries are unclear. Where should you test? At which layer?

When your code base has clear module boundaries, testing becomes much easier.

The `/improve-codebase-architecture` skill explores your codebase naturally, looking for confusions:

- Where does understanding one concept require bouncing between many small files?
- Where have pure functions been extracted just for testability, but real bugs hide in how they're called?
- Where do tightly coupled modules create integration risk?

Then it presents candidates for deepening opportunities - chances to deepen shallow modules into deeper ones.

![Three different interface designs presented side-by-side](https://res.cloudinary.com/total-typescript/image/upload/c_limit,w_3840/f_auto/q_auto/v1773675118/ai-hero-images/xcsyngiu3zdojvugipqz?_a=BAVMn6DY0)

Three different interface designs presented side-by-side

Do this once a week or after a surge of development. As you keep refining your codebase, you'll notice the quality of the agent's output goes up.

**If you have a garbage code base, the AI will produce garbage within that code base.**

That's five of seven. The rest — grill-with-docs, domain-model, triage — and a changelog of updates live at [/skills](https://www.aihero.dev/skills).

## Why This Matters: Treating AI Like Engineers

The most successful way to get code quality up from agents is to treat them like humans. Humans with weird constraints, sure - humans with no memory who are cloned and go right to work. But humans nonetheless.

[Check out the skills repository](https://github.com/mattpocock/skills) to get started.
