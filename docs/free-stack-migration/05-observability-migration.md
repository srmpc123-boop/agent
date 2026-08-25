# 05 — Observability Migration Plan

This document details the observability and logging migration plan for **Agentic AI Data Agent**.

---

## 🔍 Current Observability Audit

* **Current Implementation**: Relies on standard Python `print()` statements.
* **Paid Services**: No paid observability vendors (Datadog, New Relic) are integrated.

---

## 💡 Free Open-Source Observability Stack

1. **Standard Python Structured Logging**: Replace `print()` statements with standard `logging` or `structlog` emitting formatted JSON log output to stdout and file logs (`logs/agent.log`).
2. **Optional Free / Self-Hosted Tracing (LangSmith / Langfuse)**:
   - **LangSmith Free Tier**: Includes 5,000 free traces per month (`LANGCHAIN_TRACING_V2=true`).
   - **Self-Hosted Langfuse**: Can be run locally via Docker Compose (`docker compose up langfuse`).
