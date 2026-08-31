# 23 — Technical Interview Readiness Guide

This document presents 10 key technical interview questions, comprehensive answers, and code reference locations for defending **Agentic AI Data Agent**.

---

## 🎯 Top Technical Interview Q&A

### Q1: "Why did you build this project using LangGraph instead of linear chains?"
> **Answer**: *"Linear chains cannot handle cyclical feedback loops or dynamic intent routing. In text-to-SQL generation, queries frequently fail due to database syntax errors. With LangGraph, I built a state machine featuring an explicit reflection node (`sql_error_reflection_node`) and conditional retry edge. If PostgreSQL query execution fails, the captured database error is fed back into the LLM context, allowing the agent to self-correct up to 3 times automatically."*
> **Code Location**: [agents/sql_analyst.py:L142-L200](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L142-L200)

### Q2: "How do you protect your database against SQL injection or destructive queries?"
> **Answer**: *"We enforce a multi-layered guardrail strategy. First, all queries pass through an LLM Safety Judge (`is_safe_sql`) using Pydantic structured output (`JudgeSchema`) that screens for destructive operations (`DROP`, `DELETE`, `TRUNCATE`, `ALTER`). Unsafe queries are routed to `canceled_sql` and never reach PostgreSQL. Second, queries execute against read-only analytics views."*
> **Code Location**: [agents/sql_analyst.py:L95-L119](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L95-L119)

### Q3: "How do you securely execute LLM-generated Python code in your ETL and Visualization tools?"
> **Answer**: *"Before calling `exec()`, we pass the generated Python code through an AST parser (`ast.parse()`) in `utils/etl_tools.py`. The AST tree is walked to inspect import statements, rejecting execution if forbidden system modules like `os`, `sys`, `subprocess`, or `socket` are detected."*
> **Code Location**: [utils/etl_tools.py:L78-L95](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L78-L95)

### Q4: "How do you manage LLM API costs?"
> **Answer**: *"We implemented zero-cost LPU inference using Groq (`ChatGroq`) with model tiering. Cheaper models (`llama-3.1-8b-instant`) handle fast intent classification, question curation, and text formatting, while high-reasoning models (`llama-3.3-70b-versatile`) are used for SQL generation, safety judging, and python code generation."*
> **Code Location**: [utils/llm_pick.py:L14-L45](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L14-L45)

### Q5: "How do you measure whether agent performance regresses after prompt or model changes?"
> **Answer**: *"We built an automated LLM-as-a-Judge benchmark evaluation suite (`evals/run_evals.py`). It tests routing precision %, SQL execution success rate %, guardrail safety precision, and response latency across benchmark test categories."*
> **Code Location**: [evals/run_evals.py:L1-L85](file:///e:/AI_Data_Agent-main/evals/run_evals.py#L1-L85)
