---
title: Claude Code 项目结构
type: source_note
source: https://coding.stormzhang.ai/claude-code/13-project-structure.html
created: 2026-06-27
updated: 2026-06-27
tags:
  - Claude Code
  - AI编程
  - 项目配置
  - 工作流
keywords:
  - .claude
  - CLAUDE.md
  - settings.json
  - gitignore
  - 配置优先级
related:
  - 2026-06-14-Codex全解-视频文档-46bd05f5565d.md
  - 2026-06-24-Codex-Cloud-云端任务工作流.md
  - 2026-06-24-Codex-斜杠命令与快捷键.md
  - 2026-06-25-Claude-Code-MCP.md
  - 2026-06-25-Claude-Code-如何工作.md
  - 2026-06-25-Claude-Code-安装与使用.md
  - 2026-06-25-Claude-Code-简介.md
  - 2026-06-27-Claude-Code-交互界面与快捷键.md
review:
  status: candidate
  concepts:
    - Claude Code 项目级与用户级配置
    - .claude 目录结构
    - Claude Code 配置文件的 git 提交边界
    - Claude Code 配置优先级与合并规则
  last_reviewed:
  next_review:
---

# 摘要

这篇文章解释 Claude Code 在项目目录和用户主目录中保存哪些配置。核心是区分两个位置：项目里的 `./.claude/` 跟随仓库和团队协作，用户主目录的 `~/.claude/` 跟随个人偏好并跨项目生效。

文章重点梳理 `CLAUDE.md`、`settings.json`、`settings.local.json`、`commands/`、`rules/`、`skills/`、`agents/`、`.mcp.json` 等文件和目录的用途，并强调哪些内容应该提交到 git，哪些属于个人本地配置或敏感信息，绝不能提交。

# 核心观点

- Claude Code 有项目级和用户级两套配置：项目级配置服务当前仓库和团队共享，用户级配置服务个人跨项目偏好。
- `CLAUDE.md` 和 `rules/` 属于给 Claude 阅读的指导，`settings.json` 属于 Claude Code 强制执行的配置。
- 项目级 `.claude/` 可以包含共享配置、斜杠命令、规则、技能和子代理；这些目录在用户级 `~/.claude/` 中也可存在，但作用范围不同。
- `.mcp.json` 位于项目根目录，用于团队共享 MCP server 配置；个人 MCP 配置存在用户级配置中。
- 团队共享的 `CLAUDE.md`、`.claude/settings.json`、`commands/`、`rules/`、`skills/`、`agents/` 可以提交 git。
- `settings.local.json`、`CLAUDE.local.md`、任何包含密钥或 token 的文件都不应提交；密钥应通过环境变量引用。
- 配置优先级从高到低为 Managed、命令行参数、Local、Project、User；但标量值通常覆盖，数组值会跨作用域合并。

# 我的理解

这篇文章的价值不在于教某个具体功能，而是给 Claude Code 的文件系统模型建立地图。后续学习权限、MCP、Skill、Subagent、记忆系统时，都需要先知道配置究竟落在哪个目录、谁能看到、会不会进 git。

对本知识库来说，可迁移的重点是“作用域”和“提交边界”：团队事实放项目级，个人偏好放用户级或 local 文件，敏感凭据不落盘或不进仓库。配置优先级也需要和具体字段类型一起看，不能简单理解成后一层完全覆盖前一层。

# 可复用方法

- 判断配置位置时先问两个问题：这是项目事实还是个人习惯？是否需要团队共享？
- 项目规范写入 `CLAUDE.md` 或 `rules/`，权限和 hook 等强约束写入 `settings.json`。
- 临时个人覆盖写入 `settings.local.json`，个人项目偏好写入 `CLAUDE.local.md` 并加入忽略规则。
- 共享命令、技能和子代理放项目级 `.claude/` 并提交；个人常用命令放用户级 `~/.claude/`。
- 提交前检查 `.claude/` 和根目录配置，确保 local 文件和密钥没有进入 git。

# 项目关联

这篇资料可补充 `wiki/Claude Code.md` 中的“项目结构与配置作用域”。它也适合和 Codex 的 `AGENTS.md`、权限配置、MCP 接入等主题对照：不同工具命令不通用，但“项目级规则、用户级偏好、敏感信息不提交”的原则通用。

# 需要复习的知识点

- Claude Code 项目级与用户级配置
- `.claude` 目录结构
- Claude Code 配置文件的 git 提交边界
- Claude Code 配置优先级与合并规则
