# 全站文章审查与重写记录

审查日期：2026-09-21。基线：`bfb7051a5f5b76ac1071287c7351af7dc71f8013`。

覆盖 `content/posts/` 全部 **87 篇**。以近期 GLM Infra Agent、Devin Fusion、Warp Skill 改进等文章的具体问题、连贯机制、证据归属和适用边界为参考。

## 处理结果

- **重写：66 篇**。
- **修订：11 篇**。
- **导航更新：4 篇**。
- **元数据：1 篇**。
- **保留：5 篇**。

6 月及以前的 60 篇全部重写。8—9 月的 27 篇中，6 篇重写、11 篇针对性修订、4 篇只同步文章改名后的导航文字、1 篇补来源标签，5 篇保留。

重写围绕各篇自己的问题重新组织正文，补足输入、机制、结果和限制；没有统一套用小标题，也没有把原文未报告的判断写成用户经历。保留文章路径和全部首次发布日期。正文、标题或摘要改动更新 `lastmod`，纯来源标签调整保留原时间。

## 发现并修正的主要问题

- 表达：反复使用“真正”“不是……而是……”“我的判断”，长段总结缺少具体信息，部分文章代写未经提供的个人体验。
- 机制：把编辑工具、缓存、上下文与多 Agent 方案写成口号，遗漏输入输出、失败恢复或执行条件。
- 事实：区分性能结果的分母与基线、原型和生产交付、讲者估算和已验证结果；纠正 Cursor 与课程中的讲者归因。
- 视频：纠正 Week 2 后半时间戳并同步来源记录；重写 Week 4 的 Connector 改造、Week 7 的迁移成本、Week 9 的实验与临床边界。
- 来源：为 Uber Arm 迁移补齐两份原文归档；说明开源生态 2.0 归档标题与正文错配，按实际正文解读。
- 维护：修复 Grill Me 定位链接；保留原 ccstatusline JSON；按当前文章标题同步 4 个专题和相关内链。

## 审校与验证

- 77 篇有实质正文写作的稿件均经过独立 reviewer 审查，返修后全部 PASS；逐篇证据见下表及同目录 JSON。Record & Replay 的独立验收限于本次历史范围声明。
- 其余 10 篇由主审逐篇阅读全文，核对原文关键论点、公开文档或文章固定版本边界，决定保留、导航更新或元数据整理。
- 首次发布日期、必需 frontmatter、时区和 `lastmod` 规则检查通过；旧文 60 篇无遗漏。
- Hugo 构建与 `scripts/check_site.py public` 通过。
- 桌面 1440×1100 浏览器遍历 87 篇：均为 HTTP 200，无页面横向溢出；触发懒加载后无损坏图片。另查看 8 篇代表文章的正文截图，覆盖长标题、代码、表格和既有图示。
- 14 份 PDF 的当前文件、固定 GitHub 提交版本与正式 Hugo 产物逐一按字节比对一致；PDF 文件与子模块指针未修改。视频原文、站点 PDF 和 GitHub 链接映射均已核对。

## 逐篇记录

