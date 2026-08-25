# 07 — Dependency Cleanup Plan

This document outlines the modifications made to project dependency configuration files (`pyproject.toml` and `requirements.txt`) to support the free Groq stack.

---

## 📦 Dependency Package Changes

| Package Name | Old Status | New Status | Reason for Change |
| --- | --- | --- | --- |
| **`langchain-groq`** | Missing | **ADDED (`>=0.2.0`)** | Core dependency for free LPU-powered Groq LLM inference. |
| **`langchain-openai`** | Required | Optional | Retained for multi-provider support, but no longer required. |
| **`langchain-anthropic`** | Required | Optional | Retained for multi-provider support, but no longer required. |
| **`langchain`** | Required | Required | Core agentic framework. |
| **`langgraph`** | Required | Required | Core multi-agent state graph orchestration framework. |
| **`pandas`** | Required | Required | In-memory data transformation engine. |
| **`psycopg2-binary`** | Required | Required | Native PostgreSQL database driver. |
| **`pydantic`** | Required | Required | Data validation and structured output schemas. |
| **`python-dotenv`** | Required | Required | Environment variable loader. |

---

## 📄 Updated Package Specs

### `pyproject.toml`
```toml
[project]
name = "data-agent"
version = "0.1.0"
description = "Agentic AI Data Agent - Free Stack Edition"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "dotenv>=0.9.9",
    "faker>=40.36.0",
    "ipython>=9.16.1",
    "langchain>=1.3.14",
    "langchain-groq>=0.2.0",
    "langchain-anthropic>=1.5.4",
    "langchain-openai>=1.4.3",
    "langgraph>=1.2.11",
    "pandas>=3.0.5",
    "psycopg2-binary>=2.9.12",
    "pyarrow>=25.0.1",
    "pydantic>=2.13.4",
    "requests>=2.31.0",
]
```
