---
date: '2024-12-10T17:22:55+08:00'
lastmod: '2026-03-11T23:00:00+08:00'
title: '初始化Mac系统'
summary: "记录一下初始化一个Mac系统需要干些什么"
description: "记录一下初始化一个Mac系统需要干些什么"
tags: ["init","default"]
author: "Qian"
isCJKLanguage: true
showToc: true
---
# 初始化Mac

初始化一台新的 Mac 时，我通常会先把基础开发软件、语言环境和效率工具补齐。这里记录一份我自己常用的安装清单，后面重装系统时可以直接照着走。

## 基础开发软件

### Sublime Text

[官网](https://www.sublimetext.com/)

轻量文本编辑器。

安装 `Package Control`。

设置鼠标滚轮缩放大小: [参考](https://blog.csdn.net/dmcpxy/article/details/98854954)

Mac终端中使用Sublime打开文件: [参考](https://www.jianshu.com/p/b77f058dd4a7)

### Homebrew

Mac 上最常用的包管理器。

国内安装: [参考](https://brew.idayer.com/)

终端使用代理加速的正确方式: [参考](https://weilining.github.io/294.html)

插件:

- [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md)
- [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md)

### iTerm2

终端工具。

[参考](https://zhuanlan.zhihu.com/p/550022490)

插件安装建议自己上github看，里面很多东西说的都有些不对

### Warp

[官网](https://www.warp.dev/)

另一款终端工具，可按需选择。

### Sequel Ace

SQL Client。

[项目地址](https://github.com/Sequel-Ace/Sequel-Ace)

### Typora

Markdown 编辑器。

[官网](https://typora.io/)

### Visual Studio Code

通用代码编辑器。

[官网](https://code.visualstudio.com/)

### SourceGit

Git GUI。

[官网](https://sourcegit-scm.github.io/)

## 开发环境

### nvm

[安装文档](https://www.nvmnode.com/guide/download.html)

Node.js 版本管理。

安装 Node.js LTS:

```bash
nvm install --lts
```

### gvm

[项目地址](https://github.com/moovweb/gvm)

Go 版本管理。

常用命令:

```bash
gvm listall
gvm install go1.26.1 -B
gvm use go1.26.1 --default
```

## 效率工具

### 输入法

任意中文输入法，方便shift切换中英文输入

### Snipaste

截图+贴图

[官网](https://www.snipaste.com/)

### Go2Shell

finder下当前目录打开shell

[官网](https://zipzapmac.com/Go2Shell)

### hidden

隐藏顶端状态栏图标

[项目地址](https://github.com/dwarvesf/hidden)


### Stats

系统监控小组件

[项目地址](https://github.com/exelban/stats)

### Scroll Reverser

鼠标滚轮反向

[官网](https://pilotmoon.com/scrollreverser/)

### Rectangle

分屏软件，有windows中的快速分屏体验

[项目地址](https://github.com/rxhanson/Rectangle)

### uTools

建议插件：json, diff, 翻译

[官网](https://www.u.tools/)

### Skim

PDF 阅读器。

[官网](https://skim-app.sourceforge.io/)

## Chrome 插件

### Screenity

录屏插件。

### OneTap

收纳标签页。

### 沉浸式翻译

翻译插件。

### Proxy SwitchyOmega 3 (ZeroOmega)

代理切换插件。

## 摸鱼好用

### Tango

Android 投屏。

[官网](https://app.tangoapp.dev/)
