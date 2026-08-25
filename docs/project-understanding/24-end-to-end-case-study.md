# 24 — Complete End-to-End Case Study

This document walks through a complete runtime trace of a real user request executed against the exact codebase.

---

## 🎯 Case Study Scenario

* **User Prompt**: *"Find the top 3 users with the most completed rides and display their full name and total ride count."*
* **Target Subsystem**: SQL Analyst Graph via Data Agent Router.

---

## 🔬 Execution Walkthrough

### Step 1: Request Entry
* **File**: [main.py:L5-L8](file:///e:/AI_Data_Agent-main/main.py#L5-L8)
* **Code Executed**:
  ```python
  response = data_agent.invoke(
      {"messages": [HumanMessage(content="Find the top 3 users with the most completed rides and display their full name and total ride count.")],
       "route_response": ""}
  )
  ```

---

### Step 2: Router Classification
* **File**: [agents/data_agent.py:L26-L36](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L26-L36) (`router_node`)
* **Function**: `router_node(state)`
* **Input State**: `state.messages[-1].content` = `"Find the top 3 users with..."`
* **LLM Invocation**: `llm_router.invoke(...)`
* **LLM Output**: `RouterSchema(answer="sql", comments="Request requires database querying and aggregation on rides table.")`
* **State Mutation**: `state.route_response = "sql"`
* **Branch Decision**: `route_edge` returns `"sql_node"`.

---

### Step 3: SQL Sub-Graph Invocation
* **File**: [agents/data_agent.py:L51-L71](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L51-L71) (`sql_node`)
* **Constructed Input**:
  ```python
  input_schema = {
      "messages": [],
      "user_question": "Find the top 3 users with the most completed rides and display their full name and total ride count.",
      "curated_ques": "",
      "prompt_query_context": "",
      "generated_sql_query": "",
      "is_safe": "No",
      "comments": "",
      "sql_query_execution_result": "",
      "final_answer": ""
  }
  ```
* **Call**: `sql_analyst.invoke(input_schema)`

---

### Step 4: SQL Node - `curate_ques`
* **File**: [agents/sql_analyst.py:L15-L26](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L15-L26)
* **Action**: Calls `pick_llm("low")`.
* **Result**: `state.curated_ques` = `"Find top 3 users with highest count of completed rides."`

---

### Step 5: SQL Node - `prompt_query_context`
* **File**: [agents/sql_analyst.py:L29-L66](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L29-L66)
* **Action**: Connects to PostgreSQL, extracts `public` schema metadata.
* **Metadata Fetched**: `users` table (`user_id`, `first_name`, `last_name`), `rides` table (`ride_id`, `rider_id`, `status`), plus sample data rows.

---

### Step 6: SQL Node - `generate_sql`
* **File**: [agents/sql_analyst.py:L70-L80](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L70-L80)
* **Action**: Passes schema context and curated question to `pick_llm("medium")`.
* **Generated SQL Query**:
  ```sql
  SELECT u.first_name, u.last_name, COUNT(r.ride_id) AS ride_count
  FROM public.users u
  JOIN public.rides r ON u.user_id = r.rider_id
  WHERE r.status = 'completed'
  GROUP BY u.user_id, u.first_name, u.last_name
  ORDER BY ride_count DESC
  LIMIT 3;
  ```

---

### Step 7: SQL Node - `is_safe_sql`
* **File**: [agents/sql_analyst.py:L84-L105](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L84-L105)
* **Action**: Evaluates query using `JudgeSchema`.
* **Result**: `JudgeSchema(answer="Yes", comments="SELECT query with JOIN and GROUP BY; safe read-only query.")`
* **Routing**: `is_safe_sql_edge` routes to `execute_sql`.

---

### Step 8: SQL Node - `execute_sql`
* **File**: [agents/sql_analyst.py:L120-L138](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L120-L138)
* **Action**: Calls `DatabaseUtil.execute_sql(query)`.
* **Result Fetched**: `"[('Alice', 'Smith', 42), ('Bob', 'Jones', 38), ('Charlie', 'Brown', 35)]"`

---

### Step 9: SQL Node - `represent_final_answer`
* **File**: [agents/sql_analyst.py:L142-L165](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L142-L165)
* **Action**: Formats result tuple into clean text via `pick_llm("low")`.
* **Output Text**:
  > "The top 3 users with the most completed rides are:
  > 1. Alice Smith — 42 rides
  > 2. Bob Jones — 38 rides
  > 3. Charlie Brown — 35 rides"
