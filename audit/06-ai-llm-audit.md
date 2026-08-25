# 06 — AI / LLM Quality Audit

This audit evaluates model selection, tiering, temperature configuration, context management, structured output usage, and LLM guardrails in **Agentic AI - Data Agent**.

---

## 🧠 LLM Architecture Evaluation

### 1. Model Selection & Tiering Strategy (`utils/llm_pick.py`)
The system uses a tiered model resolution strategy:
- **Low Tier** (`"low"`): Used for simple tasks like question curation (`curate_ques`) and final text synthesis (`represent_final_answer`).
- **Medium Tier** (`"medium"`): Used for SQL generation (`generate_sql`) and SQL safety judging (`is_safe_sql`).
- **Claude Tier** (`"claude"`): Used for top-level intent routing (`llm_router`) and complex Pandas code generation (`transform_load_tool`).

#### Evaluation:
- **Strengths**: Tiering models by task difficulty optimizes latency and token costs.
- **Weakness**: As noted, the model strings in `utils/llm_pick.py` (`gpt-5.6-luna`, `gpt-5.6-terra`, `claude-sonnet-5`) are invalid API model names that must be updated.

---

### 2. Structured Output Implementation (`with_structured_output`)
The codebase uses Pydantic schemas bound to LLMs via `with_structured_output`:
- [agents/data_agent.py:L20](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L20): `llm_router = llm.with_structured_output(RouterSchema)`
- [agents/sql_analyst.py:L89](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L89): `llm_judge = llm.with_structured_output(JudgeSchema)`

#### Evaluation:
- **Rating**: **Excellent**. Ensures 100% deterministic output formatting for critical routing decisions and safety verdicts.

---

### 3. Context Management & Prompt Grounding
In `agents/sql_analyst.py`, the `prompt_query_context` node fetches table schemas, column data types, and 5 sample rows per table using `DatabaseUtil.schema_details("public")`.

#### Evaluation:
- **Strengths**: Providing sample data in the prompt grounds the LLM, preventing hallucinated column names.
- **Weakness**: Injecting sample data for all tables on every request consumes excessive prompt tokens. For large databases with 50+ tables, this will overflow LLM context limits.

---

## ⚡ Summary AI/LLM Checklist

| Dimension | Assessment | Notes |
| --- | --- | --- |
| Temperature Setting | Fixed at `0` | Ideal for deterministic code/SQL generation. |
| Token Optimization | Needs Improvement | Ingests full database schema on every query. |
| Hallucination Guardrails | Implemented | Injects live schema preview; passes output to SQL judge. |
| Fallback Models | Not Implemented | No automatic failover if API call fails. |
| Response Streaming | Not Implemented | Synchronous model invocations only. |
