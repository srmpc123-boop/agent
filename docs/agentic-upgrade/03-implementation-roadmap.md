# 03 — Implementation Roadmap & Time-Constrained Plans

This document provides a 7-phase master implementation roadmap, time-budgeted development plans, and a complete file-by-file modification plan.

---

## 🗺️ Master 7-Phase Strategic Roadmap

```text
Phase 1: Security & Reliability Foundation (P0)
   └── Fix database.py connection leak, update model strings, sandbox exec()

Phase 2: Agentic Core & Self-Correction (P0/P1)
   └── Implement SQL syntax error reflection loop & task state models

Phase 3: Backend API & REST Integration (P1)
   └── Implement FastAPI server (POST /api/v1/tasks, GET /status)

Phase 4: Evaluation & Benchmarking Framework (P1)
   └── Build evals/ suite testing routing, SQL accuracy, and safety

Phase 5: Observability & Tracing (P1)
   └── Integrate LangSmith distributed tracing & structlog JSON logging

Phase 6: Multi-Agent Expansion (P1/P2)
   └── Add Data Visualization Agent & Streamlit Interactive UI

Phase 7: Production Hardening (P2)
   └── Add connection pooling, audit logging, & Human-in-the-Loop breakpoints
```

---

## ⏱️ Time-Constrained Execution Plans

### 1. 1-Hour Plan (Immediate Stability Upgrade)
- **Goal**: Stop graph crashes, update API model names, and sandbox code execution.
- **Tasks**:
  1. Remove `connection.close()` from `finally` blocks in [utils/database.py](file:///e:/AI_Data_Agent-main/utils/database.py#L57-L58).
  2. Update invalid model identifiers in [utils/llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L18-L30) to `"gpt-4o-mini"`, `"gpt-4o"`, and `"claude-3-5-sonnet-20240620"`.
  3. Wrap `exec()` in [utils/etl_tools.py:L89](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L89) with AST import validation checking for forbidden modules (`os`, `sys`, `subprocess`).
- **Files Modified**: `utils/database.py`, `utils/llm_pick.py`, `utils/etl_tools.py`.

---

### 2. 3-Hour Plan (Core Agentic Upgrade)
- **Goal**: Complete 1-Hour plan + implement SQL self-correction loop and FastAPI server.
- **Tasks**:
  1. All 1-Hour tasks above.
  2. **SQL Reflection Node**: Add `sql_error_reflection_node` and conditional retry edge in [agents/sql_analyst.py](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py) to catch PostgreSQL syntax errors and retry up to 3 times.
  3. **FastAPI REST Server**: Create `app.py` exposing `POST /api/v1/tasks` and `GET /api/v1/tasks/{id}`.
- **Files Modified**: `agents/sql_analyst.py`, `app.py` [NEW].

---

### 3. 6-Hour Plan (Resume & Portfolio Grade Upgrade)
- **Goal**: Complete 3-Hour plan + LangSmith tracing, evaluation benchmark suite, and Streamlit UI.
- **Tasks**:
  1. All 3-Hour tasks above.
  2. **LangSmith Tracing**: Add tracing environment variables and structured JSON logging.
  3. **Evaluation Suite**: Create `evals/run_evals.py` testing routing precision and SQL execution accuracy.
  4. **Streamlit UI**: Create `app_ui.py` with an interactive chat interface rendering live agent thoughts and data tables.
- **Files Modified**: `utils/llm_pick.py`, `evals/run_evals.py` [NEW], `app_ui.py` [NEW].

---

### 4. 12-Hour Plan (Hackathon Winner Grade Upgrade)
- **Goal**: Complete 6-Hour plan + Data Visualization Agent and Human-in-the-Loop approval.
- **Tasks**:
  1. All 6-Hour tasks above.
  2. **Data Visualization Agent**: Build `agents/viz_analyst.py` to generate Matplotlib/Seaborn plots from query results.
  3. **HITL Breakpoints**: Add `interrupt()` approval breakpoints in `etl_analyst.py` before running dataset transformations over 50MB.
- **Files Modified**: `agents/data_agent.py`, `agents/viz_analyst.py` [NEW], `agents/etl_analyst.py`.

---

### 5. 1-Week Plan (Production-Grade Autonomous Platform)
- **Goal**: Full implementation of all 27 Target Architecture layers including connection pooling, database audit logs, dynamic replanning, and E2B cloud sandbox execution.

---

## 📁 File-Level Implementation Plan

| Action | Target File Path | Purpose / Responsibilities |
| --- | --- | --- |
| **[MODIFY]** | [utils/database.py](file:///e:/AI_Data_Agent-main/utils/database.py) | Remove `connection.close()` in `finally`; add `ThreadedConnectionPool`. |
| **[MODIFY]** | [utils/llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py) | Update model names to valid API identifiers; add cost-aware routing. |
| **[MODIFY]** | [utils/etl_tools.py](file:///e:/AI_Data_Agent-main/utils/etl_tools.py) | Add AST validation & sandboxed code execution in `execute_code()`. |
| **[MODIFY]** | [Models/schema.py](file:///e:/AI_Data_Agent-main/Models/schema.py) | Add `TaskState`, `TaskPlan`, `PlanStep`, and `AuditLog` schemas. |
| **[MODIFY]** | [agents/sql_analyst.py](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py) | Add `sql_error_reflection_node` and retry conditional edge. |
| **[MODIFY]** | [agents/etl_analyst.py](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py) | Add HITL approval breakpoint for high-impact file operations. |
| **[MODIFY]** | [agents/data_agent.py](file:///e:/AI_Data_Agent-main/agents/data_agent.py) | Register `viz_analyst` node and Supervisor planning orchestration. |
| **[NEW]** | `app.py` | FastAPI REST API backend service with task endpoints. |
| **[NEW]** | `app_ui.py` | Streamlit interactive web chat dashboard. |
| **[NEW]** | `agents/viz_analyst.py` | Matplotlib/Seaborn chart generation agent. |
| **[NEW]** | `evals/run_evals.py` | LLM-as-a-Judge benchmark evaluation test harness. |
| **[NEW]** | `tests/test_agents.py` | `pytest` unit test suite for graph nodes and tools. |
