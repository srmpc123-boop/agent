# 22 — Design Patterns and Architectural Decisions

This document details the software design patterns and key architectural choices present in **Agentic AI - Data Agent**.

---

## 🎨 Architectural & Design Patterns Identified

### 1. Router Pattern (Hierarchical Intent Routing)
* **Where implemented**: `agents/data_agent.py` (`router_node` + `route_edge`).
* **How it works**: Analyzes intent at the top node and routes control flow exclusively to specialized domain sub-graphs.
* **Why chosen**: Keeps SQL and ETL agent prompts, states, and tools cleanly isolated.

### 2. Guardrail / LLM-as-a-Judge Pattern
* **Where implemented**: `agents/sql_analyst.py` (`is_safe_sql` + `is_safe_sql_edge`).
* **How it works**: Before running LLM-generated code/queries on production infrastructure, a separate LLM invocation validates safety against strict criteria (`JudgeSchema`).
* **Why chosen**: Prevents catastrophic SQL operations (`DROP TABLE`, `DELETE FROM`) from reaching PostgreSQL.

### 3. ReAct (Reasoning + Acting) Tool Loop
* **Where implemented**: `agents/etl_analyst.py` (`llm_node` + `tool_node` + `is_tool_call`).
* **How it works**: LLM decides which tool to call, receives execution feedback as `ToolMessage`, and recursively decides whether to invoke additional tools or finish.

### 4. Dynamic Factory Pattern
* **Where implemented**: `utils/llm_pick.py` (`pick_llm`).
* **How it works**: Decouples model instantiation from agent logic using a central tier resolver function.

### 5. Schema Introspection Pattern
* **Where implemented**: `utils/database.py` (`schema_details`).
* **How it works**: Programmatically inspects `information_schema` at runtime and injects table columns and sample data into LLM prompts instead of hardcoding schema text.

---

## ⚖️ Tradeoff Analysis of Major Decisions

| Architectural Decision | Advantage | Disadvantage / Risk |
| --- | --- | --- |
| Dynamic `exec()` for Pandas Transformations | Highly flexible; can perform any complex data transformation requested by user. | Major security vulnerability if untrusted input is passed without sandbox containerization. |
| In-Memory SQL Guardrail Judge | Fast; prevents destructive DB executions without complex permissions. | Relying solely on LLM judge can occasionally misclassify or miss clever SQL obfuscations compared to SQL AST parsers. |
| Dynamic Schema Injection | SQL generator automatically adapts to schema changes in PostgreSQL. | Ingests sample data into prompt tokens on every request, increasing API costs. |
