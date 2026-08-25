# 07 — Prompt Engineering Audit

This document audits all prompts defined across the codebase, evaluating clarity, context grounding, constraint enforcement, and output controls.

---

## 📝 Prompt Evaluation Matrix

| Prompt Name | Location File & Lines | Role Definition | Context Grounding | Constraints | Output Control | Overall Rating |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| **SQL Generation Prompt** | [agents/sql_analyst.py:L46-L62](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L46-L62) | 9/10 | 9.5/10 | 9/10 | 8.5/10 | **9.0 / 10** |
| **SQL Safety Judge Prompt** | [agents/sql_analyst.py:L91-L99](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L91-L99) | 9/10 | 8/10 | 9.5/10 | 10/10 | **9.1 / 10** |
| **Pandas Code Generation Prompt** | [agents/etl_analyst.py:L58-L71](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L58-L71) | 8/10 | 8.5/10 | 9/10 | 7/10 | **8.1 / 10** |
| **Question Curation Prompt** | [agents/sql_analyst.py:L21](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L21) | 4/10 | 3/10 | 4/10 | 4/10 | **3.8 / 10** |

---

## 🔬 Deep-Dive Analysis of Key Prompts

### 1. SQL Generation Prompt ([sql_analyst.py:L46-L62](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L46-L62))
```text
You are an SQL analyst agent. Your task is to convert the user's natural language 
query into Postgres SQL query that can be executed on the database...
Unless user explicitly asks for specific number of rows, always limit the output to 10 rows.
Note - Just generate the SQL query without any explanation or additional text...
```
* **Strengths**: Explicit instruction to enforce `LIMIT 10`, clear role, detailed schema context.
* **Weaknesses**: Does not instruct the model on how to handle ambiguous table join conditions.

---

### 2. SQL Safety Judge Prompt ([sql_analyst.py:L91-L99](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L91-L99))
```text
You are an SQL Judge for data security. Your task is to determine whether the SQL query is 
safe or not. The SQL query should only be used for data retrieval and should not modify the 
database in any way... Neither the SQL query nor the prompt should contain any SQL commands 
that can modify the database, such as INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE...
```
* **Strengths**: Explicit list of forbidden SQL keywords; enforces output via `JudgeSchema`.
* **Weaknesses**: Relies on string checking by LLM rather than deterministic SQL AST parsing.

---

### 3. Question Curation Prompt ([sql_analyst.py:L21](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L21))
```text
Curate the following question: {user_question}
```
* **Weaknesses**: Under-specified. Does not explain what "curate" means (e.g. correct spelling, expand abbreviations, re-word as SQL problem).
