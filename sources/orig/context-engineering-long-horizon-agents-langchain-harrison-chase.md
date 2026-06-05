---
title: "Context Engineering Our Way to Long-Horizon Agents: LangChain's Harrison Chase"
source_url: "https://www.youtube.com/watch?v=vtugjs2chdA"
domain: "youtube.com"
description: "A Training Data interview with Harrison Chase on long-horizon agents, context engineering, traces, and LangChain's role in agent infrastructure."
retrieved_at: "2026-06-05T21:16:57+08:00"
extractor: "defuddle"
---

![](https://www.youtube.com/watch?v=vtugjs2chdA)

Harrison Chase, cofounder of LangChain and pioneer of AI agent frameworks, discusses the emergence of long-horizon agents that can work autonomously for exte...

## Transcript

### Introduction

**0:00** · People use traces from the start to just tell what's going on under the hood. And it's way more impactful in agents than in single LLM applications because in single LM applications, you get some bad response from the LLM. You know exactly what your prompt is. You know exactly what the context that goes in is because that's determined by code and then you get something out. In agents, they're running and and and repeating and so you don't actually know what the context at step 14 will be because there's 13 steps before that that could pull arbitrary things in. So like what exactly is everything's context engineering?

**0:28** · Context engineering is such a good term.

**0:30** · I wish I came up with that term. Like it actually really describes like everything we've done at Langchain um without knowing that that term existed.

**0:36** · But like traces just like tell you what's in your context and that's so important.

**0:57** · Welcome to training data. Harrison, you are our very first guest on training data and the AI space has moved so quickly uh in the 18 months or so since we originally interviewed you and so I'm delighted to get you on the show today.

**1:09** · Um topics of the moment. I think there's nobody better than you to talk about some of these topics. We're going to talk first about long horizon agents and agent harnesses. Pat and I had this blog post on this yesterday. I know this is something that you are deeply um fluent in. And then we're going to talk about what's the difference between building long horizon agents versus building software um and the role that you see Lang Chain playing in that ecosystem.

**1:30** · And then finally, I just want to chat with you about the future. I think you single-handedly, you know, kind of saw the agent opportunity I think before anybody. You know, we were back in the GP3 days and um I think you see the future for what's happening with agents and so I'm just excited to chat with you open-endedly about the future as well.

**1:46** · I am really excited as well. Thank you guys for having me back. It's quite an honor. I'll tell my mom again and that I'm back on the line.

**1:53** · Wonderful. Okay, let's start with long horizon agents.

### Discussing Long Horizon Agents

**1:57** · Yes, that was a great term. You guys wrote a great article.

**1:59** · Sony's good at naming things.

**2:01** · We're not going to get into the the backstory there. Um, what do you think?

**2:04** · What do you agree with? What do you disagree with?

**2:06** · I mean, uh, I agree that they're starting to finally work. I think like the idea of running an LLM in a loop and just having it go was, uh, was always the idea of agents from the start. uh autog was basically this then this is why it took off and and captured so many people's imagination because it was just an LLM running a loop completely deciding what to do. The issue is the models weren't really good enough and the scaffolding and harnesses around them weren't really good enough and I think the models got better.

**2:31** · We learned more about what makes a good harness over the past few years and now they start to like really really work and you see this in coding first and I think that's the domain where they're taking off the most and that's spreading to other domains but you can give a task to an agent and you still need to communicate to it what you want it to do and it needs to have the right tools and all of that but it can actually operate for longer and longer periods of time and so that yeah the long horizons kind of like uh uh framing of it I think is really really apt and really really good.

**2:59** · Awesome. Um, what are your favorite examples of long horizon agents and I guess what shapes you see them taking?

### Examples of Long Horizon Agents

**3:05** · So, coding is the place where there's the most. I think that's the one that I probably use. Yeah, that's the one that I use the most. Um, adjacent to that, I think like really good ones are AI SRRES. So, Traversal I think is a Sequoia company and and they have an AI SR that that that operates over longer time horizons. research in general and

**3:25** · I'd call like AISR kind of research like they're taking a incident and they're going and digging through logs like research in general is a really really good task because it ends up producing like a first draft of something and the issue with agents is they aren't like reliable to 99 of reliability but they can do a ton of work and and more and more work over longer time horizons. So if you can find these framings where they run for a long period of time but produce like a first draft of something those to me are like the killer applications of long horizon agents right now.

**3:51** · So like I coding coding is an example of that like coding you usually put up a PR you don't directly push to prod unless you're vibe coding which is also starting to get better and better.

**4:00** · Uh AISR usually surface it to a human who comes in and then reviews it. Report generation you don't send it out to all of your followers right away. You look at it you edit it. It creates like a first draft of something. So we see this in uh we see this in finance a bunch.

**4:14** · This is this is a huge research opportunity. Customer support. We see a lot of things pivoting from kind of like the initial the initial customer support was like first-line response like someone messages you just respond really quickly and there's still that and and that's going great but now there's examples K is a great example of this where it's like humans and AI working together when the first line fails you

**4:35** · escalate to a human you don't just have the human handle it you have this long horizon agent run in the background produce a report of everything that happened and then hand it off to the to the to the agent there um to the human agent there agent starts to get confusing in customer support.

**4:50** · Um, so so I think the killer use case of all of these is places where you have like this first draft type of concept.

### Harness Engineering and Model Integration

**4:56** · And then how much of the uh the why now do you think is the models themselves are just so good versus people are doing really smart things on the harness side?

**5:06** · And maybe even before we get to that, can you say a word for for our listeners on like you know how you frame the the harness versus the model in terms of the actual composition of an agent?

**5:14** · Yeah.

**5:14** · So and and I'll maybe I'll maybe bring in like framework as well because I think early on I mean that's how we describe lang chain as that's what lang chain is it's an agent framework and now and now we have deep agents which I'd call an agent harness and we get asked about what's the difference so a model is obviously the LLM tokens messages in

**5:32** · messages out um the framework would be abstractions around that so making it easy to switch between models uh adding abstractions for other things like tools and vector stores and memory and things like that but pretty like unopinion about what goes in there more values are more like batteries included. So when we talk about deep agents we're talking about we we actually give it a planning tool by default. So it has a tool that that that comes built into the harness. That's pretty opinionated that like this is the right way to do things.

**6:04** · Um we do compaction. So you have these long horizon agents. They're running for long periods of time. Context windows are larger but they're still not infinite. And so at some point you need to compact that. How do you do that?

**6:14** · There's a lot of research going on there right now. Uh, one of the other sets of tools that we and a lot of people are giving to these agents are tools for interacting with the file system whether directly or via bash and and this is it's kind of tough to separate from the models because the models are being trained on a lot of this data as well.

**6:33** · And so there's this kind of evolution between like I don't know if we could have known that like these file system based harnesses are the best thing at like if if we fast if we go back two years ago I don't think we could have known that because models weren't really being trained on that as much as they are now and so they're kind of evolving together. So so I think it's like a combination of things. It's the models absolutely are getting better.

**6:54** · Reasoning models are helping helping a lot. Um, but it's also the fact that we're figuring out all these primitives around compaction and uh and planning and and these file system tools being really useful. And so it's I I do think it's a combination of both.

### Evolution of Agent Frameworks

**7:09** · Um I remember in in that very first episode we did together, you know, you described laying graph I think as the almost the cognitive framework.

**7:19** · Yeah.

**7:19** · Uh of of the of the agent. Is that the right way to think about what the the harness is? Uh yeah, I think I think that's right. Yeah, so we we build we build deep agents on top of Langraph. It's one particular kind of like langraph instance. It's very opinionated. It's more general purpose.

**7:34** · Um and so I think early on we talked about general purpose architectures and more specific architectures. And what we've seen is that a lot of the specificity for tasks previously that might have been in langraph because you needed to put more structure on the models. Now that specificity is moving into the tools and the instructions. So there's still the same level of complexity. It's just in natural language. And so prompting and editing those prompts and and and automatic maybe automatically updating those is becoming a part, but the harness is remaining a little bit more fixed.

**8:07** · Um what's the hardest thing to get right on the harness side? And do you think, you know, do you think individual companies can actually excel at the harness engineering side of things? Who do you admire there? Uh I think a lot of the companies that are doing the best harness engineering are coding companies. Honestly, I think that's the place where it's taken off a bunch. I mean you look at cloud code. I would argue a big reason for the popularity of cloud code is the harness itself.

**8:32** · Um does that by the way imply that harnesses are better built by foundation model companies than by third party startups?

**8:43** · I I I don't know. Um I so the next company I was going to mention is Factory which is another coding company and and I think you look at at the harness they've done there. AMP um is another coding company has a has a has a really good harness. Um I think there's pros and cons. They there definitely is some aspect of the harness being tied to a model. Um and and maybe not just not a specific model but a family of models.

**9:09** · So like all cloud models like anthropic fine-tunes on some specific tools.

**9:13** · OpenAI fine-tunes on different ones. So like I think probably probably probably probably probably when we were doing this last time we maybe talked about how prompts need to be different for one model versus another. Hardnesses also need to be slightly different for one family of of things versus the other but there are similarities. Uh all of them use the file system in in in some sense.

**9:30** · Um so I think this is I I I I actually don't know the answer to that. It's a really interesting uh thing. Um we see that a lot of the coding com a lot everyone who's building a coding company is basically building their own harness right now. Yeah.

**9:43** · Um, and there's all these leaderboards and you can see it's actually kind of interesting if you go to terminal bench 2, which I think is probably the one of the more kind of like popular coding benchmarks right now. You can actually see they they have like the the agent harness and then the model and so you can see the variation in performance and claude code is not at the top of that.

**10:02** · Um, so there's there's differences but I think it it doesn't necessarily mean that the model labs are better at it. It just means that you have to understand how the models work and people who look at the at what makes a harness tick around the model can can get some performance gains there.

**10:19** · Yeah.

**10:20** · What do you think goes into, you know, making the harness tick? Like what do you think that the guys at the top of the leaderboard are doing exceptionally well?

**10:26** · I think part of it is definitely understanding like what tools the models uh trained on. So uh I think OpenAI trains really heavily on Bash. I think Anthropic has an explicit kind of like file editing tools and so I think leaning into that is part of it. Um compaction is becoming more and more of a thing. Uh so especially as you start doing longer horizon tasks like you start to fill up the context window and so what do you do there is a really big question and there's a bunch of strategies for for kind of like approaching that. I'd argue that's part of a harness.

**10:55** · I mean, so all of these harnesses also this is where like skills and MCPs and sub aents start to come into play as well and you can use those in like different ways and and I don't know how I I don't think a ton of like skills or sub agents are trained into the models yet like those are still pretty new.

**11:13** · Yeah.

**11:13** · Um and and so like one one of the things that we see in our harness is like when you have a sub agent the the the the main model needs to communicate with it like well it needs to it needs to give it all the appropriate information. it needs to let the sub aent know that it needs to like give it its final response out. So like we would see some failure modes where the sub aent because basically what happens is you kick off the sub agent and then only the final response is passed back to the main agent. And so we'd see some failure modes where the sub agent would do a bunch of work and then it would be basically like look at my work above and then you know pass that back to the main agent and it can't see it and it's like what are you talking about?

**11:43** · And so like that type of like prompting to get these pieces to work together is a big part of it. So like skills, sub agents, MCP, there there are like prompts in all of these harnesses that make them work well or don't make work them work well. And they're they're hundreds of of lines long if you look at some of the the the ones that are out there.

**12:03** · Can I ask you a question on how this has evolved and um since you've always been really kind of on the bleeding edge of what are people doing around the models to make them work in the real world, right? If we think about in our simplistic view on like what the big inflection points over the last five years have been feels like there was a big inflection point around pre-training when chatbd came out. Feels like there was a big inflection point around reasoning when 01 came out. Feels like just recently there's been a third big inflection point around these long horizon agents with cloud code and opus 45.

**12:35** · Um in your world the world of all the stuff around the models that that makes them work in the real world. Would you have a different set of inflection points? Like what have the major changes been? I remember we talked about cognitive architectures a couple years ago and now we're talking about frameworks and agent harnesses. Like what have the major leaps in um sort of the design around the model?

**12:58** · Yeah. What have they been?

**13:00** · So I think there's maybe like three eras I would say. I'd say like early on and this is when Langchain was just started like these were still the raw like text in text out like not even chatbased models. And so they didn't have any of the tool calling. They didn't have any content blocks, any reasoning at all. They were really just like really really basic. Uh and so the the things that people were doing were mostly like single prompts or like chains. Um and and it wasn't even possible to do anything like that complicated.

**13:27** · Then a lot of the model labs started training in a lot of like the tool calling into the models and they got really good at kind or they tried to make them good at like thinking and planning and they still weren't they still weren't good yet. they sort of weren't good as they as they are today. Um, but they were good enough to like decide what to do. And this is where like the custom cognitive architectures would come in more into play because you'd ask it explicitly like what do I do here? But it was like a very like point in time and then you go down this branch and then like what do I do here?

**13:54** · And maybe there's a loop and and there started to be some loops but it's still a little bit more kind of like scaffolding around it.

**14:00** · And then there was an inflection point and I don't know where exactly that was.

**14:03** · I would say I think we noticed it probably in like June July of this year where we saw Cloud Code taking off, deep research taking off, Manis taking off and these all use the same architecture under the hood of just the the LLM running in the loop but like cleverly like a lot of a lot of hardness is context engineering like everything around contraction context engineering sub agents context skills context engineering. So we basically saw them using the same core algorithm but making just like improvements on context engineering and we're like oh that's interesting that's pretty different than before. And so that's when we started working on deep agents.

**14:34** · I think for a lot of people in the coding community, I think probably like Opus 4 5 was when they started to like really feel this. It might have also just coincided with winter break when everyone went home and started using claude code and realiz how good it was.

**14:47** · Um but I think like around like November, December like I think there's has been this like at least I I sense a pretty big like vibe shift in like people just like yeah you throw hard problems at these things and you get long horizon agents. And so I don't know whether it was early 2025 or late 2025, but at some point the models got good enough and and that's when we moved from like scaffolds to to harnesses.

**15:08** · And what's next on this arc?

**15:11** · I I wish I could tell you. Um, I mean I do think that like this algorithm of just running the LM in a loop and letting it orchestrate its own uh let letting it really choose what to pull into context and and and doing stuff there that is like it's so simple and so general purpose like I mean that was the core idea of agents and all along and and and we're finally there.

**15:30** · Um if you look at some of the manual scaffolding like maybe some of that goes away. So like compaction is still very manual like the the harness author decides what to do with it. Anthropic has some interesting things where they let the model decide like when to compact things. We don't really see a ton of people using that. Maybe that'll be a part that's next. Uh part of what we're really interested in is memory as well. If you think about memory in the context of this, that's also context engineering, right?

**15:56** · It's context engineering over longer time horizons and it's a slightly different set of contexts, but it's still giving that to the to the LLM. And I think uh I think like the the core algorithm is is is pretty like it's pretty simple. It's run the LLM in a loop and we're finally there and it kind of works. And so I think there'll be a bunch of like context engineering tricks around it.

**16:19** · And maybe some of that is giving the context engineering actually to the LLM like letting like the anthropic thing.

**16:24** · Maybe some of that is just pulling in new types of context. The models will will probably get better. They'll probably I mean they'll probably get better and better at these types of longer horizon tasks. that'll be great as well. Um, one of the big questions on my mind it so a lot of these harnesses that we see are very coding specific.

**16:40** · Yeah. Um, and that's where we first started to really see these long horizon uh, agents take off and even for non-coding tasks I think you can make an argument that like writing code is really useful and uh, can be general purpose.

**16:55** · I was going to ask you are coding agents is that a subcategory or are coding agents just agents? Meaning the job of an agent is to figure out how to get a computer to do useful stuff and code is a pretty good way to get a computer to do useful stuff.

**17:09** · I don't know. Um this is one of the big so I I I very very strongly believe that like right now if you're building a long horizon agent, you need to give it access to a file system. Like there's so many things you can do with a file system in terms of context management.

**17:22** · Like when we talk about compaction, one strategy is to summarize but put all the messages in the file system so that if it needs to look it up, it can. Uh, another strategy is when you have like big tool call results, don't pass it all to the model. Put it in the file system and let it looking let it look it up.

**17:36** · Now you can do all of that without like a real file system actually without letting it write code. So we have a concept of like a virtual file system where it's just backed by Postgress or something like that and it's more scalable, but there are obviously things you can do with code that you can't do with a virtual file system. You can't run code in a virtual file system. Um, so like writing scripts is like really useful for that.

**17:54** · Yeah.

**17:54** · Um, and I think a coding agent can be general purpose, but I don't know if that means that today's coding agents are, if that makes sense. Because I think a lot of the coding agents today are pretty optimized for coding tasks. And so I think it's possible that a general purpose agent is a coding agent, but I don't know if like the reverse is true if if if that kind of like makes sense.

**18:15** · Yeah. Yeah. Yeah.

**18:15** · We're thinking about that a lot as well.

**18:17** · Are all agents coding agents?

**18:18** · Yeah. That's that's one of the biggest things that we're thinking about right now.

### Building Long Horizon Agents vs. Software

**18:22** · Yeah.

**18:22** · Maybe can we transition into talking about what goes into building a long horizon agent versus building software? Um can you maybe describe the software development stack for for 1.0 code development and um and what's different now? And I thought you had a really good X article on this. Maybe maybe just summarize the the punch line.

**18:41** · I've been I to think about this a bunch because we like to say that build and I think a lot of people would agree that like building agents is different than building software. But like what exactly is different? Cuz I think it's it's easy and lazy to say that it's different, but what actually is different? These might sound obvious, but hopefully that's good and they're not controversial. But like um when you're building software, all of the logic is in the code in the software and you can see it there. When you're building an agent, the logic for how your applications works is not all in the code. A large part of it comes from the model.

**19:10** · And so what this means is that you can't just look at the code and tell exactly what the agent would do in a specific scenario. you actually have to run it. And so and so and so what does that mean? And and I think that's the biggest difference by the way like we're introducing like these nondeterministic systems into it and it's a black box and it lives outside and I think all that that's that's the biggest difference. So what exactly does that mean? I think like one thing that that means is that in order to tell what the application is actually doing, you can't look at the code. You have to look at actually what it does in in real life.

### Understanding Non-Deterministic Systems

**19:41** · Um, and so I think one of the the one of the things that one of the things that we do that is most popular is Langmith. One of the core parts of that is tracing. Why are traces so popular?

### The Importance of Tracing in Lang Smith

**19:52** · Because they tell you exactly what goes on inside your agent at every step. Um, and it's different than software traces where in software you kind of have your system over here and it emits a bunch of like uh stuff and you you know you look at it when maybe there's some errors but you don't need like everything and and you usually only turn that on when you put it in production because if it's local you just put a breakpoint or something like that. in agents like people use traces from the start to just tell what's going on under the hood.

**20:19** · And and it's way more impactful in agents than in single LLM applications because in single LM applications you get some bad response from the LLM. You know exactly what your prompt is. You know exactly what the context that goes in is because that's determined by code and then you get something out. In agents they're running and and and repeating and so you don't actually know what the context at step 14 will be because there's 13 steps before that that could pull arbitrary things in. So, like what exactly is everything's context engineering. Context engineering is such a good term. I wish I came up with that term.

### Context Engineering and Its Significance

**20:48** · Like it actually really describes like everything we've done at Langchain um without knowing that that term existed. But like traces just like tell you what's in your context. And that's so important. And so then and so like what does that mean? That means that the the source of truth for software is in code. In for agents it's a combination now of code and and and traces are where you can see the source of truth.

**21:10** · technically in you know all those millions of parameters but like you can't really do anything with that. So now so now that means that traces become a place where you start to think about testing because now you can't you can test you can test some parts still of of the harness and and and you can do some unit testing offline but like in order to get the the what the test cases are you probably want to use the traces to construct that. You probably want to be testing online.

### Testing and Collaboration in Agent Development

**21:32** · That's probably more important in agents than it is in software is online testing because behavior doesn't emerge until until it's actually being used with with real world inputs. Um, we see traces becoming a point of collaboration for teams because if something goes wrong, it's not, oh, let's go look at the code in GitHub.

**21:49** · It's let's go look at the trace. We see this in our open source as well when people are being like, hey, deep agents like went off the rails here. What happened? Our response is like send us a lang trace. Like we can't really help you debug if it's if it's not that.

**22:01** · Previously would be like, show me the code, right? So there's think there's a transition there. And then I think the other thing that's and and so that was the blog post that I wrote on next which got a lot of good feedback on. I'm still kind of figuring out how to like phrase it but I think that's that's a big part of it. Um the other thing which I'm still trying to think through as well is I think building agents is more iterative. And we used to say that and I would kind of roll my eyes because building software is iterative as well, right? You you ship it, you get feedback and it's it's constant iteration. That's like what it is.

### Iterative Nature of Building Agents

**22:29** · I think the difference is that in software you're you're you're kind of like iterating based on what you want the software to do. Like you have some idea, you ship it, you get feedback. Oh, maybe this, you know, button is confusing. Maybe this uh maybe users actually want to do X instead of Y, but you know what the software does before you ship it. With agents, you don't know what the agent does before you ship it. You have an idea, but you don't really know what it does before you ship it.

**22:54** · And so I think there's way more iteration involved in order to get it like accurate, get it like right and passing like conceptual unit tests basically.

### The Role of Memory in Agent Development

**23:04** · Um, and building upon that like this is actually why I think memory is really important as well. Um, because memor is like learning from those interactions. And so if now you have a process that's like way more iterative. And so now you have to like it's it's way harder to build as a developer because I have to like change the system prompt like way more than I would have to change code in order to get it just perform like correctly.

**23:27** · Yeah.

**23:28** · So that's where memory comes in because if there's a way where the system can kind of like learn by itself that cuts down the iteration that you have to do as a developer and makes it easier to build these types of agents. So that's another kind of like angle that I I like I absolutely think agents are different than building software. I think it's also a little cliche to say that and so I've tried to think about what exactly is different and those are like the two things that I've kind of come up with.

**23:49** · Well, and I'm curious on that too. Um, one of the questions there's a big public market debate right now is are the existing software companies going to make it. And if you analogize to when on-prem software went to cloud, very few actually did make it because it turned out that building cloud software was actually quite different than building on-prim. And since you're in the middle of kind of how people are building with AI, um what's your take on not necessarily the public market question, but how different is it?

### Challenges for Existing Software Companies

**24:18** · Like do you see have you seen a lot of people who kind of like were good at building software the old way and now they're good at building software the new way? Or is it more just you either grow up building it the new way or you never get it? Like do you think people can make the leap? a lot of young founders out there right now which which makes me think that certainly it seems like the younger people without a lot of preconceived notions on how to build software you know have the blank slate that has allowed them to like pick up on a lot of this stuff.

**24:46** · I do think we we have consistently heard that a lot of the people who are on these agent engineering teams are more junior developers uh more junior builders even um who yeah don't have those preconceived notions. Our applied AI team internally definitely skews on the on the younger side.

**25:08** · Um I do think I mean in terms of kind of like I think there's like a there's like a person aspect to this. There's also like a company aspect to this. Like I do think that like data is still really really really valuable. Um I think when you think about this harness basically there's like if if harnesses become I by the way I I don't think that most people will build their own harness in the long run because it's actually way harder than than building a framework. And so I think they'll uh use uh a harness from us or from someone else.

**25:37** · And so if you think about what goes into that it's like the prompt and the instructions and then the tools that it's connected to. And I think one thing that this is more at the company level now, but like one thing that existing companies have is all the data and all the APIs if if you've done a good job at that then I think it will actually be pretty easy to plug those in and get real value out of things. Um we were talking to someone in the finance space and and they are saying yeah like the value of data is just going up and up and up and up. So if you're a previous uh software vendor and you have this data that is valuable like you should be able to expose it to agents and get a lot of value out of that.

**26:08** · Yeah.

**26:08** · The other part of it though is the instructions on what to do with that data and that's probably like more net new um in terms of like how to use that data. That's probably you probably had some ideas about that as a software vendor but you didn't kind of like consolidate it. You didn't have it because that was something that humans would still do. Like a lot of what agents are doing what humans would still do. So you'd give them the tools to do it but you wouldn't have tried to like automate that or you wouldn't have successfully automated it before kind of like agents.

**26:35** · And so that part I think is is is newer and we're also seeing a lot of demand like I think a lot of the a lot of the vertical startups um rogo is a great example of someone who has experience in finance and is bringing that knowledge to agents and the reason that's kind of like effective is because a lot of the agents are driven by by knowledge and and and and and not like world knowledge but like knowledge on how to do specific patterns. Um so kind of yeah I think there's like are the people who are building software the right people to build agents.

**27:04** · Um I think we saw a lot of really senior developers adopt agentic coding and so I think it it it's a mindset thing but like yeah there there is maybe a younger skew there. Um and then and then for companies depends on the data.

**27:18** · Yeah.

**27:18** · Even Pat's on on cloud code. So even old guys can get it.

**27:22** · Sonia got me on there.

**27:25** · Um okay. Okay. So, it seems like the trace is a core artifact you think in kind of this new world of of agent development and it's something that linksmith helps a lot with. What other core artifacts do you think are there?

**27:36** · And specifically, I'm wondering about eval.

**27:38** · Yeah, I think um maybe artifact is the wrong word.

**27:42** · Components.

### Human Judgment in Evaluating Agents

**27:43** · Component. Yeah, I mean I I I think one other thing that is different between building software and and building agents is that to evaluate software you could pretty reliably you you could rely on tests and assertions of of things programmatically.

**27:56** · Um with agents a lot of what they're doing is things that humans would do. So in order to judge them you need to bring human judgment into that. And that's another thing that we try to do in Lingsmith is how can you bring you've got these traces how can you bring human judgment to them? And so that like one obvious way to do that is to bring humans into the equation. Um and so we see data labeling startups doing really well. Uh we have a concept of annotation cues in Langmith to bring people in there. And so that actual like actual human judgment is is a big part of it.

**28:23** · And this is humans annotating the actual trace. So like ah the agent did this and this and this and that was good or bad.

**28:29** · Yeah.

**28:29** · Yeah. Um saying and and sometimes giving like natural language feedback on it like this is good, this is bad, should have done this. sometimes just like correcting it like actually like laying out what the what the uh correct steps were kind of depends on the use case and it's probably different for model companies doing RL than it is for for agent companies building building agents. Yeah.

**28:48** · Um but it's bringing that human judgment to it. Um but then another thing we see is trying to build proxies for this human judgment. And this is where LLM as a judge type things come in where you can run an LLM or something else that you know has some semblance of human judgment in it to grade the the thing that requires human judgment. Um, and so one of the things that we think a lot about is how to make building these elements as judges easy because a big part of them is making sure that they're aligned with your human judgment and human preferences. And so and because if they're not, you know, then your then your greater is just bad.

**29:18** · And so we have a we have a concept in Langmith called align evals. Um, where a human goes in labels some traces and then that that builds an LLM as a judge that that kind of like is calibrated against those traces. Um because a bit yeah a big part of it is bringing this human judgment and you just want to make sure that if you're bringing a proxy of it it's it's well calibrated.

**29:38** · Interesting. I remember when we first got into business with you we were emailing about LLM as judge. Is it a viable idea or not? So it seems like it's come a long way.

**29:45** · Okay.

**29:45** · So there's there's a few different aspects of LM as a judge, right? There's like the immediate like so what most people use them for in eval is like taking this trace and give it a score of like one to to zero or or 0 to 10 or something like that. And yeah, I think that's valu uh viable and people are doing that. They're doing it offline.

**30:01** · They're also doing it online because some of these judgments you don't need ground truth for. But I think the other area where this comes into is uh I mean you you kind of see this in the coding agents themselves like the coding agents will they'll work up until something then they hit an error and they get an error and then they have to correct there and so they're kind of judging their previous work. And so and and we also see this in memory like a big part of memory is like reflecting on traces and then updating something. And so like can LLM reflect on traces that are either like their own or their own from a previous session or someone?

**30:33** · Yeah, absolutely. I think they can. We see this all across evals and just like error correcting and and memory. It's all kind of the same thing.

**30:41** · I see. And then maybe Okay, so you have all this you you have all the traces.

**30:46** · Yep.

**30:47** · You have the evals.

**30:48** · Yep.

**30:48** · Um I think the natural question that comes to mind for me is is the EVEL like a reward signal for reinforcement learning or is it a feedback mechanism for you know a human engineer to improve the harness or for agent engineers to improve the harness because everyone's no one's no one's coding manual anymore. They're all using these.

**31:06** · So yeah, one big thing that we've seen is like um we we have a Langmith MCP and we have Langmith fetch which is a CLI because coding agents are actually great at using CLIs. um you give that to an agent and it can pull down traces and diagnose what went wrong and then and then it brings those traces into the codebase where it can then fix it. That's absolutely a pattern that we are seeing and and we really really really want to support that pattern.

**31:30** · Crazy. Yeah, I know.

**31:31** · And it's good.

**31:32** · Yeah.

**31:32** · Yeah. Yeah. Yeah. It's good. Like it it Yeah, it um and and so we see I'm probably more bullish on that than on kind of like reinforcement learning at least for like the agent app kind of like companies right now. That seems like real recursive self-improvement though.

**31:47** · Yeah, I think I think uh again there's still a human in the loop. So like uh back to the point around around like things are good when you can do something as a first draft like it it changes the prompt and then the human reviews it and like it it keeps it on the rails. But like um I absolutely so so one of the things we launched was Langmith agent builder which is a no code way to build agents. One of the cool things that we have in there is memory. Um, and so right now the way that memory works is when you interact with an agent, so it's not in the background yet.

**32:16** · It's not like pulling down its traces, but when you interact with the agent, if you say, "Oh, you should instead of X, you should have done Y," it will go to its own instructions, which are just files, and it will edit those files. So then in the future, and so that's also kind of like a a version of this. One thing we do want to add is like the thing that runs every night, looks at all the traces for the day, updates its own instructions, and so the dreaming thing.

**32:36** · Yeah. Yeah. Sleep time compute. Um, yeah, sleep time compute. Is that what it's called?

**32:40** · That's a term. Yeah, I think Leta came up with that. It's It's a great term. Yeah, that is good.

**32:45** · Love it.

**32:46** · Awesome. Okay, let's talk more about the future. Um, what are you what are you most excited about? Sounds like you was talking a lot about memory here.

### Future of Agent Development and Memory

**32:53** · I like memory a bunch. Yeah, I mean I think asking the agents to improve themselves is I mean I think very very cool and can be useful in a lot of situations. Not useful in all situations by the way. like if I'm chatting so so chat GPT added memory I don't actually really use that feature that much and I don't think it's created any more stickiness for me to use the product or anything like that and I think part of the reason is when I go to chat GPT I do

**33:16** · like everything's a one-off thing like I don't really repeat myself that much I have like I'm asking about software I'm asking about food trips like everything um in agent builder that you you build kind of like specific workflows for specific things so I have an email agent Um, and I actually I know it's been emailing me for two years.

**33:37** · Well, so, okay, so I had an email agent outside of agent builder and it had this like memory as part of it. We then built agent builder and I wanted to move it into it and it didn't have all of my memories and that was a big even though it had the same starter prompt and the same tools and that was actually a I still haven't fully switched over because it kind of sucks now compared to

**33:57** · what it was before like the compared to the other one and I if I just interact with it then it will get better and it will stop sucking but like that's where memory I think can be like a real moat and I absolutely think that we're at a point right now where LLM can look at traces and change things about their code. Um, and I think the question then becomes how do you do that in a way that's uh safe and acceptable to to users. Um, but I I I think that's absolutely uh something that we'll see more of for specific scenarios, not all of them.

**34:27** · Like I still don't know if this would be useful in chat GPT in this form at least.

**34:31** · Yeah.

**34:32** · How do you think the UI around working with long horizon agents will evolve?

### Async and Sync Modes in Long Horizon Agents

**34:37** · I think there probably needs to be like a sync mode and an async mode. So long horizon agents running for a long time, probably default would be some sort of like async way to manage them. Like you're if if it runs for like a day, you're not just going to sit there and wait for it to finish. You're probably going to kick off another one and another one and do a bunch of work. And so I think this is where like async management of things comes into play. I think things like linear and Jira and canban boards and maybe even email are uh interesting to look at for inspiration about like what it looks to like to basically manage a lot of these agents.

**35:07** · But I think for a lot of these at some point you're going to want to uh switch into synchronous communication with uh these agents because they come back with a research report and you want to give it feedback that it wrote something wrong. And I actually think chat's like reasonably good at that. The only thing that I'll maybe say there is that so many of these agents are now modifying other things like files in a file system that having some way to view that like state is really important.

**35:31** · And so you see this in coding um where IDE's ids are still used when you want to go in and manually kind of like change code and and uh even when I kick off uh cloud code when it finishes I sometimes I pull it up and look at the code that it actually wrote. Um and so I think I think having a a way to view that state is interesting.

**35:52** · One of the one of the really cool things that Anthropic did with their Claude co-work um when you set it up, you choose the directory that it's kind of like working in and you're basically saying like this is your environment. Um and obviously like that's what you do in coding as well.

**36:07** · You open your ID to a particular directory. But I think that's a nice mental kind of like framing is like this is your workspace. That could workspace could be a Google drive. It could be a notion page. Um, it could be anything that like stores state and then you and the agent are collaborating on that state. You kick it off, you manage maybe a bunch of these running asynchronously.

**36:26** · Then you go into sync mode where you chat with it, but you also view this state. And so that's kind of what I see right now.

**36:32** · And this is like your agent inbox idea then of, you know, to to enable the sync mode, your agent's going to have to need a way of reaching you.

**36:39** · Yeah, exactly. And so yeah, so the agent inbox or something we launched that about a year ago and and had this idea of like ambient agents that ran in the background and pinged you and the first version of that didn't have a sync mode and so it would ping you and then you'd give a response but then you'd kind of just wait for it to ping you again but oftentimes like when I was switching in to email you and respond to you, I would I would I would I would say very small things and I didn't want to switch out and wait like I I you're really important. So I wanted to like be in the sync mode in this conversation with the agent.

**37:07** · And so one of the things we added was this was was now when you open the inbox you're brought into chat and chat is very synchronous and that was actually a big unlock. So I actually think having just an async mode. I don't think that really works right now. Maybe in the future if they get so good that you don't really need to like correct them as much it gets more viable. But at least right now I think we see people switching from async to sync and back and forth.

### The Role of Code Sandboxes and File Systems

**37:29** · What do you think of code sandboxes?

**37:32** · Like is is every agent going to have access to a sandbox? Is every agent going to have access to or a computer?

**37:38** · Is every agent going to have access to a browser?

**37:40** · Really good question. Something we're thinking a bunch about. I think uh I think coding has clearly worked more than browser use so far. So at least in the short term, it seems like if any of those are going to be a key part there, it's going to be this code execution part. Um file systems, I'm completely file system pled. I think in some form agent should have access to some file system coding. I'm maybe not as pilled, but I'm probably like I'm like maybe like 90% there. Like yeah, I think like it is definitely possible. There are it's maybe for like the longer um tale of use cases.

**38:13** · So maybe there's something where if you're doing something repeated, you need code less, but I think file systems are still useful because that repeated thing could be generating a lot of context and and you need to do context engineering. Um but for the long tale of things, coding's great and there's really no replacement for that. browser use. Um, I think the models just aren't good enough at it right now from what we've seen.

**38:34** · Um, you could probably give like a coding agent a CLI to do browser use and there's probably some approximation there. There's probably some people doing some I think I have seen some cool stuff there.

**38:43** · Um, and then computer use is like a weird hybrid of the two. Um, so if Yeah, code sandboxes, I really like code sandboxes.

**38:49** · Yeah. Yeah.

**38:50** · Cool. Um, Harrison, thank you so much for joining us today. you have consistently seen the future on agents and it was really cool to have this conversation and talk about how context engineering has evolved to the current point in time with with harnesses and and long horizon agents and so thank you for for driving that future and thank you for always chatting with us about it.

### Conclusion and Future Predictions

**39:08** · Thank you for having me on. I look forward to being back on sometime in the future and being completely wrong about everything I said today. So it's very hard to predict the future.
