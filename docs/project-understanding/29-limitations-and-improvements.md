# 29 — Project Weaknesses, Limitations, and Improvements

This document presents a critical engineering audit of bugs, security risks, technical debt, and improvement opportunities in **Agentic AI - Data Agent**.

---

## 🚨 Critical Defect & Bug Analysis

### 1. Database Connection Lifecycle Bug
* **Location**: [utils/database.py:L57-L58](file:///e:/AI_Data_Agent-main/utils/database.py#L57-L58) & [L76-L77](file:///e:/AI_Data_Agent-main/utils/database.py#L76-L77)
* **Problem**: `schema_details()` and `execute_sql()` close `self.connection` in their `finally` blocks:
  ```python
  finally:
      if cursor: cursor.close()
      if connection: connection.close() # Closes shared self.connection!
  ```
* **Severity**: **High**. Reusing a single `DatabaseUtil` object across nodes raises a `psycopg2.InterfaceError` on subsequent database calls.
* **Fix**: Remove `connection.close()` from `finally` blocks, or create fresh connection instances per query.

---

### 2. Arbitrary Python Code Execution Security Vulnerability
* **Location**: [utils/etl_tools.py:L89](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L89)
* **Problem**: `exec(code)` runs un-sanitized, LLM-generated code directly in the host process with full system permissions.
* **Severity**: **High**. Vulnerable to prompt injection attacks that could execute malicious commands on the host OS.
* **Fix**: Sandbox code execution inside an isolated container (e.g. Docker, `e2b`) or restrict module imports via AST analysis.

---

### 3. Model Naming Discrepancy
* **Location**: [utils/llm_pick.py:L18-L30](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L18-L30) vs [README.md:L165-L167](file:///e:/AI_Data_Agent-main/README.md#L165-L167)
* **Problem**: `utils/llm_pick.py` uses placeholder model strings (`gpt-5.6-luna`, `gpt-5.6-terra`, `claude-sonnet-5`) while `README.md` claims `gpt-3.5-turbo`, `gpt-4-turbo`, and `claude-3-opus`.
* **Severity**: **Medium**. Running out of the box fails unless `utils/llm_pick.py` model strings are mapped to standard production OpenAI/Anthropic API identifiers.

---

### 4. Database Password Typo in Module Code
* **Location**: [utils/database.py:L84](file:///e:/AI_Data_Agent-main/utils/database.py#L84)
* **Problem**: Standalone execution block contains `"password": "potgres"` (typo missing 's').
* **Severity**: **Low** (only affects standalone script execution of `database.py`).

---

## 🛠️ Summary Recommendation Table

| Issue | File Location | Priority | Recommended Action |
| --- | --- | --- | --- |
| DB Connection Closing Bug | `utils/database.py` | High | Keep connection open or use connection pooling. |
| Security Risk (`exec()`) | `utils/etl_tools.py` | High | Sandbox python code execution. |
| Model Naming Discrepancy | `utils/llm_pick.py` | Medium | Update to standard OpenAI/Anthropic model names. |
| Missing Unit Tests | Root directory | Medium | Add `pytest` suite for nodes and tools. |
