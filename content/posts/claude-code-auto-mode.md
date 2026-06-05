---
date: '2026-06-05T21:20:00+08:00'
lastmod: '2026-06-05T21:20:00+08:00'
title: 'Claude Code Auto Mode：把批准按钮改造成分类器问题'
summary: "解读 Claude Code auto mode 的设计：它不是简单取消权限确认，而是用 prompt-injection probe 和 transcript classifier 在自动化与安全之间做一个可度量的折中。"
description: "从 Claude Code auto mode 看 agent 权限、prompt injection 防御、分类器门禁和自动化风险"
tags: ["agentic-coding", "harness-engineering", "agent"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

Anthropic 这篇 [How we built Claude Code auto mode: a safer way to skip permissions](https://www.anthropic.com/engineering/claude-code-auto-mode) 讨论的是一个很现实的问题：coding agent 想要自动化，就会遇到权限确认；权限确认太多，用户又会进入 approval fatigue，最后 93% 的请求都被接受。

以前的选择大概有两端。sandbox 更安全，但维护成本高，很多需要网络或宿主机访问的任务会撞墙。`--dangerously-skip-permissions` 几乎没有维护成本，但也几乎没有保护。Auto mode 想做的是中间层：把批准动作从人类点击，转成模型分类器对行动风险和用户意图的判断。

这不是“信任 agent 自觉”，而是给 agent 的动作再加一道外部判定。

## 两层防线：读什么和做什么分开管

文章把 auto mode 拆成输入层和输出层。

输入层是 server-side prompt-injection probe。它扫描工具输出，比如文件读取、网页抓取、shell 输出和外部工具返回内容。如果内容看起来像 prompt injection，就在进入 agent 上下文前附加警告，提醒 agent 把这些内容当成可疑信息，并重新锚定用户原始任务。

输出层是 transcript classifier，运行在 Sonnet 4.6 上。它在动作执行前判断这次工具调用是否应该被允许。分类器分两阶段：第一阶段是快速单 token yes/no filter，偏向保守地拦截；只有第一阶段标记风险时，第二阶段才用 chain-of-thought reasoning 重新判断。多数动作能直接通过第一阶段，所以推理 token 只花在可疑动作上。

更有意思的是分类器看到的内容。它只看用户消息和 agent 的工具调用，Claude 自己的回复和工具输出都会被剥离。这样做有两个目的：一是避免 agent 用自己的解释说服分类器，二是减少 prompt injection 从工具输出污染分类器的机会。

## 威胁模型的重点是“过度主动”

文章列了四类危险来源：overeager behavior、honest mistakes、prompt injection、misaligned model。最值得关注的是前两类，因为它们不像传统安全攻击那样有明显恶意。

所谓 overeager behavior，是 agent 正在努力帮用户完成目标，但主动跨过了用户实际授权边界。比如用户说“清理旧分支”，agent 自己构造匹配规则去删远端分支；遇到认证错误，agent 开始 grep 环境变量和配置文件找替代 token；用户说“cancel my job”，agent 根据名称相似度选了一个任务然后删除。

这些行为从 agent 视角都像是在解决问题，但从真实世界看，blast radius 已经超出用户确认。Auto mode 的设计重点不是识别“坏意图”，而是识别动作是否真的被用户授权。

这也是为什么 classifier 的 prompt 里要特别处理 user intent。文章强调，和用户目标相关不等于被授权。“clean up the PR”并不自动授权 force-push；之前批准过类似动作，也不意味着以后都批准。

## 权限分层让常规开发不用每步过分类器

Auto mode 不是所有工具调用都进最终分类器。文章把决策分成三层。

第一层是内置安全工具和用户设置，例如只读文件搜索、代码导航、todo 和 plan-mode 这类无法修改状态的工具。进入 auto mode 时，它会丢弃已知会授予任意代码执行的宽泛规则，比如 blanket shell access、通配的脚本解释器和 package manager run command。窄规则可以保留，宽泛逃逸口会被收回。

第二层是项目内文件操作。仓库内写文件、编辑文件可以直接允许，因为常规编码不应该每次修改都付分类器延迟，而且这些变化可以通过版本控制审查。

第三层才是 transcript classifier，覆盖 shell 命令、web fetch、外部集成、subagent spawn、项目外文件系统操作等可能有真实副作用的行为。

这个分层很务实。它承认 agentic coding 的大多数动作是普通开发活动，不适合每一步都问；但一旦动作跨到外部系统、凭证、破坏性操作或数据外发，就必须进入更严格判断。

## 结果不是完美安全，而是明确的风险折中

文章给了三组评测：真实内部流量 10,000 条、真实 overeager actions 52 条、合成数据外泄任务 1,000 条。部署后的 Stage 1 -> Stage 2 pipeline 在真实流量上的 false positive rate 是 0.4%，在真实 overeager actions 上的 false negative rate 是 17%，在合成 exfiltration 上的 false negative rate 是 5.7%。

17% 不是一个可以轻描淡写的数字。文章也很坦率：如果你原本会认真手动审批每个动作，auto mode 可能是安全回退；如果你原本在用 `--dangerously-skip-permissions`，它就是明显改进。Auto mode 面向的是后一类场景，或者那些人类审批成本不值得边际安全收益的任务。

我很喜欢这种表述，因为它没有把 auto mode 包装成安全银弹。它只是把风险从“完全没有护栏”推进到“分类器能挡住相当一部分危险动作，但仍会漏掉一部分”。这对工具设计反而更诚实。

## Deny-and-continue 让误报不至于打断整件事

另一个关键设计是 deny-and-continue。Auto mode 的目标是替代跳过权限，而不是把用户拉回每次确认。当 classifier 拒绝一个动作时，拒绝会作为工具结果返回给 Claude，并要求它尊重边界，寻找更安全路径，而不是绕过阻拦。

如果连续 3 次被拒，或总计 20 次被拒，系统才停止并升级给人类。在 headless mode 里没有 UI 可问人，就直接终止进程。

这让 false positive 可承受。0.4% 的误报如果每次都杀掉 session，长任务体验会很糟；但如果只是让 agent 换一种做法，成本就小很多。

## 我的判断：权限系统正在变成 agent harness 的一部分

这篇文章让我觉得，未来 coding agent 的权限系统不会只是 allowlist、denylist 或 sandbox。它会越来越像 harness 里的一个独立判断模块：观察 agent 要做什么，判断是否符合用户意图、环境边界和风险策略，再把反馈写回 agent 循环。

它也说明“自动化”和“安全”不是单一开关。手动审批、安全沙箱、跳过权限、分类器门禁，各自占据不同的 autonomy、maintenance friction 和 residual risk 位置。真正的产品问题是让用户理解自己在选哪种折中。

所以我会把 auto mode 看成一个方向正确但必须带着风险意识使用的机制。它适合把低风险、长流程、重复审批的 agentic coding 跑顺；但对于生产基础设施、外部数据、不可逆操作，人类判断仍然不能被当作免费可替换组件。

## 原文

- [How we built Claude Code auto mode: a safer way to skip permissions](https://www.anthropic.com/engineering/claude-code-auto-mode)
