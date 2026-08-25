# 19 — Improvement Backlog

This document presents a prioritized engineering backlog of all bug fixes, refactorings, security enhancements, and feature additions for **Agentic AI - Data Agent**.

---

## 🎯 Prioritized Engineering Backlog

```text
Priority Scale:
- P0: Critical / System Breaking Defect
- P1: Very High Value / Core Architectural Fix
- P2: High Value Feature / Major Improvement
- P3: Medium Value / Polishing & Refactoring
- P4: Optional / Low Priority Extension
```

| Priority | ID | Task Description | Area | Effort | Risk |
| --- | --- | --- | --- | --- | --- |
| **P0** | **BUG-01** | Remove `connection.close()` from `finally` blocks in `utils/database.py` to fix closed connection crashes. | Database | 15 mins | Low |
| **P0** | **SEC-01** | Replace `exec()` in `utils/etl_tools.py` with sandboxed Python code execution (`RestrictedPython` / `e2b`). | Security | 2 hours | Medium |
| **P0** | **CFG-01** | Update model strings in `utils/llm_pick.py` from placeholder names (`gpt-5.6-luna`) to valid OpenAI/Anthropic model IDs. | Configuration | 15 mins | Low |
| **P1** | **TST-01** | Create `tests/` directory with `pytest` unit tests for `router_node`, `is_safe_sql`, and `extract_load_tool`. | Testing | 3 hours | Low |
| **P1** | **API-01** | Implement FastAPI REST wrapper exposing `POST /query` endpoint for `data_agent.invoke()`. | Backend | 2 hours | Low |
| **P2** | **AGT-01** | Implement SQL error self-correction retry edge from `execute_sql` back to `generate_sql` when DB returns syntax error. | Agents | 1.5 hours | Medium |
| **P2** | **OBS-01** | Replace `print()` statements with structured JSON logging and enable LangSmith tracing environment variables. | Observability | 1 hour | Low |
| **P3** | **UI-01** | Build a lightweight Streamlit web chat UI showing interactive graph state and step-by-step tool executions. | UX / UI | 3 hours | Low |
| **P3** | **DOC-01** | Remove hardcoded Windows paths in `utils/etl_tools.py` test comments and clean commented-out code blocks. | Cleanup | 30 mins | Low |
