# 20 — Time-Based Improvement Roadmap

This roadmap provides concrete, step-by-step action plans based on available development time budgets.

---

## ⏱️ Budget 1: 30 Minutes (Immediate Fixes)

### Tasks:
1. **Fix DB Connection Bug ([utils/database.py](file:///e:/AI_Data_Agent-main/utils/database.py#L57-L58))**: Remove `connection.close()` from `finally` blocks in `schema_details` and `execute_sql`.
2. **Fix Invalid LLM Model Names ([utils/llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L18-L30))**: Map `"low"` to `"gpt-4o-mini"`, `"medium"` to `"gpt-4o"`, and `"claude"` to `"claude-3-5-sonnet-20240620"`.
3. **Fix DB Password Typo ([utils/database.py:L84](file:///e:/AI_Data_Agent-main/utils/database.py#L84))**: Change `"potgres"` to `"postgres"`.

* **Impact**: Restores 100% execution reliability for multi-query graph invocations.

---

## ⏱️ Budget 2: 2 Hours (Production Readiness Core)

### Tasks:
1. Complete all 30-minute tasks above.
2. **Sandbox Code Execution ([utils/etl_tools.py:L89](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L89))**: Wrap code execution inside AST checks or containerized execution to neutralize security vulnerability.
3. **Build FastAPI REST Server**: Create `app.py` with `POST /query` endpoint wrapping `data_agent.invoke()`.
4. **Structured Logging**: Replace `print()` statements with standard Python `logging`.

* **Impact**: Converts raw script into a safe, secure, production-deployable microservice API.

---

## ⏱️ Budget 3: 6 Hours (Full Portfolio Upgrade)

### Tasks:
1. Complete all 2-hour tasks above.
2. **Implement `pytest` Suite**: Create `tests/` with 10 unit/integration tests for router, SQL judge, and tools.
3. **Build SQL Error Retry Edge**: In `agents/sql_analyst.py`, route DB execution errors back to `generate_sql` for automatic query correction.
4. **Build Streamlit Chat UI**: Create `app_ui.py` providing an interactive web interface for non-technical users.

* **Impact**: Transforms the project into a top-tier resume project and hackathon winner.
