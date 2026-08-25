# 04 — Complete Project Structure

This document provides a tree diagram and deep directory breakdown of the **Agentic AI - Data Agent** codebase.

---

## 📁 Repository Directory Tree

```text
e:/AI_Data_Agent-main/
├── .env.example                     # Template environment variables file
├── .gitignore                       # Git exclusion rules
├── .python-version                  # Python runtime version pin (3.12)
├── README.md                        # Project documentation (high-level description)
├── feed_db.py                       # PostgreSQL schema creation & CSV bulk loader script
├── main.py                          # Main execution entry point
├── pyproject.toml                   # Project dependencies and packaging metadata
├── requirements.txt                 # Alternative requirements file
├── test_schema_details.txt          # Saved output from running utils/database.py standalone
├── uv.lock                          # Locked dependency tree for uv package manager
│
├── Models/                          # Pydantic state & structured output schemas
│   ├── __init__.py                  # Package marker
│   └── schema.py                    # AgentSchema, JudgeSchema, ETLAgentSchema, RouterSchema, DataAgentSchema
│
├── agents/                          # LangGraph agent graphs and nodes
│   ├── __init__.py                  # Package marker
│   ├── data_agent.py                # Top-level router agent graph
│   ├── etl_analyst.py               # ETL workflow agent graph (API extraction & Pandas code exec)
│   └── sql_analyst.py               # SQL analysis graph (curation, schema context, safety judge, execution)
│
├── utils/                           # Toolkits, DB drivers, and helper utilities
│   ├── __init__.py                  # Package marker
│   ├── database.py                  # PostgreSQL DatabaseUtil driver & schema extractor
│   ├── etl_tools.py                 # ETLTools class (extract_load, transform_load_context, execute_code)
│   └── llm_pick.py                  # Dynamic LLM provider/tier selection factory
│
└── data/                            # File storage & sample datasets
    ├── extract/                     # Destination folder for raw extracted API files
    │   └── extracted_data.csv       # Sample API output file
    ├── transform/                   # Destination folder for transformed output files
    ├── payments.csv                 # PostgreSQL seeding dataset (payment records)
    ├── ratings.csv                  # PostgreSQL seeding dataset (ride rating records)
    ├── rides.csv                    # PostgreSQL seeding dataset (trip records)
    ├── users.csv                    # PostgreSQL seeding dataset (user records)
    └── vehicles.csv                 # PostgreSQL seeding dataset (vehicle records)
```

---

## 📂 Directory Breakdown & Responsibilities

### 1. Root Level (`/`)
* **Responsibility**: Application bootstrapping, dataset seeding, environment configuration.
* **Key Files**:
  - [main.py](file:///e:/AI_Data_Agent-main/main.py): Launches sample queries through `data_agent.invoke()`.
  - [feed_db.py](file:///e:/AI_Data_Agent-main/feed_db.py): Creates PostgreSQL tables and populates sample CSV data.

### 2. `agents/`
* **Responsibility**: Encapsulates all LangGraph graphs, agent nodes, prompt templates, and routing logic.
* **Key Files**:
  - [data_agent.py](file:///e:/AI_Data_Agent-main/agents/data_agent.py): Outer router graph.
  - [sql_analyst.py](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py): 7-node graph for text-to-SQL workflows.
  - [etl_analyst.py](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py): ReAct tool-calling graph for ETL file pipelines.

### 3. `Models/`
* **Responsibility**: Single source of truth for Pydantic data schemas used across all graph states and LLM structured outputs.
* **Key Files**:
  - [schema.py](file:///e:/AI_Data_Agent-main/Models/schema.py): State classes and LLM response models.

### 4. `utils/`
* **Responsibility**: Low-level database drivers, filesystem/API operations, and LLM factory functions.
* **Key Files**:
  - [database.py](file:///e:/AI_Data_Agent-main/utils/database.py): `DatabaseUtil` PostgreSQL interface.
  - [etl_tools.py](file:///e:/AI_Data_Agent-main/utils/etl_tools.py): File I/O, web requests, and code execution.
  - [llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py): `pick_llm` model resolver.

### 5. `data/`
* **Responsibility**: Contains CSV datasets for PostgreSQL database initialization as well as output directories (`extract/` and `transform/`) for file processing tools.
