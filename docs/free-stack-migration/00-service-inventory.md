# 00 — Service Inventory and Dependency Audit

This document provides a complete inventory of every external service, LLM provider, API client, database, and infrastructure dependency found in **Agentic AI Data Agent** prior to migration.

---

## 📊 Complete Service & Dependency Audit Table

| Service | Purpose | Current Provider | Paid / Free? | Free Tier Available? | Required? | Free / Open-Source Replacement |
| --- | --- | --- | --- | --- | --- | --- |
| **LLM Inference (Primary)** | Router & Code Generation | Anthropic (`ChatAnthropic`) | Paid | No (Trial only) | **Yes** | **Groq (`ChatGroq`) with `llama-3.3-70b-versatile`** |
| **LLM Inference (Secondary)** | Curation, SQL & Safety Judge | OpenAI (`ChatOpenAI`) | Paid | No | **Yes** | **Groq (`ChatGroq`) with `llama-3.1-8b-instant`** |
| **Relational Database** | Analytical data storage | PostgreSQL (`psycopg2-binary`) | Free / Open Source | Yes (Self-hosted / local) | **Yes** | **Local PostgreSQL (No migration needed)** |
| **Vector Database** | Embeddings & Vector Search | None | N/A | N/A | **No** | **N/A (Uses PostgreSQL relational introspection)** |
| **Search Engine API** | Web Search | None | N/A | N/A | **No** | **N/A (Uses HTTP API requests via `requests`)** |
| **Observability Platform** | Distributed Tracing & Metrics | None | N/A | N/A | **No** | **Python `logging` + Optional Open-Source LangSmith / Structlog** |

---

## 🔬 Detailed External Service Breakdown

### 1. Anthropic API (`langchain-anthropic`)
* **Provider**: Anthropic PBC
* **Purpose**: Used for high-tier LLM operations including top-level router classification (`RouterSchema`) and Pandas code generation.
* **Files Using It**: [agents/data_agent.py:L18](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L18), [agents/etl_analyst.py:L56](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L56), [utils/llm_pick.py:L30](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L30).
* **Environment Variable**: `ANTHROPIC_API_KEY`
* **Cost Model**: Paid per input/output token.
* **Migration Strategy**: Replace with **Groq API (`GROQ_API_KEY`)** running `llama-3.3-70b-versatile`.

### 2. OpenAI API (`langchain-openai`)
* **Provider**: OpenAI Inc.
* **Purpose**: Used for lower and medium tier LLM operations (question curation, text-to-SQL query generation, SQL safety judge).
* **Files Using It**: [utils/llm_pick.py:L18-L28](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L18-L28).
* **Environment Variable**: `OPENAI_API_KEY`
* **Cost Model**: Paid per input/output token.
* **Migration Strategy**: Replace with **Groq API (`GROQ_API_KEY`)** running `llama-3.1-8b-instant`.

---

## 🏷️ Dependency Classification

- **Category A (Fully Free / Open Source)**: PostgreSQL (`psycopg2-binary`), Pandas, Pydantic, Requests.
- **Category D (Paid & Currently Required - Needs Migration)**: OpenAI API (`ChatOpenAI`), Anthropic API (`ChatAnthropic`).
- **Category E (Local Alternative Available)**: Groq API (High-speed free-tier LLM inference) or local Ollama execution.
