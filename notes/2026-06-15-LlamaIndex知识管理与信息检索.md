---
title: LlamaIndex 知识管理与信息检索
type: source_note
source: raw/2026-06-15-LlamaIndex知识管理与信息检索.ipynb
created: 2026-06-15
updated: 2026-06-15
tags:
  - LlamaIndex
  - RAG
  - 信息检索
  - 工作流
keywords:
  - Data Connectors
  - NodeParser
  - VectorStoreIndex
  - Query Engine
  - Chat Engine
  - Text2SQL
  - Workflow
related:
  - 2026-06-15-RAG高级技术与实践.md
  - 2026-06-15-中医临床智能诊疗助手-API版.md
  - 2026-06-15-中医临床智能诊疗助手-本地模型版.md
review:
  status: candidate
  concepts:
    - LlamaIndex 核心模块
    - 文档加载与节点解析
    - 索引和检索后处理
    - Query Engine 与 Chat Engine
    - Text2SQL
    - LlamaIndex Workflow
  last_reviewed:
  next_review:
---

# 摘要

这份课件覆盖 LlamaIndex 从数据加载、文本切分、节点解析、索引、检索后处理到问答生成的完整链路，并进一步介绍 Prompt、LLM、Embedding 底层接口、完整 RAG 系统、Text2SQL 和 Workflow。

# 核心观点

1. LlamaIndex 将知识应用拆分为数据接入、解析、索引、检索、后处理和响应合成等模块。
2. 普通文本切分与结构化节点解析适用于不同文档，切分方式会直接影响检索质量。
3. `VectorStoreIndex`、Retriever、Postprocessor 和 Response Synthesizer 可以组合成可定制的查询流程。
4. Query Engine 面向单轮查询，Chat Engine 增加对话上下文处理。
5. 课件把 LlamaIndex 的应用扩展到 Text2SQL、ChatBI 和事件驱动工作流。

# 我的理解

LlamaIndex 的价值主要在于统一知识接入和检索生成组件，使开发者能够替换模型、向量库、解析器和检索器，而不必从头搭建整条链路。该表述是根据课件模块划分做出的归纳。

# 可复用方法

- 按数据源选择 Reader 或 Data Connector，再根据文档结构选择 Splitter 或 NodeParser。
- 将索引、检索器、后处理器和响应合成器分别配置与测试。
- 单轮知识问答优先使用 Query Engine，需要上下文时再引入 Chat Engine。
- 对低相关结果增加相似度过滤、融合检索或 LLM 重排序。
- 工作流中将数据准备、工具和事件步骤解耦，便于调试与可视化。

# 项目关联

这份资料与本知识库的数据分层和知识检索目标直接相关，可作为未来增加多格式解析、语义索引和问答工作流的框架参考。

# 需要复习的知识点

- Reader、Document、Node 和 Index 的关系。
- TextSplitter 与 NodeParser 的适用差异。
- Retriever、Postprocessor 和 Response Synthesizer 的职责。
- Query Engine 与 Chat Engine 的区别。
- Text2SQL 的风险和验证方式。
- Workflow 的事件与步骤模型。
