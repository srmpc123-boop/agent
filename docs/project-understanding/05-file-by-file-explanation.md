# 05 — File-by-File Explanation

This document provides a comprehensive analysis of every Python script and configuration file in the repository.

---

## 📄 1. `main.py`
* **Path**: [main.py](file:///e:/AI_Data_Agent-main/main.py)
* **Purpose**: Primary execution entry point for testing user queries against the compiled Data Agent graph.
* **Why this file exists**: Provides an executable interface to run the entire multi-agent system.
* **Imports**:
  - `data_agent` from `agents.data_agent` ([main.py:L1](file:///e:/AI_Data_Agent-main/main.py#L1))
  - `HumanMessage` from `langchain_core.messages` ([main.py:L2](file:///e:/AI_Data_Agent-main/main.py#L2))
* **Execution Role**: Top-level driver.
* **Input**: Dictionary containing `messages` list with a `HumanMessage` and an empty `route_response`.
* **Output**: Prints full state output returned by `data_agent.invoke()`.
* **Side Effects**: Triggers API calls, file writes, or database queries depending on prompt.

---

## 📄 2. `feed_db.py`
* **Path**: [feed_db.py](file:///e:/AI_Data_Agent-main/feed_db.py)
* **Purpose**: Database initializations and data loading script.
* **Why this file exists**: Establishes PostgreSQL schema (`public`), creates 5 tables (`users`, `vehicles`, `rides`, `payments`, `ratings`), sets foreign keys/indexes, and bulk-loads CSV records using PostgreSQL `COPY`.
* **Imports**: `os`, `csv`, `psycopg2`, `psycopg2.sql`, `dotenv.load_dotenv` ([feed_db.py:L1-L6](file:///e:/AI_Data_Agent-main/feed_db.py#L1-L6))
* **Key Functions & Logic**:
  - `DB_CONFIG`: Map constructed from environment variables (`host`, `port`, `database`, `user`, `password`).
  - `create_tables_sql`: Multiline DDL string creating schema, tables, foreign keys, check constraints, and performance indexes ([feed_db.py:L42-L212](file:///e:/AI_Data_Agent-main/feed_db.py#L42-L212)).
  - `load_csv(table_name, csv_file, columns)`: Uses `cursor.copy_expert()` with `COPY public.<table_name> (...) FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',', NULL '')` ([feed_db.py:L243-L281](file:///e:/AI_Data_Agent-main/feed_db.py#L243-L281)).
  - Data Truncation: Executes `TRUNCATE TABLE ratings, payments, rides, vehicles, users CASCADE;` before loading ([feed_db.py:L227-L235](file:///e:/AI_Data_Agent-main/feed_db.py#L227-L235)).
* **Side Effects**: Modifies PostgreSQL database state (drops data, creates schema/tables, populates thousands of rows).

---

## 📄 3. `Models/schema.py`
* **Path**: [Models/schema.py](file:///e:/AI_Data_Agent-main/Models/schema.py)
* **Purpose**: Pydantic schema definitions for state management and structured outputs.
* **Why this file exists**: Defines strict type contracts for graph states and LLM decisions.
* **Classes**:
  1. `AgentSchema(BaseModel)` ([Models/schema.py:L6-L15](file:///e:/AI_Data_Agent-main/Models/schema.py#L6-L15)):
     - SQL Agent state model.
     - Attributes: `messages` (`Annotated[list, add]`), `user_question`, `curated_ques`, `prompt_query_context`, `generated_sql_query`, `is_safe`, `comments`, `sql_query_execution_result`, `final_answer`.
  2. `JudgeSchema(BaseModel)` ([Models/schema.py:L18-L20](file:///e:/AI_Data_Agent-main/Models/schema.py#L18-L20)):
     - Safety judge structured output schema (`answer`: `"Yes"`/`"No"`, `comments`).
  3. `ETLAgentSchema(BaseModel)` ([Models/schema.py:L23-L24](file:///e:/AI_Data_Agent-main/Models/schema.py#L23-L24)):
     - ETL Agent state model (`messages`: `Annotated[list, add]`).
  4. `RouterSchema(BaseModel)` ([Models/schema.py:L26-L28](file:///e:/AI_Data_Agent-main/Models/schema.py#L26-L28)):
     - Top-level router structured output schema (`answer`: `"sql"`/`"etl"`, `comments`).
  5. `DataAgentSchema(BaseModel)` ([Models/schema.py:L30-L32](file:///e:/AI_Data_Agent-main/Models/schema.py#L30-L32)):
     - Outer Data Agent graph state model (`messages`, `route_response`).

---

## 📄 4. `agents/data_agent.py`
* **Path**: [agents/data_agent.py](file:///e:/AI_Data_Agent-main/agents/data_agent.py)
* **Purpose**: Outer router agent graph that directs user queries to either `sql_analyst` or `etl_analyst`.
* **Imports**: `sql_analyst`, `etl_analyst`, `pick_llm`, `RouterSchema`, `DataAgentSchema`, `StateGraph`, `START`, `END`.
* **Nodes**:
  - `router_node(state)` ([agents/data_agent.py:L26-L36](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L26-L36)): Calls LLM with `RouterSchema` to determine `"sql"` vs `"etl"`.
  - `etl_node(state)` ([agents/data_agent.py:L38-L49](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L38-L49)): Invokes `etl_analyst.invoke()`.
  - `sql_node(state)` ([agents/data_agent.py:L51-L71](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L51-L71)): Constructs `input_schema` and invokes `sql_analyst.invoke()`.
* **Routing Edge**: `route_edge(state)` checks `state.route_response` and branches to `"sql_node"` or `"etl_node"`.

---

## 📄 5. `agents/sql_analyst.py`
* **Path**: [agents/sql_analyst.py](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py)
* **Purpose**: Specialized graph for converting natural language queries into safe, executable PostgreSQL queries.
* **Nodes**:
  1. `curate_ques(state)` ([sql_analyst.py:L15-L26](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L15-L26)): Re-phrases/cleans original question via low-tier LLM.
  2. `prompt_query_context(state)` ([sql_analyst.py:L29-L66](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L29-L66)): Queries PostgreSQL schema details via `DatabaseUtil` and constructs prompt context.
  3. `generate_sql(state)` ([sql_analyst.py:L70-L80](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L70-L80)): Generates raw SQL query using medium-tier LLM.
  4. `is_safe_sql(state)` ([sql_analyst.py:L84-L105](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L84-L105)): Validates SQL safety via LLM structured judge (`JudgeSchema`).
  5. `canceled_sql(state)` ([sql_analyst.py:L109-L116](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L109-L116)): Returns cancellation message if query is unsafe.
  6. `execute_sql(state)` ([sql_analyst.py:L120-L138](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L120-L138)): Runs SQL query via `DatabaseUtil.execute_sql()`.
  7. `represent_final_answer(state)` ([sql_analyst.py:L142-L165](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L142-L165)): Generates natural language summary of SQL query execution results.

---

## 📄 6. `agents/etl_analyst.py`
* **Path**: [agents/etl_analyst.py](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py)
* **Purpose**: ReAct-style agent graph for API data extraction and dynamic Pandas transformations.
* **Tools**:
  - `@tool extract_load_tool`: Extracts data from API URL and saves file.
  - `@tool transform_load_tool`: Reads dataset context, prompts LLM for Pandas code, and executes code via `ETLTools.execute_code()`.
* **Nodes**:
  - `llm_node(state)` ([etl_analyst.py:L93-L109](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L93-L109)): Prompts tool-bound LLM.
  - `tool_node(state)` ([etl_analyst.py:L112-L132](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L112-L132)): Iterates over `state.messages[-1].tool_calls`, invokes tool, and appends `ToolMessage`.

---

## 📄 7. `utils/database.py`
* **Path**: [utils/database.py](file:///e:/AI_Data_Agent-main/utils/database.py)
* **Purpose**: Encapsulates PostgreSQL database interactions using `psycopg2`.
* **Class**: `DatabaseUtil`
  - `__init__(db_config)`: Establishes connection (`self.connection`).
  - `schema_details(schema_name)`: Queries `information_schema` for tables and columns, fetches 5 sample rows per table, formats context string.
  - `execute_sql(query)`: Executes query string, fetches all rows, commits transaction, and returns string representation.
* **Potential Issue**: Lines 57-58 and 76-77 close `self.connection` inside `finally` blocks. This renders the `DatabaseUtil` instance unusable for subsequent calls!

---

## 📄 8. `utils/etl_tools.py`
* **Path**: [utils/etl_tools.py](file:///e:/AI_Data_Agent-main/utils/etl_tools.py)
* **Purpose**: Low-level operational toolkit for web requests, Pandas loading, and Python code execution.
* **Methods**:
  - `extract_load(url, output_folder, format)`: Calls `requests.get()`, normalizes JSON via `pd.json_normalize(data['results'])`, exports CSV/JSON/Parquet.
  - `transform_load_context(file_path)`: Reads preview dataset and returns `str(df.head(3))`.
  - `execute_code(code)`: Executes code string via `exec(code)`.

---

## 📄 9. `utils/llm_pick.py`
* **Path**: [utils/llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py)
* **Purpose**: Factory method for instantiating LLM objects based on difficulty tier.
* **Function**: `pick_llm(level: str)`
  - Tier `"low"` -> `ChatOpenAI(model_name="gpt-5.6-luna", temperature=0)`
  - Tier `"medium"` -> `ChatOpenAI(model_name="gpt-5.6-terra", temperature=0)`
  - Tier `"high"` -> `ChatOpenAI(model_name="gpt-5.6-sol", temperature=0)`
  - Tier `"claude"` -> `ChatAnthropic(model_name="claude-sonnet-5")`
* **Discrepancy Note**: The model names (`gpt-5.6-luna`, etc.) are non-standard placeholder model strings. In practice, these must be updated to valid OpenAI (`gpt-4o-mini`, `gpt-4o`) or Anthropic (`claude-3-5-sonnet-20240620`) model strings.
