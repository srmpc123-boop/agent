# 04 — Agent-by-Agent Audit

This document audits every individual agent sub-graph in the **CURRENT Agentic AI Data Agent** codebase.

---

## 🤖 Agent 1: Master Data Router Agent (`data_agent`)

* **File**: [agents/data_agent.py](file:///e:/AI_Data_Agent-main/agents/data_agent.py)
* **Purpose**: Classifies user intent and routes execution to specialized sub-agent graphs.
* **Responsibilities**: Receives user prompt, invokes `RouterSchema` structured output, updates `route_response`, and delegates to `sql_node`, `etl_node`, or `viz_node`.
* **Model**: Resolves `pick_llm("claude")` (Groq `llama-3.3-70b-versatile`).
* **State**: `DataAgentSchema` (`messages`, `route_response`).
* **Strengths**: Clean separation of routing from tool execution.
* **Weaknesses**: Cannot decompose complex multi-goal prompts (e.g. "Run SQL query AND generate chart") into a multi-step execution plan.
* **Score**: **8.5 / 10**

---

## 🤖 Agent 2: SQL Analyst Agent (`sql_analyst`)

* **File**: [agents/sql_analyst.py](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py)
* **Purpose**: Converts natural language into safe PostgreSQL queries and executes them.
* **Responsibilities**: Curation (`curate_ques`), schema introspection (`prompt_query_context`), SQL generation (`generate_sql`), safety verification (`is_safe_sql`), execution (`execute_sql`), self-correction retry (`sql_error_reflection_node`), and final answer formatting (`represent_final_answer`).
* **Model**: Uses `pick_llm("low")`, `pick_llm("medium")`, and `pick_llm("high")`.
* **State**: `AgentSchema` (`user_question`, `generated_sql_query`, `is_safe`, `sql_retry_count`, `sql_error_message`, `final_answer`).
* **Strengths**: **Contains an automated reflection loop** that captures PostgreSQL syntax errors and retries query generation up to 3 times automatically. Structured safety judge blocks DDL/DML.
* **Weaknesses**: Hardcoded limit of 3 retries.
* **Score**: **9.2 / 10 (Strongest Agent)**

---

## 🤖 Agent 3: ETL Analyst Agent (`etl_analyst`)

* **File**: [agents/etl_analyst.py](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py)
* **Purpose**: Extracts web API data and performs dataset transformations.
* **Responsibilities**: ReAct loop calling `extract_load_tool` (API extraction) and `transform_load_tool` (Pandas execution).
* **Model**: Resolves `pick_llm("claude").bind_tools(tools)`.
* **State**: `ETLAgentSchema` (`messages`).
* **Strengths**: ReAct tool loop pattern allows multi-step tool calls.
* **Weaknesses**: Tool responses are returned as raw text strings rather than structured objects.
* **Score**: **8.2 / 10**

---

## 🤖 Agent 4: Data Visualization Agent (`viz_analyst`)

* **File**: [agents/viz_analyst.py](file:///e:/AI_Data_Agent-main/agents/viz_analyst.py)
* **Purpose**: Generates Matplotlib and Seaborn charts from data prompts.
* **Responsibilities**: Generates Python visualization code, executes code via `ETLTools.execute_code`, saves PNG images to `data/visualizations/`, and returns chart file paths.
* **Model**: Resolves `pick_llm("medium")` (`llama-3.3-70b-versatile`).
* **State**: `VizAgentSchema` (`chart_code`, `chart_image_path`, `summary`).
* **Strengths**: Dynamic PNG chart rendering displayed live in Streamlit UI.
* **Weaknesses**: Relies on Regex to parse python code blocks from LLM markdown.
* **Score**: **8.5 / 10**

---

## 🏆 Agent Ranking Summary

1. **Strongest Agent**: `sql_analyst` (Features schema introspection, safety judging, and self-correction reflection loop).
2. **Most Innovative Agent**: `viz_analyst` (Dynamic Matplotlib/Seaborn chart rendering).
3. **Agent Needing Refinement**: `data_agent` (Needs multi-step planning capability).
