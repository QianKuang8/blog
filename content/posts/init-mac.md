---
date: '2024-12-10T17:22:55+08:00'
lastmod: '2026-09-21T10:11:16+08:00'
title: "初始化 Mac 开发环境：安装顺序与恢复检查"
summary: "按基础工具、终端编辑器、语言环境和效率工具整理 Mac 初始化清单，说明每一步如何检查，以及哪些旧记录尚未复核。"
description: "Mac 开发环境恢复清单：Homebrew、Node.js、Go、编辑器与常用效率工具。"
tags: ["init"]
categories: ["原创文章"]
author: "Qian"
isCJKLanguage: true
showToc: true
---

重装 Mac 时，最容易遗漏的通常是开发环境之间的连接：终端能否找到编译器，项目用了哪个语言版本，编辑器能否复用同一套工具链。这里把原有安装清单按使用顺序整理，先恢复能工作的环境，再补充日常工具。

2026 年 9 月 21 日修订时核对了 Homebrew、nvm 与 Go 的官方入口；没有在全新系统上重跑整套安装。原记录未保存 macOS 版本、芯片架构和各工具版本，因此下文是恢复清单，具体兼容性仍应以目标机器和软件官方说明为准。

## 先确认系统，再配置基础工具

开始前记录系统版本与处理器架构：

```bash
sw_vers
uname -m
```

这两项信息决定应该下载哪个安装包，也方便排查命令行里混入另一种架构的问题。安装 [Homebrew](https://brew.sh/) 时按官方页面的步骤操作，并完成安装器最后输出的 shell 配置。Apple Silicon 的默认前缀是 `/opt/homebrew`，Intel Mac 通常是 `/usr/local`；不要把另一台机器的路径原样复制过来。

安装后新开一个终端，检查命令是否可见：

```bash
command -v brew
brew --version
git --version
```

这里检查的是基础工具能否被当前 shell 找到。具体项目能否构建，还要在语言环境准备好后单独验证。

## 终端和编辑器按工作习惯选择

终端先保留一个主力，避免同时迁移多套快捷键和 shell 配置。原清单中的候选是 [iTerm2](https://iterm2.com/)、[Warp](https://www.warp.dev/) 和 [cmux](https://cmux.com/)；cmux 的项目资料也可从 [GitHub](https://github.com/manaflow-ai/cmux) 查阅。选择时关注标签与分屏、通知、远程连接和已有配置是否便于恢复。

Shell 辅助插件按需加入：[zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md) 用于命令高亮，[zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) 用于输入建议。先确认基础 shell 正常，再逐项加插件，出问题时更容易定位。

编辑器按用途保留：

| 工具 | 清单中的用途 |
| --- | --- |
| [Visual Studio Code](https://code.visualstudio.com/) | 项目开发与扩展环境 |
| [Sublime Text](https://www.sublimetext.com/) | 快速查看、编辑文本 |
| [Typora](https://typora.io/) | Markdown 写作 |
| [Sequel Ace](https://github.com/Sequel-Ace/Sequel-Ace) | MySQL / MariaDB 数据库客户端 |
| [SourceGit](https://sourcegit-scm.github.io/) | 图形化查看 Git 历史与差异 |

恢复编辑器后，打开一个真实项目，检查终端、格式化工具和项目命令能否正常运行。只启动应用还不足以确认开发环境完整。

## 语言版本跟着项目走

Node.js 使用 [nvm 官方仓库](https://github.com/nvm-sh/nvm) 的安装说明。没有项目约束时，可以安装 LTS；已有项目则优先遵循它记录的 Node.js 版本：

```bash
nvm install --lts
node --version
npm --version
```

旧清单还使用过 [gvm](https://github.com/moovweb/gvm) 管理 Go。是否保留版本管理器，取决于是否需要同时维护多个 Go 版本；单一版本也可以按 [Go 官方安装说明](https://go.dev/doc/install) 配置。不要沿用文章里某个固定版本号作为所有项目的默认值，先看项目的 `go.mod` 与工具链约定，再检查：

```bash
go version
go env GOARCH GOOS
```

语言命令可用以后，再运行项目自己的构建或测试。这样可以区分“工具已经安装”和“项目依赖能够工作”。

## 效率工具按实际缺口补充

以下保留原清单的工具入口，便于回查；它们不是必须全部安装的一组依赖。

| 使用任务 | 工具入口 |
| --- | --- |
| 截图与贴图 | [Snipaste](https://www.snipaste.com/) |
| 从 Finder 目录打开终端 | [Go2Shell](https://zipzapmac.com/Go2Shell) |
| 整理菜单栏图标 | [Hidden Bar](https://github.com/dwarvesf/hidden) |
| 查看系统资源 | [Stats](https://github.com/exelban/stats) |
| 调整滚轮方向 | [Scroll Reverser](https://pilotmoon.com/scrollreverser/) |
| 窗口排列 | [Rectangle](https://github.com/rxhanson/Rectangle) |
| 快速调用小工具 | [uTools](https://www.u.tools/)，按需配置 JSON、diff、翻译 |
| PDF 阅读 | [Skim](https://skim-app.sourceforge.io/) |
| Android 投屏 | [Tango](https://app.tangoapp.dev/) |

输入法则确认中英文切换快捷键符合习惯。浏览器扩展原记录包含 Screenity、沉浸式翻译与 Proxy SwitchyOmega 3（ZeroOmega）；标签页收纳工具曾记为“OneTap”，名称及具体扩展未核实，暂不把它作为确定的安装项。

## 留下一份下次能复用的记录

完成初始化后，记录系统版本、架构、语言版本和实际运行过的项目命令。若某一步依赖代理、特定权限或单独的 shell 配置，也一并记下。下一次迁移就能先恢复这些已确认的前提，再决定是否继续沿用原来的应用清单。
