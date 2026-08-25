# 02 — Feature Priority Matrix

This document evaluates and ranks all proposed upgrade features by business impact, technical depth, portfolio value, implementation effort, and domain relevance.

---

## 📊 Feature Evaluation & Priority Matrix

```text
Priority Scale:
- P0: Critical Infrastructure / Bug Fix (Must do first)
- P1: Very High Value / Core Agentic Capability
- P2: High Value Feature / Major Enhancement
- P3: Medium Value / UX & Polishing
- P4: Optional Extension / Non-Essential
```

| Feature Name | Business / Agentic Impact | Technical Depth | Resume Value | Difficulty | Relevance | Priority |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| **Fix Database Connection Closing Bug** | **10 / 10** | **4 / 10** | **5 / 10** | **Low** | **10 / 10** | **P0** |
| **Fix Invalid Model Identifiers (`utils/llm_pick.py`)**| **10 / 10** | **2 / 10** | **4 / 10** | **Low** | **10 / 10** | **P0** |
| **Sandbox Python Code Exec (`ETLTools.execute_code`)**| **9 / 10** | **8 / 10** | **9 / 10** | **Medium** | **10 / 10** | **P0** |
| **SQL Error Self-Correction Reflection Loop** | **9.5 / 10** | **8.5 / 10** | **9.5 / 10** | **Medium** | **10 / 10** | **P0** |
| **LangSmith Tracing & Structured Logging** | **9 / 10** | **7.5 / 10** | **9 / 10** | **Low** | **10 / 10** | **P1** |
| **FastAPI REST API Server Wrapper (`app.py`)** | **8.5 / 10** | **7 / 10** | **8.5 / 10** | **Low** | **9 / 10** | **P1** |
| **Automated Evaluation Benchmark Suite (`evals/`)** | **9 / 10** | **9 / 10** | **9.5 / 10** | **Medium** | **9.5 / 10** | **P1** |
| **Data Visualization Sub-Agent (`viz_analyst`)** | **8 / 10** | **7.5 / 10** | **8 / 10** | **Medium** | **9 / 10** | **P1** |
| **Streamlit Interactive Chat & Trace Dashboard** | **8 / 10** | **6 / 10** | **8 / 10** | **Low** | **9 / 10** | **P1** |
| **Cost-Aware Model Routing Optimization** | **7.5 / 10** | **7 / 10** | **8 / 10** | **Low** | **9 / 10** | **P2** |
| **Human-in-the-Loop Approval Breakpoints** | **7.5 / 10** | **8 / 10** | **8.5 / 10** | **Medium** | **8 / 10** | **P2** |
| **Structured Multi-Step Task Planner (`PlannerAgent`)**| **7 / 10** | **8.5 / 10** | **8.5 / 10** | **High** | **8 / 10** | **P2** |
| **PostgreSQL Task Execution Audit Log Table** | **7 / 10** | **6 / 10** | **7 / 10** | **Low** | **8.5 / 10** | **P2** |
| **Schema Metadata Caching** | **6.5 / 10** | **5 / 10** | **6 / 10** | **Low** | **8 / 10** | **P3** |
| **Vector Schema RAG (ChromaDB for 50+ tables)** | **4 / 10** | **7 / 10** | **6 / 10** | **High** | **4 / 10** | **P4 (Avoid)** |
| **Kubernetes Container Deployment** | **3 / 10** | **8 / 10** | **5 / 10** | **High** | **3 / 10** | **P4 (Avoid)** |

---

## 🎯 Implementation Rationale

1. **Why P0 Features Come First**:
   - Fixing `database.py` connection bugs and model names takes less than 30 minutes but immediately stops graph crashes.
   - Sandboxing `exec()` removes the single highest security risk in the codebase.
   - The SQL reflection loop is the single most important Agentic AI feature, demonstrating self-correction.

2. **Why P1 Features Provide Maximum Resume Impact**:
   - **LangSmith Tracing** + **Automated Evaluation Suite** prove you understand AI system observability and regression benchmarking.
   - **FastAPI** + **Streamlit** provide immediate backend and UI access for live recruiter demos.

3. **Why P4 Features Are Avoided**:
   - Vector Schema RAG is unneeded for a 5-table dataset. Direct schema introspection is faster and 100% accurate.
   - Kubernetes adds infrastructure maintenance overhead without adding agentic AI value.
