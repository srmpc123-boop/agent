# 27 — Beginner Learning Path

This document divides learning the **Agentic AI - Data Agent** project into 6 progressive competency levels.

---

## 📈 6-Level Competency Roadmap

### Level 1 — Conceptual Understanding
* **Goal**: Understand what the system does without diving into Python code.
* **Reading**:
  - [01-project-overview.md](file:///e:/AI_Data_Agent-main/docs/project-understanding/01-project-overview.md)
  - [02-prerequisites-and-concepts.md](file:///e:/AI_Data_Agent-main/docs/project-understanding/02-prerequisites-and-concepts.md)
* **Check Point**: Can you explain to a colleague why the project has a separate SQL Agent and ETL Agent?

---

### Level 2 — Architecture & Environment Setup
* **Goal**: Install the project locally and run the database initialization script.
* **Tasks**:
  - Setup local `.venv`, run `pip install -e .` or `uv pip install -r requirements.txt`.
  - Configure `.env`.
  - Execute `python feed_db.py`.
  - Read [13-database-and-storage.md](file:///e:/AI_Data_Agent-main/docs/project-understanding/13-database-and-storage.md) and [19-deployment-and-runtime.md](file:///e:/AI_Data_Agent-main/docs/project-understanding/19-deployment-and-runtime.md).

---

### Level 3 — Data Models & Low-Level Utilities
* **Goal**: Understand state contracts and operational helper classes.
* **Files to Study**:
  - [Models/schema.py](file:///e:/AI_Data_Agent-main/Models/schema.py)
  - [utils/database.py](file:///e:/AI_Data_Agent-main/utils/database.py)
  - [utils/etl_tools.py](file:///e:/AI_Data_Agent-main/utils/etl_tools.py)
  - [utils/llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py)

---

### Level 4 — Agent Graph Implementation
* **Goal**: Master LangGraph state graphs, nodes, and conditional edges.
* **Files to Study**:
  - [agents/sql_analyst.py](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py)
  - [agents/etl_analyst.py](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py)
  - [agents/data_agent.py](file:///e:/AI_Data_Agent-main/agents/data_agent.py)

---

### Level 5 — Runtime Tracing & Debugging
* **Goal**: Trace requests step-by-step from input to output.
* **Files to Study**:
  - [main.py](file:///e:/AI_Data_Agent-main/main.py)
  - [07-complete-execution-flow.md](file:///e:/AI_Data_Agent-main/docs/project-understanding/07-complete-execution-flow.md)
  - [24-end-to-end-case-study.md](file:///e:/AI_Data_Agent-main/docs/project-understanding/24-end-to-end-case-study.md)

---

### Level 6 — System Modification & Extension
* **Goal**: Add new agents, tools, or database tables.
* **Reading & Exercises**:
  - [25-how-to-modify-the-project.md](file:///e:/AI_Data_Agent-main/docs/project-understanding/25-how-to-modify-the-project.md)
  - Exercise: Add a new custom tool to `ETLTools` and register it in `etl_analyst.py`.
