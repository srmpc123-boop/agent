# 03 — Technology Stack

This document provides a complete inventory of every language, library, database, framework, and tool used in **Agentic AI - Data Agent**.

---

## 🛠️ Complete Technology Inventory

### 1. Programming Languages & Managers
* **Python (`>=3.12`)**: Core programming language. Defined in [.python-version](file:///e:/AI_Data_Agent-main/.python-version#L1) and [pyproject.toml](file:///e:/AI_Data_Agent-main/pyproject.toml#L6).
* **`uv` / `pip`**: Fast Python package installer and dependency resolver. Indicated by [uv.lock](file:///e:/AI_Data_Agent-main/uv.lock) and [pyproject.toml](file:///e:/AI_Data_Agent-main/pyproject.toml).

---

### 2. Core Agentic & AI Frameworks

#### LangGraph (`>=1.2.11`)
* **Purpose**: Stateful multi-agent graph orchestration.
* **Why used**: Constructs cyclical agent execution flows (`StateGraph`, `START`, `END`, conditional edges).
* **Where used**:
  - [agents/data_agent.py](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L76-L99)
  - [agents/etl_analyst.py](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L136-L160)
  - [agents/sql_analyst.py](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L169-L210)

#### LangChain Core & Tools (`>=1.3.14`)
* **Purpose**: Prompt templates, base message types (`HumanMessage`, `AIMessage`, `ToolMessage`), and `@tool` decorators.
* **Where used**:
  - Message handling across all files in `agents/`.
  - `@tool` definitions in [agents/etl_analyst.py](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L18-L81).

#### Provider Integrations
- **`langchain-openai` (`>=1.4.3`)**: Interfaces with OpenAI models (`ChatOpenAI`) in [utils/llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L18-L28).
- **`langchain-anthropic` (`>=1.5.4`)**: Interfaces with Anthropic Claude models (`ChatAnthropic`) in [utils/llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L30).

---

### 3. Data Processing & Validation

#### Pydantic (`>=2.13.4`)
* **Purpose**: Data modeling, graph state schemas, and structured LLM outputs.
* **Where used**: [Models/schema.py](file:///e:/AI_Data_Agent-main/Models/schema.py#L1-L32).

#### Pandas (`>=3.0.5`)
* **Purpose**: In-memory data frame manipulation, JSON normalization, CSV/JSON/Parquet export.
* **Where used**:
  - `ETLTools.extract_load()` in [utils/etl_tools.py:L35-L41](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L35-L41)
  - `ETLTools.transform_load_context()` in [utils/etl_tools.py:L64-L75](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L64-L75)
  - LLM-generated transformation code in [agents/etl_analyst.py:L78](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L78)

#### PyArrow (`>=25.0.1`)
* **Purpose**: Columnar storage engine backend for Pandas Parquet reading/writing.
* **Where used**: Indirect dependency for `.to_parquet()` and `.read_parquet()`.

---

### 4. Database & Connectivity

#### PostgreSQL & `psycopg2-binary` (`>=2.9.12`)
* **Purpose**: Relational database storage and native Python database driver.
* **Where used**:
  - Bulk loading CSV data via `cursor.copy_expert()` in [feed_db.py:L275](file:///e:/AI_Data_Agent-main/feed_db.py#L275).
  - Dynamic schema extraction and query execution in [utils/database.py](file:///e:/AI_Data_Agent-main/utils/database.py#L10-L77).

---

### 5. Environment & Utilities

#### `python-dotenv` (`>=0.9.9`)
* **Purpose**: Loads environment variables from `.env` into `os.environ`.
* **Where used**:
  - [feed_db.py:L6](file:///e:/AI_Data_Agent-main/feed_db.py#L6)
  - [utils/llm_pick.py:L4](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L4)

#### `requests`
* **Purpose**: Fetching remote HTTP JSON payloads.
* **Where used**: [utils/etl_tools.py:L28](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L28).

#### `IPython` (`>=9.16.1`)
* **Purpose**: Renders Mermaid graph PNG visualizations (`Image(graph.draw_mermaid_png())`).
* **Where used**: Optional graph export sections in `data_agent.py`, `sql_analyst.py`, `etl_analyst.py`.

---

## 🔍 Technology Evaluation & Alternatives

| Component | Choice in Project | Alternatives | Architectural Tradeoff |
| --- | --- | --- | --- |
| Agent Orchestrator | LangGraph | AutoGen, CrewAI | LangGraph provides fine-grained graph control and deterministic state machine transitions. |
| Database | PostgreSQL | SQLite, MySQL, DuckDB | PostgreSQL provides robust standard SQL features and `information_schema` introspection. |
| DB Driver | `psycopg2-binary` | `asyncpg`, `SQLAlchemy` | Direct `psycopg2` SQL strings are simple, though ORMs offer abstraction. |
| Validation | Pydantic v2 | Python dataclasses | Pydantic integrates cleanly with LangChain `with_structured_output`. |
