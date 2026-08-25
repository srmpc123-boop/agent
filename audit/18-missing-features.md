# 18 — Missing Features Audit

This document identifies missing features that would provide high value to **Agentic AI - Data Agent**, categorized by priority and difficulty.

---

## 📋 Categorized Missing Features

### 1. Must-Have (Critical Infrastructure Gaps)
- **FastAPI Web Server Interface**: Currently the project can only be invoked via Python script (`main.py`). Needs a REST API layer (`POST /api/query`).
- **Connection Pooling (`psycopg2.pool`)**: Replaces buggy single connection pattern in `utils/database.py`.
- **Sandboxed Python Code Executor**: Replaces raw `exec()` in `utils/etl_tools.py` with `e2b` or Docker container execution.

### 2. High Value (Enhances Capabilities)
- **SQL Error Self-Correction Loop**: If PostgreSQL returns a syntax error, route back to `generate_sql` with the error message so the LLM can fix its query.
- **Data Visualization Agent**: A 3rd sub-agent graph (`viz_analyst`) that generates Matplotlib/Seaborn charts from SQL or CSV query results.
- **Interactive UI (Streamlit / Next.js)**: Web chat interface displaying graph execution state and intermediate tool calls.

### 3. Nice to Have (Enterprise Features)
- **Schema RAG**: Embed table schemas into vector storage for databases with 50+ tables, retrieving only relevant table contexts per query.
- **Structured Observability (LangSmith)**: Tracing token costs, latencies, and node failures.

---

## 🛠️ Feature Impact & Difficulty Matrix

| Feature | Category | Difficulty | Impact | Affected Files |
| --- | --- | --- | --- | --- |
| FastAPI REST Interface | Must Have | Low | High | `main.py`, `app.py` [NEW] |
| DB Connection Pooling | Must Have | Low | High | `utils/database.py` |
| Sandboxed Code Exec | Must Have | Medium | High | `utils/etl_tools.py` |
| SQL Self-Correction Loop | High Value | Medium | High | `agents/sql_analyst.py` |
| Visualization Agent | High Value | Medium | High | `agents/data_agent.py`, `agents/viz_analyst.py` [NEW] |
| Web UI (Streamlit) | High Value | Low | High | `app_ui.py` [NEW] |
