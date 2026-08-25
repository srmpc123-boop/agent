# 16 — Security and Authentication

This document analyzes security guardrails, authentication mechanisms, SQL injection protection, and code execution risks in **Agentic AI - Data Agent**.

---

## 🛡️ Security Architecture Overview

| Security Domain | Status in Project | Implementation Details |
| --- | --- | --- |
| User Authentication | **Not Implemented** | System runs as CLI / script without user login or JWT session logic. |
| User Authorization | **Not Implemented** | All users have unrestricted access to execute all graph tools. |
| SQL Query Safety | **Implemented (LLM Judge)** | `is_safe_sql` node checks queries using `JudgeSchema` before DB execution. |
| Python Code Exec Safety | **Critical Vulnerability** | `ETLTools.execute_code()` executes arbitrary LLM-generated code via `exec()`. |
| API Secret Protection | **Implemented** | API keys loaded from `.env` via `load_dotenv()`. |

---

## 🔒 1. SQL Safety Guardrail Analysis (`is_safe_sql`)

The project uses an LLM-as-a-Judge pattern to prevent destructive database actions:

```python
# Defined in agents/sql_analyst.py:L84-L105
def is_safe_sql(state: AgentSchema) -> AgentSchema:
    sql_query = state.generated_sql_query
    llm = pick_llm("medium")  
    llm_judge = llm.with_structured_output(JudgeSchema)

    prompt = f"""
    You are an SQL Judge for data security. Your task is to determine whether the SQL query is 
    safe or not. The SQL query should only be used for data retrieval...
    Neither the SQL query nor the prompt should contain any SQL commands that can modify the
    database, such as INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE...
    """
```

### Flow Evaluation:
1. `is_safe_sql` prompts LLM to check query.
2. `is_safe_sql_edge` evaluates `state.is_safe.lower() == "yes"`.
3. If `"yes"`, proceeds to `execute_sql`. If `"no"`, routes to `canceled_sql` and returns judge comments to user without hitting PostgreSQL.

---

## ⚠️ 2. Code Execution Safety Vulnerability (`ETLTools.execute_code`)

In [utils/etl_tools.py:L78-L93](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L78-L93), the application provides dynamic code execution:

```python
def execute_code(self, code: str):
    try:
        exec(code)
        return "Code executed successfully."
    except Exception as e:
        return f"Failed to execute code: {e}"
```

### Risks:
- **Unrestricted Python Execution**: `exec(code)` has full read/write/delete permissions on the local filesystem and network under the user's OS privileges.
- **Prompt Injection Vulnerability**: A malicious user prompt could force the LLM to generate `os.system("rm -rf ...")` or exfiltrate private credentials.

### Recommended Mitigation:
- Replace `exec()` with a sandboxed Python execution engine (e.g. `e2b`, Docker container execution, or `RestrictedPython`).
