# 16 — Hackathon Evaluation

This document evaluates **Agentic AI - Data Agent** from the perspective of a technical hackathon judge.

---

## 🏆 Hackathon Scorecard

| Criterion | Score / 10 | Judge's Rationale |
| --- | ---: | --- |
| **Problem Value** | **8.5 / 10** | Solves real pain: non-technical users querying DBs and running ETL pipelines. |
| **Innovation** | **7.5 / 10** | Combining text-to-SQL safety guardrails with tool-driven ETL file execution. |
| **Technical Complexity** | **8.0 / 10** | Multi-agent LangGraph architecture with structured outputs & database seeding. |
| **Agentic AI Usage** | **8.0 / 10** | Genuine multi-agent routing, tool calling, and schema context injection. |
| **Implementation Depth** | **7.5 / 10** | Complete relational database schema + web extraction tools. |
| **Demo Potential** | **8.5 / 10** | Graph PNG exports (`data_agent_graph.png`) provide visual appeal. |
| **Presentation Potential** | **8.0 / 10** | Clear 3-tier story: Intent Router -> SQL Safety Analyst -> ETL File Analyst. |
| **Reliability in Live Demo** | **4.0 / 10** | High risk of connection closed errors or model identifier failures during live demo! |
| **Overall Hackathon Rating** | **7.9 / 10** | **Strong Competitor / Top Contender (with bug fixes)** |

---

## 💡 Hackathon Judge Insights

### What Would Impress Judges:
- **Visual Graph Rendering**: Showing `data_agent.get_graph().draw_mermaid_png()` in the presentation slides visually proves it's a structured state graph rather than a black-box prompt chain.
- **SQL Safety Guardrail**: Demonstrating an intentional malicious prompt (e.g. *"Delete all inactive users"*) and showing the LLM Judge block the query live with safety comments creates a powerful "wow" factor.

### What Would Make Judges Skeptical:
- If `utils/database.py` crashes mid-demo due to the connection closing bug.
- If live LLM code execution (`exec()`) fails due to markdown parsing issues.

### Ideal Hackathon Demo Flow:
1. **Show Architecture Slide**: Router -> SQL Agent (with Judge) + ETL Agent.
2. **Demo 1 (Text-to-SQL Query)**: *"Show me the top 3 drivers by average rating in Toronto"*. Show generated SQL and natural language result.
3. **Demo 2 (Safety Guardrail)**: *"Delete all rides with status cancelled"*. Show judge intervention (`JudgeSchema(answer="No")`).
4. **Demo 3 (ETL API Extraction)**: *"Extract Pokemon API data and save as CSV"*. Show generated file under `data/extract/`.
