# 文章队列

## 视频笔记领取说明

- 领取任务时，把状态改成 `进行中 — <agent 名称>`；一个 agent 同时只领取一篇。
- `可领取` 可以直接进入 `sources/video → PDF → 博文 → reviewer` 流程；`先修订` 或 `先补审校` 必须先关闭备注中的问题。
- 建议优先处理 Week 6。
- slug 作为文章、来源记录和 PDF 文件的稳定映射，除非发现冲突，不再修改。
- 发布完成并验证 Pages 后，从本文件移除对应条目。具体流程见 `WORKFLOW.md` 和 `BLOG_PROMPTS.md`。

## Stanford MS&E435 系列

- [ ] **生成式 AI 经济学：从技术供给到产业价值分配**
  - 状态：`可领取`
  - 原视频：[Economics of Generative AI](https://www.youtube.com/watch?v=LNSvp-9b-J0)
  - 来源目录：`/Users/bytedance/Documents/学习/生成式AI经济学_Stanford_MSE435_Week1`
  - slug：`stanford-mse435-week-01-generative-ai-economics`
  - tags：`视频笔记`、`行业动向`
  - 备注：21 页 PDF；review PASS；元数据齐全。

- [ ] **GPU 经济：从 Token 成本到 AI 基础设施回报**
  - 状态：`可领取`
  - 原视频：[The GPU Economy](https://www.youtube.com/watch?v=BBl8bNJP6ds)
  - 来源目录：`/Users/bytedance/Documents/学习/GPU经济_Stanford_MSE435_Week2`
  - slug：`stanford-mse435-week-02-gpu-economics`
  - tags：`视频笔记`、`model-engineering`、`行业动向`
  - 备注：最终 review PASS；使用 `output/pdf/GPU经济_课程笔记.pdf`，不要误用较小的旧 render 版或附加访谈素材。

- [x] **从电子到 Token：吉瓦级 AI 工厂的工程与经济学**
  - 状态：`已发布`
  - 原视频：[Building AI Factories](https://www.youtube.com/watch?v=GcCGzfKdCd0)
  - 来源目录：`/Users/bytedance/Documents/学习/AI工厂与吉瓦级基础设施_Stanford_MSE435_Week3`
  - slug：`stanford-mse435-week-03-ai-factories-gigawatt-infrastructure`
  - tags：`视频笔记`、`model-engineering`、`行业动向`
  - 备注：30 页 PDF；两轮 review PASS；Round 1 四项 Medium 已全部修正，Round 2 确认通过。

- [ ] **企业 AI 与软件即服务：SaaS 会消失，还是价值会重新上移？**
  - 状态：`可领取`
  - 原视频：[Enterprise AI and SaaS](https://www.youtube.com/watch?v=sRvrXL83N-c)
  - 来源目录：`/Users/bytedance/Documents/学习/企业AI与软件即服务_Ali_Ghodsi_Stanford_MSE435_Week4`
  - slug：`stanford-mse435-week-04-enterprise-ai-saas`
  - tags：`视频笔记`、`agent`、`行业动向`
  - 备注：23 页 PDF；review PASS；收入数字需保留“内部估算、未经独立审计”的边界。

- [ ] **AI 基础设施与前沿实验室：推理、能源与规模化实验的闭环**
  - 状态：`可领取`
  - 原视频：[Infrastructure, Capstone Case](https://www.youtube.com/watch?v=4k53z3Ysjg0)
  - 来源目录：`/Users/bytedance/Documents/学习/AI基础设施与前沿实验室案例_Stanford_MSE435_Week5`
  - slug：`stanford-mse435-week-05-ai-infrastructure-frontier-labs`
  - tags：`视频笔记`、`model-engineering`、`行业动向`
  - 备注：21 页 PDF；两轮 review PASS；Round 1 三项 Medium（Trainium 归因、电网风险、章节编号）已全部修正并通过复核。

- [x] **解锁企业内部知识：从通用模型到可验证的企业智能**
  - 状态：`已发布`
  - 原视频：[Enterprise Internal Knowledge](https://www.youtube.com/watch?v=LRGX-gTegVA)
  - 来源目录：`/Users/bytedance/Documents/学习/企业内部知识智能_Stanford_MSE435_Week6`
  - slug：`stanford-mse435-week-06-enterprise-knowledge-intelligence`
  - tags：`视频笔记`、`context-engineering`、`行业动向`
  - 备注：22 页 PDF；两轮 review PASS；素材成熟。

- [ ] **从定制模型到推理云：AI 应用商业化的基础设施选择**
  - 状态：`可领取`
  - 原视频：[Applications, Applied AI](https://www.youtube.com/watch?v=Qh7Oxvo5sJI)
  - 来源目录：`/Users/bytedance/Documents/学习/AI推理云与应用商业化_Baseten_Stanford_MSE435_Week7`
  - slug：`stanford-mse435-week-07-inference-cloud-ai-commercialization`
  - tags：`视频笔记`、`model-engineering`、`行业动向`
  - 备注：26 页 PDF；最终 review PASS；根目录 PDF 与 render 版逐字节一致，发布时选定一个作为源文件。

- [x] **AI 编程与软件未来：从一次性软件到 Agent-to-Agent 经济**
  - 状态：`已发布`
  - 原视频：[Applications, Coding AI](https://www.youtube.com/watch?v=HA7lZd7zk3M)
  - 来源目录：`/Users/bytedance/Documents/学习/AI编程与软件未来_Stanford_MSE435_Week8`
  - slug：`stanford-mse435-week-08-ai-coding-software-future`
  - tags：`视频笔记`、`agentic-coding`、`行业动向`
  - 备注：22 页 PDF；最终 review PASS；与现有博客主题最相关。

- [ ] **从分子 CAD 到自主湿实验室：AI 生命科学的下一步**
  - 状态：`可领取`
  - 原视频：[Applications, AI in Life Sciences](https://www.youtube.com/watch?v=nWKiJHKIZfo)
  - 来源目录：`/Users/bytedance/Documents/学习/AI生命科学_Stanford_MSE435_Week9`
  - slug：`stanford-mse435-week-09-ai-life-sciences`
  - tags：`视频笔记`、`model-engineering`、`行业动向`
  - 备注：22 页 PDF；review PASS；只使用 Stanford 主视频，避免混入 No Priors 附加素材。

## 独立访谈与演讲

- [x] **代理时代如何做设计：从确定性界面到协作式产品**
  - 状态：`已发布`
  - 原视频：[How To Design In The Agent Era](https://www.youtube.com/watch?v=P06RgnUKX_I)
  - 来源目录：`/Users/bytedance/Documents/学习/代理时代的设计_How_To_Design_In_The_Agent_Era`
  - slug：`agent-era-design`
  - tags：`视频笔记`、`agent`
  - 备注：32 页 PDF；Round 2 PASS；源 PDF 约 40.4 MB，按既定规则原样发布。

- [ ] **打造高人才密度团队：从招聘漏斗到人才系统**
  - 状态：`可领取`
  - 原视频：[The playbook for building high talent density teams](https://www.youtube.com/watch?v=zegYJ6dhIg4)
  - 来源目录：`/Users/bytedance/Documents/学习/打造高人才密度团队_Adam_Ward`
  - slug：`building-high-talent-density-teams`
  - tags：`视频笔记`
  - 备注：19 页 PDF；独立审校 PASS（无 High、无 Medium）；九章主线完整，经验数字边界清晰，ethical guardrails 到位。

- [ ] **从读懂房间到直接叙事：沟通战略如何形成影响力**
  - 状态：`可领取`
  - 原视频：[The Comms Strategist Behind Anduril, Shopify & Cognition](https://www.youtube.com/watch?v=DFImJfJGXl0)
  - 来源目录：`/Users/bytedance/Documents/学习/沟通战略与直接叙事_Lulu_Cheng_Meservey`
  - slug：`communication-strategy-direct-narrative`
  - tags：`视频笔记`
  - 备注：23 页 PDF；最终 review PASS；字幕为英文自动字幕，发布时明确标注。
��明确标注。
