# 21 — Important Classes and Functions

This document catalogs the most important classes, functions, and nodes in **Agentic AI - Data Agent**, ranked by architectural criticality.

---

## 🏆 Tier 1: Critical Core Components

### 1. `pick_llm(level: str)`
* **Location**: [utils/llm_pick.py:L6-L34](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L6-L34)
* **Purpose**: Central factory function that instantiates `ChatOpenAI` or `ChatAnthropic` models based on requested difficulty level (`"low"`, `"medium"`, `"high"`, `"claude"`).
* **Callers**: Used across all nodes in `data_agent.py`, `sql_analyst.py`, and `etl_analyst.py`.

### 2. `DatabaseUtil`
* **Location**: [utils/database.py:L4-L78](file:///e:/AI_Data_Agent-main/utils/database.py#L4-L78)
* **Purpose**: Database driver wrapper managing PostgreSQL connections, schema context retrieval (`schema_details`), and query execution (`execute_sql`).
* **Callers**: `prompt_query_context()` and `execute_sql()` in `sql_analyst.py`.

### 3. `ETLTools`
* **Location**: [utils/etl_tools.py:L5-L94](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L5-L94)
* **Purpose**: Toolkit providing web extraction (`extract_load`), file preview context (`transform_load_context`), and code execution (`execute_code`).
* **Callers**: `extract_load_tool` and `transform_load_tool` in `etl_analyst.py`.

---

## 🥈 Tier 2: Graph Nodes & Routing Functions

### 4. `router_node(state: DataAgentSchema)`
* **Location**: [agents/data_agent.py:L26-L36](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L26-L36)
* **Purpose**: Classifies user query into `"sql"` or `"etl"` via LLM structured output.

### 5. `is_safe_sql(state: AgentSchema)`
* **Location**: [agents/sql_analyst.py:L84-L105](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L84-L105)
* **Purpose**: Evaluates generated SQL query safety using LLM Judge guardrail (`JudgeSchema`).

### 6. `prompt_query_context(state: AgentSchema)`
* **Location**: [agents/sql_analyst.py:L29-L66](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L29-L66)
* **Purpose**: Inspects live PostgreSQL schema metadata and formats system prompt context for SQL generation.

---

## 🥉 Tier 3: State Schemas ([Models/schema.py](file:///e:/AI_Data_Agent-main/Models/schema.py))

* `AgentSchema`: Manages SQL Agent state variables.
* `JudgeSchema`: Validates SQL safety judge output.
* `RouterSchema`: Validates intent classification output.
* `DataAgentSchema`: Manages top-level router graph state.
* `ETLAgentSchema`: Manages ETL ReAct message state.
