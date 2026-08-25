# 08 — Agent Architecture

This document presents a comprehensive analysis of all agents in the **Agentic AI - Data Agent** project.

---

## 🤖 Summary Agent Matrix

| Agent Name | Location File | Primary Role | Underlying LLM Tier | Tools Available | Input Schema | Output Schema |
| --- | --- | --- | --- | --- | --- | --- |
| **Data Agent (Router)** | [agents/data_agent.py](file:///e:/AI_Data_Agent-main/agents/data_agent.py) | Classifies intent & routes to sub-agents | `"claude"` (`ChatAnthropic`) | Sub-graphs (`sql_analyst`, `etl_analyst`) | `DataAgentSchema` | `DataAgentSchema` |
| **SQL Analyst Agent** | [agents/sql_analyst.py](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py) | Text-to-SQL generation & safety execution | `"low"` / `"medium"` (`ChatOpenAI`) | PostgreSQL Driver (`DatabaseUtil`), LLM Judge | `AgentSchema` | `AgentSchema` |
| **ETL Analyst Agent** | [agents/etl_analyst.py](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py) | Web API extraction & Pandas transformations | `"claude"` (`ChatAnthropic`) | `extract_load_tool`, `transform_load_tool` | `ETLAgentSchema` | `ETLAgentSchema` |

---

## 🔍 Agent 1: Data Agent (Outer Router)

* **Definition**: Top-level graph manager.
* **Goal**: Analyzes incoming natural language prompts and delegates execution to specialized domain graphs.
* **Graph Definition**:
  ```python
  data_agent_graph = StateGraph(DataAgentSchema)
  data_agent_graph.add_node("router_node", router_node)
  data_agent_graph.add_node("etl_node", etl_node)
  data_agent_graph.add_node("sql_node", sql_node)
  ```
* **Decision Logic**: `llm_router.invoke(message)` maps to `RouterSchema`.
  - `"sql"`: User prompt relates to relational database queries.
  - `"etl"`: User prompt relates to file downloads, API extraction, or data transformations.

---

## 🔍 Agent 2: SQL Analyst Agent

* **Definition**: 7-node pipeline graph for secure natural language database querying.
* **Graph Nodes**:
  1. `curate_ques`: Re-writes user prompt into a clear SQL task.
  2. `prompt_query_context`: Dynamically inspects PostgreSQL schema and builds prompt context.
  3. `generate_sql`: Converts context and question into a raw SQL query.
  4. `is_safe_sql`: Evaluates query safety using LLM Judge (`JudgeSchema`).
  5. `canceled_sql`: Handles unsafe queries and explains rejection.
  6. `execute_sql`: Runs safe SQL queries against PostgreSQL.
  7. `represent_final_answer`: Synthesizes raw database records into clear text.
* **Safety Mechanism**: Direct DDL/DML protection (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `CREATE` are blocked by `is_safe_sql`).

---

## 🔍 Agent 3: ETL Analyst Agent

* **Definition**: ReAct tool-calling graph for data pipeline operations.
* **Graph Structure**:
  - `llm_node`: Prompts LLM bound with `[extract_load_tool, transform_load_tool]`.
  - `tool_node`: Iterates over LLM requested tool calls and appends execution observations.
  - `is_tool_call` conditional edge: Loops back to `llm_node` until LLM finishes calling tools.
* **Capabilities**:
  - `extract_load_tool`: Downloads JSON data from REST APIs and converts to CSV, JSON, or Parquet.
  - `transform_load_tool`: Analyzes dataset head preview, prompts LLM for Pandas code, and executes code via Python `exec()`.
