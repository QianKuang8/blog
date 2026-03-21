---
date: '2026-03-21T23:00:00+08:00'
lastmod: '2026-03-21T23:00:00+08:00'
title: 'AI Coding 工具推荐'
summary: "记录一些好用的 AI Coding 相关工具"
description: "记录一些好用的 AI Coding 相关工具"
tags: ["ai-coding", "tools"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

记录一些好用的 AI Coding 相关工具。

## ccstatusline

Claude Code CLI 的状态栏美化工具，支持 Powerline 样式、多行状态栏、自定义 widgets 等。

![Demo](https://raw.githubusercontent.com/sirmalloc/ccstatusline/main/screenshots/demo.gif)

### 核心功能

- **Powerline 支持** - 箭头分隔符、主题、自定义字体
- **丰富的 Widgets** - 40+ 可选组件（Model、Git、Tokens、Context 等）
- **交互式配置** - 内置 TUI 配置界面
- **跨平台** - 支持 macOS、Linux、Windows

### 我常用的 Widgets

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
  "powerline": {
    "enabled": true,
    "separators": [""],
    "separatorInvertBackground": [false],
    "endCaps": [""],
    "autoAlign": true,
    "theme": "solarized"
  },
  "defaultPadding": " "
}
```

### 安装

```bash
npx -y ccstatusline@latest
```

- GitHub: [sirmalloc/ccstatusline](https://github.com/sirmalloc/ccstatusline)
