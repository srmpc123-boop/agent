# 05 — Orchestration Review

This document traces and evaluates the multi-agent graph orchestration in the **CURRENT Agentic AI Data Agent** codebase.

---

## 🔄 Dynamic Execution Tracing

```text
User Request / API Prompt
       ↓
[ router_node ] (data_agent.py) -> Structured Output RouterSchema
       ↓
   route_edge (Conditional Branching)
   ┌───┼───────────────┐
   ↓   ↓               ↓
 "sql" "etl"         "viz"
   ↓   ↓               ↓
[sql_node] [etl_node] [viz_node]
   │       │           │
   │       ├─► [llm_node] ◄──┐ (ReAct Loop)
   │       │      │          │
   │       │   is_tool_call  │
   │       │      ├─► tool_node
   │       │      └─► END
   │       │
   │       └─► [generate_chart_node] ──► END
   │
   └─► [curate_ques] ──► [prompt_query_context] ──► [generate_sql]
                                                       │
                                                 [is_safe_sql]
                                                       │
                                                 is_safe_sql_edge
                                                  ┌────┴─────┐
                                                "Yes"       "No"
                                                  ↓          ↓
                                            [execute_sql] [canceled_sql]
                                                  │          │
                                       check_sql_execution  END
                                         ┌────────┴────────┐
                                      Error &          Success /
                                    Retries < 3       Max Retries
                                         ↓                 ↓
                           [sql_error_reflection_node] [represent_final_answer]
                                         │                 │
                                         └─► generate_sql  END
```

---

## 🎯 Orchestration Evaluation

1. **Routing**: Performed using Pydantic `RouterSchema` structured output. Fast and reliable.
2. **Cyclical Reflection**: In `sql_analyst.py`, failed PostgreSQL executions route back to `sql_error_reflection_node` -> `generate_sql` -> `is_safe_sql` -> `execute_sql`.
3. **ReAct Tool Loop**: In `etl_analyst.py`, standard LangGraph `tools_condition` pattern loops until tool execution terminates.
4. **Termination Guarantee**: All graphs feature clear `END` edges. Reflection loop is capped at `sql_retry_count < 3` to prevent infinite loops.

---

## 📐 Orchestration Score

```text
Orchestration Score: 8.5 / 10
```
- **Strengths**: Dynamic graph routing, ReAct tool execution loop, explicit reflection self-correction retry edges, and guaranteed termination bounds.
- **Improvement**: Inter-agent state passing uses dictionary wrappers rather than a single unified memory graph.
