# 02 — Prerequisites and Concepts

Before exploring the source code of **Agentic AI - Data Agent**, you should understand the core concepts and frameworks used throughout the repository.

---

## 🔑 Core Concepts & Frameworks

### 1. LangGraph StateGraph & State Machine
* **What it means**: LangGraph is a library for building stateful, multi-actor applications with LLMs using graph structures. A `StateGraph` defines nodes (Python functions that receive state and return state updates) and edges (control flow transitions between nodes).
* **Why it exists**: Linear LLM chains (`LLMChain`) cannot handle dynamic loops, branching, human-in-the-loop validation, or complex multi-agent delegation.
* **How used in THIS project**:
  - Main router graph: `data_agent_graph = StateGraph(DataAgentSchema)` in [agents/data_agent.py](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L76)
  - SQL graph: `sql_agent_graph = StateGraph(AgentSchema)` in [agents/sql_analyst.py](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L169)
  - ETL graph: `etl_analyst_graph = StateGraph(ETLAgentSchema)` in [agents/etl_analyst.py](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L136)

### 2. Pydantic State & Reducers
* **What it means**: Pydantic models define schema validation for data structures. In LangGraph, state is passed as a Pydantic model or TypedDict. Reducers (like `Annotated[list, add]`) specify how state updates from nodes are merged into the existing state.
* **Why it exists**: Ensures strong typing across node boundaries and maintains message histories across graph iterations.
* **How used in THIS project**:
  - `AgentSchema`, `JudgeSchema`, `ETLAgentSchema`, `RouterSchema`, `DataAgentSchema` in [Models/schema.py](file:///e:/AI_Data_Agent-main/Models/schema.py#L6-L32).
  - Notice `messages : Annotated[list,add]` in `AgentSchema` ([Models/schema.py:L7](file:///e:/AI_Data_Agent-main/Models/schema.py#L7)), which appends new messages returned by nodes to the existing message list.

### 3. Structured Outputs (`with_structured_output`)
* **What it means**: Forces the LLM to output responses matching a Pydantic schema instead of plain text, using OpenAI/Anthropic function calling or JSON mode under the hood.
* **Why it exists**: Guarantees deterministic, machine-readable decisions (e.g. `{"answer": "sql", "comments": "..."}`) for routing and classification nodes.
* **How used in THIS project**:
  - Router classification: `llm_router = llm.with_structured_output(RouterSchema)` in [agents/data_agent.py:L20](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L20)
  - SQL Safety Judge: `llm_judge = llm.with_structured_output(JudgeSchema)` in [agents/sql_analyst.py:L89](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L89)

### 4. LangChain Tool Calling (`@tool`)
* **What it means**: The `@tool` decorator transforms Python functions into tools with JSON schemas describing their arguments so that LLMs can select and call them autonomously.
* **Why it exists**: Allows LLMs to interact with external APIs, filesystems, and databases.
* **How used in THIS project**:
  - `extract_load_tool` in [agents/etl_analyst.py:L18-L35](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L18-L35)
  - `transform_load_tool` in [agents/etl_analyst.py:L37-L81](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L37-L81)
  - Bound to LLM via `llm.bind_tools(tools)` in [agents/etl_analyst.py:L88](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L88)

### 5. PostgreSQL Schema Introspection
* **What it means**: Querying `information_schema.tables` and `information_schema.columns` to programmatically extract database structure.
* **Why it exists**: LLMs require exact table and column names to write error-free SQL queries.
* **How used in THIS project**:
  - Implemented in `DatabaseUtil.schema_details("public")` in [utils/database.py:L16-L60](file:///e:/AI_Data_Agent-main/utils/database.py#L16-L60). Retrieves tables, column data types, and top 5 sample records per table.

### 6. Dynamic Code Generation & Execution (`exec()`)
* **What it means**: Having an LLM write executable Python code (e.g. Pandas code) as text, and passing that text to Python's built-in `exec()` function.
* **Why it exists**: Enables open-ended data transformation operations (filtering, aggregation, pivoting) without pre-defining every single pandas tool function.
* **How used in THIS project**:
  - Implemented in `ETLTools.execute_code(code)` in [utils/etl_tools.py:L78-L93](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L78-L93) and invoked inside `transform_load_tool` ([agents/etl_analyst.py:L79](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L79)).

---

## 📋 Concept Mapping Matrix

| Concept | Used In File | Key Function / Symbol |
| --- | --- | --- |
| Hierarchical Graph Routing | `agents/data_agent.py` | `router_node`, `route_edge` |
| ReAct Tool Loop | `agents/etl_analyst.py` | `llm_node`, `tool_node`, `is_tool_call` |
| Guardrail Judge Pattern | `agents/sql_analyst.py` | `is_safe_sql`, `is_safe_sql_edge` |
| Pydantic Schemas | `Models/schema.py` | `AgentSchema`, `JudgeSchema`, `RouterSchema` |
| Dynamic LLM Tiering | `utils/llm_pick.py` | `pick_llm(level)` |
| Relational DB Ingestion | `feed_db.py` | `load_csv()`, PostgreSQL `COPY` |
