# 11 — Performance Audit

This document analyzes latency, token overhead, database efficiency, and synchronous execution bottlenecks in **Agentic AI - Data Agent**.

---

## ⚡ Latency & Bottleneck Analysis

### 1. Sequential Model Calls in SQL Pipeline
For a single user prompt entering the SQL pipeline, the system triggers **4 separate synchronous LLM calls**:
1. `router_node`: Router classification model call (`ChatAnthropic`).
2. `curate_ques`: Question curation model call (`ChatOpenAI` low).
3. `generate_sql`: SQL generation model call (`ChatOpenAI` medium).
4. `is_safe_sql`: SQL safety judge model call (`ChatOpenAI` medium).
5. `represent_final_answer`: Final answer synthesis model call (`ChatOpenAI` low).

* **Impact**: Total round-trip latency is the cumulative sum of 5 sequential HTTP API requests (~3.5 to 8.0 seconds).
* **Optimization**: Combine `curate_ques` and `generate_sql` into a single LLM invocation.

---

### 2. Token Overhead from Complete Schema Introspection
In `utils/database.py:L16-L60`, `schema_details()` fetches table columns and 5 sample rows for **all 5 tables** in the PostgreSQL schema on every request.

* **Impact**: Injects ~1,500 to 3,000 extra context tokens into every prompt context, increasing LLM token costs and latency.
* **Optimization**: Cache schema information in memory; only fetch top sample rows for relevant tables identified by prompt analysis.

---

### 3. Synchronous Blocking I/O
The entire application runs synchronously without `async/await` (`asyncio`). Network API requests (`requests.get`) and database operations (`psycopg2`) block the main thread.
