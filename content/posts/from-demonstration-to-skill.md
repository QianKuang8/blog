---
date: '2026-09-03T16:49:48+08:00'
lastmod: '2026-09-03T17:02:21+08:00'
title: '录下操作之后，Agent 学到的不是坐标，而是方法'
summary: "Codex Record & Replay 与 Claude Record a Skill 都从一次演示中提炼可复用方法，但它们保存和交接证据的方式不同，也带来不同的安全边界。"
description: "从一次每周数据填报出发，拆解桌面演示如何变成 Skill、下一次任务为何不是宏回放，以及录制证据可能超出任务范围的问题。"
tags: ["agent", "harness-engineering"]
categories: ["原创文章"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

假设你每周都要完成一次数据填报：先从周报里找到本周金额，再打开数据后台，填进正确的记录，最后确认提交成功。金额每周都变，单元格和页面字段也可能移动，但任务目标始终相同。

过去，我们会把这套流程写成操作手册，或者录成依赖鼠标坐标的宏。现在，[Codex Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay) 和 [Claude Record a Skill](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) 提供了另一种路径：你亲自做一遍，Agent 观察这次演示，再把其中的方法整理成可复用的 Skill。

我的判断是，这类产品真正有价值的部分不在“录制”，而在录制之后的抽象。录制器留下的是供 Agent 理解的证据；Skill 保存的是任务方法；下一次执行时，Agent 还要结合新的输入、当前界面和可用工具重新完成任务。它不是把旧动作再播放一遍。

![每周从周报读取当前金额，填入数据后台并确认提交成功](/blog/images/original/from-demonstration-to-skill/task-scenario.svg)

## 录下来，不等于录制宏

宏保存的是这一次怎样操作：在某个坐标点击，输入一个固定值，再点击另一个坐标。只要窗口尺寸、数据或页面布局变化，旧轨迹就可能失效。

Skill 要保存的是另一层内容：到哪里找本周金额，怎样确认目标记录，提交后用什么结果判断任务完成。假设这周的金额是 `42,680`，下周变成 `43,210`，Skill 不应该记住两个数字中的任何一个；它应该要求 Agent 每次重新读取“本周金额”。

这也是两项产品共同的主线：

> 录制并留下证据 → Agent 理解证据并生成 Skill → 在新任务中使用 Skill

![用户录下演示并留下证据，Agent 从证据中提炼 Skill，随后在新任务中使用这套方法](/blog/images/original/from-demonstration-to-skill/end-to-end-overview.svg)

OpenAI 的官方说明强调，适合录制的流程应当有相对稳定的步骤和清楚的成功标准。录制结束后，Agent 起草的 Skill 会写明何时使用、需要哪些输入、执行哪些步骤，以及怎样验证结果。这里已经能看出它和宏的差别：产品关心的不只是动作，还关心输入和验收。

## Agent 看见的不是同一种证据

Codex 和 Claude 都需要先理解一次具体演示，但它们交给 Agent 的材料不同。

| | Claude Record a Skill | Codex Record & Replay |
|---|---|---|
| 主要证据 | 动作文字、筛选后的关键帧、应用信息和可选旁白 | 事件、AX 界面快照和本地 JSON / JSONL 文件 |
| 交接方式 | 把图文材料组成 Cowork 任务内容 | Agent 查询录制状态，取得文件路径后读取 |
| 擅长表达 | 控件外观、页面变化和用户口头说明 | 控件名称、值、层级和事件顺序 |
| 需要警惕 | 画面和旁白可能带入任务外信息 | 输入文字和 AX 界面值可能超过直接操作范围 |

![同一次演示，在 Claude 和 Codex 中变成两类不同的录制证据](/blog/images/original/from-demonstration-to-skill/what-is-recorded.svg)

Claude 会把连续输入整理成一次键入，把鼠标按下、移动和松开整理成一次拖拽，并保留能够说明界面变化的画面。用户开启麦克风后，旁白还可以补充“为什么跳过这一步”或“遇到两种情况时怎样选择”这类只看屏幕很难推断的信息。Anthropic 的说明同时指出，视频和音频不会被保留，Cowork 任务中会留下从录制中选出的截图。

以下文件结构和交接路径来自当前版本的研究观察，不代表长期产品承诺。Codex 当前的录制证据主要落在本地文件中。`session.json` 保存会话信息和材料位置，`events.jsonl` 按时间追加应用切换、窗口变化、点击、输入、文本选择和诊断事件。事件还可以携带 macOS Accessibility（AX）信息，用控件标题、值和层级描述界面。于是一次点击不只是“鼠标在这里按下”，还可能带有“浏览器窗口中标题为‘提交’的按钮”这样的语义。

两种材料没有绝对优劣。图片更容易保留视觉状态，结构化事件更容易检索和归纳。真正重要的是：它们此时仍是一包关于“这一次发生了什么”的证据，还不是可复用方法。

## 从证据到方法，最难的是区分固定项和变量

Agent 拿到录制证据后，需要回答四个问题：这套方法适用于什么任务，每次要确认哪些输入，应该怎样操作，以及什么结果才算完成。最终产物通常是一份以 `SKILL.md` 为核心的普通 Skill。

周报填报可以被整理成下面这样：

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

1. 打开指定周报，找到“本周金额”和对应期间。
2. 打开数据后台中该期间的记录。
3. 找到“本周金额”字段，填写从周报读取的金额。
4. 提交更新。

## 完成标准

- 页面显示“提交成功”。
- 对应记录中的金额与周报一致。

如果金额位置、目标字段或记录不明确，先询问用户，不要猜测。
```

![Agent 从单次演示中提炼固定方法，把本次金额和位置改写为下次再确认的变量](/blog/images/original/from-demonstration-to-skill/demo-to-rule.svg)

这一步最容易犯的错，是把偶然细节误写成永久规则。一次演示只能证明“这次金额在 B7”，不能证明它每周都在 B7；只能证明“这次按钮位于右下角”，不能证明页面永远不会改版。Agent 必须把能确认的任务结构写进 Skill，把不确定的部分留作每次执行时重新查找或向用户确认。

完成标准同样关键。点击“提交”只说明按钮被按下；出现成功提示，并且记录里的金额与周报一致，才说明任务完成。一个只记录步骤、不记录验收条件的 Skill，最多复用了动作，没有复用责任边界。

生成后仍需要用户审阅。用户要检查 Agent 有没有把本周金额、临时文件路径、一次性的页面位置，甚至敏感信息写成固定规则。保存成功也只说明方法已经写好；它能否在新环境中执行，要到下一次任务里验证。

## 所谓 Replay，其实是带着方法重新做一次

新的一周到来后，Agent 获得三类上下文：保存后的 Skill、这次任务的新数据，以及产品编排层提供的工具、权限和运行规则。页面变化时，它重新定位对象；输入变化时，它重新读取数据；执行结束后，它按照 Skill 的完成标准检查结果。

![保存的 Skill、当前任务和产品编排层共同决定下一次执行](/blog/images/original/from-demonstration-to-skill/replay-execution.svg)

从目前已核验的机制看，两边都没有依靠一套独立工具逐事件播放旧录制。OpenAI 的官方文档也把 Replay 描述为：在新对话中使用生成的 Skill，提供本次变化的值，再让产品使用当前环境里的 Computer Use、浏览器操作或已安装插件完成工作流。

这意味着，执行能力不只来自 Skill。Skill 规定方法，但产品还要负责发现并加载它，选择当前可用的工具，处理权限和错误，并把结果交回 Agent 验收。只复制一份 `SKILL.md`，并不能保证另一套环境拥有相同工具，更不能保证任务一定成功。

两项产品的架构差异主要影响证据怎样采集、存放和交接。Claude 把录制编排放在 Mac 客户端与 Cowork 任务中；Codex 把采集和文件管理交给独立的 Computer Use 服务，Agent 在录制结束后的新一轮中取得材料。两条路径最后都会回到普通的 Agent 与 Skill 流程。

![Claude 的宿主内集成与 Codex 的独立录制服务](/blog/images/original/from-demonstration-to-skill/architecture-comparison.svg)

## 录制范围不会自动等于任务范围

录制产品还有一个更容易被忽略的问题：用户心里的任务边界，和录制器实际采集的证据边界并不相同。

用户只是想演示登录后台、填写金额并确认结果，但录制期间可能还输入了密码，屏幕旁边开着机密文件，旁白里提到了客户底价。它们与任务方法无关，却可能进入录制材料。

![用户只想演示登录和填报，录制证据却可能包含任务之外的信息](/blog/images/original/from-demonstration-to-skill/security-boundary-story.svg)

**键盘输入。** 密码框显示圆点，只能说明界面没有把字符画出来。Claude 在 macOS Secure Input 生效时会把对应按键标为安全输入；否则，动作文字仍可能包含实际键入。Codex 的键盘事件也可能保留输入，并记录当时是否处于 Secure Input 状态；这个状态标记不等于文字已经被过滤。

**屏幕与界面。** Claude 的录制会产生屏幕材料，官方也明确提醒关闭不希望被捕获的文件、应用和对话。当前已核验的 Codex 录制证据不包含截图，但窗口标题、选中文字和 AX 控件值仍可能进入事件。较完整的 AX 界面树还可能带入前台窗口里没有被直接操作的字段。

**语音旁白。** 旁白能解释意图，也能把客户名称、内部地址、账号或密码转成文字。Secure Input 只处理键盘输入，不会保护说出口的信息。

**最终 Skill。** Codex 的生成指导要求用占位符替换密码、验证码和 API Key，避免它们原样进入 `SKILL.md`。这不会反向删除原始录制证据。录制材料和最终 Skill 是两个独立的数据边界，不能只审查后者。

OpenAI 建议录制时避免秘密和敏感数据，Anthropic 也提醒用户关闭不希望被捕获的内容。这不是普通的使用技巧，而是录制式工作流的基本前提：证据越丰富，Agent 越容易理解任务；同一批证据也越可能超过任务所需范围。

## 我的判断：核心不是录制器，而是抽象与验收

Record & Replay 和 Record a Skill 降低了“把经验写成说明”的门槛，但没有消除知识抽象本身的难度。一次演示里混合着目标、方法、临时数据、界面偶然性和用户没有说出口的判断。产品必须从这些材料中分出哪些应该固化，哪些应该每次重查，哪些必须追问。

因此，判断一项录制功能是否可靠，我更关心三件事：它能否把固定方法和本次数据分开，能否把成功标准写进 Skill，以及能否让用户清楚地审阅录制证据与最终产物。录制得更完整，只解决了“看见什么”；真正的复用质量取决于 Agent “怎样理解”，以及下一次任务“怎样证明做对了”。

对使用者来说，最稳妥的流程也很朴素：录制前收起无关和敏感内容；生成后检查变量、歧义与完成标准；保存后用一组变化过的数据做一次真实验证。这样得到的才是一套可复用方法，而不是一份看起来很像 Skill 的旧操作记录。

## 参考资料

- [OpenAI：Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay)
- [OpenAI 官方视频：Record & Replay in Codex](https://www.youtube.com/watch?v=ZK3JhU73W18)
- [Anthropic：How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Anthropic：Skills overview](https://claude.com/docs/skills/overview)
- [Anthropic：Creating custom skills](https://claude.com/docs/skills/how-to)
- [Anthropic：Let Claude use your computer in Cowork](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork)
