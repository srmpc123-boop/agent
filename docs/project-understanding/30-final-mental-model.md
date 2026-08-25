# 30 — Final Mental Model

If you close the repository right now, this document captures the core mental model of how **Agentic AI - Data Agent** functions.

---

## 🧠 The 4-Layer Mental Model

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        1. ROUTING LAYER                                │
│  Receives user query -> Classifies via RouterSchema -> Dispatches      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
           ┌────────────────────────┴────────────────────────┐
           ▼                                                 ▼
┌───────────────────────────────────────┐ ┌──────────────────────────────┐
│       2A. SQL ANALYST SUBSYSTEM       │ │   2B. ETL ANALYST SUBSYSTEM  │
│  - Introspects DB schema & samples    │ │  - Tool 1: Extract API JSON  │
│  - Generates SQL string               │ │  - Tool 2: Pandas Context    │
│  - Evaluates safety (LLM Judge)       │ │  - Exec: Dynamic Python exec │
│  - Executes query on PostgreSQL       │ └──────────────┬───────────────┘
│  - Formats text response              │                │
└──────────────────┬────────────────────┘                │
                   │                                     │
                   ▼                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        3. STORAGE & DATA LAYER                         │
│  - PostgreSQL relational tables (users, rides, payments, vehicles)     │
│  - Local file system (/data/extract/, /data/transform/)                │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🔑 Key Principles to Remember

1. **Routing before Action**: The system never runs SQL queries or file tools directly from user input. A top-level router always classifies intent first.
2. **Schema-Aware Text-to-SQL**: The SQL Analyst injects live database table columns and top 5 sample rows into prompt context to prevent missing-column errors.
3. **LLM-as-a-Judge Guardrail**: Generated SQL queries pass through an in-memory LLM judge that blocks `DROP`, `DELETE`, `UPDATE`, and `INSERT` commands.
4. **Tool-Driven File Pipelines**: The ETL Analyst uses ReAct tool calls to fetch REST API data and run generated Pandas code for custom data transformations.
