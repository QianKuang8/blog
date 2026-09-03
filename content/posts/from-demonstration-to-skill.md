---
date: '2026-09-03T16:49:48+08:00'
lastmod: '2026-09-03T17:09:31+08:00'
title: '从一次演示到可复用 Skill：Codex Record & Replay 与 Claude Record a Skill'
summary: "比较 Codex Record & Replay 与 Claude Record a Skill 如何把一次桌面演示变成可复用 Skill，以及两种证据形态、执行机制和安全边界的差异。"
description: "从录制证据、Skill 生成、再次执行和安全边界四个方面，比较 Codex Record & Replay 与 Claude Record a Skill。"
tags: ["agent", "harness-engineering"]
categories: ["原创文章"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

假设你每周都要完成一次数据填报。金额和页面位置会变，但任务目标始终相同。

你当然可以把步骤写成操作手册。不过，Codex Record & Replay 和 Claude Record a Skill 提供了另一种办法：你亲自做一遍，Agent 观察过程，再把其中的方法整理成可复用的 Skill。

这两项功能几乎同期出现。OpenAI 在 2026 年 6 月为 macOS 上的 ChatGPT / Codex 发布了 [Record & Replay](https://learn.chatgpt.com/codex/extend/record-and-replay)，让用户演示一次工作流，再由 Agent 把操作写成可复用的 Skill。Anthropic 在 2026 年 7 月为 Claude for Mac 的 Cowork 推出了 [Record a Skill](https://x.com/claudeai/status/2079595988998554047)，同样录制屏幕、点击、键入和语音，再由 Claude 生成 Skill。两者解决的问题相似，但内部机制明显不同——这正是本文要展开的内容。

本文所说的 Agent，是能理解任务并使用浏览器、外部服务接口或桌面工具的 AI。Skill 是给 Agent 看的工作说明，写明它适用于什么任务、需要哪些输入、应该怎样操作，以及如何检查结果。在这两项功能中，Agent 根据用户的演示起草这份说明。

这听起来像"录制宏"，实际机制却不同。宏通常重放旧按键和鼠标坐标；Record & Replay 和 Record a Skill 先让 Agent 理解演示，再由 Agent 写出方法。下次执行时，Agent 面对的是新的数据和新的界面，它需要重新找到目标、选择工具并检查结果。

## 先看任务：每周填一次，数据和位置都会变

先把产品机制放到一边，只看这项工作。用户从"九月周报"读取本周金额 `42,680`，再打开数据后台，把金额填进"经营数据"，提交后确认页面显示成功。

![每周从周报读取当前金额，填入数据后台并确认提交成功](/blog/images/original/from-demonstration-to-skill/task-scenario.svg)

下周的金额会变成 `43,210`，单元格和后台字段也可能移动，但任务没有变：找到本周的正确金额，填入正确记录，并确认结果。Record & Replay 要保存的正是这套方法，而不是这一次的数字和点击位置。

## 一眼看懂：从一次操作到一种方法

从用户视角看，两项产品的主线完全相同：

> 录制并留下证据 → Agent 理解证据并生成 Skill → 在新任务中使用 Skill

![用户录下演示并留下证据，Agent 从证据中提炼 Skill，随后在新任务中使用这套方法](/blog/images/original/from-demonstration-to-skill/end-to-end-overview.svg)

接下来，我们继续用每周填报的例子，依次回答三个问题：录制结束后留下什么，Agent 怎样把这些证据写成 Skill，以及保存的 Skill 怎样在下一次任务中工作。

## 第一阶段：录制结束后，留下了什么？

用户先在表格中找到 `42,680`，再切到浏览器，把数字填进"本周金额"，最后点击"提交"。同一次演示，在 Claude 和 Codex 中会变成两类不同的录制证据。

![同一次演示，在 Claude 和 Codex 中变成两类不同的录制证据](/blog/images/original/from-demonstration-to-skill/what-is-recorded.svg)

Claude 保存动作文字、关键帧、应用信息和可选旁白；Codex 保存事件与 AX 快照。Claude 的录制证据包含图片，Codex 的录制证据由 JSON / JSONL 文本组成。

### Claude：动作文字、关键帧与可选旁白

Claude 的默认方式会连续采集画面，同时记录键鼠操作和当时位于前台的应用。录制结束后，客户端把原始输入整理成动作文字：连续输入合并成一次键入，鼠标按下、移动和松开合并成一次拖拽，应用切换也成为一条动作。这些动作按发生顺序排列，并保留录制时刻。

Claude 最终保留筛选后的关键帧：画面变化较大时保留完整画面，只变化一小块时保留变化区域。动作文字记录点击位置、输入和应用切换；相邻图片则显示控件的样子，以及提交后页面发生的变化。

如果用户开启语音，Claude 还会生成一段独立的旁白文本。它不属于任何一条动作记录。

### Codex：事件与 AX 快照

Codex 把录制结果写入本地文件。`session.json` 保存会话信息和文件位置；`events.jsonl` 按时间保存应用切换、窗口变化、点击、键盘输入、文本选择和诊断信息。JSONL 是一种一行保存一条 JSON 记录的文本格式，适合边录制边追加事件。

每条事件还可以带上 macOS 的辅助功能信息。AX 是 macOS 的辅助功能接口；AX 快照用结构化数据描述界面的控件、标题、值和层级。Codex 可以先保存较完整的界面树，随后只记录相对前一次快照发生的变化。这样，一次点击不仅记录"鼠标按下"，还可以带上"浏览器窗口中标题为'提交'的按钮"。

Claude 的证据保留筛选后的画面；Codex 的证据用结构化事件和界面文字描述操作。它们仍只是一次演示留下的材料，还不是 Skill。下一阶段，两项产品会用不同方式把证据交给 Agent。

## 第二阶段：Agent 怎样把录制证据写成 Skill？

两项产品先以不同方式把证据交给 Agent：Claude 把多模态材料放进 Cowork 任务；Codex 让 Agent 查询本地文件的位置。

### Claude：把多模态材料组成一条 Cowork 消息

Claude 客户端把动作文字、关键帧、应用信息和旁白交给 Cowork。已有任务优先使用交错的文字与图片内容块；新建任务则携带文字消息和同一批图片。Cowork 是 Claude for Mac 的任务工作区，Agent 直接从本轮任务读取这些材料。下面这张图展示已有 Cowork 任务中的消息形态。

![已有 Cowork 任务中，Claude 把动作文字和关键图片交错放入消息](/blog/images/original/from-demonstration-to-skill/claude-agent-input.svg)

### Codex：让 Agent 查询结构化文本文件

Codex 的主要材料继续保存在 `session.json` 和 `events.jsonl` 中。用户通过原生控件停止录制后，产品让原对话继续一轮；Agent 随后查询录制状态，取得这些文件的位置。交接过程如下：

```text
录制已经结束，请继续处理。
→ Agent 查询录制状态
→ 取得 …/session.json 和 …/events.jsonl
→ 读取文件并创建 Skill
```

状态查询返回的是文件位置，不是整份事件日志。Agent 随后打开 `events.jsonl`，按顺序读取事件，并在需要时展开其中的 AX 文字。

![Codex Agent 通过本地路径打开 events.jsonl，读取事件与 AX 文字](/blog/images/original/from-demonstration-to-skill/codex-agent-input.svg)

### 两套产品怎样生成和保存 Skill？

取得证据后，Agent 会沿两条不同路径起草并保存 Skill：

![Claude 和 Codex 通过不同的生成指导与保存交互，把录制证据写成 Skill](/blog/images/original/from-demonstration-to-skill/evidence-to-skill.svg)

Claude 的 Record 流程用产品提示指导 Agent 解读演示和选择工具。主路径先展示可审阅的草案（proposal）；proposal 不可用时，流程回退到通用 `skill-creator`。用户可以用 `Save` 保存新 Skill；若录制内容与已有 Skill 重叠，也可以用 `Update` 更新它。proposal 只用于审阅和保存，不是生成器 Skill。

Codex 的 `record-and-replay` Skill 指导 Agent 读取事件、区分变量和处理歧义，再调用通用 `skill-creator` 组织、写入并校验文件；`skill-creator` 支持创建和更新 Skill。

### Agent 最终写出什么？

最终产物不是回放文件，而是一份给 Agent 读取的 `SKILL.md`。它需要写清何时使用、每次确认什么、怎样操作，以及如何判断完成。

![普通 Skill 以 SKILL.md 为核心，写明适用场景、可变输入、操作方法和成功标准](/blog/images/original/from-demonstration-to-skill/skill-anatomy.svg)

下面是一份完整的周报填报 Skill 示例：

```markdown
---
name: weekly-business-data-entry
description: 从每周报表读取本周金额，更新数据后台中的对应记录，并核验提交结果。用于每周经营数据填报。
---

# 每周经营数据填报

## 开始前确认

- 本周使用的报表和期间
- 周报中“本周金额”的位置
- 后台中需要更新的记录和字段

## 操作步骤

1. 打开指定的周报，找到“本周金额”和对应期间。
2. 打开数据后台中该期间的记录。
3. 找到“本周金额”字段，填写从周报读取的金额。
4. 提交更新。

## 完成标准

- 页面显示“提交成功”。
- 对应记录中的金额与周报一致。

如果金额位置、目标字段或记录不明确，先询问用户，不要猜测。
```

这份 Skill 将“读取本周金额、更新对应记录、核验结果”写成固定方法，将 `42,680`、本周报表和记录位置留作每次执行时确认的变量。

![Agent 从单次演示中提炼固定方法，把本次金额和位置改写为下次执行时再确认的变量](/blog/images/original/from-demonstration-to-skill/demo-to-rule.svg)

一次演示无法说明所有细节是否固定。例如，它不能证明金额所在的单元格每周不变。遇到这类歧义，Agent 应询问用户。

生成后，用户还要检查草案，确保 Agent 没有把这周的金额、单元格或文件路径写成固定规则。

保存只说明工作方法已经写好；是否能在新环境中成功执行，要到下一项任务中验证。

## 第三阶段：Skill 怎样在下一次任务中工作？

新的一周到了。金额变成 `43,210`，它在"九月周报"中换了行，后台里的"本周金额"字段也换了位置。下一次任务的核心上下文是保存后的 Skill。

![保存的 Skill、当前任务和产品编排层共同决定下一次执行](/blog/images/original/from-demonstration-to-skill/replay-execution.svg)

再次执行由三部分共同决定：Skill 规定目标、可变输入、步骤和成功标准；当前任务提供新的数据与页面；产品编排层加载 Skill，并提供浏览器、Computer Use、外部服务接口和相应权限。

Agent 可以先从表格读取 `43,210`，再操作后台并检查提交结果。工具或页面发生变化时，它会重新定位对象，而不是复现上周的坐标。

两边都没有逐事件播放旧录制的工具。Codex 虽以文本保存录制证据，执行时仍可使用 Computer Use；这正说明重新执行依靠 Skill 与当前工具，而不是独立的录制回放引擎。

录制器留下证据，产品把证据交给 Agent，Agent 写成 Skill；下一次任务中，Skill 与产品编排层共同指导执行。下面把这条链放回两套产品的内部组件中。

## 同一条主线背后的两套架构

两项产品最直观的架构差别，是录制器放在哪里。Claude 把录制编排放在 Mac 客户端内部；Codex 把采集和文件管理交给独立运行的 Computer Use 服务。

![Claude 的宿主内集成与 Codex 的独立录制服务](/blog/images/original/from-demonstration-to-skill/architecture-comparison.svg)

Claude 客户端管理开始、停止和临时录制状态，随应用安装的原生模块收集键鼠动作、连续画面和可选旁白。客户端整理出动作文字和关键帧，再组成包含真实图片的 Cowork 消息。用户从录制到查看草案，一直留在 Claude 的任务体系中。

Codex 的 Record & Replay 插件规定怎样发起、停止和处理录制。录制请求先到达本地桥接进程，再由桥接进程交给 Computer Use 服务。Computer Use 服务管理录制状态、原生控件和事件文件。按照这一协议，Agent 发起录制后应结束当前一轮对话；Computer Use 服务仍会继续记录桌面操作。

用户从原生控件停止后，产品让原对话继续一轮。Agent 随后查询录制状态，取得本地文件的位置并读取内容。控制请求经过本地桥接进程，录制证据则留在服务写出的文件中。

这套进程边界解释了第二阶段的交接差异。Claude 客户端先把输入和画面整理成多模态消息；Codex 服务边录边把语义事件写成文本文件，Agent 之后再从文件中归纳工作流。

两边最后都会回到普通的 Agent 与 Skill 流程。架构改变了材料如何采集、存放和交接，却没有把其中一边变成宏播放器。

## 安全边界：录制范围可能超过任务范围

前面的架构差异不仅决定材料的形式，也决定 Agent 可能看到什么。还是以周报填报为例：用户只想教会 Agent 登录后台、填写金额并确认结果。录制时，用户还会输入密码，屏幕旁边开着机密文件，并说出一句包含客户底价的旁白。

![用户只想演示登录和填报，录制证据却可能包含任务之外的信息](/blog/images/original/from-demonstration-to-skill/security-boundary-story.svg)

**键盘输入。** 密码框把字符显示成圆点时，Claude 的关键帧里也只有圆点。圆点显示由目标应用完成。若目标应用也开启了 macOS Secure Input，Claude 会把这段按键记作 `[secure input]`；否则，动作文字里仍可能出现真实输入。

Codex 的键盘事件也可能保留实际输入，并记录当时是否处于 Secure Input 状态；这个标记不等于输入文字已经被过滤。

**屏幕画面。** Claude 会从鼠标所在显示器挑选关键帧。只要机密文件出现在关键帧中，文件标题、客户名称、金额和正文片段就都可能随图片进入 Cowork。

当前已核验的 Codex 录制证据不包含截图。因此，文件只是出现在屏幕上时，不会作为图片进入材料。用户切换到该文件、点击控件或选择文字后，窗口标题、选中的文字和界面字段值仍可能写入事件。AX 快照中的 `fullTree` 还可能捕获前台窗口中任务范围之外的控件值，即使用户没有直接操作这些控件。

**语音旁白。** Claude 开启语音后，会把整段录音转成独立的旁白文字。录制时说出的客户名称、内部地址、账号或密码也可能出现在这段文字中；Secure Input 只影响键盘输入，不会处理语音。

**最终 Skill。** Codex 的生成指导要求 Agent 用占位符代替密码、验证码和 API 密钥。这可以避免它们原样写进最终 Skill，却不会删除原始录制中的内容。无论哪种产品，只要 Agent 把录制证据中的具体信息写进 `SKILL.md`，它们就会随 Skill 保存。

这些机制只能遮住部分敏感信息，不能保证录制证据只包含完成任务所需的内容。

## 结论：录制的是证据，复用的是方法

Codex Record & Replay 和 Claude Record a Skill 都先把一次桌面演示变成 Agent 可以理解的录制证据，再由 Agent 区分固定方法和本次数据，写成普通 Skill。下一次任务中，Agent 会根据新的数据和界面重新规划操作并检查结果，而不是重复旧坐标。

两者的关键差别在于 Agent 能看到什么、又怎样取得材料：Claude 接收 Cowork 图文消息，Codex 读取 Computer Use 服务保存的本地事件和 AX 快照。之后，两条路径重新汇合：Agent 都从证据中提炼方法，并依靠 Skill、当前任务以及产品编排层提供的工具和权限执行。

这也解释了录制证据为何可能包含任务范围之外的信息：两套录制机制按各自方式采集演示期间的输入、画面、界面状态或旁白，而不是只接收整理好的操作手册。任务之外的信息可能进入 Agent，甚至被写入最终 Skill。也就是说，"录制"决定 Agent 能看到哪些证据，"复用"则依靠 Agent 在新环境中重新执行方法。

## 官方来源

- [OpenAI：Record & Replay guide](https://learn.chatgpt.com/docs/extend/record-and-replay)
- [OpenAI：Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan/)
- [OpenAI 官方视频：Record & Replay in Codex](https://www.youtube.com/watch?v=ZK3JhU73W18)
- [Anthropic：How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Anthropic：Get started with Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)
- [Anthropic：Skills overview](https://claude.com/docs/skills/overview)
- [Anthropic：Creating custom skills](https://claude.com/docs/skills/how-to)
- [Anthropic：Let Claude use your computer in Cowork](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork)
