# 14 — API Documentation

This document covers both internal programmatic APIs (Python state graph APIs) and external HTTP API integrations in **Agentic AI - Data Agent**.

---

## 🌐 1. Internal Programmatic Graph API

The system does not expose a HTTP REST API server (like FastAPI or Flask). Instead, it exposes a programmatic Python invocation interface via compiled LangGraph objects.

### `data_agent.invoke(input_dict)`

* **File Location**: [agents/data_agent.py:L99](file:///e:/AI_Data_Agent-main/agents/data_agent.py#L99)
* **Purpose**: Primary programmatic API to send natural language requests into the multi-agent system.
* **Input Schema**:
  ```python
  {
      "messages": [
          HumanMessage(content="Your prompt text here")
      ],
      "route_response": ""
  }
  ```
* **Return Value**: Updated `DataAgentSchema` dictionary containing all accumulated messages, final model answer, or tool execution outputs.

#### Usage Example:
```python
from agents.data_agent import data_agent
from langchain_core.messages import HumanMessage

result = data_agent.invoke({
    "messages": [HumanMessage(content="Show me total payments by payment method")],
    "route_response": ""
})

print(result["messages"][-1].content)
```

---

## 🔗 2. Sub-Agent Programmatic APIs

### `sql_analyst.invoke(input_dict)`
* **File Location**: [agents/sql_analyst.py:L210](file:///e:/AI_Data_Agent-main/agents/sql_analyst.py#L210)
* **Input Schema**:
  ```python
  {
      "messages": [],
      "user_question": "What is the average rating of drivers in Toronto?",
      "curated_ques": "",
      "prompt_query_context": "",
      "generated_sql_query": "",
      "is_safe": "No",
      "comments": "",
      "sql_query_execution_result": "",
      "final_answer": ""
  }
  ```
* **Return Value**: Fully populated `AgentSchema` dictionary.

---

### `etl_analyst.invoke(input_dict)`
* **File Location**: [agents/etl_analyst.py:L160](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L160)
* **Input Schema**:
  ```python
  {
      "messages": [
          HumanMessage(content="Extract data from https://pokeapi.co/api/v2/pokemon and save to data/extract in csv format")
      ]
  }
  ```
* **Return Value**: Populated `ETLAgentSchema` dictionary containing execution observations.

---

## 📡 3. External HTTP API Integration (`extract_load_tool`)

* **Target Services**: Any public REST API returning JSON payloads (e.g. `https://pokeapi.co/api/v2/pokemon`).
* **HTTP Client**: `requests.get(url)` in [utils/etl_tools.py:L28](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L28).
* **Expected Response Schema**: JSON object containing a `'results'` array key (e.g. `{"results": [...]}`).
* **Error Handling**: Captures `requests.exceptions.RequestException` and returns error status string.
