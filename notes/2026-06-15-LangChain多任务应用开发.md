---
title: LangChain 多任务应用开发
type: source_note
source: raw/2026-06-15-LangChain多任务应用开发.ipynb
created: 2026-06-15
updated: 2026-06-15
tags:
  - LangChain
  - LCEL
  - RAG
  - AI应用开发
keywords:
  - ChatModel
  - 结构化输出
  - Function Calling
  - Document Loaders
  - OutputParser
  - Runnable
related: []
review:
  status: candidate
  concepts:
    - LangChain 核心组件
    - ChatModel 输入输出
    - 结构化输出与 Function Calling
    - 文档加载和文本切分
    - LCEL 组合模型
    - LangChain 与 LlamaIndex 的差异
  last_reviewed:
  next_review:
---

# 摘要

这份课件介绍 LangChain 的模型 I/O、结构化输出、Function Calling、文档加载与处理、向量检索，以及 Chain 和 LangChain Expression Language（LCEL）。示例还涉及使用 LCEL 构建 RAG、切换模型，并比较 LangChain 与 LlamaIndex 的定位。

# 核心观点

1. LangChain 对不同模型供应商提供统一的 ChatModel 和消息接口。
2. Output Parser、Pydantic 模型和 Function Calling 可将自然语言输出转为结构化数据或工具调用。
3. Document Loader、Text Splitter、Embedding 和 Vector Store 构成数据连接与检索链路。
4. LCEL 使用 Runnable 组合 Prompt、模型、解析器和检索组件，支持流水线式应用构建。
5. 课件将 LangChain 侧重的应用编排与 LlamaIndex 侧重的知识接入和检索进行对比。

# 我的理解

LangChain 的主要价值是把模型调用、数据连接和任务编排统一为可组合组件。LCEL 能降低简单链路的胶水代码，但复杂应用仍需要明确状态、错误处理和可观察性。后一句是基于课件组件设计做出的推断。

# 可复用方法

- 先用 ChatModel 和消息对象统一不同模型的调用方式。
- 需要稳定机器输出时使用结构化输出并执行字段校验。
- Function Calling 只负责生成调用意图，实际工具仍需权限控制和参数验证。
- 使用 LCEL 将 Prompt、Retriever、Model 和 Parser 拆成可独立测试的 Runnable。
- 模型切换时保持统一输入输出契约，并用固定样例做回归测试。

# 项目关联

这份资料可用于未来构建知识库问答、自动化处理链和多模型切换能力，也能与 LlamaIndex 课件形成框架选型对照。

# 需要复习的知识点

- ChatModel、Message 和 PromptTemplate 的关系。
- 结构化输出、Output Parser 与 Function Calling 的区别。
- 文档加载、切分、嵌入和检索的完整链路。
- Runnable 与 LCEL 管道如何组合。
- LangChain 与 LlamaIndex 各自更适合解决什么问题。
