# 22 — Keep, Improve, Redesign, Remove, and Add Categorization

This document categorizes all components of the **CURRENT Agentic AI Data Agent** into architectural action buckets.

---

## 🏷️ Component Action Matrix

### 1. KEEP (Already Excellent)
- **`agents/sql_analyst.py`**: The 8-node state graph with SQL generation, `JudgeSchema` safety check, and `sql_error_reflection_node` self-correction loop.
- **`utils/llm_pick.py`**: The provider LLM factory with Groq `ChatGroq` default and fallback provider options.
- **`app.py`**: FastAPI server with CORS, health check, and task submission endpoints.
- **`app_ui.py`**: Streamlit visual dashboard with chat, graph rendering, and evals.
- **`evals/run_evals.py`**: Automated LLM-as-a-Judge benchmark harness.

### 2. IMPROVE (Refine in Future)
- **`utils/etl_tools.py`**: AST code validator works well; can be enhanced with E2B micro-VM container isolation.
- **`utils/database.py`**: Connection bug is fixed; add connection pooling for high API concurrency.

### 3. REDESIGN (Architecture Overhaul)
- **Multi-Goal Planning**: Upgrade `router_node` in `data_agent.py` to a multi-step `PlannerAgent` for compound queries.

### 4. REMOVE (De-clutter)
- Obsolete legacy test scripts (`test_agent.py`, `agent_1.py`) in root directory.

### 5. ADD (Missing Features)
- `Dockerfile` and `docker-compose.yml` for single-command production container deployment.
- `tests/test_agents.py` pytest unit test harness.
