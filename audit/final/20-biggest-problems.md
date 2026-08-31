# 20 — Top Problems Audit

This document details the top remaining technical issues and areas for improvement in the **CURRENT Agentic AI Data Agent** codebase.

---

## ⚠️ Top 10 Technical Observations & Remaining Issues

| Rank | Observation / Issue | Severity | Affected File | Impact | Recommended Fix |
| --- | --- | --- | --- | --- | --- |
| 1 | **Missing Docker Container Manifest** | Medium | Root directory | Lacks `Dockerfile` for containerized deployment | Add `Dockerfile` & `docker-compose.yml` |
| 2 | **No Unit Test Suite (`pytest`)** | Medium | `tests/` | Benchmark harness exists, but missing unit tests | Add `tests/test_agents.py` with pytest |
| 3 | **Ephemeral Graph Memory** | Low | `agents/data_agent.py` | State is lost across server restarts | Add `MemorySaver` / `SqliteSaver` checkpointer |
| 4 | **No Multi-Goal Task Planner** | Low | `agents/data_agent.py` | Router selects one branch per prompt | Add `PlannerAgent` node to break down compound goals |
| 5 | **Regex Parsing for Python Code** | Low | `agents/viz_analyst.py` | Relies on regex to extract code from markdown | Use Pydantic structured output for code generation |
| 6 | **Manual Model Fallback** | Low | `utils/llm_pick.py` | Requires manual `LLM_PROVIDER` environment toggle | Add automatic try-except provider fallback |
| 7 | **Hardcoded Connection Credentials** | Low | `utils/database.py` | Default credentials in fallback args | Enforce strict env variable loading |
| 8 | **No Connection Pool in DatabaseUtil** | Low | `utils/database.py` | Recreates cursor on each query | Add `psycopg2.pool.ThreadedConnectionPool` |
| 9 | **Raw String Outputs in Tool Responses**| Low | `agents/etl_analyst.py` | Tools return string text | Standardize tool outputs using Pydantic models |
| 10 | **Unused Old Test Scripts** | Low | `test_agent.py` | Legacy scratch files present in workspace | Clean up obsolete scratch scripts |
