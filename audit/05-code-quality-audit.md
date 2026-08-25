# 05 — Code Quality Audit

This document provides a line-by-line code quality audit inspecting readability, naming conventions, type hints, exception handling, and technical debt across the codebase.

---

## 🔍 Specific Code Findings & Defect Table

| ID | File Path & Lines | Severity | Problem Description | Recommended Fix |
| --- | --- | --- | --- | --- |
| **CQ-01** | [utils/database.py:L57-L58](file:///e:/AI_Data_Agent-main/utils/database.py#L57-L58), [L76-L77](file:///e:/AI_Data_Agent-main/utils/database.py#L76-L77) | **Critical** | `self.connection` is closed inside `finally` block of `schema_details` and `execute_sql`. Sub-sequential queries fail. | Remove `connection.close()` from `finally` or instantiate fresh connections. |
| **CQ-02** | [utils/etl_tools.py:L89](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L89) | **Critical** | `exec(code)` runs un-sanitized LLM-generated string as code. | Containerize or use `RestrictedPython`/`e2b`. |
| **CQ-03** | [utils/llm_pick.py:L18-L30](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L18-L30) | **High** | Uses non-standard model strings (`gpt-5.6-luna`, `claude-sonnet-5`) that throw API errors on real accounts. | Replace with standard model identifiers (`gpt-4o-mini`, `claude-3-5-sonnet-20240620`). |
| **CQ-04** | [utils/database.py:L84](file:///e:/AI_Data_Agent-main/utils/database.py#L84) | **Medium** | Typo in password key in module standalone test: `"password": "potgres"`. | Fix string to `"postgres"`. |
| **CQ-05** | [agents/etl_analyst.py:L76](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L76) | **Medium** | Brittle string manipulation to clean LLM markdown block: `.strip().strip('```').strip().lstrip('python').strip()`. | Use regular expressions or structured output to extract Python code. |
| **CQ-06** | Across all files in `agents/` | **Low** | Missing type hints on node parameters and return signatures. | Add complete Python type annotations (`state: DataAgentSchema -> DataAgentSchema`). |

---

## 🧹 Code Smell Audit

1. **Dead / Commented-Out Code**:
   - In `agents/etl_analyst.py:L176-L182`, 7 lines of alternative invocation logic are commented out.
   - In `agents/sql_analyst.py:L202-L203`, 2 lines of edge definitions are commented out.
2. **Hardcoded Windows Path References**:
   - In `utils/etl_tools.py:L97`, standalone test hardcodes Windows path: `"C:\\Data_Agent\\data\\extract\\extracted_data.csv"`.
