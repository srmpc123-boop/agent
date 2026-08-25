# 26 — Code Reading Roadmap

This document outlines the optimal reading sequence to study this repository effectively from beginner to advanced level.

---

## 🗺️ Recommended 10-Step Reading Plan

```text
Step 1: System Overview
   └── README.md & pyproject.toml

Step 2: Configuration & Environment
   └── .env.example & utils/llm_pick.py

Step 3: State Models & Contracts
   └── Models/schema.py

Step 4: Database Ingestion & Drivers
   ├── feed_db.py
   └── utils/database.py

Step 5: Operational ETL Utilities & Tools
   └── utils/etl_tools.py

Step 6: Specialized Agent Graphs
   ├── agents/sql_analyst.py
   └── agents/etl_analyst.py

Step 7: Master Router Graph
   └── agents/data_agent.py

Step 8: Application Launcher
   └── main.py

Step 9: Runtime Case Study & Diagrams
   ├── docs/project-understanding/23-project-diagrams.md
   └── docs/project-understanding/24-end-to-end-case-study.md

Step 10: Extension & Customization
   └── docs/project-understanding/25-how-to-modify-the-project.md
```

---

## 📖 Step-by-Step Rationale

1. **Start with [pyproject.toml](file:///e:/AI_Data_Agent-main/pyproject.toml)**: Understand external library dependencies (`langgraph`, `langchain`, `pandas`, `psycopg2`).
2. **Read [Models/schema.py](file:///e:/AI_Data_Agent-main/Models/schema.py)**: State schemas govern all data passed through LangGraph nodes. Understanding `AgentSchema` and `RouterSchema` first makes node code instantly clear.
3. **Study [utils/database.py](file:///e:/AI_Data_Agent-main/utils/database.py) & [feed_db.py](file:///e:/AI_Data_Agent-main/feed_db.py)**: Learn how relational data is structured and how schema context is extracted.
4. **Examine [agents/sql_analyst.py](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py)**: Deep dive into the 7-node text-to-SQL state pipeline and safety guardrail judge.
5. **Examine [agents/etl_analyst.py](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py)**: Deep dive into tool calling and dynamic Pandas execution.
6. **Finish with [agents/data_agent.py](file:///e:/AI_Data_Agent-main/agents/data_agent.py) & [main.py](file:///e:/AI_Data_Agent-main/main.py)**: See how the router ties the sub-agents together into an entry point.
