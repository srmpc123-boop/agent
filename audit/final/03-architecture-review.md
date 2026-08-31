# 03 — Current Architecture Review

This document provides a thorough architectural audit of the **CURRENT state** of the codebase.

---

## 🏛️ Layer-by-Layer Architectural Audit

### 1. Client / Presentation Layer
- **Streamlit Web Dashboard ([app_ui.py](file:///e:/AI_Data_Agent-main/app_ui.py))**: Provides an interactive browser UI with chat, graph rendering, and evaluation metrics.
- **FastAPI REST API ([app.py](file:///e:/AI_Data_Agent-main/app.py))**: Exposes REST endpoints (`POST /api/v1/tasks`, `GET /api/v1/schema`) for programmatic access.
- **CLI Entry Point ([main.py](file:///e:/AI_Data_Agent-main/main.py))**: Quick command-line interface.

### 2. Orchestration & Agent Layer
- **Master Router Agent ([agents/data_agent.py](file:///e:/AI_Data_Agent-main/agents/data_agent.py))**: Evaluates prompts and routes to `"sql"`, `"etl"`, or `"viz"` sub-graphs.
- **SQL Analyst Sub-Graph ([agents/sql_analyst.py](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py))**: 8-node state machine with SQL generation, safety judging, database execution, and reflection self-correction retry loop.
- **ETL Analyst Sub-Graph ([agents/etl_analyst.py](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py))**: ReAct tool loop agent interacting with API and Pandas tools.
- **Data Visualization Sub-Graph ([agents/viz_analyst.py](file:///e:/AI_Data_Agent-main/agents/viz_analyst.py))**: Python code generator producing Matplotlib/Seaborn charts.

### 3. Model & Infrastructure Integration Layer
- **LLM Factory ([utils/llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py))**: Resolves `LLM_PROVIDER` (defaults to Groq `ChatGroq`) with fallback support for OpenAI and Anthropic.
- **Database Utility ([utils/database.py](file:///e:/AI_Data_Agent-main/utils/database.py))**: Manages PostgreSQL database connection lifecycle and schema introspection.
- **ETL Tools ([utils/etl_tools.py](file:///e:/AI_Data_Agent-main/utils/etl_tools.py))**: Provides HTTP web extraction, dataset preview context, and AST-validated python code execution.

---

## 🎯 Architectural Decisions Evaluation

- **[EXCELLENT] Reflection Retry Loop**: Moving from a single-pass DAG to a cyclical retry graph in `sql_analyst.py` is an exceptional agentic pattern.
- **[EXCELLENT] Decoupled LLM Provider Factory**: `utils/llm_pick.py` allows switching between Groq, OpenAI, and Anthropic seamlessly via `LLM_PROVIDER`.
- **[GOOD] AST Safety Check**: Adding AST module inspection before `exec()` in `utils/etl_tools.py` mitigates arbitrary code execution risks.
- **[QUESTIONABLE] Fixed Retries in State**: Retries are tracked via `state.sql_retry_count` in `AgentSchema`. It works well, but using a dedicated LangGraph Checkpointer would provide persistent time-travel debugging.

---

## 📐 Architecture Rating

```text
Architecture Score: 8.5 / 10
```
- **Strengths**: Clean layer separation, stateful graph execution, self-correction reflection loop, and provider flexibility.
- **Weakness**: Lacks containerized Docker deployment files.
