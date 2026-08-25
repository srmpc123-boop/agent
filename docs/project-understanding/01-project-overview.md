# 01 — Project Overview

## Metadata
- **Project Name**: Agentic AI - Data Agent
- **Repository Location**: `e:/AI_Data_Agent-main`
- **Primary Framework**: LangGraph / LangChain / Python 3.12+
- **Database**: PostgreSQL (`psycopg2-binary`)

---

## 🎯 Purpose & Problem Statement

### What is this project?
The **Agentic AI Data Agent** is an autonomous multi-agent Python application designed to act as an AI-powered Data Engineer and SQL Analyst. It translates natural language user prompts into complex database queries or data extraction/transformation pipelines.

### Why was it built?
Traditional data operations require non-technical stakeholders to rely on data engineers or analysts to:
1. Write custom SQL queries against relational databases.
2. Ensure queries do not accidentally modify or delete production data.
3. Write ETL scripts using Python/Pandas to fetch data from web APIs and transform CSV/JSON/Parquet files.

This project automates both workflows by orchestrating specialized AI agents that dynamically discover database schema details, construct and safety-check SQL queries, fetch external API data, and execute Pandas code.

---

## ⏱️ Explanations at Different Detail Levels

### 30-Second Explanation (Beginner Friendly)
> Imagine having an AI assistant that understands plain English and can either answer complex questions about your company database or automatically download, clean, and save files from web APIs. You just ask a question, and the AI determines whether it needs to talk to your PostgreSQL database or write a Python script to handle files, execute the work safely, and give you the final result.

### 2-Minute Explanation (Technical Overview)
> The **Data Agent** is a multi-agent system implemented using **LangGraph**. When a natural language query arrives at [main.py](file:///e:/AI_Data_Agent-main/main.py#L4-L8), it passes into a top-level **Router Graph** ([agents/data_agent.py](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L26-L36)). 
> - If the user asks a database question (e.g., *"What payment methods are used?"*), the router dispatches the request to the **SQL Analyst Agent** ([agents/sql_analyst.py](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L169-L210)). This agent inspects PostgreSQL table metadata, generates a SQL query, passes the query through an **LLM Safety Judge** to block harmful commands like `DROP` or `DELETE`, runs the SQL query against PostgreSQL, and formats the output.
> - If the user asks for data extraction or transformation (e.g., *"Fetch pokemon data from PokeAPI and save to CSV"*), the router dispatches the request to the **ETL Analyst Agent** ([agents/etl_analyst.py](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L136-L160)). This agent uses tool calling to run custom API fetch routines or generate Pandas Python code executed in a sandbox-like environment.

### 10-Minute Explanation (Deep Architectural Walkthrough)
> The repository is structured into a hierarchical state graph architecture:
> 
> ```mermaid
> graph TD
>     User([User Query]) --> Main[main.py]
>     Main --> DataAgent[agents/data_agent.py: data_agent graph]
>     
>     subgraph Router Level
>         DataAgent --> RouterNode[router_node]
>         RouterNode --> RouteEval{route_edge}
>     end
>     
>     subgraph Sub-Agents
>         RouteEval -- route == 'sql' --> SQLAgent[agents/sql_analyst.py: sql_analyst graph]
>         RouteEval -- route == 'etl' --> ETLAgent[agents/etl_analyst.py: etl_analyst graph]
>     end
>     
>     subgraph SQL Pipeline
>         SQLAgent --> Curate[curate_ques]
>         Curate --> PromptCtx[prompt_query_context: DatabaseUtil.schema_details]
>         PromptCtx --> GenSQL[generate_sql]
>         GenSQL --> Judge[is_safe_sql: LLM Judge]
>         Judge -- safe == 'Yes' --> ExecSQL[execute_sql: DatabaseUtil.execute_sql]
>         Judge -- safe == 'No' --> CancelSQL[canceled_sql]
>         ExecSQL --> FinalAns[represent_final_answer]
>     end
>     
>     subgraph ETL Pipeline
>         ETLAgent --> LLMNode[llm_node: ChatAnthropic.bind_tools]
>         LLMNode --> ToolEval{is_tool_call}
>         ToolEval -- Tool Calls Present --> ToolNode[tool_node]
>         ToolNode --> ExtractLoad[extract_load_tool: ETLTools.extract_load]
>         ToolNode --> TransformLoad[transform_load_tool: ETLTools.transform_load_context + exec]
>         ToolNode --> LLMNode
>         ToolEval -- No Tool Calls --> END([End ETL Execution])
>     end
> ```
>
> 1. **State Management**: LangGraph manages state via Pydantic models defined in [Models/schema.py](file:///e:/AI_Data_Agent-main/Models/schema.py#L6-L32). The messages state variable relies on `Annotated[list, add]` to aggregate history.
> 2. **Dynamic LLM Selection**: [utils/llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L6-L34) dynamically instantiates `ChatOpenAI` or `ChatAnthropic` instances based on specified tier (`low`, `medium`, `high`, `claude`).
> 3. **Database Integration**: [feed_db.py](file:///e:/AI_Data_Agent-main/feed_db.py#L42-L212) defines a PostgreSQL schema for a ride-hailing dataset (`users`, `vehicles`, `rides`, `payments`, `ratings`) and loads sample CSV files using PostgreSQL `COPY`. [utils/database.py](file:///e:/AI_Data_Agent-main/utils/database.py#L16-L78) inspects `information_schema.tables` and `information_schema.columns` to inject table columns and top 5 sample rows directly into the SQL generation prompt context.

---

## 🌟 Major Features
- **Natural Language Query Routing**: Automatically routes intent to SQL or ETL workflows.
- **Dynamic PostgreSQL Schema Introspection**: Fetches real-time database schema information including sample rows.
- **LLM Safety Guardrail**: Evaluates SQL queries via structured Pydantic output (`JudgeSchema`) to prevent destructive actions (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `TRUNCATE`, `ALTER`).
- **Web API Extractor**: Converts JSON response payloads from external HTTP APIs into CSV, JSON, or Parquet files.
- **Dynamic Python Code Execution**: Generates Pandas transformation scripts based on dataset preview rows and executes them via `exec()`.

---

## 📊 Project Maturity & Implementation Status
- **Maturity Level**: Functional Proof-of-Concept / Prototype.
- **Strengths**: Elegant graph separation with LangGraph; strong prompt engineering for schema context inclusion; clean Pydantic schema validation.
- **Key Limitations**:
  - `DatabaseUtil` in [utils/database.py](file:///e:/AI_Data_Agent-main/utils/database.py#L57-L58) closes its DB connection in `finally` blocks, causing connection failure on subsequent calls if single-instance reused.
  - Model names in `utils/llm_pick.py` (`gpt-5.6-luna`, `gpt-5.6-terra`, `claude-sonnet-5`) are placeholders/non-standard API model identifiers that require adjustment for production OpenAI/Anthropic accounts.
  - Python `exec()` in `ETLTools` runs arbitrary LLM-generated code without sandbox isolation.
