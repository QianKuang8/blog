---
date: '2026-03-21T23:00:00+08:00'
lastmod: '2026-09-08T15:34:44+08:00'
title: 'ccstatusline：我的 Claude Code 状态栏配置'
summary: "记录我在 Claude Code CLI 中使用的 ccstatusline 配置，显示模型、上下文长度和 Git 变更。"
description: "ccstatusline 的常用 Widgets、个人配置与安装命令。"
tags: ["agentic-coding", "code-editing"]
categories: ["原创文章"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

这里保存我在 Claude Code CLI 中使用的 ccstatusline 配置，方便以后恢复状态栏。实际核验日期和对应的 Claude Code、ccstatusline、终端环境版本尚未记录。

## ccstatusline

Claude Code CLI 的状态栏美化工具，支持 Powerline 样式、多行状态栏、自定义 widgets 等。

![Demo](https://raw.githubusercontent.com/sirmalloc/ccstatusline/main/screenshots/demo.gif)

### 核心功能

- **Powerline 支持** - 箭头分隔符、主题、自定义字体
- **丰富的 Widgets** - 40+ 可选组件（Model、Git、Tokens、Context 等）
- **交互式配置** - 内置 TUI 配置界面
- **跨平台** - 支持 macOS、Linux、Windows

### 我常用的 Widgets

- **Model** - 显示当前使用的模型名称
- **Context Length** - 显示当前上下文窗口大小
- **Git Branch** - 显示当前 git 分支
- **Git Changes** - 显示 git 变更统计（+insertions, -deletions）

### 我的配置

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

### 安装

```bash
npx -y ccstatusline@latest
```

- GitHub: [sirmalloc/ccstatusline](https://github.com/sirmalloc/ccstatusline)
