# 11 — Tools and Function Calling

This document details all tools registered for agent function calling within **Agentic AI - Data Agent**.

---

## 🛠️ Tool Registry Overview

Tools are defined in [agents/etl_analyst.py](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L18-L81) using LangChain's `@tool` decorator and backed by helper methods in `ETLTools` ([utils/etl_tools.py](file:///e:/AI_Data_Agent-main/utils/etl_tools.py)).

| Tool Name | File & Function | Purpose | Inputs | Returns | External Calls |
| --- | --- | --- | --- | --- | --- |
| `extract_load_tool` | [agents/etl_analyst.py:L18](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L18) | Downloads API JSON and saves as CSV/JSON/Parquet | `url: str, output_folder: str, format: str` | Success/Failure string | `requests.get(url)` |
| `transform_load_tool` | [agents/etl_analyst.py:L38](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py#L38) | Analyzes file preview, generates Pandas code via LLM, and executes code | `input_file_path: str, output_folder: str, output_format: str, user_question: str` | Execution logs & executed code | LLM call + Python `exec()` |

---

## 🔬 Tool 1: `extract_load_tool`

### Implementation Signature
```python
@tool
def extract_load_tool(url: str, output_folder: str, format: str) -> str:
    """
    Extracts data from API (url) and loads it into desired location (output_folder).
    """
    etl_tools = ETLTools()
    return etl_tools.extract_load(url, output_folder, format)
```

### Execution Steps (`ETLTools.extract_load`)
1. Computes absolute output folder path relative to project root ([utils/etl_tools.py:L24-L25](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L24-L25)).
2. Sends HTTP GET request via `requests.get(url)`.
3. Normalizes JSON payload: `df = pd.json_normalize(data['results'])` ([utils/etl_tools.py:L35](file:///e:/AI_Data_Agent-main/utils/etl_tools.py#L35)).
4. Saves data to target format (`df.to_csv`, `df.to_json`, or `df.to_parquet`).
5. Returns confirmation message: `"Data successfully extracted and saved to..."`.

---

## 🔬 Tool 2: `transform_load_tool`

### Implementation Signature
```python
@tool
def transform_load_tool(input_file_path: str, output_folder: str, output_format: str, user_question: str) -> str:
    """
    Transforms data from specified file and loads into desired location.
    """
```

### Execution Steps
1. Calls `ETLTools.transform_load_context(input_file_path)` to load file into Pandas and extract top 3 preview rows (`str(df.head(3))`).
2. Invokes LLM (`"claude"`) with dataset preview and user transformation requirements to write standalone Pandas code.
3. Strips markdown block formatting (`strip('```').lstrip('python')`).
4. Passes generated code string to `ETLTools.execute_code(pandas_code)`, which executes code using Python's `exec(code)` built-in.
5. Returns executed code and execution status string.

---

## 🔄 LLM Function Calling Loop Mechanics

```mermaid
sequenceDiagram
    participant LLM as LLM (llm_node)
    participant Graph as ETL Graph (is_tool_call)
    participant ToolNode as tool_node
    participant ETLTools as ETLTools / Python exec

    LLM->>Graph: Returns AIMessage with tool_calls=[{name: "extract_load_tool", args: {...}}]
    Graph->>ToolNode: Routes to tool_node
    ToolNode->>ETLTools: Invokes tool function with args
    ETLTools-->>ToolNode: Returns observation string
    ToolNode->>Graph: Appends ToolMessage(content=observation, tool_call_id=...)
    Graph->>LLM: Routes back to llm_node with updated message history
    LLM-->>Graph: Returns final AIMessage response (no tool_calls)
    Graph->>END: Terminates execution
```
