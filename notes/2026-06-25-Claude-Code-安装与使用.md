---
title: Claude Code 安装与使用
type: source_note
source: https://coding.stormzhang.ai/claude-code/02-install.html
created: 2026-06-25
updated: 2026-06-27
tags:
  - Claude Code
  - AI编程
  - 开发环境
  - CLI
keywords:
  - 原生安装
  - 账号要求
  - 登录验证
  - 安装排错
related:
  - 2026-06-24-Codex-斜杠命令与快捷键.md
  - 2026-06-25-Claude-Code-MCP.md
  - 2026-06-25-Claude-Code-如何工作.md
  - 2026-06-25-Claude-Code-简介.md
  - 2026-06-27-Claude-Code-交互界面与快捷键.md
  - 2026-06-27-Claude-Code-项目结构.md
review:
  status: candidate
  concepts:
    - Claude Code 原生安装方式
    - Claude Code 账号与系统要求
    - CLI 工具安装排错流程
  last_reviewed:
  next_review:
---

# 摘要

这篇文章说明 Claude Code 的安装、登录、验证、升级、卸载和常见报错处理。作者强调当前优先选择官方原生安装脚本，而不是旧的 npm 全局安装方式，因为原生安装支持后台自动更新，权限问题更少。

文章分别给出 macOS/Linux/WSL、Windows PowerShell、Windows CMD 的安装入口，并提醒国内网络通常需要代理才能稳定访问 Claude 相关下载地址。

# 核心观点

- 安装前要确认三件事：系统版本满足要求、账号可用于 Claude Code、使用方式选择 CLI、桌面 App 或编辑器集成。
- 免费版 Claude.ai 账号不能使用 Claude Code；文章列出的可用类型包括 Pro、Max、Team、Enterprise 或 Console/API 账号。
- 官方脚本是首选安装方式；Homebrew、WinGet、npm 属于备选方式，其中 npm 更容易遇到权限和更新问题。
- Windows 用户要区分 PowerShell 与 CMD：两者安装命令不同，终端用错会出现命令不识别或语法错误。
- 安装后可通过 `claude --version`、`which claude` 或 `where claude` 等方式验证命令是否进入 PATH。
- 登录后可以通过 `claude doctor` 检查环境；若登录卡住，需要检查网络、浏览器回跳和命令行环境。
- 排错时要注意多个安装来源同时存在的问题，避免 PATH 里旧版本或 npm 版本与原生版本冲突。

# 我的理解

这篇文章不是单纯列安装命令，而是在强调“安装路径选择”本身会影响后续维护成本。对 CLI 类 AI 工具来说，最容易出问题的通常不是模型能力，而是网络、账号、PATH、权限、终端类型和多版本冲突。

迁移到本知识库时需要保留一个边界：文中的命令和账号要求是 Claude Code 相关信息，不能直接推断为 Codex 或其他 AI 编程工具的要求。涉及最新版本、账号和安装命令时仍应回查官方资料。

# 可复用方法

- 安装 CLI 工具前先确认系统要求、账号权限、网络条件和目标终端。
- 优先选择官方推荐安装路径，避免使用过期教程中的旧包名或旧安装方式。
- 安装后按“版本号、PATH、诊断命令、登录状态”顺序验证。
- 出现异常时先排查终端类型、网络代理、PATH 顺序和多版本冲突。

# 项目关联

这篇资料可作为“AI 编程工具环境配置”的参考模板。以后整理 Codex、Claude Code 或其他 CLI 工具安装资料时，可以复用这种结构：前置条件、平台命令、验证、登录、升级卸载、常见报错。

# 需要复习的知识点

- Claude Code 原生安装方式
- Claude Code 账号与系统要求
- CLI 工具安装排错流程