| 文章 | 处理 | 原问题 / 保留理由 | 本次处理 |
| --- | --- | --- | --- |
| [维护这个 Hugo 博客：从本地写作到 GitHub Pages 发布](../../content/posts/build-blog-tips.md) | 重写 | 仅有零散命令，缺首次初始化、构建和上线验收。 | 按本站实际流程重组，解释日期、子模块、预览与正式产物。 |
| [初始化 Mac 开发环境：安装顺序与恢复检查](../../content/posts/init-mac.md) | 重写 | 软件逐项堆叠，缺使用顺序；非官方安装入口与固定版本易过期。 | 按准备、工具、语言、项目验证重组；改官方入口，保留未实测范围。 |
| [Uber 的 Arm 迁移：先打通构建，再推广到多架构运行](../../content/posts/uber-arm-migration.md) | 重写 | 两段摘要未解释迁移机制，缺历史原文归档。 | 补两份defuddle归档，解释构建依赖、双架构验证与渐进回退。 |
| [按任务选择 Skill：创建、开发、设计追问与仓库索引](../../content/posts/useful-skills.md) | 重写 | 只列名称与功能，缺选择依据；Grill Me路径失效。 | 按任务和预期产物组织，修复Grill Me路径，原样保留历史KB需求。 |
| [ccstatusline 配置笔记：在 Claude Code 中查看模型、上下文与 Git 状态](../../content/posts/ai-coding-tools.md) | 重写 | 功能宣传多于恢复步骤；上下文长度与窗口上限混淆。 | 围绕四项指标、TUI启动、接入及恢复验收组织；保留JSON。 |
| [Zed Edit Prediction：用局部重写预测下一次编辑](../../content/posts/zed-edit-prediction.md) | 重写 | 旧文重复使用真正/核心和第一人称赞赏；把局部重写泛化为编辑范式胜负，延迟与训练过程不完整。 | 围绕输入输出、保留契约、训练、延迟和交互重构；补清历史范围与模型裁判边界。 |
| [Continue Instinct：从编辑轨迹训练 Next Edit 模型](../../content/posts/continue-instinct.md) | 重写 | 反复拔高开源意义，未解释样本与梯度机制；速度和本地部署边界不清。 | 以样本构建、训练、质量和速度口径重组，去除代写个人态度。 |
| [Copilot Next Edit Suggestions：把一次修改接成后续编辑](../../content/posts/copilot-next-edit-suggestions.md) | 重写 | 套话和代写用户观点较多；将原型跨文件愿景、具体交互和研究方向混为稳定产品能力。 | 按编辑历史、建议粒度、序列体验与延迟重组，补足案例并划清原型边界。 |
| [Augment Next Edit：从编辑意图到跨文件修改](../../content/posts/augment-next-edit.md) | 重写 | 将合成编辑数据误概括为“不是 commit history”；未经归档支持的 session_id 案例；无依据断言定位层决定竞争胜负。 | 解释三层输入输出、两种检索职责和 diff 应用约束；删除未支撑案例与个人态度，保留发布时未来计划边界。 |
| [Cursor Instant Apply：用原文件加速完整重写](../../content/posts/cursor-instant-apply.md) | 重写 | 大量真正/我觉得句式，diff假设写得过实，缺数据构造及评估范围。 | 按输入输出、训练、推理与评估解释完整链路，保留历史原文链接。 |
| [Aider Unified Diff：编辑格式与补丁容错如何减少代码省略](../../content/posts/aider-unified-diffs.md) | 重写 | 反复拔高格式价值却遗漏关键实验；把格式选择写成通用因果结论。 | 补入无行号 hunk 机制、基准设计和量化结果，明确两套基准、组合方案及行为等价边界。 |
| [Assisted Generation：小模型草拟，大模型批量验证](../../content/posts/huggingface-assisted-generation.md) | 重写 | 把内存瓶颈写成所有场景定律；反复拔高“可变计算”，且暗示 token 不再经过大模型；历史限制未标明。 | 改为候选验证机制、长度调整与性能条件；澄清大模型仍验证全部接受位置，区分吞吐和单请求延迟。 |
| [Code Surgery：模型生成的修改怎样落到文件里](../../content/posts/code-surgery-edit-tools.md) | 重写 | 将不同工具归为单一演化轴，重复抽象handoff口号，缺部分成功与缩进机制。 | 按协议、定位、恢复、模型合并组织，说明方案非互斥并保留历史观察边界。 |
| [Building Effective Agents：按任务的不确定性选择编排方式](../../content/posts/building-effective-agents.md) | 重写 | 将模式清单写成固定升级路径，反复重复方法论，缺少模式适用条件和具体输入输出。 | 围绕控制流、动态拆解、反馈循环与 ACI 重写；纠正必须逐级升级的含义。 |
| [2025 年 Agent 产品与架构：从交互辅助到持续执行](../../content/posts/2025-ai-product-architecture-evolution.md) | 重写 | 把二手综述的行业判断直接写成事实；宣称 Copilot/ReAct 失效；名词堆叠和泛化个人判断。 | 按任务交付链组织；保留规划验证、编排、时序记忆与计费机制，明确统计示例假设和二手来源边界。 |
| [Agent Engineering：把生产轨迹接回评估与迭代](../../content/posts/agent-engineering-new-discipline.md) | 重写 | 以旧方法失灵制造对立，反复定义新学科，trace被写成直接解释内部决策。 | 围绕执行轨迹、分工、回归材料和上线范围重写。 |
| [Manus 上下文工程：缓存、外部记忆与长任务反馈](../../content/posts/manus-context-engineering.md) | 重写 | 缓存指标被绝对化，重复宏大论断；未说明工具约束接口条件、可恢复记忆条件及缓存与多样性关系。 | 按多轮输入成本、动作约束、可恢复压缩和下一轮反馈重组，保留历史时点。 |
| [Codex Agent Loop：工具结果如何进入下一轮推理](../../content/posts/unrolling-codex-agent-loop.md) | 重写 | 大篇幅赞赏 runtime 而缺调用对象说明；混淆手工摘要与后续 compact；“终止即完成”边界不清。 | 沿数据流重写；说明 call_id、SSE、无状态语义、缓存不缩窗口、压缩演进及产物验收。 |
| [Agentic Coding：把目标、代码修改与验证接成循环](../../content/posts/introduction-to-agentic-coding.md) | 重写 | 存在归档未提及的CLAUDE.md归因；终端与IDE对立过度；Rakuten被宣称普遍闭环证明。 | 删除无源归因，以API认证示例解释执行链，细分权限与验证，收窄案例结论。 |
| [从 Claude Code 到 Deep Agent：业务知识如何进入长任务](../../content/posts/agent-year-review-claude-code-to-deep-agent.md) | 重写 | 原标题把作者判断写成事实；代写个人认同；缺少产品示例和经验数据的证据限定。 | 聚焦专业验收、技能渐进加载、上下文分工和工具分层；标清行业收敛及触发率为作者观察。 |
| [Context Engineering：检查模型每一步实际看到了什么](../../content/posts/the-rise-of-context-engineering.md) | 重写 | 旧文凭空定位为 2026 工程现实；不断宣称“真正改写失败归因”，把作者经验写成通用结论。 | 用失败时输入复原串起动态上下文、三类故障和可观测性；给出明确标为应用说明的诊断例子。 |
| [Context Engineering：管理 Agent 每一步能看到的信息](../../content/posts/context-engineering-for-agents.md) | 重写 | 分类复述与内存隐喻重复，缺少write/select关系和隔离信息成本。 | 用保存取回、检索、压缩和交接解释完整信息流，区分正确性与相关性。 |
| [文件系统与 Agent 上下文：保存、检索和重新读取](../../content/posts/filesystems-for-context-engineering.md) | 重写 | 过度宣称文件系统最便宜最稳定和默认内存；把检索优势绝对化，遗漏自更新尚未解决。 | 按三种信息集合和保存/检索/使用链条重写，解释互补检索及工作记忆边界。 |
| [Cursor 动态上下文发现：把完整资料留在可检索文件里](../../content/posts/dynamic-context-discovery.md) | 重写 | 把少给上下文泛化为模型升级规律；46.9% 被用于推导质量提高；目录与工具发现的具体机制较浅。 | 逐场景解释静态索引到文件读取；保留摘要恢复条件、认证状态与统计口径。 |
| [CursorBench：把真实开发会话变成评测任务](../../content/posts/cursorbench.md) | 重写 | 标题绝对化真实会话与公开benchmark优劣，未区分内部任务分布、参考解与唯一答案。 | 按采样、评分、线上消融和复现解释，明确公开指标范围。 |
| [CLI Coding Agent 选型：从功能表读出运行边界](../../content/posts/every-cli-coding-agent-compared.md) | 重写 | 把历史清单写成当前行业结论，未说明核验范围；IDE/CLI 二分过度，缺少选型操作性。 | 加归档时点与未实测说明，改为功能到任务环节的比较方法，区分隔离/审批/恢复和 Agent/编排层。 |
| [Agentic Engineering 的八个层级：从上下文到后台协作](../../content/posts/the-8-levels-of-agentic-engineering.md) | 重写 | 把作者经验阶梯写成必经工程体系；弱化 Level 8 实验性与成本；第一人称认同重复。 | 用表格给完整八级地图，重点解释 codify、converse 验证、独立审查和后台交接成本。 |
| [减少人工读 diff，需要先建立哪些验证](../../content/posts/how-to-kill-the-code-review.md) | 重写 | 把作者激进主张写成确定趋势，未标客座立场与编辑异议；分层验证条件不足。 | 以spec产物、验证证据、权限与共同盲点组织，收窄取消审查结论。 |
| [Kilo 扩展重构：共享执行核心与并行任务管理](../../content/posts/we-completely-rebuilt-the-kilo-vs-code-extension.md) | 重写 | 预发布状态与迁移限制被省略；将子 Agent 和独立 worktree 会话混为自动编排；泛化行业未来。 | 按共享核心、三种并行、worktree、行级反馈展开，补 provider UI 与迁移限制。 |
| [SWE-bench Verified：测试错配与数据污染如何影响分数](../../content/posts/why-swe-bench-verified-no-longer-measures-frontier-coding-capabilities.md) | 重写 | 标题“失效”过于笼统；审计样本限制和污染实验方法不充分；将更换基准泛化为整个范式退场。 | 围绕评分契约重构，明确 138 子集分母、两类测试案例、污染证据与意图边界及 Pro 的局限。 |
| [Deep Agents 提分：从失败轨迹调整 Harness](../../content/posts/improving-deep-agents-with-harness-engineering.md) | 重写 | 已有机制较多但我觉得/核心重复，退出hook被称强制验证，预算优势归因不足。 | 按重复失败映射各中间件，区分提醒与验收，保留实验条件和完整数值。 |
| [Harness Engineering：让 Agent 读取约束并验证运行结果](../../content/posts/harness-engineering-leveraging-codex-in-an-agent-first-world.md) | 重写 | 叙述偏宏观，“人工直接出手视为失败”过度推演；百万行口径与局部性能目标需更明确。 | 围绕任务受阻、运行反馈、知识地图、可执行约束和持续清理重组，限定吞吐策略。 |
| [Claude Code 早期访谈：薄 Harness 怎样接入开发流程](../../content/posts/claude-code-anthropic-agent-terminal.md) | 重写 | 历史访谈未标明阶段，部分 RAG/安全和薄 harness 结论过强；删略了经验性质和模型失败例。 | 围绕分层、semantic lint、授权、搜索、验收重构；保留时间戳，区分估算、内部体验与实证。 |
| [Continuous AI：让仓库事件触发协作任务](../../content/posts/continuous-ai.md) | 重写 | 概念重复与平台愿景过多，缺触发到产物的机制及团队成本。 | 围绕工作流输入输出、平台分工、触发频率和可检查收益重写。 |
| [Cursor 团队访谈：预测编辑、应用修改与验证结果](../../content/posts/cursor-team-interview.md) | 重写 | 长文细节散而重复；将 Shadow Workspace 完整沙箱、跨文件等方向与既有能力混在一起。 | 完整阅读 14 万字符访谈后围绕预测/应用/验证三环重组，解释 cache warming 与 speculative edits，明确隐藏窗口不保存条件。 |
| [写清任务、边界与输出：Claude 提示工程指南解读](../../content/posts/prompt-engineering-best-practices.md) | 重写 | 模板判断和 API 比喻代替具体用法；将 prefill 引导说成格式保证；部分模型技巧未标历史版本。 | 以指标提取串起结果契约、示例、缺失值、链式拆分和验证；保留未实测及接口版本边界。 |
| [Claude Code Subagents：怎样拆分任务与交接结果](../../content/posts/subagents-in-claude-code.md) | 重写 | 独立上下文被等同客观、并行耗时表述过满，Hooks与subagent边界模糊。 | 重写任务契约、依赖、证据和自动化职责；补Stop hook一次阻止后放行的实际代码边界。 |
| [Claude Code Auto Mode：如何判断动作是否越过授权](../../content/posts/claude-code-auto-mode.md) | 重写 | 基本机制准确但偏赞同式复述；缺少 reasoning-blind 的信息损失、多 Agent 交接与样本量限制。 | 按输入/输出检查、权限分层、两阶段指标、交接与恢复重组；保留具体残余风险。 |
| [长任务 Harness：把生成、验收与返工连成循环](../../content/posts/harness-design-long-running-apps.md) | 重写 | 旧文漏掉评价器校准与中间版本偏好，容易让高分等同质量；6h/200 与单 Agent 比较未解释范围及预算混杂。 | 补四维评分条件、QA 调校、具体缺陷、代际 reset 演进和逐项消融；完整应用后 QA 可多轮返工。 |
| [读懂 LLM 架构差异：缓存、专家与长上下文的取舍](../../content/posts/big-llm-architecture-comparison.md) | 重写 | 旧文仅术语清单，未解释多数机制，也据此预言架构趋势。 | 完整阅读长原文后按缓存、历史状态、专家、训练稳定性重组，增加具体数字和比较条件。 |
| [LLM 开源生态图 2.0：先看筛选口径，再看项目变化](../../content/posts/llm-open-source-development.md) | 重写 | 直接将移出名单等同生态筛选，遗漏统计门槛变化；基础设施稳定性与行业趋势断言过强。 | 从方法论变化起笔，补 1.0/2.0 采样与门槛，再解释三层职责、指标与开放边界。 |
| [Harness 可视化：把仓库规则接回交付流程](../../content/posts/harness-engineering-visual-control.md) | 重写 | 原文短但旧解读多口号，混同看到配置与约束已经生效，结尾“控制面”无细化。 | 按反馈阶段和触发关系解释；增加明确标为本文分析的存在/接入/执行三层证据。 |
| [Harness 与 SDD：让任务约束能被找到、执行和验证](../../content/posts/harness-engineering-vs-sdd.md) | 重写 | 短文重复放大器比喻，遗漏原文跨服务案例与漂移机制，绝对化Spec必要性。 | 从错误码、导航、验证和规范漂移重组，区分作者实践与通用结论。 |
| [Agentic Coding 的边界：验收标准与审查带宽](../../content/posts/agentic-coding-boundary.md) | 重写 | 旧文过度抽象且漏掉 DRY/TDD 反论和具体登录例子；把作者训练数据判断当普遍事实。 | 加入语义复用、行为/回归测试、OTP 模拟实现与隐性知识实例，围绕交付总工作量组织。 |
| [2025 大模型开源生态快照：如何读懂项目热度变化](../../content/posts/llm-open-source-2-landscape.md) | 重写 | 旧文将热度变化升级为不可替代性/生死判断；忽略 2025 观察窗口和 OpenRank 入选门槛；扩展了归档未重点支持的生态链。 | 重组为方法口径、应用需求、基础设施依赖与使用边界；显式历史快照，去未核验收购新闻与性能夸张。；独立审校后明确归档标题与正文版本不一致，仅解释135项目正文快照，不采用标题出入榜数量。 |
| [Harrison Chase 谈长程 Agent：上下文、交接与可审查结果](../../content/posts/context-engineering-long-horizon-agents-langchain-harrison-chase.md) | 重写 | 旧文省略具体交接失败与来源时间点，将口头可靠性数值和趋势讲得过实。 | 基于完整转录围绕初稿、状态、交接、trace和同步异步工作重写，加关键时间链接。 |
| [唐杰谈领域大模型：通用能力、记忆与应用反馈](../../content/posts/domain-llm-pseudo-proposition.md) | 重写 | 旧文用 RAG/tools 等系统路线替换作者实际论点，并擅自预测专用模型减少，遗漏 AGI 未实现时领域模型长期存在的限定。 | 恢复作者领域数据进入主模型的长期主张与现实限定，区分记忆/学习/自评估，移除自创未来预测。 |
| [AI 研发度量：把规约、执行过程与验收结果连起来](../../content/posts/ai-native-software-engineering-observability-control.md) | 重写 | 原文若干指标倡议被当统一事实；“无人干预越长越好”的有效产出前提不够；规约格式和真实质量混同。 | 用问题-过程-结果映射解释指标，补规约/测试有效性、文字指令/可执行控制的层次。 |
| [Prompt Engineering Guide：从具体问题查找提示工程资料](../../content/posts/prompt-engineering-guide.md) | 重写 | 材料仅首页但旧文泛化成长周期指南结论，并代写个人判断。 | 改成短资源导读，写明实际归档范围，以问题驱动阅读作为明确建议。 |
| [Agentic AI Landscape：用三层地图定位项目](../../content/posts/llm-oss-landscape.md) | 重写 | 来源是短 README，旧文据此过度推导项目生存风险和基础链路优越性。 | 保持短文，补归档范围、代表性/适用性区别与 CSV/动态资料/issue 的阅读路径。 |
| [五个 Agent Skills：从需求澄清到可测试的实现](../../content/posts/five-agent-skills-i-use-every-day.md) | 重写 | 旧文主要概括流程闭环，缺少“代码能回答就先查”与深模块细节，作者实践被写为普遍效果。 | 按产物交接解释五技能；补纵向切片、依赖、单行为测试和深模块；明示未安装实测。 |
| [Claude Auto-Caching：怎样复用 Agent 的稳定上下文](../../content/posts/prompt-auto-caching-with-claude.md) | 重写 | 仅谈经济价值，未解释自动断点与历史状态区别；10%易被读成总成本折扣。 | 补充prefill/decode、断点前缀示例、自动化范围与费用口径，去除规模化必然论。 |
| [Claude Code 团队的 Skills 实践：把反复踩坑的经验变成任务包](../../content/posts/claude-code-how-we-use-skills.md) | 重写 | 泛称最值得读和最小单位，九类堆列却缺少具体机制；把 measuring 推导成原文已有完备效果评估。 | 以验证、runbook 和库参考解释边界，补配置/历史/升级数据风险和依赖管理限制，区分使用记录与质量证据。 |
| [Seeing Like an Agent：工具如何随模型能力调整](../../content/posts/claude-code-seeing-like-an-agent.md) | 重写 | 仅解读 AskUserQuestion，遗漏原文过半的 Todo/Tasks、搜索与 Guide；抽象“认知负担”未对应案例。 | 恢复四组实质案例并连接模型能力演进；明确提问等待、任务依赖与 Guide 上下文隔离。 |
| [Coding Agent 的六个组件怎样接成执行循环](../../content/posts/components-of-a-coding-agent.md) | 重写 | 用引擎类比代替机制，六组件缺输入输出，猜想暗示为模型可替代结论。 | 按执行链串联6组件，重点区分存储/输入、校验/语义正确、同步示例/并行收益。 |
| [拆解 skill-creator：分别验证触发、产物与改进效果](../../content/posts/anthropic-skill-creator-breakdown.md) | 重写 | 将评估流程拔高为自动自改进系统，触发与效果评估区别不够；test 用于选优仍被写成防过拟合保证。 | 分开任务基线/产物断言/比较分析/入口优化，增加示例数据非真实成绩和留出集参与选优的统计边界。 |
| [长程 Agent 的上下文设计：存储、发现、缓存与交接](../../content/posts/effective-agent-design.md) | 重写 | 旧文泛化环境为产品更强原因；offload/cache/isolate 概念合并过度；经验更新未解释不改权重与再评估。 | 按四个资源问题组织，明确三策略不同作用及交接代价，补 GEPA 与 context learning。 |
| [Claude Code 如何围绕稳定前缀设计缓存](../../content/posts/claude-code-prompt-caching-is-everything.md) | 重写 | 重复隐形地基口号，将不换模型写成普遍规则，未区分压缩调用与压缩后会话。 | 围绕前缀布局、状态更新、工具搜索、fork和整次成本重写，补权限与缓存分层。 |
| [Coding Agent 推理排障：两种 KV Cache 竞态如何污染输出](../../content/posts/scaling-pain-coding-agent-serving.md) | 重写 | 旧文基本事实正确但指标相关性与根因略混，LayerSplit 只有数字没有机制，多个异常率口径未充分分开。 | 重写完整时序链和两种同步约束，补 LayerSplit 所有权/广播/重叠机制，限定监控阈值与修复范围。 |
| [上下文工程的四个动作：写入、选择、压缩与隔离](../../content/posts/why-context-engineering-needed.md) | 重写 | 旧文把 2024 Kimi 个人经验写得像通用长度限制；不加条件重复 judge 不需要搜索证据；末尾多 Agent 预测被认同为路线。 | 按状态生命周期重构四动作，明确历史实验限制和评估器证据需求；区分存储、筛选、压缩和交接。 |
| [下一波 AI 的分水岭：组织能否兑现模型能力](../../content/posts/understanding-next-ai-wave.md) | 修订 | 重复表面/真正句式，结尾引入未定义系统兑现率。 | 简化为产品、端到端任务与交付的观察问题，保留三张图。 |
| [用 HTML 承接 Agent 输出：阅读、交互与结果回传](../../content/posts/claude-code-unreasonable-effectiveness-html.md) | 重写 | 虚构第一人称体验；把个人格式偏好写成普遍升级方向。 | 解释呈现、交互导出与产物衔接，保留生成时间和diff代价。 |
| [Claude Code 会话管理：继续、回退、压缩与委派怎样选择](../../content/posts/claude-code-session-management-1m-context.md) | 重写 | 虚构个人使用经历；压缩失败原因与回退收益绝对化。 | 按任务连续性比较五种操作；区分上下文回退与外部状态。 |
| [当代码生成越来越容易：智能体软件的价值转向可靠运行](../../content/posts/stanford-mse435-week-08-ai-coding-software-future.md) | 修订 | 开头与结尾重复拔高，自驾驶云设想容易被当现状。 | 精炼交付检查和主张边界，明确自驾驶云为设想。 |
| [美团 31 万行代码库重构：规范、迁移 SOP 与分层验收](../../content/posts/meituan-agent-ai-coding-refactor.md) | 重写 | 把AI看全、零排期和AI预审写成普遍保证，遗漏测试分工。 | 保留风险定向、分层契约、迁移SOP、预审和人工主导测试链。 |
| [代理时代的设计：执行更便宜，判断更昂贵](../../content/posts/agent-era-design.md) | 修订 | 开头和结论套话；瓶颈迁移被称作固定规律。 | 改成具体评审任务和完整迭代检查，保留三个设计案例。 |
| [高人才密度团队怎样招聘：岗位定义、人才地图与双向评估](../../content/posts/building-high-talent-density-teams.md) | 修订 | 标题与总结过强；经验框架被写成通用因果定律。 | 重写开头与结尾，解释样本和职责，增加推荐网络自身偏差。 |
| [企业专用化如何形成反馈闭环：Eval、上下文与运行框架](../../content/posts/stanford-mse435-week-06-enterprise-knowledge-intelligence.md) | 修订 | 标题与开头人为对立，六步结尾重复，产品在线更新像实现认证。 | 保留eval/reward/verifier和三层系统，强化讲者归因与更新验证。 |
| [沟通战略怎样落地：理解受众、直接触达与可信叙事](../../content/posts/communication-strategy-direct-narrative.md) | 修订 | 开头套话，结尾重复六点；文学转述被写成心理学证明。 | 围绕受众/主张/证据收束，明确小说属受访者复述。 |
| [GPU 经济：把推理硬件、任务成本与用户价值放在一起看](../../content/posts/stanford-mse435-week-02-gpu-economics.md) | 修订 | 后半时间戳整体偏早，100x/芯片设计/社会契约归因混淆，市场数字缺依据。 | 重写后半与索引、同步来源记录；区分Madra与Gerstner并去掉无源数字。 |
| [生成式 AI 的价值分布：怎样理解收入与利润的倒三角](../../content/posts/stanford-mse435-week-01-generative-ai-economics.md) | 修订 | 口述估算被摘要写成现状；结尾重复态度。 | 改问题与收束，注明历史估计及口述75%与图表重算不一致。 |
| [从电子到 Token：吉瓦级 AI 工厂的物理约束与经济回报](../../content/posts/stanford-mse435-week-03-ai-factories-gigawatt-infrastructure.md) | 修订 | 以能源过剩推导工作负载灵活性，把token服务当风险对冲；成本差异未说明。 | 重写边界分析，区分机房与IT成本、收入回收与利润。 |
| [企业 AI 怎样形成交付收益：Databricks 连接器的流程重构](../../content/posts/stanford-mse435-week-04-enterprise-ai-saas.md) | 重写 | 两天原型与九个月交付混比，三项流程改造误写，示例比例未标假设。 | 按输入缺口、原型/交付、三约束与三重构组织，补全结果及限制。 |
| [AI 基础设施的竞争单位：从名义算力到可交付智能的端到端系统](../../content/posts/stanford-mse435-week-05-ai-infrastructure-frontier-labs.md) | 修订 | 100GW被误标思想实验；推理与瓶颈规律表述过强。 | 校正愿景/即席估算/思想实验，按任务路径收束。 |
| [AI 生命科学的两层循环：分子设计如何连接实验验证](../../content/posts/stanford-mse435-week-09-ai-life-sciences.md) | 重写 | single-person pipeline归因错误，临床前四年像可整体省去，杰文斯推论过强。 | 按两层循环、设计迭代、实验需求、两类物理接口重写。 |
| [从前沿 API 到定制模型：推理成本、质量与控制权的取舍](../../content/posts/stanford-mse435-week-07-inference-cloud-ai-commercialization.md) | 重写 | 反方问题讲者错误，成本幅度和体验改进过强，API共享被等同可复制。 | 按质量/总成本/数据控制/推理平台重写，补讲者无内部数据边界。 |
| [从一次演示到可复用 Skill：Codex Record & Replay 与 Claude Record a Skill](../../content/posts/from-demonstration-to-skill.md) | 修订 | 实现比较没有固定客户端build号，当前措辞容易被当作新版能力保证。 | 增加2026年9月初观察范围，保留原有结构、示例和图。 |
| [从电脑活动到下一步行动：Computer History](../../content/posts/from-activity-to-action.md) | 导航更新 | 问题场景、三阶段机制、授权与数据边界清楚。 | 保留成熟解释与图示；仅按改名结果同步相关阅读标签。 |
| [Uber 软件工厂：围绕有效交付优化 Agent 成本](../../content/posts/uber-efficient-software-factory.md) | 导航更新 | 成本拆解、模型评测、工具轮询与上下文机制完整。 | 保留具体案例及统计口径，按文章改名同步相关阅读。 |
| [Claude Code 团队如何工作：目标委派、动态工作流与验证反馈](../../content/posts/how-claude-code-team-uses-claude-code.md) | 元数据 | 正文结构和证据边界成熟；缺官方发布者来源标签。 | 正文保留，补anthropic来源标签并保留lastmod。 |
| [从压缩历史到按需恢复：Codex 上下文压缩的新实验](../../content/posts/from-compaction-to-context-recovery.md) | 保留 | 固定源码commit和CLI版本，传统压缩/远端恢复/服务依赖分层清楚。 | 保留正文与全部图示。 |
| [Harness Engineering：用行为评估守住 Agent 的关键动作](../../content/posts/harness-engineering-behavioral-evaluations.md) | 导航更新 | 假设案例明确，行为断言与最终验收的证据层次清楚。 | 保留正文，按文章改名同步相关阅读。 |
| [Claude Platform 成本优化：缓存、指令与 effort 如何配合](../../content/posts/reducing-cost-and-improving-performance-with-claude-platform.md) | 保留 | 请求与任务成本分开，官方行为标了文档日期，假设案例明确。 | 保留正文，按文章改名同步相关阅读。 |
| [Warp 如何把团队反馈变成 Agent 的 Skill 改进](../../content/posts/how-warp-builds-self-improving-agents-on-claude.md) | 保留 | 任务Skill、改进Skill、反馈和合并生效分得清楚。 | 保留正文与检验建议。 |
| [Devin Fusion：双 Agent 的分工与成本](../../content/posts/cognition-local-fusion.md) | 保留 | 角色、上下文、假设委派与评测成本/分数范围清楚。 | 作为近期表达参考保留。 |
| [GPT-6 Astra 的指令整理：Skill 触发、上下文与完成边界](../../content/posts/rethinking-skills-and-prompts-for-gpt-6-astra.md) | 保留 | 原文建议与月报假设案例分开，触发/加载/验收解释连贯。 | 作为近期表达参考保留。 |
| [GLM 的 Infra Agent：用密集反馈优化推理基础设施](../../content/posts/glm-built-its-inference-infrastructure.md) | 导航更新 | 通过具体实验解释dense feedback，局部结果与端到端结果分开。 | 作为近期表达参考保留。 |

## 证据边界

- 未重新运行原文benchmark、商业客户实验或收费模型API。
- 视频依据仓库来源记录与既有PDF核对，没有重做全部字幕或重新生成PDF。
- Record & Replay内部实现没有固定客户端build号，本次补历史观察范围，未重新实测两客户端。
- Harrison长程Agent等历史网页归档包含视频转录，保留既有栏目，未伪造PDF或新增视频发布。

这些边界限制的是结论强度。历史案例保留其时间范围，没有用今天的产品状态替换原文的历史观察。文章上线后的部署结果由本次提交对应的 GitHub Pages workflow 单独验收。

详细记录：[逐篇来源核对与独立审校结果](2026-09-21-blog-audit.json)。
