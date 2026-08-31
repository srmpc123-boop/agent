# 00 — Current Project Understanding

This document establishes an evidence-based technical understanding of the **CURRENT state** of the **Agentic AI Data Agent** codebase in `e:/AI_Data_Agent-main`.

---

## 📌 Executive Overview

**Agentic AI Data Agent** is an autonomous multi-agent data engineering, analytics, and visualization platform built with **LangGraph**, **FastAPI**, **Streamlit**, **Pydantic**, **Pandas**, **PostgreSQL**, and **Groq (`ChatGroq`)**.

It processes natural language user prompts by dynamically classifying intent and executing workflows across 4 specialized agent sub-graphs:
1. **Data Agent (Router Graph)**: Directs prompts to `"sql"`, `"etl"`, or `"viz"` sub-graphs based on LLM structured output classification (`RouterSchema`).
2. **SQL Analyst Agent**: A 8-node state machine that curates questions, introspects PostgreSQL table schemas and sample data, generates SQL queries, validates query safety via an LLM judge (`JudgeSchema`), executes safe queries on PostgreSQL, **self-corrects failed SQL queries via a reflection retry loop (up to 3 retries)**, and formats natural language text answers.
3. **ETL Analyst Agent**: A ReAct tool-calling graph using `extract_load_tool` (web API JSON extraction into CSV/JSON/Parquet) and `transform_load_tool` (AST-validated Pandas code execution).
4. **Data Visualization Agent**: A specialized graph (`agents/viz_analyst.py`) that generates Matplotlib/Seaborn Python code and saves PNG charts under `data/visualizations/`.

---

## 🗺️ Current System Architecture Diagram

```mermaid
graph TD
    Client[User / Streamlit Dashboard / HTTP Client] --> API[FastAPI Server: app.py]
    API --> DataAgent[agents/data_agent.py: data_agent]
    
    subgraph Data Agent Router
        DataAgent --> RouterNode[router_node: RouterSchema]
        RouterNode --> RouterEdge{route_edge}
    end

    subgraph SQL Analyst Subsystem with Self-Correction
        RouterEdge -- "sql" --> SQLNode[sql_node]
        SQLNode --> SQLGraph[agents/sql_analyst.py: sql_analyst]
        SQLGraph --> Curate[curate_ques]
        Curate --> Context[prompt_query_context: DatabaseUtil]
        Context --> GenSQL[generate_sql]
        GenSQL --> Judge[is_safe_sql: JudgeSchema]
        Judge -- safe == 'Yes' --> ExecSQL[execute_sql: PostgreSQL]
        Judge -- safe == 'No' --> CancelSQL[canceled_sql]
        ExecSQL --> ExecCheck{Execution Error?}
        ExecCheck -- Error & Retries < 3 --> Reflect[sql_error_reflection_node]
        Reflect --> GenSQL
        ExecCheck -- Success / Max Retries --> FormatAns[represent_final_answer]
    end

    subgraph ETL Analyst Subsystem
        RouterEdge -- "etl" --> ETLNode[etl_node]
        ETLNode --> ETLGraph[agents/etl_analyst.py: etl_analyst]
        ETLGraph --> ETLLLM[llm_node: ChatGroq.bind_tools]
        ETLLLM --> ToolCheck{is_tool_call}
        ToolCheck -- tool_calls --> ETLToolNode[tool_node]
        ETLToolNode --> ExtractTool[extract_load_tool: requests]
        ETLToolNode --> TransformTool[transform_load_tool: AST Validated exec]
        ETLToolNode --> ETLLLM
        ToolCheck -- finished --> ETLEnd[END]
    end

    subgraph Visualization Subsystem
        RouterEdge -- "viz" --> VizNode[viz_node]
        VizNode --> VizGraph[agents/viz_analyst.py: viz_analyst]
        VizGraph --> GenChart[generate_chart_node: Matplotlib / Seaborn]
        GenChart --> ChartStore[(data/visualizations/*.png)]
    end

    FormatAns --> FinalOutput([API TaskResponse / Streamlit UI])
    CancelSQL --> FinalOutput
    ETLEnd --> FinalOutput
    GenChart --> FinalOutput
```

---

## 🛠️ Complete Inventory of Current Source Files

- **`main.py`**: CLI entry point executing `data_agent.invoke()`.
- **`app.py`**: FastAPI backend service exposing `/api/v1/tasks`, `/api/v1/schema`, and `/health`.
- **`app_ui.py`**: Streamlit web chat UI with database schema inspector, mermaid graph viewer, and benchmark runner.
- **`evals/run_evals.py`**: Automated LLM-as-a-Judge evaluation benchmark harness.
- **`agents/data_agent.py`**: Master Router graph (`router_node`, `sql_node`, `etl_node`, `viz_node`).
- **`agents/sql_analyst.py`**: SQL Analyst graph with reflection self-correction retry loop.
- **`agents/etl_analyst.py`**: ReAct tool agent (`extract_load_tool`, `transform_load_tool`).
- **`agents/viz_analyst.py`**: Data Visualization chart generation agent.
- **`Models/schema.py`**: Pydantic schemas (`AgentSchema`, `JudgeSchema`, `ETLAgentSchema`, `VizAgentSchema`, `RouterSchema`, `DataAgentSchema`).
- **`utils/database.py`**: PostgreSQL connection driver & schema introspection utility (connection closed bug fixed).
- **`utils/etl_tools.py`**: API extractor, dataset preview context, and AST-validated Python code executor.
- **`utils/llm_pick.py`**: LLM provider resolver (`LLM_PROVIDER=groq` with `ChatGroq`).
- **`feed_db.py`**: PostgreSQL DDL creation & CSV bulk data loader.
