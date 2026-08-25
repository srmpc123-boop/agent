# 10 — Prompt Engineering and LLM Layer

This document catalogs every system prompt, user prompt template, LLM model configuration, and structured output binding used in **Agentic AI - Data Agent**.

---

## 🧠 LLM Factory & Model Selection (`utils/llm_pick.py`)

The system relies on a central factory function `pick_llm(level: str)` in [utils/llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L6-L34) to instantiate LLMs based on required reasoning power:

```python
def pick_llm(level: str):
    if level.lower() == "low":
        llm = ChatOpenAI(model_name="gpt-5.6-luna", temperature=0, model_kwargs={"reasoning_effort": "none"})
    elif level.lower() == "medium":
        llm = ChatOpenAI(model_name="gpt-5.6-terra", temperature=0, model_kwargs={"reasoning_effort": "none"})
    elif level.lower() == "high":
        llm = ChatOpenAI(model_name="gpt-5.6-sol", temperature=0, model_kwargs={"reasoning_effort": "none"})
    elif level.lower() == "claude":
        llm = ChatAnthropic(model_name="claude-sonnet-5")
    else:
        raise ValueError(f"Unsupported level: {level}")
    return llm
```

> [!NOTE]
> The model names (`gpt-5.6-luna`, `claude-sonnet-5`) in `utils/llm_pick.py` are placeholder model strings. Standard production environments should map these to valid model identifiers like `gpt-4o-mini`, `gpt-4o`, or `claude-3-5-sonnet-20240620`.

---

## 📝 Complete System Prompts Inventory

### 1. Router Classification Prompt
* **Defined in**: [agents/data_agent.py:L20](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L20)
* **LLM Used**: `"claude"` (`ChatAnthropic`) bound with `RouterSchema`.
* **Behavior**: Evaluates user query and forces output matching `RouterSchema(answer="sql" | "etl", comments="...")`.

---

### 2. SQL Question Curation Prompt
* **Defined in**: [agents/sql_analyst.py:L21](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L21)
* **LLM Tier**: `"low"`
* **Template**:
  ```text
  Curate the following question: {user_question}
  ```
* **Objective**: Cleans informal user phrasing into a structured analytics request.

---

### 3. SQL Query Context & Generation Prompt
* **Defined in**: [agents/sql_analyst.py:L46-L62](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L46-L62)
* **LLM Tier**: `"medium"`
* **Template**:
  ```text
  You are an SQL analyst agent. Your task is to convert the user's natural language 
  query into Postgres SQL query that can be executed on the database. You are provided 
  with the user's original query and the schema details of the database, including
  table names, column names, data types, and sample data for each table so that 
  you can understand the structure of the database and generate an accurate SQL query.
  Unless user explicitly asks for specific number of rows, always limit the output to 10 rows.
  Note - Just generate the SQL query without any explanation or additional text because
  this query will be executed directly on the database. So, the output should be SQL
  ready to be executed without any modifications.  
  
  User's Original Query: {curated_question}

  Database Schema Details:
  {schema_info}
  ```

---

### 4. SQL Safety Judge Guardrail Prompt
* **Defined in**: [agents/sql_analyst.py:L91-L99](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L91-L99)
* **LLM Tier**: `"medium"` with `JudgeSchema`
* **Template**:
  ```text
  You are an SQL Judge for data security. Your task is to determine whether the SQL query is 
  safe or not. The SQL query should only be used for data retrieval and should not modify the 
  database in any way. Neither the SQL query nor the prompt should contain any SQL commands that can modify the
  database, such as INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, or any other commands that can change
  the structure or content of the database. If the SQL query is safe, respond with 'Yes' otherwise respond with 
  'No'. Additionally, provide comments explaining your decision.
  Here's the SQL query to evaluate:
  {sql_query}
  ```

---

### 5. Final SQL Answer Synthesis Prompt
* **Defined in**: [agents/sql_analyst.py:L149-L157](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L149-L157)
* **LLM Tier**: `"low"`
* **Template**: Synthesizes PostgreSQL result tuples and original curated question into user-friendly text without exposing raw SQL strings.

---

### 6. Pandas Code Generation Prompt
* **Defined in**: [agents/etl_analyst.py:L58-L71](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L58-L71)
* **LLM Tier**: `"claude"`
* **Template**: Instructs model to output pure executable Pandas Python code (no markdown formatting, no explanations) given input dataset preview rows (`head(3)`).
