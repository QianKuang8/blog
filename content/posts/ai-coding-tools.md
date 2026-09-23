---
date: '2026-03-21T23:00:00+08:00'
lastmod: '2026-09-21T10:12:54+08:00'
title: "ccstatusline 配置笔记：在 Claude Code 中查看模型、上下文与 Git 状态"
summary: "保留一份包含模型、上下文长度、Git 分支和变更统计的个人状态栏配置，并说明启动、接入与恢复检查。"
description: "ccstatusline 的组件选择、历史 JSON 配置与 Claude Code 状态栏恢复步骤。"
tags: ["agentic-coding", "code-editing"]
categories: ["原创文章"]
author: "Qian"
isCJKLanguage: true
showToc: true
learning_status: done
---

在 Claude Code 终端里反复确认模型、上下文和 Git 状态，会打断正在进行的任务。这里保留一份 ccstatusline 配置，把这些信息放进同一行，便于以后恢复。

2026 年 9 月 21 日核对了项目 README 中的启动命令和配置入口，没有重新运行状态栏。下面的 JSON 来自原有个人配置，原记录未保存对应的 Claude Code、ccstatusline 和终端版本；恢复时需要检查当前版本是否仍接受这些字段。

## 一行里保留哪些信息

[ccstatusline](https://github.com/sirmalloc/ccstatusline) 用于定制 Claude Code CLI 的状态栏，提供交互式配置界面。下面保留的四项分别回答一个操作问题：

| 组件 | 查看目的 |
| --- | --- |
| Model | 确认当前使用的模型 |
| Context Length | 观察当前上下文长度；它不等于模型允许的最大窗口 |
| Git Branch | 确认正在操作的分支 |
| Git Changes | 查看工作区增删行统计，提醒自己检查差异 |

这些指标帮助定位当前状态。上下文长度不能说明模型是否记住了所有约束，Git 变更统计也不能代替差异审查或测试结果。

## 打开配置界面，再接入 Claude Code

先确认 Node.js 与 npm 可用，然后按项目 README 启动配置界面：

```bash
npx -y ccstatusline@latest
```

这条命令会通过 npm 获取并运行工具。`latest` 随发布时间变化，适合打开当前版本；需要复现旧环境时，应记录并固定实际使用的版本。

在界面中选择组件、排列顺序和颜色，再按工具提供的安装流程接入 Claude Code。打开 TUI 和在 Claude Code 中看到状态栏，是两个分别需要确认的结果。接入后进入一个已知 Git 仓库，检查模型、分支与变更是否对应当前会话。

## 保存的配置

下面保留原 JSON，包含四个组件、颜色以及 Powerline 布局设置。它适合作为恢复参考；如果当前版本的配置格式已经改变，先用 TUI 创建可工作的配置，再迁移组件与样式偏好。

```json
{
  "version": 3,
  "lines": [
    [
      {
        "id": "ed25e781-e11d-4a01-9b13-77ffbf4cf4b5",
        "type": "model",
        "backgroundColor": "bgGreen",
        "rawValue": false
      },
      {
        "id": "3",
        "type": "context-length",
        "color": "brightBlack",
        "rawValue": false
      },
      {
        "id": "5",
        "type": "git-branch",
        "color": "magenta"
      },
      {
        "id": "7",
        "type": "git-changes",
        "color": "yellow",
        "metadata": {
          "hideNoGit": "false"
        }
      }
    ],
    [],
    []
  ],
  "flexMode": "full-minus-40",
  "compactThreshold": 60,
  "colorLevel": 2,
  "defaultPadding": " ",
  "inheritSeparatorColors": false,
  "globalBold": false,
  "powerline": {
    "enabled": true,
    "separators": [""],
    "separatorInvertBackground": [false],
    "startCaps": [],
    "endCaps": [""],
    "theme": "solarized",
    "autoAlign": true
  }
}
```

## 恢复后检查显示与含义

先确认四个组件都有内容，再检查字符和分隔符是否正常。遇到空白、乱码或错位时，分别检查组件的数据来源、终端字体和布局宽度，避免一次修改全部设置。

最后记录工具版本、终端环境和实际显示结果。以后再次迁移时，这份记录能帮助区分格式变化、数据缺失和字体问题。

## 参考资料

- [ccstatusline 项目与启动说明](https://github.com/sirmalloc/ccstatusline)
- [ccstatusline 使用文档](https://github.com/sirmalloc/ccstatusline/blob/main/docs/USAGE.md)
