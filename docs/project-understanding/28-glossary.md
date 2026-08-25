# 28 — Technical Glossary

This glossary defines domain-specific terms used throughout the **Agentic AI - Data Agent** project.

---

## 📖 Project Terms Glossary

### 1. LangGraph StateGraph
* **Definition**: A stateful graph orchestration framework built by LangChain. Nodes are Python functions that receive the graph state and return state updates.
* **In this project**: Used to build `data_agent_graph`, `sql_agent_graph`, and `etl_analyst_graph`.

### 2. Router Node (`router_node`)
* **Definition**: An agent node that inspects a user prompt and uses structured output to return an intent classification string (`"sql"` vs `"etl"`).
* **In this project**: Implemented in [agents/data_agent.py:L26-L36](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L26-L36).

### 3. SQL Safety Judge (`is_safe_sql`)
* **Definition**: An LLM guardrail pattern that evaluates generated SQL query safety against non-destructive criteria before allowing database execution.
* **In this project**: Implemented in [agents/sql_analyst.py:L84-L105](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L84-L105).

### 4. Tool Calling (`@tool`)
* **Definition**: A mechanism allowing an LLM to request the execution of predefined local Python functions by emitting formatted JSON function names and arguments.
* **In this project**: Used by `ETL Analyst Agent` for `extract_load_tool` and `transform_load_tool`.

### 5. Pydantic Reducer (`Annotated[list, add]`)
* **Definition**: A LangGraph annotation telling the graph engine to append new list items returned by a node to the existing state list rather than overwriting it.
* **In this project**: Used for the `messages` attribute in `AgentSchema`, `ETLAgentSchema`, and `DataAgentSchema` in [Models/schema.py](file:///e:/AI_Data_Agent-main/Models/schema.py).

### 6. Schema Introspection
* **Definition**: Querying relational database metadata tables (`information_schema.tables` and `information_schema.columns`) to discover table structures dynamically.
* **In this project**: Implemented in `DatabaseUtil.schema_details("public")` in [utils/database.py:L16-L60](file:///e:/AI_Data_Agent-main/utils/database.py#L16-L60).

### 7. Dynamic Code Execution (`exec()`)
* **Definition**: Python built-in function that parses and evaluates string input as Python code at runtime.
* **In this project**: Implemented in `ETLTools.execute_code()` in [utils/etl_tools.py:L78-L93](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L78-L93).
