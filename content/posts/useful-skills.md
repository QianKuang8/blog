---
date: '2026-03-12T23:30:00+08:00'
lastmod: '2026-03-21T22:00:00+08:00'
title: '好用的Skills'
summary: "记录一些好用的Skills"
description: "记录一些好用的Skills"
tags: ["skills", "default"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

## 简介

Skills 是一种扩展机制，可以为 Claude 添加特定领域的知识和工作流程。这里记录一些好用的 Skills。

## Skill Creator

官方技能，用于创建、修改和改进 Claude Skills。

- GitHub: [anthropics/skills/skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)

## Superpowers

一个完整的软件开发工作流框架，包含多个可组合的 skills。核心流程：brainstorming → worktrees → planning → subagent execution → TDD → code review → merge。

主要包含的技能：
- **brainstorming** - 在写代码前进行设计讨论
- **test-driven-development** - RED-GREEN-REFACTOR 循环
- **systematic-debugging** - 系统性调试流程
- **writing-plans** - 编写详细实现计划
- **subagent-driven-development** - 派发子代理执行任务
- **requesting-code-review** - 代码审查
- **using-git-worktrees** - 使用 git worktree 隔离开发

- GitHub: [obra/superpowers](https://github.com/obra/superpowers)

## Grill Me

用于对计划或设计进行深度审查的技能。通过 relentless 的提问方式，逐个解决设计决策树中的每个分支，直到达成共识。对于每个问题，会提供推荐的答案。

- GitHub: [mattpocock/skills/grill-me](https://github.com/mattpocock/skills/tree/main/grill-me)

## GitHub KB

个人定制的 GitHub 仓库知识库管理技能，用于管理本地仓库索引和搜索 GitHub。

创建时的 prompt：

```
/skill-creator 请帮我做一个github-kb的技能
1.我的本地有一个github目录，就是当前文件夹，我希望你记住它，并且在其根目录创建CLAUDE.md, 每一个repo给一个一句话的摘要记录在里面。请在SKILL.md里用@引用这个文件
2.如果没有找到这个目录，询问用户，并更新自己的SKILL.md
3.当用户说下载一个repo，请使用git命令下载到这个目录，下载完后请更新CLAUDE.md
4.这个技能会在任何时候用户提到github或者repo，或者仓库时触发，并优先在本地目录寻找用户提到的仓库，并分析查询，回答用户的问题。
5.你可以充分使用gh命令，在github上搜索issue pr repository等来回答用户问题
```

## 参考资料

- [anthropics/skills - GitHub](https://github.com/anthropics/skills)
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Creating custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Agent Skills 官网](http://agentskills.io)
