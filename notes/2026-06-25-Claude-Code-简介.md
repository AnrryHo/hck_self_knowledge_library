---
title: Claude Code 简介
type: source_note
source: https://coding.stormzhang.ai/claude-code/01-what-is-claude-code.html
created: 2026-06-25
updated: 2026-06-27
tags:
  - Claude Code
  - AI编程
  - 开发工具
  - 工作流
keywords:
  - 代理式编程
  - 项目级上下文
  - 跨文件修改
  - 工具对比
related:
  - 2026-06-14-Codex全解-视频文档-46bd05f5565d.md
  - 2026-06-24-Codex-Cloud-云端任务工作流.md
  - 2026-06-24-Codex-斜杠命令与快捷键.md
  - 2026-06-25-Claude-Code-MCP.md
  - 2026-06-25-Claude-Code-如何工作.md
  - 2026-06-25-Claude-Code-安装与使用.md
  - 2026-06-27-Claude-Code-交互界面与快捷键.md
  - 2026-06-27-Claude-Code-项目结构.md
review:
  status: candidate
  concepts:
    - Claude Code 的代理式工作方式
    - ChatGPT、Copilot、Cursor 与 Claude Code 的定位差异
    - AI 编程工具中的人机分工边界
  last_reviewed:
  next_review:
---

# 摘要

这篇文章介绍 Claude Code 的基本定位：它是 Anthropic 官方的命令行版 AI 编程搭档，能够读取整个项目、直接修改文件、运行命令，而不只是像聊天框一样给出代码建议。

文章还说明 Claude Code 的多种使用形态，包括终端、VS Code/Cursor 插件、JetBrains 插件、桌面 App、网页和手机端。作者强调这些形态底层是同一个 Claude Code 引擎，项目说明文件、配置和 MCP 服务可跨形态复用。

# 核心观点

- Claude Code 的关键差异不是“会写代码”，而是能在项目上下文里动手执行：读文件、改文件、跑命令、追踪错误。
- 它适合处理真实项目中的理解、重构、修 bug、补测试、清理 lint、升级依赖、写 release notes、处理 Git 工作流等任务。
- 它不能替用户做最终技术决策，也不能保证代码绝对正确；用户仍然需要审查 diff、判断业务逻辑和把关提交。
- 作者用三个类比区分工具：ChatGPT 像顾问，Copilot/Cursor 的经典补全形态像智能输入法，Claude Code 像能独立干活的搭档。
- 入门时可以用 `claude --version` 判断本机是否已经安装 Claude Code。

# 我的理解

这篇文章的核心价值是帮初学者建立“代理式编程工具”的边界感。Claude Code 的优势不是替代程序员，而是把重复、跨文件、需要上下文追踪的执行工作交给 AI。

对本知识库已有 Codex 资料来说，Claude Code 可以作为同类工具的对照对象：两者都强调项目上下文、文件修改、命令执行和人工审查，但具体命令、权限、平台和生态不同。后续整理时应避免把 Claude Code 的配置文件、命令和 MCP 用法直接套到 Codex 上。

# 可复用方法

- 判断一个任务是否适合交给代理式编程工具：是否需要读多个文件、修改项目、跑测试或清理重复工作。
- 使用 AI 编程工具时保留人类职责：明确目标、说明业务规则、审查 diff、决定是否提交。
- 学新工具先建立工具地图：它是什么、在哪里运行、能做什么、不能做什么、和已有工具差在哪。

# 项目关联

这篇资料可用于补充 AI 编程工具主题，尤其适合和现有 Codex 资料对照，帮助明确“聊天式问答、编辑器补全、代理式执行”三类工具的差异。

# 需要复习的知识点

- Claude Code 的代理式工作方式
- ChatGPT、Copilot、Cursor 与 Claude Code 的定位差异
- AI 编程工具中的人机分工边界
