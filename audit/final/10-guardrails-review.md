# 10 — Guardrails and Safety Review

This document audits input/output safety guardrails, SQL injection protection, and code execution constraints across the **CURRENT Agentic AI Data Agent** codebase.

---

## 🛡️ Guardrails Defense Matrix

```text
User Input -> Router Agent -> Sub-Graph
                                │
               ┌────────────────┴────────────────┐
               ↓                                 ↓
       [ SQL Subsystem ]                 [ ETL Subsystem ]
               │                                 │
     SQL Generator Node                Pandas Code Generator
               │                                 │
               ↓                                 ↓
     [ SQL Safety Judge ]             [ AST Code Validator ]
   Evaluates via JudgeSchema        Scans AST for prohibited imports
               │                                 │
       ┌───────┴───────┐                 ┌───────┴───────┐
       ↓               ↓                 ↓               ↓
    "Yes"             "No"             Clean         Violation
       ↓               ↓                 ↓               ↓
 Execute Query    Cancel Query      Execute Code    Block Execution
```

---

## 🔒 Implemented Safety Layer Details

1. **SQL Safety Judge (`is_safe_sql`)**:
   - **Location**: [agents/sql_analyst.py:L95](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L95)
   - **Mechanism**: Passes generated SQL queries through an LLM judge using `with_structured_output(JudgeSchema)`.
   - **Behavior**: Evaluates query intent and flags queries containing `DROP`, `DELETE`, `TRUNCATE`, `ALTER`, or unauthorized schema modifications as `is_safe = "No"`.
   - **Enforcement**: Graph conditional edge `is_safe_sql_edge` routes unsafe queries to `canceled_sql` and terminates graph execution without touching PostgreSQL.

2. **AST Code Execution Sandbox (`execute_code`)**:
   - **Location**: [utils/etl_tools.py:L78](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L78)
   - **Mechanism**: Parses code using Python's `ast.parse()` module.
   - **Behavior**: Inspects AST nodes for module imports and blocks execution if forbidden system packages (`os`, `sys`, `subprocess`, `shutil`, `socket`) are detected.

---

## 📐 Guardrails Score

```text
Guardrails & Safety Score: 8.5 / 10
```
- **Strengths**: Multi-layer defense comprising LLM safety judging for SQL queries and AST static analysis for Python code execution.
