---
title: Claude Code MCP 外部工具集成
type: source_note
source: https://coding.stormzhang.ai/claude-code/22-mcp.html
created: 2026-06-25
updated: 2026-06-27
tags:
  - Claude Code
  - MCP
  - AI编程
  - 工具集成
keywords:
  - MCP server
  - stdio
  - HTTP transport
  - 工具权限
  - 提示注入
related:
  - 2026-06-25-Claude-Code-如何工作.md
  - 2026-06-25-Claude-Code-安装与使用.md
  - 2026-06-25-Claude-Code-简介.md
  - 2026-06-27-Claude-Code-交互界面与快捷键.md
  - 2026-06-27-Claude-Code-项目结构.md
review:
  status: candidate
  concepts:
    - MCP 的用途与安全边界
    - stdio、HTTP、SSE 三种 MCP 传输形态
    - MCP server 作用域 local、project、user
    - MCP 工具调用的批准机制
  last_reviewed:
  next_review:
---

# 摘要

这篇文章介绍 Claude Code 如何通过 MCP 连接外部工具和数据源。作者把 MCP 比作扩展坞：Claude Code 默认主要处理本地文件和命令，而 MCP 提供统一接口，让它连接 Jira、GitHub、数据库、Figma、Sentry、Notion 等外部服务。

文章重点讲解 MCP server 的传输形态、添加命令、作用域、连接状态、首次批准机制以及第三方 server 的信任风险。

# 核心观点

- MCP 是 Model Context Protocol，是用于 AI 工具集成的开源标准，解决模型无法直接访问外部服务的问题。
- 本地工具通常使用 stdio 形态，通过 `claude mcp add <name> -- <command>` 启动本地进程。
- 云服务优先使用 HTTP 形态，通过 `claude mcp add --transport http <name> <url>` 连接远程服务。
- SSE 属于已弃用形态，遇到旧配置时可识别，但新配置应优先使用 HTTP。
- `claude mcp add` 的选项需要放在 server 名称之前，`--` 后面的内容属于启动 server 的命令参数。
- MCP server 有三种作用域：`local` 只在当前项目且仅自己使用，`project` 写入项目 `.mcp.json` 并可随 Git 共享，`user` 对用户所有项目生效。
- 添加 server 后可用 `claude mcp list` 或会话内 `/mcp` 查看状态，包括 Connected、Needs authentication、Failed to connect、Pending approval 等。
- 项目级 `.mcp.json` 的 server 首次加载需要用户批准；工具第一次调用也需要批准。
- 第三方 MCP server 存在信任和提示注入风险，连接前应确认来源可信，数据库等敏感资源优先使用只读权限。

# 我的理解

这篇文章把 MCP 的实用价值和安全边界讲得比较完整。MCP 让代理式工具从“只处理本地项目”扩展到“操作整个工具链”，但这也意味着外部数据、第三方代码、认证凭据和提示注入风险会一起进入工作流。

对本知识库来说，MCP 是一个值得单独复习的主题。它不只是 Claude Code 的功能，也是一类 AI 工具集成标准。整理时要区分协议层概念和 Claude Code 的具体命令：stdio、HTTP、server 作用域、工具权限这些概念可迁移，`claude mcp add` 等命令只属于 Claude Code。

# 可复用方法

- 判断是否需要 MCP：如果经常从外部系统复制内容到 AI 对话，就考虑连接对应 server。
- 本地工具优先 stdio，远程云服务优先 HTTP，避免新增 SSE 配置。
- 个人实验用 local，跨项目常用工具用 user，团队共享配置用 project。
- 对第三方 server 做信任检查，敏感系统使用只读账号，避免给生产库写权限。
- 添加后用列表命令检查状态，首次调用时确认工具来源和权限请求。

# 项目关联

这篇资料可和现有 Codex 主题中的“能力扩展：插件、Skill、CLI 或 MCP”相互参照。它也适合成为后续整理 MCP 概念页的核心来源之一。

# 需要复习的知识点

- MCP 的用途与安全边界
- stdio、HTTP、SSE 三种 MCP 传输形态
- MCP server 作用域 local、project、user
- MCP 工具调用的批准机制
