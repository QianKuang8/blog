---
date: '2026-09-10T16:07:27+08:00'
lastmod: '2026-09-10T16:07:27+08:00'
title: '从压缩历史到按需恢复：Codex 上下文压缩的新实验'
summary: "旧方法通过压缩，把过去整理成可以继续携带的交接材料；新方法通过笔记和历史查询，让模型先接上进度，再找回下一步需要的细节。"
description: "比较 Codex 的传统上下文压缩与切窗后按需恢复实验，解释笔记、历史查询、窗口切换及其服务依赖。"
tags: ["context-engineering", "agentic-coding"]
categories: ["原创文章"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

编程 Agent 会不断积累对话、代码和工具结果，模型能处理的内容却有容量限制。**上下文压缩**会把后续需要读入的材料变短，为继续工作腾出空间。

2026 年 9 月，Codex 通过 [PR #42385][experimental-pr] 加入了一个实验入口：切窗时跳过摘要生成，再通过笔记和历史查询找回任务。本文比较这套实验与传统压缩方法；所查版本中新旧路径仍然并存。[路径选择][dispatch]

<a id="guide"></a>

以修复上传取消问题为例，这段持续的会话叫作 **session**；模型当前读到的材料叫作**上下文**，它的容量受**上下文窗口**限制。会话可以继续，窗口容量却不会随任务增长。[会话与窗口状态][session-state]

![同一 session 内，基础指令、用户消息、模型回复、工具调用和结果逐步累积，当前上下文接近容量上限，需要为继续工作腾出空间](/blog/images/original/from-compaction-to-context-recovery/00-session-and-limit.svg)

图中的回复、工具调用和工具结果不断累积，直到窗口接近上限。读文件或运行测试，都可能带回一大段代码或日志，留给下一步的空间也随之减少。实际系统通常会提前整理输入，并为后续生成预留空间。[窗口预算与上限][context-limit]

假设用户要求：“修复取消后上传仍继续的问题，保持公开 API 不变。”Codex 已经找到原因、补传了取消信号，单元测试也通过了，但还没验证真实网络请求是否会终止。此时若上下文满了，腾出空间只是第一件事；它还必须记得用户的约束、当前进度和未完成的验证。

Codex 有两种不同的交接思路。**旧方法先压缩历史，带着较短的交接材料继续；新方法先记下进度，换一个窗口，再按需找回旧信息。**[压缩与切窗的路径选择][dispatch]

![旧方法先压缩历史再继续；新方法记下进度，换窗后按需找回旧信息](/blog/images/original/from-compaction-to-context-recovery/01-three-paths.svg)

<a id="old-method"></a>

## 一、旧方法：先压缩历史，再带着交接材料继续

旧方法像是在工作告一段落时写一份交接单。把目标、已完成的工作和下一步整理好，接下来就可以根据这份较短的材料继续，不必反复携带所有排查过程。

### 把几十次排查，整理成一份交接材料

最直观的方式是让模型写摘要。Codex 把当前对话和一份摘要要求交给模型，请它整理进度、关键决定、用户约束，以及尚未完成的工作。[摘要生成流程][local-input] 对于上传取消问题，摘要可以是：

> **目标**：取消操作应终止上传，保持公开 API 不变。  
> **已确认**：取消信号没有传入上传请求。  
> **已完成**：补传信号，单元测试通过。  
> **下一步**：验证真实网络请求能否在取消后终止。

这份交接单保住了任务骨架。模型接着读到它，就知道应当继续验证网络行为，而不是重新从头查代码。Codex 还会保留一部分用户原话，将它们和摘要一起放进后续上下文。旧的搜索、代码片段和工具结果，则主要通过摘要中的结论发挥作用。[摘要与保留内容的组织方式][local-retention]

除了可读的文字摘要，Codex 也有专门的远端压缩路径，生成供模型继续使用的压缩状态。调用方无法直接读懂这种状态的内部表示，但它同样用于携带后续工作所需的信息。[远端压缩流程][remote-request]、[压缩项定义][compaction-type] 文字摘要和远端压缩的实现不同，共同思路都是：**先把已经发生的事情整理成较小的表示，再带着它继续。**

### 压缩后，模型下一次看到什么？

Session 还在继续，变化的是下一次模型调用的输入。以文字摘要为例，基础指令会重新组织，一部分用户内容按规则保留；先前大量模型回复、工具调用和工具结果所记录的过程，由一份较短的摘要承接。[压缩后内容的组织方式][local-retention]

![旧方法的压缩前后：同一 session 的容量限制不变，较短的交接材料替换长过程，留出供后续新消息使用的空间](/blog/images/original/from-compaction-to-context-recovery/02b-legacy-context-after.svg)

此后生成的新回复、新工具调用和新工具结果，继续加入这份较短的上下文。窗口容量没有变，腾出来的是后续工作的空间。图中展示的是简化后的组成；远端压缩可以使用不透明的压缩状态，直接保留哪些旧消息也会因路径而异。[远端压缩][remote-request]

### 难点在于：现在要决定，以后会用到什么

一份交接单必须有所取舍。哪些失败尝试可以省略，哪个约束必须留下，哪段测试输出还会用到，都需要在整理时判断。例如，摘要只写“单元测试通过”，通常已经足够指导下一步。但如果网络验证失败，Codex 可能需要回头确认：之前的测试到底覆盖了哪条取消路径？它模拟的情况，与真实网络请求有什么不同？如果这些细节没有被保留，交接材料本身就回答不了。Codex 需要重新读取代码、找到旧记录，或再做一次验证。

更棘手的是把状态写错：把“单元测试通过”概括成“问题已解决”，下一轮可能直接跳过还没做的网络验证。旧方法的难点由此显现：它要用有限的篇幅，为尚未发生的后续工作提前挑选信息。新方法把这项选择拆开了一部分——进度先记下来，细节等真正需要时再找。

<a id="new-method"></a>

## 二、新方法：换一个上下文窗口，再按需找回过去

新方法把“知道做到哪里”和“保留全部细节”分开处理。Codex 用 **notes** 保存简短的工作笔记，记录目标、约束、进度和下一步；用 **history** 提供旧对话和工具记录的查询入口。笔记帮助模型接上任务，历史让它在需要时核对原先发生过什么。[笔记与历史工具][history-contract]

**这套实验中的 notes 和 history 由远端服务提供。** 模型请求写笔记时，Codex 客户端把内容提交给服务；换窗以后，客户端再按模型的请求取回笔记或历史片段。它们与工作目录中的源码、文件和本地会话日志分开，笔记也不是自动写进项目目录的普通文件。[远端服务调用][history-backend]

![Codex 客户端组织同一 Session 的窗口 A 和 B，远端 notes 与 history 保存跨窗口状态；客户端写入笔记、请求记录历史，切窗后再读取所需内容](/blog/images/original/from-compaction-to-context-recovery/03-state-boundaries.svg)

图中以桌面使用为例：**本地 Codex 客户端**组织当前输入并操作项目文件，**OpenAI 远端的 Notes / History 服务**保存笔记与历史。远端材料只有被读回的部分，才重新占用当前窗口。模型接口不自动提供这套远端恢复服务。

窗口快满时，Codex 可以通过 `new_context` 开启新的上下文窗口。任务仍然是原来的任务，已经修改的代码也还在；改变的是模型接下来读入的工作材料。[新窗口的定义][new-context-spec]、[窗口切换实现][start-window] 它怎样接着完成上传取消的验证？整个过程可以顺着四步来看。

### 第一步：边做边记，把当前进度留下来

模型不必等到窗口最后一点空间，才开始回顾整个任务。它可以随着工作推进，更新一份简短笔记。[模型的笔记与恢复指引][model-recovery] 发现原因时，记下“取消信号没有传入上传请求”；改完代码后，更新为“已补传信号”；测试通过后，再补上“单元测试通过，真实网络行为待验证”。

除了进度，笔记还可以附上关键记录的引用，例如用户“不改公开 API”的原话，以及刚才的测试结果。这样既能保持笔记简短，也为后续核对留下了路标。

### 第二步：换一个窗口，给后续工作腾出空间

接近容量限制时，Codex 会提醒模型准备交接；模型也可以主动请求新窗口。[交接提醒][reminders] 客户端随后重建上下文。新窗口里会有基础工作说明和恢复指引，之前那一长串用户消息、代码与工具输出则不再自动带入。这次切换跳过了专门生成摘要的步骤。[切窗流程][rollover] 这时，项目文件仍然保留着刚才的修改。旧材料退出模型眼前的窗口，也不意味着旧日志在这一步被删除。[活动历史与日志的处理][history-replace]

![新方法的换窗前后：同一 session 从窗口 A 切到窗口 B，刚切完仅有重建的基础内容；模型再发出读取笔记和历史的工具调用，工具结果进入窗口 B 后恢复任务背景](/blog/images/original/from-compaction-to-context-recovery/05b-new-context-after.svg)

图中“刚换完”和“读回之后”都是窗口 B。模型在窗口 B 发出新的工具调用，笔记和历史片段作为工具结果进入当前上下文。查回的用户要求，也以这次工具结果的形式供模型核对。[历史工具的返回方式][history-output] 因此，换窗只是先腾出空间。真正把两段工作接起来的是后面的读取与恢复。

### 第三步：先读笔记，知道该从哪里继续

进入新窗口后，恢复指引会让模型先读取工作笔记。看到“已补传取消信号，单元测试通过，下一步验证真实网络请求”，它就能接上刚才的工作。[恢复指引][model-recovery] 这里，笔记承担的是定位作用：把 Codex 带回当前任务，而不是让它重读几十次搜索和试错。如果下一步只需要检查网络请求，它可以直接继续。如果发现还缺少某段背景，就沿着笔记中的引用回查历史。

### 第四步：需要哪个细节，就找回哪段记录

假设真实网络验证失败了。Codex 需要弄清：之前通过的单元测试，究竟验证了什么？笔记里可以只写“单元测试通过”，再附上测试记录的引用。模型根据引用读取那段命令和输出，先确认跑过哪些测试、结果如何，再结合测试代码核对覆盖范围。如果没有现成引用，也可以先搜索或浏览历史，找到相关条目后再读取。[历史查询与读取][history-tools]

![工作笔记指向用户要求和测试原记录：笔记告诉模型下一步，原记录供它核对具体细节](/blog/images/original/from-compaction-to-context-recovery/06-checkpoint-references.svg)

找回的信息会进入新窗口。于是，此刻模型眼前的材料可能只有：基础工作说明、一份进度笔记、用户的 API 约束、一段必要的测试输出，以及后续新产生的工作内容。此前那些与下一步无关的搜索结果，就不必全部读回来了。以后需要其中某段，再去找那一段。

整个过程连起来，就是：**边做边记 → 开新窗口 → 读笔记接上进度 → 按需查历史 → 继续工作。**

### 这套恢复需要什么配套？

**模型接口与历史恢复服务，是两项不同的能力。** 换用其它模型服务提供商（provider），不会自动获得 OpenAI 这套远端恢复服务；如果没有接入笔记、历史或自建替代服务，这套完整恢复流程就不能直接使用。[原生恢复服务的条件][extension-gate] 具体结果取决于实际启用的切窗配置，而不只取决于选择了哪家模型服务。[实验入口与模型默认值][activation-gates]、[切窗路径选择][dispatch]

| 使用情况 | 在所查版本中会发生什么 |
|---|---|
| 自定义 provider，仅打开实验入口，未另行启用切窗 | 入口检查不通过，继续选择原有压缩路径。 |
| 另行启用底层切窗，却没有恢复服务 | 仍可能换窗，但无法按图示流程找回任务；不会自动退回摘要。 |

<a id="comparison"></a>

## 三、新方法比旧方法好在哪里？

新方法先记住任务进度，再根据下一步的需要决定读回哪些历史记录。与旧方法相比，改变的不只有交接动作，还有服务依赖和调用开销。

| 读者关心的问题 | 旧方法：压缩后携带 | 本次实验：切窗后按需恢复 |
|---|---|---|
| **交接时做什么？** | 生成较短的摘要或压缩状态，再继续。 | 平时维护笔记；切窗时跳过专门的摘要生成。 |
| **处理后，下一次调用先读到什么？** | 保留的内容，加上交接材料。 | 基础说明与恢复指引；任务进度需要读回。 |
| **后来缺一个细节呢？** | 若交接材料没有留下，要另外找日志、文件或重新验证。 | 根据笔记引用或搜索，读取相应历史条目。 |
| **什么时候挑选细节？** | 压缩时，提前挑选预计有用的信息。 | 写笔记先留进度；下一步再决定回读哪些细节。 |
| **增加哪些调用？** | 摘要或远端压缩调用，之后携带交接材料。 | 写笔记、读笔记与查询历史；省去切窗时的摘要调用。 |
| **需要什么配套？** | 模型能够生成摘要，或服务支持专门的压缩接口。 | 可用的笔记与历史服务，以及能正确记录、恢复的模型。 |

新方案的主要收益，是把“先接进度，再查依据”纳入恢复流程。旧方法也能另行读取日志，但需要另外找到相应的读取入口。与此同时，笔记遗漏、历史服务不可用、反复搜索和过量回读，都会影响恢复效果与开销。是否更快或更省，需要在具体任务中测量。[压缩路径][dispatch]、[切窗实现][rollover]、[恢复指引][model-recovery]

<a id="conclusion"></a>

## 四、结论：理解压缩，也要看信息怎样恢复

旧方法通过压缩，把过去整理成可以继续携带的交接材料；新方法通过笔记和历史查询，让模型先接上进度，再找回下一步需要的细节。回到上传取消问题，无论跨过几个窗口，Codex 都应该记得用户要求保持公开 API 不变，知道单元测试已经通过，并继续完成真实网络请求的验证。

**理解上下文压缩，要看清哪些内容留在窗口里，哪些保存在窗口外，以及需要时怎样把它们找回来。**

---

**资料来源**

本文依据 [OpenAI Codex 源码 `d648947`][commit]（2026 年 9 月 8 日）及其[压缩路径][dispatch]、[切窗实现][rollover]、[笔记与历史工具][history-contract]。文中的任务与图示用于解释机制，未进行性能对照测量。新方法的实验入口随 [CLI 0.153.0][release] 交付，所查版本中新旧方法仍然并存。

[commit]: https://github.com/openai/codex/tree/d6489472f3c15e87d2d7763a5fde033545c530f8
[release]: https://github.com/openai/codex/releases/tag/rust-v0.153.0
[experimental-pr]: https://github.com/openai/codex/pull/42385
[dispatch]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/core/src/tasks/compact.rs#L35-L80
[rollover]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/core/src/compact_token_budget.rs#L21-L92
[local-input]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/core/src/compact.rs#L248-L297
[local-retention]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/core/src/compact.rs#L670-L759
[remote-request]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/core/src/compact_remote_request.rs#L31-L98
[compaction-type]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/protocol/src/models.rs#L1195-L1220
[new-context-spec]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/core/src/tools/handlers/new_context_window_spec.rs#L8-L16
[start-window]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/core/src/session/mod.rs#L4224-L4280
[history-replace]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/core/src/session/mod.rs#L3778-L3853
[reminders]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/core/src/session/token_budget.rs#L178-L215
[model-recovery]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/models-manager/models.json#L105-L110
[history-contract]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/ext/history-notes/src/tools.rs#L24-L95
[history-tools]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/ext/history-notes/src/tools.rs#L142-L188
[context-limit]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/core/src/session/context_window.rs#L57-L109
[history-output]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/ext/history-notes/src/tools.rs#L331-L398
[history-backend]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/ext/history-notes/src/backend.rs#L29-L91
[session-state]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/core/src/state/session.rs#L32-L55
[extension-gate]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/ext/history-notes/src/extension.rs#L44-L63
[activation-gates]: https://github.com/openai/codex/blob/d6489472f3c15e87d2d7763a5fde033545c530f8/codex-rs/core/src/session/token_budget.rs#L21-L158
