# 12 — Data Flow

This document details how data structures, schemas, input/output formats, and state state mutations flow across the entire **Agentic AI - Data Agent** system.

---

## 🌊 Master Data Lifecycle Architecture

```text
User Input Prompt (str)
         │
         ▼
[main.py] -> Wraps in HumanMessage & initial DataAgentSchema dict
         │
         ▼
[agents/data_agent.py: router_node]
   └── Parses state.messages[-1].content
   └── Returns RouterSchema(answer: "sql"|"etl", comments: str)
   └── Mutates state.route_response
         │
  ┌──────┴──────────────────────────────┐
  ▼                                     ▼
[sql_node]                           [etl_node]
  │                                     │
  ├─> Constructs AgentSchema dict       ├─> Invokes ETLAgentSchema graph
  ├─> Curates question                  ├─> Tool calls extract/transform
  ├─> Injects DB schema text context    ├─> Mutates message history with ToolMessage
  ├─> Generates SQL string              └─> Returns updated state
  ├─> Evaluates JudgeSchema ("Yes"/"No")
  ├─> Executes SQL -> Raw string tuples
  └─> Synthesizes text AIMessage
         │
         ▼
Final Output returned to main.py / User
```

---

## 📐 Data State Schema Specifications (`Models/schema.py`)

### 1. `DataAgentSchema` (Outer Graph State)
* **Fields**:
  - `messages`: `Annotated[list, add]` - Appends conversation history.
  - `route_response`: `str` - Holds `"sql"` or `"etl"` routing directive.

### 2. `RouterSchema` (LLM Decision DTO)
* **Fields**:
  - `answer`: `Literal["sql", "etl"]` - Forced routing decision.
  - `comments`: `str` - LLM reasoning for classification.

### 3. `AgentSchema` (SQL Analyst State)
* **Fields**:
  - `messages`: `Annotated[list, add]`
  - `user_question`: `str` - Unmodified input query.
  - `curated_ques`: `str` - Cleaned analytics query.
  - `prompt_query_context`: `str` - SQL prompt containing full schema details.
  - `generated_sql_query`: `str` - Raw generated SQL statement.
  - `is_safe`: `Literal["Yes", "No"]` - Safety verdict.
  - `comments`: `str` - Judge evaluation notes.
  - `sql_query_execution_result`: `str` - Raw string of DB tuple result.
  - `final_answer`: `str` - Formatted natural language response.

### 4. `JudgeSchema` (Safety LLM DTO)
* **Fields**:
  - `answer`: `Literal["Yes", "No"]`
  - `comments`: `str`

### 5. `ETLAgentSchema` (ETL Analyst State)
* **Fields**:
  - `messages`: `Annotated[list, add]`

---

## 🔀 Transformation Example Matrix

| Stage | Input Format | Output Format | Transforming Function |
| --- | --- | --- | --- |
| API Extraction | HTTP JSON (`{"results": [...]}`) | CSV / Parquet / JSON file | `ETLTools.extract_load()` via `pd.json_normalize` |
| DB Introspection | PostgreSQL catalog tables | Single multiline text string | `DatabaseUtil.schema_details()` |
| SQL Execution | SQL Query string | Python tuple list string (`"[(1, 'A')]"`)| `DatabaseUtil.execute_sql()` |
| Final Synthesis | Tuple string + Curated question | Clean English text | `represent_final_answer()` node |
