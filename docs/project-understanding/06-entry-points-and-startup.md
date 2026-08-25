# 06 — Entry Points and Application Startup

This document traces how the **Agentic AI - Data Agent** bootstraps, initializes configuration, builds graphs, and prepares for execution.

---

## 🚀 Entry Points Overview

The project features two primary entry points:

1. **`main.py`** (Application Entry Point): Main entry point for querying the compiled agent system.
2. **`feed_db.py`** (Database Bootstrap Entry Point): Data pipeline setup script to populate PostgreSQL.

---

## 📊 Application Startup Flow

```text
[Execution Trigger: python main.py]
          │
          ▼
   1. Python Interpreter Starts
          │
          ▼
   2. Module Imports Triggered
      ├── agents.data_agent imports sql_analyst & etl_analyst
      ├── utils.llm_pick loads .env via load_dotenv()
      └── Models.schema loads Pydantic models
          │
          ▼
   3. Graph Construction & Compilation
      ├── sql_agent_graph constructed & compiled -> sql_analyst
      ├── etl_analyst_graph constructed & compiled -> etl_analyst
      └── data_agent_graph compiled -> data_agent
          │
          ▼
   4. main.py Execution Block (__name__ == "__main__")
      ├── Construct HumanMessage("I want to extract data from...")
      ├── Construct initial DataAgentSchema dictionary
      └── Invoke data_agent.invoke(...)
          │
          ▼
   5. Graph Runtime Processing & Response Output
```

---

## 🔍 Line-by-Line Startup Sequence

### Step 1: Module Imports & Environment Variable Loading
When `main.py` is run:
- [agents/data_agent.py](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L4) modifies `sys.path` to ensure root imports resolve correctly.
- Importing `utils.llm_pick` triggers `load_dotenv()` ([utils/llm_pick.py:L4](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L4)), loading `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `host`, `port`, `database`, `user`, and `password` into `os.environ`.

### Step 2: LLM Factory & Sub-graph Compilation
1. In `agents/sql_analyst.py`:
   - `sql_agent_graph` is defined as a `StateGraph(AgentSchema)`.
   - Nodes (`curate_ques`, `prompt_query_context`, `generate_sql`, `is_safe_sql`, `canceled_sql`, `execute_sql`, `represent_final_answer`) are registered.
   - Edges and conditional edge `is_safe_sql_edge` are attached.
   - `sql_analyst = sql_agent_graph.compile()` is executed ([agents/sql_analyst.py:L210](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L210)).
2. In `agents/etl_analyst.py`:
   - `@tool` functions `extract_load_tool` and `transform_load_tool` are instantiated.
   - `llm_bind = pick_llm("claude").bind_tools(tools)` binds the tools to Anthropic.
   - `etl_analyst_graph` is constructed with `llm_node` and `tool_node`.
   - `etl_analyst = etl_analyst_graph.compile()` is executed ([agents/etl_analyst.py:L160](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L160)).
3. In `agents/data_agent.py`:
   - `llm_router = pick_llm("claude").with_structured_output(RouterSchema)`.
   - `data_agent_graph` registers `router_node`, `etl_node`, and `sql_node`.
   - `data_agent = data_agent_graph.compile()` is executed ([agents/data_agent.py:L99](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L99)).

### Step 3: Invocation Execution
In `main.py`:
```python
response = data_agent.invoke(
    {
        "messages": [HumanMessage(content="I want to extract the data from the API endpoint 'https://pokeapi.co/api/v2/pokemon' and save it to data/extract folder in the csv format")],
        "route_response": ""
    }
)
```
Execution enters `data_agent_graph` at `START`, routing to `router_node`.
