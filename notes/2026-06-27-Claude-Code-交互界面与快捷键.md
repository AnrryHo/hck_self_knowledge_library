---
title: Claude Code 交互界面与快捷键
type: source_note
source: https://coding.stormzhang.ai/claude-code/14-interface-and-shortcuts.html
created: 2026-06-27
updated: 2026-06-27
tags:
  - Claude Code
  - AI编程
  - CLI
  - 工作流
keywords:
  - 快捷键
  - Shell 模式
  - 权限模式
  - 多行输入
related:
  - 2026-06-14-Codex全解-视频文档-46bd05f5565d.md
  - 2026-06-24-Codex-Cloud-云端任务工作流.md
  - 2026-06-24-Codex-斜杠命令与快捷键.md
  - 2026-06-25-Claude-Code-MCP.md
  - 2026-06-25-Claude-Code-如何工作.md
  - 2026-06-25-Claude-Code-安装与使用.md
  - 2026-06-25-Claude-Code-简介.md
  - 2026-06-25-Codex-斜杠命令与快捷键.md
  - 2026-06-27-Claude-Code-项目结构.md
review:
  status: candidate
  concepts:
    - Claude Code 交互界面分区
    - Claude Code 高频快捷键
    - Claude Code 输入前缀 @ 和 !
    - Claude Code 多行输入方式
  last_reviewed:
  next_review:
---

# 摘要

这篇文章介绍 Claude Code 终端交互界面的主要区域和高频键盘操作。作者把界面拆成输入框、状态行、模式/权限提示三块，并围绕 `Esc`、`Ctrl+C`、`Ctrl+D`、`Shift+Tab`、方向键、`Ctrl+L`、`Ctrl+R`、`Ctrl+O` 等快捷键说明常见操作。

文章还解释输入框中的特殊前缀：`@` 用于文件路径补全和精准引用，`!` 用于直接运行 shell 命令并把输出加入上下文，`/` 是命令或 Skill 入口，`#` 与记忆相关但版本行为可能不同。最后强调多行输入不能直接按 Enter，推荐使用 `\` + Enter 或 `Ctrl+J`。

# 核心观点

- Claude Code 界面重点看输入框、状态行、模式/权限提示；模式提示决定它动手前是否询问用户。
- `Esc` 按一次用于中断当前回答或工具调用；输入框为空时连按两次可打开回退菜单。
- `Ctrl+C` 用于中断或清空输入，连续第二次可能退出；`Ctrl+D` 直接退出会话。
- `Shift+Tab` 用于切换权限模式，例如 default、acceptEdits、plan 等；某些 Windows 环境可能使用 `Alt+M`。
- `Ctrl+L` 可在终端显示异常时重绘屏幕，保留输入和历史。
- `@` 可以精准指定文件或目录，减少模型猜错上下文的概率。
- `!` 可进入 Shell 模式，直接执行命令并把输出放入对话上下文。
- Enter 默认发送消息；多行输入应使用 `\` + Enter、`Ctrl+J`、支持环境下的 `Shift+Enter`，或用 `Ctrl+G` 打开编辑器。
- `/keybindings` 可修改部分快捷键，但 `Ctrl+C`、`Ctrl+D` 等保留键不可重绑定。

# 我的理解

这篇文章强调的是“操作层熟练度”。Claude Code 这类 CLI Agent 的效率不只取决于提示词，也取决于用户能否及时刹车、回退、切模式、点名文件和运行命令。

对新手最关键的不是一次记住所有快捷键，而是先掌握四个动作：`Esc` 刹车、`Shift+Tab` 切权限模式、`@` 指定文件、`\` + Enter 换行。它们分别对应控制风险、控制执行权限、控制上下文精度和控制输入质量。

# 可复用方法

- 执行前先看状态行中的模式提示，确认当前是默认、计划还是自动接受编辑。
- 发现方向跑偏时先按 `Esc` 中断，再补充约束，不必等它跑完。
- 提问涉及具体文件时优先用 `@路径` 点名，减少歧义。
- 需要查看仓库状态或目录内容时可用 `! git status`、`! ls` 这类 shell 命令，把输出纳入上下文。
- 长提示词用 `\` + Enter 换行；更长的需求用 `Ctrl+G` 进入编辑器编写。

# 项目关联

这篇资料可补充 `wiki/Claude Code.md` 中的“交互操作”部分，也可和现有 Codex 快捷键笔记对照。两者快捷键不完全相同，但共同点是：CLI Agent 的高效使用依赖“中断、模式切换、上下文引用、命令执行”这几类基础动作。

# 需要复习的知识点

- Claude Code 交互界面分区
- Claude Code 高频快捷键
- Claude Code 输入前缀 `@` 和 `!`
- Claude Code 多行输入方式
