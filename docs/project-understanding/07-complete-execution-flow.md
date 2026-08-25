# 07 — Complete Request / Execution Flow

This document details the step-by-step end-to-end execution flow of requests passing through the **Agentic AI - Data Agent** system.

---

## 🌊 Execution Paths

Because the top-level agent acts as an intent router, a user request follows one of two primary pathways:

1. **SQL Pipeline Path**: Natural language query → Router Node → SQL Analyst Graph → Schema Introspection → SQL Generation → LLM Guardrail Judge → PostgreSQL Execution → Natural Language Formatting.
2. **ETL Pipeline Path**: File / API operation request → Router Node → ETL Analyst Graph → Tool Selection → API Extraction / Pandas Transformation → Code Exec → Response Assembly.

---

## 🔬 Trace 1: SQL Pipeline Execution Trace

Assume user prompt: *"Which user has made the highest total payment amount?"*

```text
1. User Request Received in main.py
   └── Input: {"messages": [HumanMessage("Which user has made the highest total payment amount?")], "route_response": ""}

2. Data Agent Router Node (agents/data_agent.py: router_node)
   ├── Extract message content: "Which user has made the highest total payment amount?"
   ├── Invoke llm_router (ChatAnthropic + RouterSchema)
   ├── Model returns structured response: RouterSchema(answer="sql", comments="User is asking for database aggregation.")
   └── State update: state.route_response = "sql"

3. Conditional Edge Routing (agents/data_agent.py: route_edge)
   └── route_edge evaluates state.route_response ("sql") -> routes to "sql_node"

4. SQL Node Dispatched (agents/data_agent.py: sql_node)
   ├── Constructs SQL input schema:
   │   {"messages": [], "user_question": "Which user has made...", "curated_ques": "", ...}
   └── Invokes sql_analyst.invoke(input_schema)

5. SQL Analyst Sub-Graph: Node 1 - curate_ques (agents/sql_analyst.py)
   ├── Calls pick_llm("low") (ChatOpenAI)
   ├── Prompt: "Curate the following question: Which user has made the highest total payment amount?"
   └── Result stored in state.curated_ques: "Find the user with the maximum total payment sum."

6. SQL Analyst Sub-Graph: Node 2 - prompt_query_context (agents/sql_analyst.py)
   ├── Instantiates DatabaseUtil(conn_details)
   ├── Calls DatabaseUtil.schema_details("public")
   │   ├── Queries information_schema.tables & columns
   │   └── Queries top 5 sample rows for users, rides, payments, vehicles, ratings
   └── Injects schema details into prompt_query_context state variable

7. SQL Analyst Sub-Graph: Node 3 - generate_sql (agents/sql_analyst.py)
   ├── Calls pick_llm("medium") with prompt_query_context
   └── Model returns SQL string:
       "SELECT u.user_id, u.first_name, u.last_name, SUM(p.amount) AS total_paid
        FROM public.users u JOIN public.payments p ON u.user_id = p.user_id
        GROUP BY u.user_id, u.first_name, u.last_name
        ORDER BY total_paid DESC LIMIT 10;"

8. SQL Analyst Sub-Graph: Node 4 - is_safe_sql (agents/sql_analyst.py)
   ├── Calls pick_llm("medium").with_structured_output(JudgeSchema)
   ├── Prompt inspects query for forbidden DDL/DML (INSERT, DELETE, DROP, etc.)
   └── Model returns: JudgeSchema(answer="Yes", comments="SELECT query only.")

9. SQL Analyst Sub-Graph: Conditional Edge (is_safe_sql_edge)
   └── is_safe ("Yes") -> routes to "execute_sql"

10. SQL Analyst Sub-Graph: Node 5 - execute_sql (agents/sql_analyst.py)
    ├── Calls DatabaseUtil.execute_sql(generated_sql_query)
    ├── Executes SELECT query on PostgreSQL
    └── Result stored in state.sql_query_execution_result: "[(1042, 'John', 'Doe', Decimal('1450.50'))]"

11. SQL Analyst Sub-Graph: Node 6 - represent_final_answer (agents/sql_analyst.py)
    ├── Calls pick_llm("low") with execution result & original question
    ├── Model returns final text: "User John Doe (ID: 1042) made the highest total payments amounting to $1,450.50."
    └── Appends AIMessage to state.messages and returns to sql_node

12. Response Returned to Data Agent & Output to Main
```

---

## 🔬 Trace 2: ETL Pipeline Execution Trace

Assume user prompt: *"Extract data from 'https://pokeapi.co/api/v2/pokemon' and save to data/extract folder in csv format."*

```text
1. Router Node classifies request as "etl" -> routes to etl_node.
2. etl_node invokes etl_analyst sub-graph.
3. etl_analyst: llm_node receives message history, selects extract_load_tool with args:
   {"url": "https://pokeapi.co/api/v2/pokemon", "output_folder": "data/extract", "format": "csv"}.
4. is_tool_call detects tool call -> routes to tool_node.
5. tool_node executes extract_load_tool:
   ├── Makes HTTP GET request to PokeAPI
   ├── Normalizes JSON output via pandas (pd.json_normalize(data['results']))
   ├── Saves DataFrame to e:\AI_Data_Agent-main\data\extract\extracted_data.csv
   └── Appends ToolMessage("Data successfully extracted and saved to...")
6. tool_node routes back to llm_node.
7. llm_node sees completed ToolMessage, formats final user message: "The data from PokeAPI has been extracted and saved to data/extract/extracted_data.csv.", and terminates graph execution (is_tool_call -> END).
```
