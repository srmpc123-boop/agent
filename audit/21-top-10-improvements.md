# 21 — Top 10 Highest-Value Improvements

This document ranks the **10 highest-value improvements** across the entire audit, prioritized by `Impact × Feasibility`.

---

## 🔝 Top 10 Improvements Ranking

### 1. Fix Database Connection Closing Bug
* **Current Problem**: `utils/database.py` closes `self.connection` in `finally` blocks, breaking multi-query runs with `psycopg2.InterfaceError`.
* **Recommended Fix**: Remove `connection.close()` from `finally` or implement connection pooling.
* **Effort**: 15 minutes | **Files**: [utils/database.py](file:///e:/AI_Data_Agent-main/utils/database.py#L57-L58)

---

### 2. Fix Invalid LLM Model Identifiers
* **Current Problem**: `utils/llm_pick.py` uses non-existent model strings (`gpt-5.6-luna`, `claude-sonnet-5`).
* **Recommended Fix**: Update model strings to standard API IDs (`gpt-4o-mini`, `gpt-4o`, `claude-3-5-sonnet-20240620`).
* **Effort**: 15 minutes | **Files**: [utils/llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L18-L30)

---

### 3. Sandbox Python Code Execution (`exec()`)
* **Current Problem**: `ETLTools.execute_code()` runs un-sanitized LLM code directly on host OS via `exec()`.
* **Recommended Fix**: Containerize code execution or use `RestrictedPython` / `e2b`.
* **Effort**: 2 hours | **Files**: [utils/etl_tools.py](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L89)

---

### 4. Create Automated `pytest` Suite
* **Current Problem**: Zero automated tests in repository.
* **Recommended Fix**: Create `tests/` directory with unit tests for router, SQL judge, and tools.
* **Effort**: 3 hours | **Files**: `tests/` [NEW]

---

### 5. Add FastAPI Web REST API Layer
* **Current Problem**: System can only be invoked programmatically via Python script.
* **Recommended Fix**: Create `app.py` exposing `POST /query` endpoint.
* **Effort**: 1.5 hours | **Files**: `app.py` [NEW], [main.py](file:///e:/AI_Data_Agent-main/main.py)

---

### 6. Implement SQL Self-Correction Loop
* **Current Problem**: If PostgreSQL returns a syntax error, execution terminates.
* **Recommended Fix**: Add a conditional retry edge in `sql_analyst.py` routing syntax errors back to `generate_sql`.
* **Effort**: 1.5 hours | **Files**: [agents/sql_analyst.py](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py)

---

### 7. Replace Standard `print()` with Structured Logging & LangSmith
* **Current Problem**: No structured logs or distributed tracing.
* **Recommended Fix**: Add standard Python `logging` and enable `LANGCHAIN_TRACING_V2=true`.
* **Effort**: 1 hour | **Files**: All files in `agents/` and `utils/`

---

### 8. Build Interactive Streamlit Chat UI
* **Current Problem**: No visual user interface.
* **Recommended Fix**: Build a web chat app rendering graph states and intermediate tool calls.
* **Effort**: 3 hours | **Files**: `app_ui.py` [NEW]

---

### 9. Add Data Visualization Agent
* **Current Problem**: System returns raw text/tuples; cannot generate charts.
* **Recommended Fix**: Add a 3rd sub-agent graph (`viz_analyst`) that generates Matplotlib/Seaborn plots.
* **Effort**: 4 hours | **Files**: `agents/viz_analyst.py` [NEW], [agents/data_agent.py](file:///e:/AI_Data_Agent-main/agents/data_agent.py)

---

### 10. Optimize Schema Context Prompt Tokens
* **Current Problem**: Ingests all tables and sample rows into context on every query.
* **Recommended Fix**: Cache schema metadata and only inject sample rows for tables relevant to the query.
* **Effort**: 2 hours | **Files**: [utils/database.py](file:///e:/AI_Data_Agent-main/utils/database.py), [agents/sql_analyst.py](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py)
