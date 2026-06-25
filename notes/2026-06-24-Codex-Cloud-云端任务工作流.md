---
title: Codex Cloud 云端任务工作流
type: source_note
source: https://coding.stormzhang.ai/codex/10-cloud.html
created: 2026-06-24
updated: 2026-06-24
tags:
  - Codex
  - AI编程
  - 云端开发
  - 工作流
keywords:
  - Codex Cloud
  - 云端容器
  - 网络白名单
  - Secrets
related:
  - 2026-06-14-Codex全解-视频文档-46bd05f5565d.md
  - 2026-06-24-Codex-斜杠命令与快捷键.md
review:
  status: candidate
  concepts:
    - Codex Cloud 任务流水线
    - 云端环境配置
    - Agent 网络白名单
    - 云端与本地工作流取舍
  last_reviewed: 
  next_review: 
---

# 摘要

这篇文章介绍 Codex Cloud：通过浏览器连接 GitHub，把代码修改、测试和 PR 生成放到 OpenAI 云端隔离容器中完成。核心价值是免本地环境、支持并行、适合长任务后台运行；核心限制是必须依赖 GitHub，云端看不到本机配置，且 Agent 阶段默认不中途询问。

# 核心观点

1. **云端版的本质**：Codex Cloud = OpenAI 云端隔离容器 + GitHub 仓库 + 云端环境配置。它不是直接操作本机文件，而是在云端拉取仓库、运行任务并提交 diff/PR。
2. **任务运行是固定流水线**：建容器并拉代码 → 跑 setup script → 应用网络设置 → Agent 执行修改与验证 → 交付 diff/PR。
3. **环境配置决定云端可运行性**：需要配置运行时版本、依赖安装脚本、环境变量、Secrets、缓存策略。setup script 与 Agent 阶段不是同一个 Bash 会话，不能依赖 setup 中 `export` 的变量自动传递。
4. **网络默认收紧**：setup 阶段可联网装依赖，Agent 阶段默认断网。若必须联网，应使用域名白名单与只读 HTTP 方法收窄风险。
5. **云端与本地是分工关系**：需要本机文件、工具、全局配置或本地 MCP 时用本地；不碰本机、希望并行或后台长跑时用云端。

# 我的理解

这篇文章对知识库当前的 Codex 使用有两个直接启发：

- 云端任务更适合“明确边界、可验收、可 PR 化”的工程任务，而不适合依赖本地状态或需要频繁人工确认的探索任务。
- 如果希望云端 Codex 稳定执行本项目，需要把规则写进仓库可见文件（例如 `AGENTS.md`），而不能指望它读取本机 `~/.codex` 或本地 MCP 配置。

推断：对于本知识库这类内容整理任务，若原始资料、脚本和规则都已在仓库内，云端可用于批量整理或索引维护；但涉及本地未提交资料、浏览器登录状态或个人密钥时，应优先使用本地 Codex。

# 可复用方法

- **派云端任务前的检查清单**：
  1. 任务是否只依赖 GitHub 仓库内文件？
  2. 任务是否能用一句话定义验收标准？
  3. 依赖安装是否能通过 setup script 完成？
  4. 是否需要 Agent 阶段联网？如果需要，域名和 HTTP 方法是否最小化？
  5. 是否已在仓库内写清 `AGENTS.md`、测试命令和交付规则？
- **云端任务提示词模板**：明确“改哪些文件 / 不改哪些文件 / 预期行为 / 必跑检查 / diff 验收标准”。
- **网络配置原则**：默认 Off；必须 On 时，从 Common dependencies + GET/HEAD/OPTIONS 起步，只按需追加域名。

# 项目关联

- 本项目已有 `AGENTS.md`，适合沉淀云端 Codex 可读取的知识入库规则。
- `scripts/fuxi.py` 属于可在云端复用的机械流程；只要依赖和输入资料在仓库内，云端任务可运行索引、关联、验证等操作。
- 若资料尚未入库到 `raw/` 或涉及本地不可提交内容，则不适合直接交给云端。

# 需要复习的知识点

- Codex Cloud 的 5 步任务流水线。
- setup script、环境变量、Secrets、缓存的作用边界。
- Agent 阶段默认断网与网络白名单配置。
- 云端与本地 Codex 的任务取舍。
