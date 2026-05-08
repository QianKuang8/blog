---
title: "Claude Code: Anthropic's Agent in Your Terminal"
source_url: "https://www.latent.space/p/claude-code"
domain: "latent.space"
description: "Cat Wu and Boris Cherny from the Claude Code team stop by to tell all!"
retrieved_at: "2026-05-08T09:35:28+08:00"
extractor: "defuddle"
---

*Last few days for [AI Engineer early bird tickets](https://ti.to/software-3/ai-engineer-worlds-fair-2025/discount/LS30) - most of the [speakers](http://localhost:3000/#SpeakersList) have been announced! Limited tix for [volunteers](https://www.ai.engineer/volunteer) are available, and you can also get discounted tickets via [the official AIE Hackathon](https://cerebralvalley.ai/e/aiewf-hackathon-2025) and [the State of AIE survey](https://www.surveymonkey.com/r/57QJSF2)! The AIE Expo has [sold out](https://x.com/aiDotEngineer/status/1920142621525348774) but we have opened a [few slots](https://aiewf.cerebralvalley.ai/) for the Hackathon (winners present at AIE)!*

---

The AI coding wars have now split across four battlegrounds:

- **AI IDEs:** with two leading startups in [Windsurf](https://www.latent.space/p/windsurf) ($3B acq. by OpenAI) and [Cursor](https://www.latent.space/p/cursor) ($9B valuation) and a sea of competition behind them (like [Cline](https://cline.bot/), Github Copilot, etc).
- **Vibe coding platforms:** [Bolt.new](https://www.latent.space/p/bolt), [Lovable](https://lovable.dev/), [v0](https://v0.dev/), etc. all experiencing fast growth and getting to the tens of millions of revenue in months.
- **The teammate agents:** [Devin](https://www.youtube.com/watch?v=T7NWjoD_OuY), [Cosine](https://www.latent.space/p/cosine), etc. Simply give them a task, and they will get back to you with a full PR (with [mixed results](https://www.answer.ai/posts/2025-01-08-devin.html))
- **The cli-based agents:** after [Aider](https://github.com/Aider-AI/aider) ’s initial success, we are now seeing many other alternatives including two from the main labs: [OpenAI Codex](https://github.com/openai/codex) and [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview). The main draw is that 1) they are composable 2) they are pay as you go based on tokens used.

Since we covered all three of the first categories, today’s guests are Boris and Cat, the lead engineer and PM for Claude Code. If you only take one thing away from this episode, it’s this piece from Boris: **Claude Code is not a product as much as it’s a Unix utility.**

This fits very well with Anthropic’s product principle: “do the simple thing first.” Whether it’s the memory implementation (a markdown file that gets auto-loaded) or the approach to prompt summarization (just ask Claude to summarize), they always pick the smallest building blocks that are useful, understandable, and extensible. Even major features like planning (“/think”) and memory (#tags in markdown) fit the same idea of having text I/O as the core interface. This is very similar to the original UNIX design philosophy:

![Bringing the Unix Philosophy to the 21st Century - Brazil's Blog](https://substackcdn.com/image/fetch/$s_!A-O7!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6b4cbcd-5acd-4158-b608-038f30db1725_495x346.png)

Bringing the Unix Philosophy to the 21st Century - Brazil's Blog

Claude Code is also the most direct way to consume Sonnet for coding, rather than going through all the hidden prompting and optimization than the other products do. You will feel that right away, as the average spend per user is $6/day on Claude Code compared to $20/mo for Cursor, for example. Apparently, there are some engineers inside of Anthropic that have spent >$1,000 in one day!

If you’re building AI developer tools, there’s also a lot of alpha on how to design a cli tool, interactive vs non-interactive modes, and how to balance feature creation. Enjoy on your podcast app or [YouTube](https://youtu.be/zDmW5hJPsvQ)!

![](https://www.youtube.com/watch?v=zDmW5hJPsvQ)

### Show Notes

- [Cat Wu](https://www.linkedin.com/in/cat-wu/)
- [Boris Cherny](https://twitter.com/bcherny)
- [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
- [Aider](https://github.com/paul-gauthier/aider)
- [MCP creators episode](https://www.latent.space/p/mcp)
- [Husky](https://typicode.github.io/husky/)
- [TMUX](https://github.com/tmux/tmux)
- [Bitter Lesson](https://www.incompleteideas.net/IncIdeas/BitterLesson.html)
- [Cyclomatic Complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity)
- [Interpretability Research by Chris Olah](https://transformer-circuits.pub/)

### Timestamps

- \[00:01:59\] Origins of Claude Code
- \[00:04:32\] Anthropic’s Product Philosophy
- \[00:07:38\] What should go into Claude Code?
- \[00:09:26\] Claude.md and Memory Simplification
- \[00:10:07\] Claude Code vs Aider
- \[00:11:23\] Parallel Workflows and Unix Utility Philosophy
- \[00:12:51\] Cost considerations and pricing model
- \[00:14:51\] Key Features Shipped Since Launch
- \[00:16:28\] Claude Code writes 80% of Claude Code
- \[00:18:01\] Custom Slash Commands and MCP Integration
- \[00:21:08\] Terminal UX and Technical Stack
- \[00:27:11\] Code Review and Semantic Linting
- \[00:28:33\] Non-Interactive Mode and Automation
- \[00:36:09\] Engineering Productivity Metrics
- \[00:37:47\] Balancing Feature Creation and Maintenance
- \[00:41:59\] Memory and the Future of Context
- \[00:50:10\] Sandboxing, Branching, and Agent Planning
- \[01:01:43\] Future roadmap
- \[01:11:00\] Why Anthropic Excels at Developer Tools

## Transcript

**Alessio** \[00:00:04\]: Hey everyone, welcome to the Latent Space podcast. This is Alessio, partner and CTO at Decibel, and I'm joined by my co-host Swyx, founder of SmolAI.

**Swyx** \[00:00:12\]: Hey, and today we're in the studio with Cat Wu and Boris Cherny. Welcome. Thanks for having us.

**Cat** \[00:00:17\]: Thank you.

**Swyx** \[00:00:18\]: Cat, you and I know each other from before. I just realized Dagster as well. Yeah. And then Index Ventures and now Anthropic. It's so cool to see a friend that you know from before now working at Anthropic and shipping really cool stuff. And Boris, you're a celebrity because we were just having you outside, just getting coffee, and people recognize you from your video. Wasn't that neat?

**Boris** \[00:00:43\]: Yeah, I definitely had that experience like once or twice in the last few weeks. It was surprising.

## What is Claude Code?

**Swyx** \[00:00:48\]: Yeah. Well, thank you for making the time. We're here to talk about Claude Code. Most people probably have heard of it. We think quite a few people have tried it.

**Boris** \[00:00:56\]: But let's get a crisp, upfront definition. What is Claude Code? Yeah. So Claude Code is... What is Claude in the terminal? So, you know, Claude has a bunch of different interfaces. There is desktop, there's web, and yeah, Claude Code, it runs in your terminal. Because it runs in the terminal, it has access to a bunch of stuff that you just don't get if you're running on the web or on desktop or whatever. So it can run bash commands, it can see all of the files in the current directory, and it does all that agentically. And, yeah, I guess maybe it comes back to, like, maybe the question under the question is, like, you know, where did this idea come from? And, yeah, part of it was, we just want to learn how Claude, we want to learn how people use agents. We are doing this with the CLI form factor, because coding is kind of a natural place where people use agents today. And, you know, there's kind of product market fit for this thing. But, yeah, it's just sort of this crazy research project. And obviously, it's kind of bare bones and simple. But, yeah, it's like an agent in your terminal. That's how the best stuff starts.

**Alessio** \[00:01:59\]: Yeah. How did it start? Did you have a master plan? Did you have a master plan to build Claude Code?

**Boris** \[00:02:04\]: There was no master plan. When I joined Anthropic, I was experimenting with different ways to use the model kind of in different places. And the way I was doing that was through the public API, the same API that everyone else has access to. And one of the really weird experiments was this quad that runs in a terminal. And I was using it for kind of weird stuff. I was using it to, like, look at what music I was listening to and react to that. And then, you know, like, screenshot my, you know, video player and explain. Like, what's happening there and things like this. And this was, like, kind of a pretty quick thing to build. And it was pretty fun to play around with. And then at some point, I gave it access to the terminal and the ability to code. And suddenly, it just felt very useful. Like, I was using this thing every day. It kind of expanded from there. We gave the core team access, and they all started using it every day, which was pretty surprising. And then we gave all the engineers and researchers at Anthropic access. And pretty soon, everyone was... I was using it every day. And I remember we had this DAU chart for internal users. And I was just watching it, and it was vertical, like, for days. And we're like, all right, there's something here. We got to give this to external people so everyone else can try this, too.

**Alessio** \[00:03:17\]: Yeah.

**Boris** \[00:03:18\]: Yeah, that's where it came from.

**Alessio** \[00:03:19\]: And were you also working with Boris already? Or did this come out, and then it started growing? And then you're like, okay, we need to maybe make this a team, so to speak.

**Cat** \[00:03:28\]: Yeah, the original team was Boris, Sid. And Ben. And over time, as more people were adopting the tool, we felt like, okay, we really have to invest in supporting it, because all our researchers are using it. And this is, like, our one lever to make them really productive. And so at that point, I was using QuadCode to build some visualizations. I was analyzing a bunch of data, and sometimes it's super useful to, like, spin up a streamlet and, like, see all the aggregate stats at once. And QuadCode made it really, really easy to do. So I think I sent Boris, like, a bunch. at some point, Boris was like, do you want to just work on this? And so that's how it happened.

**Boris** \[00:04:07\]: It was actually a little, like, it was more than that on my side. You were sending all this feedback, and at the same time, we were looking for a PM. And we were, like, looking at a few people. And then I remember telling the manager, like, hey, I want Cat. Aww.

**Alessio** \[00:04:19\]: I'm sure people are curious. What's the process within Anthropic to, like, graduate one of these projects? Like, so you have kind of, like, a lot of growth. Then you get a PM. When did you decide, okay, we should, like, it's ready to go? It'll be opened up.

## Anthropic’s Product Philosophy

**Boris** \[00:04:32\]: Generally, at Anthropic, we have this product principle of do the simple thing first. And I think that the way we build product is really based on that principle. So you kind of staff things as little as you can and keep things as scrappy as you can because the constraints are actually pretty helpful. And for this case, we wanted to see some signs of product market fit before we scaled it.

**Swyx** \[00:04:51\]: Yeah, I imagine. So, like, we're putting out the MCP episode this week. And I imagine MCP also now has a team around it in much the same way. Hmm. It is now very much officially, like, sort of, like, an Anthropic product. So I'm kind of curious for Cat, like, how do you view PMing something like this? Like, what is, I guess, you're, like, sort of grooming the roadmap. You're listening to users. And the velocity is something I've never seen coming out of Anthropic.

**Cat** \[00:05:16\]: I think I PM with a pretty light touch. I think Boris and the team are, like, extremely strong product thinkers. And for the vast majority of the features on our roadmap, it's actually just, like, people who have a lot of experience. People building the thing that they wish that the product had. So very little actually is tops down. I feel like I'm mainly there to, like, clear the path if anything gets in the way and just make sure that we're all good to go from, like, a legal marketing, et cetera, perspective. Yeah. And then I think, like, in terms of very broad roadmap or, like, long-term roadmap, I think the whole team comes together and just thinks about, okay, what do we think models will be really good at in three months? And, like, let's just make sure that what we're building is really consistent. Yeah. Like, what do we think is really compatible with, like, the future of what models are capable of?

**Swyx** \[00:06:01\]: I'd be interested to double-click on this. What will models be good at in three months? Because I think that's something that people always say to think about when building AI products. But nobody knows how to think about it because it's, everyone's just, like, it's generically getting better all the time. We're getting AGI soon, so don't bother. You know, like, how do you calibrate three months of progress?

**Cat** \[00:06:20\]: I think if you look back historically, we tend to ship models every couple of months or so. So three months is just, like, an arbitrary number. I think the direction that we want our models to go in is being able to accomplish more and more complex tasks with as much autonomy as possible. And so this includes things like making sure the models are able to explore and find the right information that they need to accomplish a task, making sure that models are thorough in accomplishing every aspect of a task, making sure the models can, like, compose different tools together effectively. Yeah. These are the directions we care about. Yeah.

**Boris** \[00:06:57\]: I guess coming back to code, this kind of approach affected the way that we built code also because we know that if we want some product that has, like, very broad a product market fit today, we would build, you know, a cursor or a wind serve or something like this. Like, these are awesome products that so many people use every day. I use them. That's not the product that we want to build. We want to build something that's kind of much earlier on that curve and something that will maybe be a big product, you know, a year from now or, you know, however much time from now. As the model improves. And that's why code runs in a terminal. It's a lot more bare bones. You have raw access to the model because we didn't spend time building all this kind of nice UI and scaffolding on top of it.

## What should go into Claude Code?

**Alessio** \[00:07:38\]: When it comes to, like, the harness, so to speak, and things you want to put around it, there's one that may be prompt optimization. So obviously I use Cursor every day. There's a lot going on in Cursor that is beyond my prompt for, like, optimization and whatnot. But I know you recently released, like, you know, compacting context features and all that. How do you decide how thick it needs to be on top of the CLI? So that's kind of the share interface. And at what point are you deciding between, okay, this should be a part of clock code versus this is just something for the IDE people to figure out, for example?

**Boris** \[00:08:10\]: Yeah, there's kind of three layers at which we can build something. So the, you know, being an AI company, the most natural way to build anything is to just build it into the model and have the model do the behavior. The next layer is probably scaffolding on top, so it's like quad code itself. And then the layer after that is using quad code as a tool in a broader workflow, so to compose stuff in. You know, so for example, a lot of people use code with, you know, Tmux, for example, to manage a bunch of windows and a bunch of sessions happening in parallel. We don't need to build all of that in.

**Boris** \[00:08:42\]: Compact, it's sort of this thing that kind of has to live in the middle because it's something that we want to work when you use code. You shouldn't have to pull in extra tools on top of it. And rewriting memory in this way isn't something the model can do today. So you have to use a tool for it. And so it kind of has to live in that middle area. We tried a bunch of different options for compacting, you know, like rewriting old tool calls and truncating old messages and not new messages. And then in the end, we actually just did the simplest thing, which is ask Claude to summarize the, you know, the previous messages and just return that and that's it. And it's funny when the model is so good, the simple thing usually works. You don't have to over-engineer it. We do that for Claude who plays Pokemon too.

**Swyx** \[00:09:23\]: Just kind of interesting to see that. Yeah. It's like pattern re-emerging.

## Claude.md and Memory Simplification

**Alessio** \[00:09:26\]: And then you have the Claude.md file for the more user-driven memories, so to speak. It's like kind of like the equivalent of maybe cursor rules, I would say.

**Boris** \[00:09:36\]: Yeah. And ClaudeMD, it's another example of this idea of, you know, do the simple thing first. We had all these crazy ideas about like memory architectures and, you know, there's so much literature about this. There's so many different external products about this and we wanted to be inspired by all this stuff. But in the end, the thing we did is ship the simplest thing, which is, you know, it's a file that has some stuff. And it's auto-read into context. And there's now a few versions of this file. You can put it in the root, or you can put it in child directories, or you can put it in your home directory. And we'll read all of these in kind of different ways. But yeah, it's the simplest thing that could work.

## Claude Code vs Other Coding Tools

**Swyx** \[00:10:07\]: I think like people are interested in comparing and contrasting, obviously, because to you, obviously, this is the house tool. You work on it. People are interested in like figuring out how to choose between tools. There's the cursors of the world. There's like the devins of the world. There's aiders and there's ClaudeCode. And, you know, there's a lot of stuff. We can't try everything all at once. My question would be, where do you place it in the universe of options? Well, you can ask Claude to just try all these tools.

**Swyx** \[00:10:36\]: No self-favoring at all.

**Boris** \[00:10:39\]: Claude plays engineer. I don't know. We use all these tools in-house, too. We're big fans of all this stuff. Like ClaudeCode is, obviously, it's a little different than some of these other tools in that it's a lot more raw. Mm-hmm. Like I said, there isn't this kind of big, beautiful UI on top of it. It's raw access to the model. It's as raw as I get. So if you want to use a power tool that lets you access the model directly and use Claude for automating, you know, big workloads, you know, for example, if you have like a thousand Lint violations and you want to start a thousand instances of Claude and have it fix each one and then make a PR, then ClaudeCode is a pretty good tool. Got it. It's a tool for power workloads for power users. And I think that's just kind of where it fits. Yeah.

## Parallel Workflows and Unix Utility Philosophy

**Alessio** \[00:11:23\]: It's the idea of like parallel versus kind of like single path, one way to think about it, where like the IDE is really focused on like what you want to do versus like ClaudeCode. You kind of more see it as like less supervision required. You can kind of spin up a lot of them. Is that the right mental model?

**Boris** \[00:11:40\]: Yeah. And there's some people at Anthropic that have been racking up like thousands of dollars a day with this kind of automation. Most people don't do anything like that, but you totally could do something like that. Yeah. We think of it as like a Unix utility. Mm-hmm. Right? So it's like the same way that you would compose, you know, grep or cat or, oh, cat. Or something like this. Nice. The same way you can compose code into workflows.

**Alessio** \[00:12:03\]: The cost thing is interesting. Do people pay internally or do you get free? If you work at Anthropic, you can just run this thing as much as you want every day? It's for free internally. Nice. Yeah. I think if everybody had it for free, it would be huge.

**Alessio** \[00:12:20\]: Because like, I mean, if I think about, I pay Coursera. I use millions and millions of tokens in Coursera. That would cost me a lot more in Claude Code. And so I think like a lot of people that I've talked to, they don't actually understand how much it costs to do these things. And they'll do a task and they're like, oh, that costs 20 cents. I can't believe I paid that much. How do you think, going back to like the product side too, is like, how much do you think of that being your responsibility to try and make it more efficient versus that's not really what we're trying to do with the tool?

## Cost considerations and pricing model

**Cat** \[00:12:51\]: We really see Claude Code as like the tool that gives you the smartest abilities out of the model. We do care about cost insofar as it's very correlated with latency. And we want to make sure that this tool is extremely snappy to use and extremely thorough in its work. We want to be very intentional about all the tokens that it produces. I think we can do more to like communicate the cost with users. Currently, we're seeing costs around like $6 per day. per active user. And so it's like, it does come out to a bit higher over the course of a month in Cursor. But I don't think it's like out of band. And that's like roughly how we're thinking about it.

**Boris** \[00:13:36\]: I would add that I think the way I think about it is it's an ROI question. It's not a cost question. And so if you think about, you know, an average engineer salary and like what, you know, we were talking about this before the podcast. Like, engineers are very expensive. And if you can make an engineer 50, 70% more productive, that's worth a lot. And I think that's the way to think about it.

**Swyx** \[00:13:58\]: So if you're saying, if you're targeting Claude to be the most powerful end of the spectrum, as opposed to the less powerful, but faster, cheaper side of the spectrum, then there's typically people who recommend a waterfall, right? You try this faster, simple one. That doesn't work. You upgrade, you upgrade, you upgrade. And finally you hit Claude Code, at least for people who are token constrained that don't work at Ntopic. And part of me wants to just fast track all of that. I just want to fan out to everything all at once. And once I, once I'm not satisfied with the next one solution, I'll just sort of switch to the next. I don't know if that's real.

**Boris** \[00:14:32\]: Yeah, we're, we're definitely trying to make it a little easier to make Claude Code kind of the tool that you use for all the different workloads. So for example, we launched thinking recently. So for any kind of planning workload where you might've used other tools before you can just ask what, and that'll use, you know, chain of thought. To, to think stuff out. I think we'll get there.

## Key Features Shipped Since Launch

**Swyx** \[00:14:51\]: Maybe we'll do it this way. How about we recap like sort of the brief history of Claude Code, like between when you launched and now there, there've been quite a few ships. How would you highlight the major ones? And then we'll get to the thinking tool.

**Boris** \[00:15:04\]: And I think I'd have to like check your Twitter to remember.

**Cat** \[00:15:09\]: I think a big one that we've gotten a lot of requests for is web fetch. Yep. So we worked really closely with our legal team to make sure that, you know, the code that we shipped as secure of an implementation as possible. So we'll web fetch if a user directly provides an URL, whether that's in their call.md or in their message directly, or if a URL is mentioned in one of the previously fetched URLs. And so this way enterprises can feel pretty secure about letting their developers continue to use it. We shipped a bunch of like auto features, like autocomplete, where you can, you know, press tab to complete a file name or file path. Autocompact so that users feel like they have like infinite context since we'll compact behind the scenes. And we also shipped auto accept because we noticed that a lot of users were like, hey, like Claude Code can figure it out. I've like developed a lot of trust for Claude Code. I wanted to just like autonomously edit my files, run tests, and then come back to me later. So those are some of the big ones.

**Swyx** \[00:16:15\]: Vim mode, custom slash commands.

**Cat** \[00:16:18\]: People love Vim mode. Yeah. So that was a, that was a top request too. That one went pretty viral. Yeah.

**Boris** \[00:16:24\]: Yeah. Memory. Those are recent ones. Like the hashtag to remember.

## Claude Code writes 80% of Claude Code

**Swyx** \[00:16:28\]: So yeah. I mean, I'd love to dive into, you know, on the technical side, any of them that was particularly challenging. Paul from AIDR always says how much of it was coded by AIDR, you know? So then the question is how much of it was coded by Claude Code? Obviously there's some percentage, but I wonder if you have a number. Like 50? 80? It's pretty high. Probably near 80 I'd say. Yeah. Yeah.

**Boris** \[00:16:48\]: It's very high.

**Cat** \[00:16:49\]: Yeah. That makes sense. It's a lot of human code review though.

**Boris** \[00:16:52\]: Yeah. What a, what a human code review. I think some of the stuff has to be handwritten and some of the code can be written by quad. And there's sort of a wisdom in knowing which one to pick and what percent for each kind of task. So usually where we start is quad writes the code. And then if it's not good, then maybe a human will dive in. There's also some stuff where like I actually prefer to do it by hand. So it's like, you know, intricate data model refactoring or something. I won't leave it to quad because I have really strong opinions and it's easier to just do it and experiment than it is to explain it to quad. So yeah, I think that nets out to maybe like 80, 90% quad written code overall. Yeah.

**Alessio** \[00:17:28\]: We're hearing a lot of that in our portfolio companies, like more like series A companies is like 80, 85% of the code they write is ad generated. Yeah. Yeah. Well, that's a whole different discussion. The custom slash command. I had a question. How do you think about custom slash command MCPs? Like how does this all tie together? You know, is the slash command and clock code kind of like an extension of the MCP? Are people building things that should not be MCP, but are just kind of like self-contained things in there? How should people think about it?

## Custom Slash Commands and Integration with MCP

**Boris** \[00:18:01\]: Yeah. I mean, obviously we're big fans of MCP. You can use MCP to do a lot of different things. You can use it for custom tools and custom commands and all this stuff. But at the same time, you shouldn't have to use it. So if you just want something really simple and local, you just want, you know, some essentially like prompt that's been saved, just use local commands for that. Over time, something that we've been thinking a lot about is how to re-expose things in convenient ways. So for example, let's say you had this local command. Could you re-expose that as an MCP prompt? Yeah. Because clock code is an MCP client and an MCP server. Or similarly, let's say you pass in a custom, you know, like a custom bash tool. Is there a way to re-expose that? Re-expose that as an MCP tool? Yeah. We think generally you shouldn't have to be tied to a particular technology. You should use whatever works for you. Yeah.

**Alessio** \[00:18:48\]: Because there's some like Puppeteer. I think that's like a great way, great thing to use a clock code, right? For testing. There's like a Puppeteer MCP protocol, but then people can also write their own slash commands. And I'm curious, like where MCP are going to end up being, where it's like maybe each slash command leverages MCPs, but no command itself is an MCP because it ends up being customized. I think that's what people are still trying to figure out. It's like, should this be in the runtime or in the MCP server? I think people haven't quite figured out where the line is.

**Boris** \[00:19:20\]: Yeah. For something like Puppeteer, I think that probably belongs in MCP because there's a few like tool calls that go in that too. And so it's probably nice to encapsulate that in the MCP server.

**Cat** \[00:19:30\]: Whereas slash commands are actually just like prompts. So they're not actually tools. We're thinking about how to expose more customizability options so that people can use them. People can bring their own tools or turn off some of the tools that quad code comes with. But there's also some trickiness there because we want to just make sure that the tools people bring are things that quad is able to understand and that people don't accidentally inhibit their experience by maybe bringing a tool that is like confusing to quad. So we're just trying to work through the UX of it.

**Boris** \[00:20:05\]: Yeah. I'll give an example also of how this stuff connects. For quad code internally in the GitHub repo, we have this GitHub action that runs. And the GitHub action invokes quad code with a local slash command. And the slash command is lint. So it just runs a linter using quad. And it's a bunch of things that are pretty tricky to do with a traditional linter that's based on static analysis. So for example, it'll check for spelling mistakes, but also it checks that code matches comments. It also checks that, you know, we use a particular library for, you know, a specific command. So it checks for network fetches instead of the built-in library. There's a bunch of these specific things that we check that are pretty difficult to express just with lint. And in theory, you can go in and, you know, write a bunch of lint rules for this. Some of it you could cover, some of it you probably couldn't. But honestly, it's much easier to just write a one bullet in Markdown in a local command and just commit that. And so what we do is quad runs through the GitHub action. We invoke it with slash project colon lint. So which just invokes that local command. It'll run the linter. It'll identify any mistakes. It'll make the code changes. And then it'll use the GitHub MCP server in order to commit the changes back to the PR. And so you can kind of compose these tools together. And I think that's a lot of the way we think about code is just one tool in an ecosystem that composes nicely without being opinionated about any particular piece.

**Swyx** \[00:21:27\]: It's interesting. I have a weird chapter in my CV that makes me, I was the CLI maintainer for Nellify. And so I have a little bit of a dive. There's a decompilation of Claude Code out there that has since been taken down. But it seems like you use CommanderJS and React Inc is like the public info about this. And I'm just kind of curious, like at some point you're just, you're not even building Claude Code. You're kind of just building a general purpose CLI framework that anyone, any developer can hack to their purposes. You ever think about this? Like this level of configurability is more of like a CLI framework. Or like some new form factor that doesn't exist before.

**Boris** \[00:22:09\]: Yeah. It's definitely been fun to hack on a really awesome CLI because there's not that many of them. Yeah. But yeah, we're big fans of Ink. Yeah.

**Swyx** \[00:22:17\]: Vadim Demede. So we actually used him, used React Inc for a lot of our projects.

**Boris** \[00:22:22\]: Oh, cool. Yeah.

**Swyx** \[00:22:23\]: Yeah.

**Boris** \[00:22:24\]: Ink is amazing. It's like, it's sort of hacky and janky in a lot of ways. It's like you have React and then the renderer is just translating the React code to like ANSI language. Yeah. That's the way to render. And there's all sorts of stuff that just doesn't work at all because ANSI escape codes are like, you know, it's like this thing that started to be written like the 1970s. And there's no really great spec about it. Every terminal is a little different. So building in this way, it feels to me a little bit like building for the browser back in the day where you had to think about like Internet Explorer 6 versus Opera versus like Firefox and whatever. Like you have to think about these cross-terminal differences a lot. Yeah. So yeah, big fans of Ink because it helps abstract over that. We're also, we use Bun. So big fans of Bun. That's been, it makes writing our tests and running tests much faster. We don't use it in the runtime yet.

**Swyx** \[00:23:13\]: It's not just for speed, but you tell me, I don't want to put words in your mouth, but my impression is they help you ship the compilation, the executable. Yeah, exactly.

**Boris** \[00:23:21\]: So we use Bun to compile the code together. Yeah.

**Swyx** \[00:23:24\]: Any other pluses of Bun? I just want to track Bun versus Deno conversations. Yeah. Deno's in there. Yeah.

**Boris** \[00:23:33\]: I actually haven't used Deno back. It's been a while. Yeah. I remember Ryan.

**Swyx** \[00:23:37\]: That's what a lot of people say. Yeah. Yeah.

**Boris** \[00:23:39\]: Ryan made it back in the day and it was like, there were some ideas that I think were very cool in it, but yeah, it just never took off to that same degree. Yeah. Still a lot of cool ideas. Like being able to NPM, just import from any URL, I think is pretty amazing.

**Swyx** \[00:23:51\]: That's the dream of ESM. I was going to ask you one other feature, then we can get to the thinking tool of AutoAccept. I have this little thing I'm trying to do. I'm trying to develop thinking around for trust in agents, right? When do you say, all right, go autonomous? When do you pull the developer in? And sometimes you let the model decide. Sometimes you're like, this is a destructive action, always ask me. And I'm just curious if you have any internal heuristics around when to AutoAccept and where all this is going.

**Cat** \[00:24:25\]: We're spending a lot of time building out the permission system. So Robert on our team is leading out this work. We think it's really important to give developers the control to say, hey, these are like the allowed permissions. Generally, this includes stuff like the model's always allowed to read files or read anything. And then it's up to the user to say, hey, it's about to edit files, it's about to run tests. These are like probably the safest three actions. And then there's like a long list of other actions that users can either allow list or deny list based on regex matches with the action.

**Alessio** \[00:24:59\]: How good is that? Is writing a file ever be unsafe if you have version control? I think that's.

**Boris** \[00:25:04\]: Yeah, I think it's I think there's like a few different probably like aspects of safety to think about. So it could be useful just to break that out a little bit. So for file editing, it's actually less, I think, about safety, although there is still a safety risk. Because what might happen is, let's say the model fetches a URL and then there's a prompt injection attack in the URL. And then the model writes malicious code to disk and you don't realize it. Although, you know, there is code review as like a separate thing. Kind of where there is as protection. But I think generally for file rights, the model might just do the wrong thing. That's the biggest thing. And what we find is that if the model is doing something wrong, it's better to identify that earlier and correct it earlier. And then you're going to have a better time. If you wait for the model to just go down this like totally wrong path and then correct it 10 minutes later, you're going to have a bad time. So it's better to usually identify failures early. But at the same time, there's some cases where you just want to let the model go. So, for example, if Claude Code is. You know, it's writing tests for me. I'll just hit shift tab. Enter auto accept mode and just let it run the tests and iterate on the tests until they pass. Because I know that's a pretty safe thing to do. And then for some other tools like bash tool, it's pretty different. Because quad could run, you know, rm, rf, slash. And that would suck. That's not a good thing. So we definitely want people to be in the loop to catch stuff like that. The model is, you know, trained and aligned to not do that. But, you know, these are non-deterministic systems. So, like, you still want a human in the loop. I think that generally the way that things are trending is kind of less time between human input. Did you see the meter paper?

**Swyx** \[00:26:43\]: No. They established a Moore's law for time between human input, basically. And it's basically doubling every three to seven months is the idea. And Anthropic is currently doing super well on that benchmark. It's roughly about autonomous for 15 minutes. And it's at the 50th percentile of human effort, which is kind of cool. Highly recommend that.

**Alessio** \[00:27:04\]: I put cursor in YOLO mode all the time and just run it.

**Swyx** \[00:27:08\]: But it's fine. Which is vibe coding, right? Yeah.

## Code Review and Semantic Linting

**Alessio** \[00:27:11\]: And there's a couple of things that are interesting when you talked about alignment and the model being trained. So I always put it in a Docker container. And I have a prefix every command with, like, the Docker compose. And yesterday, my Docker server was not started. And I was like, oh, Docker is not running. Let me just run it outside of Docker. And I'm like, whoa, whoa, whoa, whoa, whoa. You should start Docker and run it in Docker. You can now go outside. That is, like, a very good example of, like, you know, sometimes you think it's doing something and then it's doing something else. And for the review side, I would love to just chat about that more. I think the linter part that you mentioned, I think maybe people skipped it over. It doesn't register the first time. But, like, going from, like, rule-based linting to, like, semantic linting, I think it's, like, great and super important. And I think a lot of companies are trying to do how do you do autonomous PR review, which I've not seen one that I use so far. They're all kind of, like, mid. So I'm curious how you think about closing the loop or making that better and figuring out especially, like, what are you supposed to review? Because these PRs get pretty big when you buy code. You know, sometimes I'm like, oh, wow. Oh, GTM. You know, it's like, am I really supposed to read all of this? It kind of seems, most of it seems pretty standard. But, like, I'm sure there are parts in there that the model wants. I would understand that are, like, kind of out of distribution, so to speak, to really look at. So, yeah, that's a very open-ended question. But any thoughts you have would be great.

## Non-Interactive Mode and Automation Use Cases

**Boris** \[00:28:33\]: The way we're thinking about it is quad code is, like I said before, it's a primitive. So if you want to use it to build a code review tool, you can do this. If you want to, you know, build, like, a security scanning, vulnerability scanning tool, you can do that. If you want to build a semantic linter, you can do that. And hopefully with code, it makes it so if you want to do this, it's just a few lines of code. And you can just have quad write that code also. Because quad is really great at writing GitHub actions.

**Cat** \[00:28:58\]: Yeah, one thing to mention is we do have a non-interactive mode, which is, like, what quad uses in these, or how we use quad in these situations to automate quad code. And also a lot of our, the companies using quad code actually use this non-interactive mode. So they'll, for example, say, hey, I have, like, hundreds of thousands of tests in my repo. Some of them are out of date. Some of them are flaky. And they'll send quad code. So they'll send quad code to look at each of these tests and decide, okay, how can I update any of them? Like, should I deprecate some of them? How do I, like, increase our code coverage? So that's been a really cool way that people are non-interactively using quad code.

**Swyx** \[00:29:38\]: What are the best practices here? Because when it's non-interactive, it could run forever. And you're not necessarily reviewing the output of everything, right? So I'm just kind of curious, how is it different in non-interactive mode? What are, like, the most important hyperparameters or arguments to solve?

**Boris** \[00:29:55\]: Yeah, and for folks that haven't used it, so non-interactive mode is just quad dash p. And then you pass in the prompting quotes, and that's all it is. It's just the dash p flag. Generally, it's best for tests that are read-only. That's the place where it works really well. And you don't, you know, super have to think about permissions and running forever and things like that. So, for example, a linter that runs and doesn't fix any issues. Or, for example, we're working on a thing where we use quad with dash p to generate the change log for quad. So every PR is just looking over the commit history. And being like, okay, this makes it into the change log, this doesn't. Because we know people have been requesting change logs, so we're just getting quad to build it. So generally, non-interactive mode, really good for read-only tests. For tests where you want to write, the thing we usually recommend is passing a very specific set of permissions on the command line. So what you can do is pass in dash dash allow tools. And then you can allow a specific tool. So, for example, not just bash, but, for example, git status. Or git diff. So you just give it a set of tools that it can use.

**Swyx** \[00:30:57\]: Or, you know, edit tool, for example. It still has default tools like file read, grep, system tools like bash and ls, and memory tools.

**Boris** \[00:31:04\]: So it still has all these tools, but allow tools just lets you, instead of the permission prompt, because you don't have that in the non-interactive mode. It's just kind of pre-accepting.

**Cat** \[00:31:15\]: And we'd also definitely recommend that you start small. So, like, test it on one test. Make sure that it has reasonable behavior. Iterate on your prompt. Then scale it up to 10. Make sure that it succeeds. Or if it fails, just, like, analyze what the patterns of failures are. And gradually scale up from there. So definitely don't kick off a run to fix, like, 100,000 tests. Yeah.

**Swyx** \[00:31:36\]: I think the... So at this point, I just, you know, I want to... This tagline is in my head that basically at Anthropic, there's Claude Code generating code. And then Claude Code also reviewing its own code. Like, at some point, right? Like, different people are setting all this up. You don't really govern that. But it's happening.

**Boris** \[00:31:53\]: Yeah, we have to be, you know, at Anthropic, there's still a human in the loop for reviewing. And I think for, you know, for ASL, this is important. So, like, for general, like, model alignment and safety.

**Swyx** \[00:32:02\]: What's ASO?

**Boris** \[00:32:03\]: Oh, so ASL, this is, like, the kind of the safety levels.

**Swyx** \[00:32:07\]: Yeah, right, right.

**Boris** \[00:32:08\]: What does it stand for?

**Cat** \[00:32:09\]: Autonomous safety level. Autonomous.

**Boris** \[00:32:12\]: Essentially, like, it's like a...

**Swyx** \[00:32:13\]: Sorry, I'm not used to the acronyms. We have a lot of these. But you've published stuff. I know. I just don't know what they're called internally. Yeah. But the point of the thing I was thinking about was we have, you know, VPs of N, CTOs listening. Like, this is all well and good for the individual developer. But the people who are responsible for the tech, the entire code base, the engineering decisions, all this is going on. My developers, like, I manage, like, 100 developers. Any of them could be doing any of this at this point. What do I do to manage this? How does my code review process change? How does my change management change? I don't know.

**Cat** \[00:32:48\]: We've talked to a lot of VPs and CTOs. Yeah. They're really excited about it. They actually tend to be quite excited because they experiment with the tool. They download it. They ask it a few questions. And, like, Claude Code, when it gives them sensible answers, they're really excited because they're like, oh, I can understand this nuance in the code base. And sometimes they even ship small features with Claude Code. And I think through that process of, like, interacting with the tool, they build a lot of trust in it. And a lot of folks actually come to us and they ask us, like, how can I roll it out more broadly? And then we'll often, like, have sessions with, like, VPs of Dev Prod and talk about these concerns around how do we make sure people are writing high-quality code. I think in general, it's still very much up to the individual developer to hold themselves up to a very high standard for the quality of code that they merge. Even if we use Claude Code to write a lot of our code, it's still up to the individual who merges it to be responsible for, like, this being well-maintained, well-documented code that has, like, reasonable abstractions. And so I think that's something that will continue to happen where Claude Code isn't its own engineer that's, like, committing code by itself. It's still very much up to the ICs to be responsible for the code that's produced. Yeah.

**Boris** \[00:34:06\]: I think Claude Code also makes a lot of this stuff, a lot of quality work becomes a lot easier. So, for example, like, I have not manually written a unit test in many months.

**Cat** \[00:34:15\]: And we have a lot of unit tests. We have a lot of unit tests.

**Boris** \[00:34:17\]: And it's because Claude writes all the tests. And, you know, before, I felt like a jerk if on someone's PR, I'm like, hey, can you write a test? Because, you know, they kind of know they want to… For code coverage? Is that still relevant? For code coverage, yeah. Okay. And, you know, they kind of know they should probably write a test and that's probably the right thing to do. And somewhere in their head, they make that trade-off where they just want to ship faster. And so you always kind of feel like a jerk for asking. But now I always ask because Claude can just write the test. Right. And, you know, there's no human work. You just ask Claude to do it and it writes it. And I think with writing tests becoming easier and with the writing lint rules becoming easier, it's actually much easier to have high-quality code than it was before.

**Swyx** \[00:34:56\]: What are the metrics that you believe in? Like, is it… A lot of people actually don't believe in 100% code coverage. Because sometimes that is kind of optimizing for the wrong thing. Arguably, I don't know. But like, obviously, you have a lot of experience in different code quality metrics. But what still makes sense?

**Boris** \[00:35:11\]: I think it's very engineering team dependent, honestly. I wish there was a one-size-fits-all answer. Yeah. Just give me the one solution. For some teams, test coverage is extremely important. For other teams, type coverage is very important. Especially if you're working in, you know, very strictly typed language. And, you know, for example, avoiding, like, NEs and JavaScript and Python. Yep. I think cyclomatic complexity kind of gets a lot of flack. But it's still, honestly, a pretty good metric just because there isn't anything better in terms of ways to measure. Yeah. For code quality. Okay.

**Swyx** \[00:35:43\]: And then productivity is obviously not lines of code. But do you care about measuring productivity? I'm sure you do.

**Boris** \[00:35:50\]: Yeah. You know, lines of code, honestly, isn't terrible. Oh, God. It has downsides. Yeah. It's terrible. Well, lines of code is terrible for a lot of reasons. Yes. But it's really hard to make anything better. It's the least terrible. It's the least terrible. There's, like, lines of code, maybe, like, number of PRs. How green your GitHub is. Yeah.

## Engineering Productivity Metrics

**Cat** \[00:36:09\]: Yeah. The two that we're really trying to nail down are, one, decrease in cycle time. So how much faster are your features shipping because you're using these tools? So that might be something like the time between first commit and when your PR is merged. It's very tricky to get right, but one of the ones that we're targeting. The other one that we want to measure more rigorously is, like, the number of features that you wouldn't have otherwise built. Hmm. We have a lot of channels where we get customer feedback. And one of the patterns that we've seen with Claude Code is that sometimes customer support or customer success will, like, post, hey, like, this app has, like, this bug. And then sometimes 10 minutes later, one of the engineers on that team will be, like, Claude Code made a fix for it. And a lot of those situations when you, like, ping them and you're, like, hey, that was really cool, they were, like, yeah, without Claude Code, I probably wouldn't have done that because it would have been too long. It would have been too much of a divergence from what I was otherwise going to do. It would have just ended up in this long backlog. So this is the kind of stuff that we really want to measure more rigorously.

**Boris** \[00:37:14\]: That was the other AGI-appealed moment for me. There was a really early version of Claude Code many, many months ago. And this one engineer at Anthropic, Jeremy, built a bot that looked through a particular feedback channel on Slack. And he hooked it up to code to have code automatically put up PRs with just fixes to all this stuff. And some of this stuff, you know, it didn't fix every issue. But it fixed a lot of the issues. You say, like, 10%, 50%? You know, this was, like, early on, so I don't remember the number. But it was surprisingly high to the point where I became a believer in this kind of workflow. And I wasn't before.

## Balancing Feature Creation and Maintenance

**Alessio** \[00:37:47\]: SAPM isn't that scary, too, in a way? Where you can build too many things, it's almost like maybe you shouldn't build that many things. I think that's what I'm struggling with the most. It's, like, it gives you the ability to create, create, create. But then at some point, you've got to support, support, support.

**Swyx** \[00:38:02\]: This is the Jurassic Park, like, your scientist is so preoccupied with what you're doing. Yeah, exactly.

**Alessio** \[00:38:06\]: I don't know if we should. Yeah. How do you make decisions? Like, now that the cost of actually implementing the thing is going down as a PM, how do you decide what is actually worth doing?

**Cat** \[00:38:15\]: Yeah, we definitely still hold a very high bar for net new features. Most of the fixes were, like, hey, this functionality is broken or this, like, there's a weird edge case that we hadn't addressed yet. So it was very much, like, smoothing out the rough edges as opposed to building something completely net new. For net new features, I think we hold a pretty high bar. High bar that it's very intuitive to use. The new user experience is, like, minimal. It's just, like, obvious that it works. We sometimes actually use Claude Code to prototype instead of using docs. Yeah, so you'll have, like, prototypes that you can play around with. And that often gives us a faster feel for, hey, is this feature ready yet? Or, like, is this the right abstraction? Is this the right interaction pattern? So it gets us faster to feeling really confident about a feature. But it doesn't circumvent the process of us making sure that the feature definitely fits in, like, the product vision.

**Boris** \[00:39:12\]: It's interesting how as it gets easier to build stuff, it changes the way that I write software. Where, like Cat's saying, like, before I would write a big design doc. And I would think about a problem for a long time before I would build it sometimes for some set of problems. And now I'll just ask Claude Code to prototype, like, three versions of it. And I'll try the feature and see which one I like better. And then that informs me much better and much faster than a doc would have. And I think we haven't totally internalized that transition yet in the industry.

**Alessio** \[00:39:41\]: Yeah, I feel the same way for some tools I build internally. People ask me, could we do this? And I'm like, I'll just, yeah, just build it. It's like, well, it feels pretty good. We should, like, polish it, you know? Or sometimes it's like, no, that's not.

**Swyx** \[00:39:57\]: It's comforting that, you know, like, your max cost is, I mean, even at Anthropic where it's theoretically unlimited. Yeah. The cost is roughly $6 a day. That gives people peace of mind. Because I'm like, $6 a day? Fine. $600 a day, we have to talk.

**Alessio** \[00:40:12\]: Like, you know. Yeah. I paid $200 a month to make Studio Ghibli photos. So it's all good. That is totally worth it.

**Cat** \[00:40:19\]: You mentioned internal tools. And that's actually a really big use case that we're seeing emerge. Because a lot of times, if you're working on something operationally intensive, if you can spin up an internal dashboard for it. Or, like, an operational tool where you can, for example, grant access to a thousand emails at once. A lot of these things, you don't really need to have, like, a super polished design. You kind of just need something that works. And Claude Code's really good at those kinds of zero to one tasks. Like, we use Streamlit internally. And there's been, like, a proliferation of how much we're able to visualize. And because we're able to visualize it, we're able to see patterns that we wouldn't have otherwise. If we were just looking at, like, raw data.

**Boris** \[00:41:04\]: Yeah. Like, I was working on also this, like, side website last week. And I just showed Claude Code the mock. So I just took the, you know, the screenshot I had, dragged and dropped it into the terminal. And I was like, hey, Claude, here's the mock. Can you implement it? And it implemented. And it looked like, you know, it sort of worked. It was a little bit crummy. And I was like, all right, now look at it in Puppeteer and, like, iterate on it until it looks like the mock. And then it did that three or four times. And then the thing looked like the mock. Yeah. This was just all manual work before.

**Swyx** \[00:41:32\]: I think we're going to ask about, like, two other features of, I guess, the overall agent pieces that we mentioned. So I'm interested in memory as well. So we talked about autocompact and memory using hashtags and stuff. My impression is that your, like you say, simplest approach works. But I'm curious if you've seen any other requests that are interesting to you or internal hacks of memory that people have explored that, like, you know, you might want to surface to others.

## Memory and the Future of Context

**Boris** \[00:41:59\]: There's a bunch of different approaches to memory. Most of them use external stores of various sorts. Like Chroma. Exactly. Yeah. There's a lot of projects like that. And, yeah, it's either a K value or kind of, like, graph stores. That's, like, the two big shapes for these. Are you a believer in knowledge graphs for this stuff? You know, I'm a big, if you talked to me before I joined Anthropic and this team, I would have said, yeah, definitely. But now, actually, I feel everything is the model. Like, that's the thing that wins in the end. And it just, as the model gets better, it subsumes everything else. So, you know, at some point, the model will encode its own knowledge graph. It'll encode its own, like, KV store if you just give it the right tools. Yeah. But, yeah, I think the specific tools, there's still a lot of room for experimentation. We just, we don't, we don't know yet.

**Swyx** \[00:42:45\]: In some ways, are we just coping for lack of context length? Like, are we doing things for memory now that if we had, like, 100 million token context window, we don't care about?

**Cat** \[00:42:55\]: I would love to have 100 million.

**Boris** \[00:42:57\]: I mean, you know, some people have claimed to have done it. We don't know if that's true or not. I guess here's a question for you, Sean. If you took all the world's knowledge and you put it in your brain. Yeah. And let's say, you know, there is, like, some treatment that you could get to make it so your brain can have any amount of context. You have, like, infinite neurons. Is that something that you would want to do or would you still want to record knowledge externally?

**Swyx** \[00:43:19\]: Putting it in my head is, like, different for me trying to use an agent tool to do it because I'm trying to control the agent. And I'm trying to make myself unlimited, but I want to make the tools that I use limited because then I know how to control them. And it's not even, like, a safety argument. It's just more like I want to know what you know. And if you don't know a thing, then sometimes that's good. Like the ability to audit what's in it. Yeah. And I don't know if this is the small brain thinking because this is not very bitter lesson, which is, like, actually sometimes you just want to control every part of what goes in there in the context. And the more you just, you know, Jesus takes care of it. Like, if you really trust the model, then you have no idea what it's paying attention to.

**Boris** \[00:43:58\]: Yeah. I don't know. Did you see the Mac interpretability stuff from Chrisola and the team that was published? Like last week? Yeah, last week. Yes. What about it? I wonder if something like this is the future. So there's an easier way to audit the model itself. And so if you want to see, like, what is stored, you can just audit the model.

**Swyx** \[00:44:15\]: Yeah. The main salient thing is that they know what features activate it per token and they can tune it up, suppress it, whatever. But I don't know if it goes down to the individual, like, item of knowledge from context, you know. Not yet.

**Boris** \[00:44:30\]: Yeah. But I wonder, you know, maybe that's the bitter lesson version of it.

**Swyx** \[00:44:34\]: Right, right. Any other comments from memory? Otherwise, we can move on to planning and thinking.

**Cat** \[00:44:38\]: We've been seeing people play around with memory in quite interesting ways, like having Claude write a logbook of all the actions that it's done. So that over time, Claude develops this understanding of what your team does, what you do within your team, what your goals are. How you like to approach work. We would love to figure out what the most generalized version of this is so that we can share broadly. I think with things like hard code, like, I think when we're developing things like hard code, it's actually less work to implement the feature and a lot of work to tune these features to make sure that they work well for general audiences, like across a broad range of use cases. So there's a lot of interesting stuff with the memory, and we just want to make sure that it works well out of the box before we share it broadly.

**Swyx** \[00:45:29\]: Agree with that.

**Boris** \[00:45:30\]: I think there's a lot more to be developed here. I guess a related problem to memory is how do you get stuff into context? Knowledge base. Knowledge base, yeah. And originally, we tried very, very early versions of Claude actually used RAG. So we, like, indexed the code base, and I think we were just using Voyage. So, you know, just off-the-shelf RAG, and that worked pretty well. And we tried a few different versions. There was RAG, and then we tried a few different kinds of search tools. And eventually, we landed on just agentic search as the way to do stuff. And there were two big reasons, maybe three big reasons. So one is it outperformed everything. By a lot. By a lot. And this was surprising. In what benchmark? This was just vibes, so internal vibes. There's some internal benchmarks also, but mostly vibes. It just felt better.

**Swyx** \[00:46:14\]: And agentic RAG, meaning you just let it look up in however many search cycles it needs. Yeah.

**Boris** \[00:46:20\]: Just using regular code searching, you know, glob, grep, just regular code search. Regular code search, yeah. Yeah. So there was, like, one. And then the second one was there was this whole, like, indexing step that you have to do for RAG. And there's a lot of complexity that comes with that because the code drifts out of sync. And then there's security issues because this index has to live somewhere. And then, you know, what if that provider gets hacked? And so it's just a lot of liability for a company to do that. You know, even for our code base, it's very sensitive. So we're kind of, we don't want to upload it to a third-party thing. It could be a first-party thing. But then we still have this out-of-sync issue. And agentic search just sidesteps all of that. So essentially, at the cost of latency and tokens, you now have really awesome search without security downsides.

**Alessio** \[00:47:01\]: Well, memory is like planning, right? There's kind of, like, memory is, like, what I like to do. And then planning is, like, now use those memories to come up with a plan to do these things.

**Swyx** \[00:47:10\]: There was one. Or maybe put it as, like, memory is sort of the past. Like, what we already did. And then planning is kind of what we will do. And it just crosses over at some point. Yeah.

**Alessio** \[00:47:19\]: I think the maybe slightly confusing thing from the outside is what you define as thinking. So there's, like, extensive thinking. There's the think tool. And it's kind of, like, thinking as in planning, which is, like, thinking before execution. And then there's, like, thinking while you're doing, which is, like, the think tool. Can you maybe just run people through the difference?

**Swyx** \[00:47:40\]: I'm already confused listening to you.

**Boris** \[00:47:42\]: Well, it's one tool. So Quad can think if you ask it to think. Generally, the usage pattern that works best is you ask Quad to do a little bit of research. Like, use some tools, pull some code into context, and then ask it to think about it. And then it can make a plan and, you know, do a planning step before you execute. There's some tools that have explicit planning modes. Like, RooCode has this and Quine has this. Other tools have it. Like, you can shift between, you know, plan and act mode or maybe a few different modes. We've sort of thought about this approach. But I think our approach to product is similar to our approach to the model, which is Bitter Lesson. So just freeform. Keep it really simple. Keep it close to the metal. And so if you want Quad to think, just tell it to think. Be like, you know, make a plan. Think hard. Don't write any code yet. And it should generally follow that. And you can do that also as you go. So maybe there's a planning stage and then Quad writes some code or whatever. And then you can ask it to think and plan a little bit more. You can do that anytime.

**Alessio** \[00:48:45\]: Yeah, I was reading through the think tool blog post. And it said, while it sounds similar to extended thinking, it's a different concept. Extended thinking is what Quad does before it starts generating. And then think it, once it starts generating, how do you stop and think? Is this all done by the Quad code harness? So people don't really have to think about the difference between the two, basically, is the idea? Yeah, you don't have to think about it. Okay. That is helpful. That is helpful. Because sometimes I'm like, man, am I not thinking right?

**Boris** \[00:49:16\]: Yeah. Yeah. And it's all chain of thought, actually, in Quad code. So we don't use the think tool. Anytime that Quad code does thinking, it's all chain of thought.

**Swyx** \[00:49:24\]: I had an insight. This is, again, something we had, a discussion we had before recording, which is in the Claude Place Pokemon HacCathon. We had access to more sort of branching environments feature, which meant that we could take any VM state, branch it, play it forward a little bit, and use that in the planning. And then I realized. The TLDR of yesterday was basically that it's too expensive to just always do that at every point in time. But if you give it as a tool to Claude and prompt it, in certain cases, to use that tool, seems to make sense. I'm just kind of curious, like your takes on overall, like, sandboxing, environment, branching, rewindability, maybe, which is something that you immediately brought up, which I didn't think about. Is that useful for Claude? Or Claude has no opinions about it?

## Sandboxing, Branching, and Agent Planning

**Boris** \[00:50:10\]: Yeah, I could talk for hours about this.

**Swyx** \[00:50:12\]: Claude probably can too. Yeah? Yeah. Let's get original tokens from you, and then we can train Claude on that. By the way, that's like explicitly what this podcast is. We're just generating tokens for people. Is this the pre-training or the post-training? It's a pre-trained data set. We got to get in there. Oh, man.

**Boris** \[00:50:28\]: Yeah. How do I buy? How do I get some tokens? Starting with sandboxing, ideally, the thing that we want is to always run code in a Docker container. And then it has freedom. And you can kind of snapshot, you know, with other kind of tools later on top. You can snapshot, rewind. Do all this stuff. Unfortunately, working with a Docker container for everything is just like a lot of work, and most people aren't going to do it. And so we want some way to simulate some of these things without having to go full container. There's some stuff you can do today. So, for example, something I'll do sometimes is if I have a planning question or a research type question, I'll ask Claude to investigate a few paths in parallel. And you can do this today if you just ask it. So say, you know, I want to refactor X to do Y. Can you research three separate ideas for how to do it? Do it in parallel. Use three agents to do it. And so in the UI, when you see a task that's actually like a sub-Claude, it's a sub-agent that does this. And usually when I do something hairy, I'll ask it to just investigate, you know, three times or five times or however many times in parallel. And then Claude will kind of pick the best option and then summarize that for you.

**Alessio** \[00:51:33\]: But how does Claude pick the best option? Don't you want to choose? What's your handoff between you should pick versus I should be the final decider?

**Boris** \[00:51:43\]: I think it depends on the problem. You can also ask Claude to present the options to you.

**Swyx** \[00:51:48\]: Probably, you know, it exists at a different part of the stack than Claude Code specifically. Claude Code as a CLI, like you could use it in any environment. So it's up to you to compose it together. Should we talk about how and when models fail? Because I think that was another hot topic for you. I'll just leave it open. Like, how do you observe Claude Code failing?

## Model Failures and Areas for Improvement

**Cat** \[00:52:06\]: There's definitely a lot of room for improvement in the models, which I think is very exciting. Most of our research team actually uses Claude Code day to day. And so it's been a great way for them to be very hands on and like experience the model failures, which makes it a lot easier for us to target these in model training and to actually provide better models, not just for Claude Code, but for like all of our coding customers. I think one of the things about the latest Sonnet 3.7 is it's a very persistent model. It's like very, very motivated to accomplish the user's goals. But it sometimes takes the user's goal very literally. And so it doesn't always fulfill what like the implied parts of the request are, because it's just so narrowed in on like, I must get X done. And so we're trying to figure out, okay, how do we give it a bit more common sense so that it knows the line between trying very hard and like, no, the user definitely doesn't want that. Yeah.

**Boris** \[00:53:06\]: Like the classic example is like, hey, go on, get this test to pass. And then, you know, like five minutes later. It's like, all right, well, I hard-coded everything. The test passes. I'm like, no, that's not what I wanted. Hard-coded the answer. Yeah. But that's the thing. Like it only gets better from here. Like these use cases work sometimes today, not, you know, not every time. And, you know, the model sometimes tries too hard, but it only gets better.

**Swyx** \[00:53:27\]: Yeah.

**Cat** \[00:53:28\]: Yeah. Like context, for example, is a big one where like a lot of times if you have a very long conversation and you compact a few times, maybe some of your original intent isn't as strongly present as it was when you first started. And so maybe the model like forgets some of what you originally told it to do. And so we're really excited about things like larger effective context windows so that you can have these like gnarly, like really long hundreds of thousands of tokens, long tasks, and make sure that quad code is on track the whole way through. Like that would be a huge lift, I think, not just for quad code, but for every coding company.

**Swyx** \[00:54:04\]: Fun story from David Hershey's keynote yesterday. He actually misses the common sense of 3.5 because 3.7 being so persistent. 3.5 actually had some entertaining stories where apparently it like gave up on tasks and just 3.7 doesn't. And when quad 3.5 gives up, it started like writing a formal request to the developers of the game to fix the game. And he has some screenshots of it, which is excellent. So if you're listening to this, you can find it on the YouTube because we'll post it. Very, very cool. One form of failing, which I kind of like. I kind of wanted to capture was something that you mentioned while we're getting coffee, which is that quad code doesn't have that much between session memory or caching or whatever you call that. Right. So it reforms the whole state for whole coffee every single time. So as to make the minimum assumptions on the changes that can happen in between. So like how consistent can it stay? Right. Like I said, I think that one of the failures is that it forgets what it was doing in the past. Unless you explicitly opt in via Claude.md. Or whatever. Is that something you worry about?

**Cat** \[00:55:11\]: It's definitely something we're working on. I think like our best advice now for people who want to resume across sessions is to tell Claude to, hey, like, write down the state of this session into this text doc. Probably not the Claude.md, but like in a different doc. And in your new session, tell Claude to read from that doc. Yeah. But we plan to build in more native ways to handle this specific workflow.

**Boris** \[00:55:36\]: There's a lot of different cases of this, right? Like sometimes you don't want Claude to have the context. And it's sort of like Git. Sometimes I just want, you know, a fresh branch that doesn't have any history. But sometimes I've been working on a PR for a while and like I need all that historical context. Right. So we kind of want to support all these cases. And it's tricky to do a one size fits all. But generally our approach to code is to make sure it works out of the box for people without extra configuration. So once we get there, we'll have something.

**Alessio** \[00:56:02\]: Do you see a future in which the commits play a bigger part? Of like in a pull request, like how do we get here? You know, there's kind of like a lot of history in how the code has changed within the PR that informs the model. But today the models are mostly looking at the current state of the branch. Yeah.

**Boris** \[00:56:20\]: So Claude for, you know, for some things that will actually look at the whole history. So for example, if it's writing, if you tell Claude, hey, make a PR for me, it'll look at all the changes since your branch diverged from main. And then, you know, take all of those into account when generating the pull request message.

**Cat** \[00:56:35\]: You might notice it running git diff as you're using it. I think it's pretty good about just tracking, hey, what changes have happened on this branch or so far and just make sure that it's like understands that before continuing on with the task.

**Boris** \[00:56:51\]: One thing other people have done is ask Claude to commit after every change. You can just put that in the ClaudeMD. There's some of these like power user workflows that I think are super interesting. Like some people are asking Claude to commit after every change. So that they can rewind really easily. Other people are asking Claude to create a work tree every time so that they could have, you know, a few Claudes running in parallel in the same repo. I think from our point of view, we want to support all of this. So again, Claude code is like a primitive and it doesn't matter what your workflow is. It should just fit in.

**Alessio** \[00:57:23\]: I know that 3.5 Haiku was the number four model on AIDR when it came out. Do you see Claude code have a world in which you have like a commit hook that uses maybe Haiku to do something like the lintel? Or stuff and things like that continuously. And then you have 3.7 as the more.

**Boris** \[00:57:39\]: Yeah, you could actually do this if you want. So you're saying like through like a pre-commit hook or like a GitHub action or?

**Alessio** \[00:57:46\]: Yeah, yeah, yeah. Say, well, kind of like run Claude code, like the lintel example that you had. I want to run it at each commit locally, like before it goes to the PR.

**Boris** \[00:57:55\]: Yeah, so you could do this today if you want. So in the, you know, if you're using like Husky or like whatever pre-commit hook system you're using or just like Git pre-commit hooks. Just add a line quad dash p.

**Alessio** \[00:58:05\]: And then, you know, whatever instruction you have and that'll run every time. Nice. And you just specify Haiku. It's really no difference, right? It's like maybe it'll work a little worse, but like I still support it.

**Boris** \[00:58:15\]: Yeah, you can override the model if you want. Generally, we use Sonnet. We default to Sonnet for most everything just because we find that it outperforms. Yeah. But yeah, you can override the model if you want. Yeah.

**Swyx** \[00:58:25\]: I don't have that much money to run commit hook on 3.7. Just as a side note on pre-commit hooks. I have worked in places where they insisted on. Having pre-commit hooks. I've worked at places where they insisted they'll never do pre-commit hooks because they get in the way of committing and moving quickly. I'm just kind of curious. Like, do you have a stance or recommendation? Oh, God. That's like asking about tabs versus spaces. A little bit. But like, you know, I think it is easier in some ways to like if you have a breaking test, go fix the test with clock code. In other ways, it's more expensive to run this at every point. So like there's trade-offs.

**Boris** \[00:59:02\]: I think for me, the biggest trade-off is. You want the pre-commit hook to run pretty quickly so that if you're either if you're a human or if you're a quad, you don't have to wait like a minute. Yeah. So you want the fast version. Yeah. Yeah. So generally, you know, pre-commit, you know, for our code base should run. Just types. Yeah. It's like less than, you know, five seconds or so. Like just types and lint maybe. And then more expensive stuff you can put in the GitHub action or GitLab or whatever you're using. Agreed.

**Swyx** \[00:59:26\]: I don't know. I like putting prescriptive recommendations out there so that people can take this and go like, this guy said it. We should do it in our team. And then that's that's a basis for decisions. Yeah. Cool. Any other technical stories to tell? You know, I wanted to zoom out into more product-y stuff, but, you know, you can get as technical as you want.

**Boris** \[00:59:47\]: I don't know. Like one anecdote that might be interesting is the night before the code launch, we were going through to burn down the last few issues and the team was up like pretty late trying to trying to do this. And one thing that was bugging me for a while is we had this like markdown rendering that we were using. And it was just, you know, it's like the markdown rendering in Quad today is beautiful. And it's just like really nice rendering in the terminal. And it is bold and, you know, headings and spacing and stuff very nicely. But we tried a bunch of these off the shelf libraries to do it. And I think we tried like two or three or four different libraries. And just nothing was quite perfect. Like sometimes the spacing was a little bit off between a paragraph and like a list. Or sometimes the text wrapping wasn't quite correct. Or sometimes the colors weren't perfect. So each one had all these issues. And all these markdown renderers are very popular. And they have, you know, thousands of stars on GitHub and have been maintained for many years. But, you know, they're not really built for a terminal. And so the night before the release at like 10 p.m., I'm like, all right, I'm going to do this. So I just asked Quad to write a markdown parser for me. And they wrote it. Zero shot. Yeah. It wasn't quite zero shot. But after, you know, like maybe like one or two prompts, they got it. And, you know, that's the markdown parser that's in code today and the reason that markdown looks so beautiful. That's a fun one.

**Swyx** \[01:00:59\]: It's interesting what the new bar is, I guess, for implementing features like this exact example where there's libraries out there that you normally reach for that you find, you know, some dissatisfaction with for literally whatever reason. You could just spin up an alternative and go off of that. Yeah.

**Boris** \[01:01:17\]: I feel like AI has changed so much and, you know, literally in the last year. But a lot of these problems are, you know, like the example we had before, a feature you might not have built before or you might have used a library. Now you can just do it yourself. Yeah. I think the cost of writing code is going down and productivity is going up. And we just have not internalized what that really means yet. Yeah. But yeah, I expect that a lot more people are going to start doing things like this, like writing your own libraries or just shipping every feature.

## Future roadmap

**Alessio** \[01:01:43\]: Just to zoom out, you obviously do not have a separate Claude Code subscription. I'm curious what the roadmap is. Like, is this just going to be a research review for much longer? Are you going to turn it into an actual product? I know you were talking to a lot of CTOs. Is there going to be a Claude Code enterprise? What's the vision?

**Cat** \[01:02:04\]: Yeah. So we have a permanent team on Claude Code. We're growing the team. We're really excited to support Claude Code in the long run. And so, yeah, well, we plan to be around for a while. In terms of subscription itself, it's something that we've talked about. It depends a lot on whether or not most users would prefer that over pay-as-you-go. So far, pay-as-you-go is the most popular. I think pay-as-you-go has made it really easy for people to start experiencing the product because there's no upfront commitment. And it also makes a lot more sense with a more autonomous world in which people are scripting Claude Code a lot more. But we also hear the concern around, hey, I want more price predictability if this is going to be my go-to tool. So we're very much still in the stages of figuring that out. I think for enterprises, given that Claude Code is very much like a productivity multiplier for ICs. And most ICs can adopt it directly. We've been just like supporting enterprises as they have questions around security and productivity monitoring. And so, yeah, we've found that a lot of folks see the announcement and they want to learn more. And so we've been just engaging in those.

**Swyx** \[01:03:16\]: Do you have a credible number for the productivity improvement? Like for people who are not in Anthopic that you've talked to, like, you know, are we talking 30%? Some number would help justify things.

**Boris** \[01:03:29\]: We're working on getting this. Yeah. We should. Yeah. It's something we're actively working on. But anecdotally for me, it's probably 2x my productivity. My God. So I'm just like, I'm an engineer that codes all day, every day. Yeah. For me, it's probably 2x. Yeah. I think there's some engineers at Anthropic where it's probably 10x their productivity. And then there's some people that haven't really figured out how to use it yet. And, you know, they just use it to generate like commit messages or something. That's maybe like 10%. So I think there's probably a big range and I think we need to study more.

**Cat** \[01:03:58\]: For reference, sometimes we're in meetings together and sales or compliance or someone is like, hey, like, we really need like X feature. And then Forrest will ask a few questions to like understand the specs. And then like 10 minutes later, he's like, all right, well, it's built. I'm going to merge it later. Anything else?

**Cat** \[01:04:18\]: So it definitely feels definitely far different than any other PM role I've had.

**Alessio** \[01:04:23\]: Do you see yourself opening that channel of the non-technical people? Talking to Claude Code and then the instance coming to you, which like they're ready to find and talk to it and explain what they want. And then you're doing kind of the review side and implementation.

**Boris** \[01:04:37\]: Yeah, we've actually done a fair bit of that. Like Megan, the designer on our team, she is not a coder, but she's landing pull requests. She uses code to do it. She designs the UI? Yeah.

**Cat** \[01:04:48\]: And she's landing PRs to our console product. So it's not even just like building on Claude Code. It's building like across our product suite in our monorepo. Right.

**Boris** \[01:04:57\]: Yeah, yeah. And similarly, you know, our data scientist uses Claude Code, right? Like, you know, like BigQuery queries. And there was like some finance person that went up to me the other day and was like, hey, I've been using Claude Code. And I'm like, what? Like, how do you even get it installed? You don't even use Git. And they're like, yeah, yeah, I figured it out. And yeah, they're using it. They're like, so Claude Code, you can pipe in because it's a Unix utility. And so what they do is they take their data, put it in a CSV, and then they take the, they cat the CSV, pipe it into code. And then they ask it code questions about the CSV. And they've been, they've been using it for that.

**Alessio** \[01:05:32\]: Yeah. That would be really useful to me because really what I do a lot of the times, like somebody gives me a feature request. I kind of like rewrite the prompt. I put it in agent mode and then I review the code. It would be great to have the PR wait for me. I'm kind of useless in the first step. Like, you know, taking the feature request and prompting the agent to write it. I'm not really doing anything. Like my work really sucks. It starts after the first run is done.

**Swyx** \[01:05:59\]: So I was going to say, like, I can see it both ways. So like, okay, so maybe I would simplify this to in the, in the workflow of non-technical people in the loop. Should the technical person come in at the start or come in at the end? Right. Or come in at the end and the start. Obviously that's the highest leverage thing because like sometimes you just need the technical person to ask the right question that the non-technical person wouldn't know to ask. And that really affects the implementation.

**Alessio** \[01:06:23\]: But isn't that the bitter lesson of the model? That the model will also be good at asking the follow-up question. Like, you know, if you're like telling the model, hey.

**Swyx** \[01:06:31\]: That's what I trust the model to do the least. Right. Sorry, go ahead. Yeah.

**Alessio** \[01:06:35\]: If you're like the model, hey, you are the person that needs to translate this non-technical person request into the best prompt for Claude Code to do a first implementation. Yeah. Like, I don't know how good the model would be today. I don't have an eval for that. But that seems like a promising direction for me. Like it's easier for me to review 10 PIs. Than it is for me to take 10 requests, then run the agent 10 times and then wait for all of those runs to be done and review.

**Boris** \[01:07:04\]: I think the reality is somewhere in between. We spend a lot of time shadowing users and watching people at kind of different levels of seniority and kind of technical depth use code. And one thing we find is that people that are really good at prompting models from whatever context, maybe they're not even technical, but they're just really good at prompting. They're really effective at using code. And if you're not very good at prompting, then code tends to go off the rails more and do the wrong thing. So I think in this stage of where models are at today, it's definitely worth taking the time to learn how to prompt model as well. But I also agree that, you know, maybe in a month or two months or three months, you won't need this anymore because, you know, the bitter lesson always wins. Please. Please do it. Please do it, Anthropic.

**Swyx** \[01:07:43\]: I think there's a broad interest in people forking or customizing Claude Code. So we have to ask, why is it not open source? We are investigating. Ah.

**Boris** \[01:07:54\]: Okay. So it's a not yet. There's a lot of tradeoffs that go into it. On one side, our team is really small and we're really excited for open source contributions if it was open source. But it's a lot of work to kind of maintain everything and like look at it. Like I maintain a lot of open source stuff and a lot of other people on the team do too. And it's just a lot of work. Like it's a full time job managing contributions and all this stuff.

**Swyx** \[01:08:21\]: Yeah. I'll just point out that you can do source available and that's, you know, solves a lot of individual use cases. Without going through the legal hurdles of a full open source.

**Boris** \[01:08:30\]: Yeah, exactly. I mean, I would say like there's nothing that secret in the source. And obviously it's all JavaScript, so you can just decompile it. Compilation's out there. It's very interesting. Yeah. And generally our approach is, you know, all the secret sauce, it's all in the model. And this is the thinnest possible wrapper over the model. We literally could not build anything more minimal. This is the most minimal thing. Yeah. So there's just not that much in it.

**Swyx** \[01:08:51\]: If there was another architecture that you would be interested in that is not the simplest, what would you use? What would you have picked as an alternative? You know, like, and we're just talking about agentic architectures here, right? Like there's a loop here and it goes through and you sort of pull in the models and tools in a relatively intuitive way. If you were to rewrite it from scratch and like choose the generationally harder path, like what would that look like?

**Cat** \[01:09:14\]: Well Boris has rewritten this, Boris and the team have rewritten this like five times.

**Swyx** \[01:09:19\]: Oh, that's a story.

**Boris** \[01:09:21\]: Yeah.

**Cat** \[01:09:21\]: It is very much the simplest thing I think by design. Okay.

**Boris** \[01:09:25\]: So it's got simpler. It got simpler. It doesn't go more complex. We've rewritten it from scratch. Yeah. Probably every three weeks, four weeks or something. And it just like all the, it's like a ship of Theseus, right? Like every piece keeps getting swapped out and just cause quad is so good at writing its own code. Yeah.

**Swyx** \[01:09:41\]: I mean, at the end of the thing, the thing that's breaking changes is the interface, the quad MCP, blah, blah, blah. Like all that has to kind of stay the same unless you really have a strong reason to change it. Yeah.

**Cat** \[01:09:51\]: I think most of the changes are to make things more simple. Right. Like to share interfaces across different components.

**Cat** \[01:10:00\]: Because ultimately we just want to make sure that the context that's given to the model is in like the purest form and that the harness doesn't intervene with the user's intent. And so very much a lot of that is just like removing things that could get in the way or that could confuse the model. Yeah.

**Boris** \[01:10:16\]: On the UX side, something that's been pretty tricky and the reason that, you know, we have a designer working on a terminal app is it's actually really hard to design for a terminal. There's just like, there's not a lot of literature on this. Like I've been doing product for a while. So like I kind of know how to build for apps and for web and, you know, for engineers in terms of like tools that have DevEx, but like terminal is sort of new. There's a lot of these really old terminal UIs that use like curses and things like this and for very sophisticated UI systems. But these are all, they all feel really antiquated by the UI standards of today. And so it's taken a lot of work to figure out how exactly do you make the app feel like fresh and modern and intuitive in a terminal. Yeah. And we've had to come up with a lot of that design language ourselves.

## Why Anthropic Excels at Developer Tools

**Swyx** \[01:11:00\]: Yeah. I mean, I'm sure you'll be developing over time. Cool. Closing question. This is just more general. Like, I think a lot of people are wondering, Anthopic has, I think it's easy to say the best brand for AI engineering, like, you know, developers and coding models. And now with like the coding tool attached to it, it just has the whole product suite of model and tool and protocol. Right. So, and I don't think this was obvious one year ago today. Like when Claude 3 launched, it was just, it was just more like, this is a general purpose models and all that. But like Claude Sonnet really took the scene as like the sort of coding tool of choice and I think built Anthopic's brand and you guys are now extending. So why is Anthropic doing so well with developers? Like, it seems like there's just no centralized, every time I talk to Anthropic people, they're like, oh yeah, we just had this idea and we pushed it and it did well. And I'm just like, there's no centralized strategy here. Or like, you know, is there an overall overarching strategy? Sounds like a PM question to me. I don't know. I would say like Dario is not like breathing down your neck going like build the best dev tools. Like he's just, you know, letting you do your thing. Everyone just wants to build awesome stuff.

**Cat** \[01:12:11\]: It's like, I feel like the model just wants to write code. Yeah, I think a lot of this trickles down from like the model itself being very good at code generation. Like we're very much building off the backs of an incredible team. I think that's the only reason why Claude Code is possible. I think there's a lot of answers to why the model itself is good at code, but I think like one high level thing would be so much of the world is run via software and there's like immense demand for great software engineers. And it's also something that like you can do almost entirely with just a laptop or like just a dev box or like some hardware. And so it just like is an environment that's very suitable for LLMs. It's an area where we feel like you can unlock a lot of economic value by being very good at it. There's like a very direct ROI there. We do care a lot about other areas too, but I think this is just one in which the models tend to be quite good and the team's really excited to build products on top of it.

**Alessio** \[01:13:17\]: And you're growing the team you mentioned. Who do you want to hire? Yeah. We are. Who's like a good fit for your team?

**Boris** \[01:13:24\]: We don't have a particular profile. So if you feel really passionate about coding and about the space, if you're interested in learning how models work and how terminals work and how like, you know, all these technologies that are involved. Yeah. Hit us up. Always happy to chat.

**Alessio** \[01:13:42\]: Awesome. Well, thank you for coming on. This was fun.

**Cat** \[01:13:45\]: Thank you.

**Boris** \[01:13:45\]: Thanks for having us.

**Cat** \[01:13:46\]: This was fun.
