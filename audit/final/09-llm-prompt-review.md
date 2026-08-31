# 09 — LLM Engineering & Prompt Review

This document audits LLM model selection, structured outputs, prompt templates, and provider configurations in the **CURRENT Agentic AI Data Agent** codebase.

---

## 🧠 LLM Provider & Model Tiering Setup

- **Default Provider**: **Groq LPU API (`ChatGroq`)**.
- **Model Mapping ([utils/llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py))**:
  - Tiers `"low"` & synthesis -> `llama-3.1-8b-instant` (Fast, zero cost, 14,400 RPD).
  - Tiers `"medium"`, `"high"`, `"claude"`, SQL & Safety Judge -> `llama-3.3-70b-versatile` (70B parameter high-reasoning model).
- **Fallback Providers**: `ChatOpenAI` and `ChatAnthropic` supported via `LLM_PROVIDER=openai` or `LLM_PROVIDER=anthropic`.

---

## 📝 Prompt Templates Audit

### 1. Intent Router Prompt ([agents/data_agent.py:L16](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L16))
- Uses Pydantic `with_structured_output(RouterSchema)`.
- Enforces strict classification: `Literal["sql", "etl", "viz"]`.

### 2. SQL Safety Judge Prompt ([agents/sql_analyst.py:L98](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L98))
- Uses Pydantic `with_structured_output(JudgeSchema)`.
- Prompt instructs LLM to inspect generated SQL for destructive operations (`DROP`, `DELETE`, `ALTER`, `TRUNCATE`).

### 3. SQL Error Reflection Prompt ([agents/sql_analyst.py:L142](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L142))
- Grounded prompt that includes original database schema, failed SQL query, and raw PostgreSQL execution error message to guide corrective query generation.

---

## 📐 LLM Engineering Score

```text
LLM Engineering Score:    8.5 / 10
Prompt Engineering Score: 8.5 / 10
Model Selection Score:    9.0 / 10
```
- **Strengths**: Cost-effective model tiering on Groq, Pydantic structured outputs, and reflective error prompts.
