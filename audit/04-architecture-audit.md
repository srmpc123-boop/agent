# 04 — Architecture Audit

This audit evaluates the architectural principles, component boundaries, data paths, and design patterns of **Agentic AI - Data Agent**.

---

## 🏛️ Architectural Strengths

1. **Clean Graph Encapsulation**: Each domain concern is cleanly encapsulated into its own LangGraph file (`data_agent.py`, `sql_analyst.py`, `etl_analyst.py`).
2. **Schema-Driven State Contracts**: State transitions rely on explicit Pydantic schemas in `Models/schema.py`, eliminating untyped dictionary parameter passing across nodes.
3. **Decoupled Database Utilities**: Database drivers and PostgreSQL schema inspectors live in `utils/database.py` rather than being embedded directly inside agent nodes.

---

## ⚠️ Architectural Weaknesses & Smells

### 1. Inconsistent Sub-Graph Invocation Pattern
In [agents/data_agent.py:L55-L67](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L55-L67), `sql_node` manually constructs a full dictionary representation of `AgentSchema` to invoke `sql_analyst.invoke(input_schema)`:
```python
input_schema = {
    "messages": [],
    "user_question": f"{message}",
    "curated_ques": "",
    "prompt_query_context": "",
    "generated_sql_query": "",
    "is_safe": "No",
    "comments": "",
    "sql_query_execution_result": "",
    "final_answer": ""
}
```
Meanwhile, `etl_node` invokes `etl_analyst` passing only `{"messages": [HumanMessage(...)]}`. Sub-graph invocations should follow a uniform pattern or use LangGraph compiled sub-graph nodes directly.

### 2. Single Point of Failure: Database Utility Instance Lifecycle
In `utils/database.py`, `DatabaseUtil` methods close `self.connection` in `finally` blocks, violating the expected lifecycle of an object-oriented database utility class.

---

## 📐 Current vs. Recommended Architecture

### Current Architecture
```text
[User] -> main.py -> DataAgent (router_node) -> [sql_node | etl_node]
                                                      │
                         ┌────────────────────────────┴──────────────────────────┐
                         ▼                                                       ▼
           SQL Analyst Graph (7 Nodes)                             ETL Analyst Graph (ReAct Loop)
      (Curate -> Context -> Gen -> Judge -> Exec -> Format)             (LLM <-> ToolNode)
                         │                                                       │
                         ▼                                                       ▼
                utils/database.py                                        utils/etl_tools.py
                         │                                                       │
                         ▼                                                       ▼
                PostgreSQL DB                                           Local Disk / Web API
```

### Recommended Architecture
```text
[User / API Gateway] ──► [FastAPI / REST Interface]
                                │
                                ▼
                   [Data Agent Supervisor Graph]
                                │
         ┌──────────────────────┴──────────────────────┐
         ▼                                             ▼
  [SQL Analyst Agent]                           [ETL Analyst Agent]
  - Auto-retry loop on SQL syntax error         - Sandboxed E2B/Docker Python execution
  - Connection-pooled DatabaseUtil              - Validated API Extractors
         │                                             │
         ▼                                             ▼
  [PostgreSQL DB]                              [S3 / Local Storage]
         │                                             │
         └──────────────────────┬──────────────────────┘
                                │
                                ▼
               [Observability / OpenTelemetry Tracing]
```
