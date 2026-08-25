# 23 — Complete Project Diagrams

This document collects essential visual Mermaid diagrams depicting the architecture, graphs, state flows, and data transitions of **Agentic AI - Data Agent**.

---

## 🗺️ 1. Master System Architecture Diagram

```mermaid
graph TD
    Client([User Prompt / CLI]) --> Main[main.py]
    Main --> DataAgentGraph[agents/data_agent.py: Data Agent Graph]
    
    subgraph Intent Routing Layer
        DataAgentGraph --> RouterNode[router_node: RouterSchema]
        RouterNode --> RouteEdge{route_edge}
    end

    subgraph SQL Execution Subsystem
        RouteEdge -- route == 'sql' --> SQLNode[sql_node]
        SQLNode --> SQLGraph[agents/sql_analyst.py: SQL Graph]
        SQLGraph --> CurateNode[curate_ques]
        CurateNode --> SchemaCtxNode[prompt_query_context]
        SchemaCtxNode --> DBUtilSchema[utils/database.py: schema_details]
        DBUtilSchema --> PGInfo[(PostgreSQL information_schema)]
        SchemaCtxNode --> GenSQLNode[generate_sql]
        GenSQLNode --> JudgeNode[is_safe_sql: JudgeSchema]
        JudgeNode --> JudgeEdge{is_safe_sql_edge}
        JudgeEdge -- safe == 'Yes' --> ExecSQLNode[execute_sql]
        ExecSQLNode --> PGExec[(PostgreSQL Database)]
        ExecSQLNode --> RepresentAns[represent_final_answer]
        JudgeEdge -- safe == 'No' --> CancelSQLNode[canceled_sql]
    end

    subgraph ETL Execution Subsystem
        RouteEdge -- route == 'etl' --> ETLNode[etl_node]
        ETLNode --> ETLGraph[agents/etl_analyst.py: ETL Graph]
        ETLGraph --> ETLLLMNode[llm_node: ChatAnthropic.bind_tools]
        ETLLLMNode --> ETLCheckEdge{is_tool_call}
        ETLCheckEdge -- Tool Calls --> ETLToolNode[tool_node]
        ETLToolNode --> ToolExtract[extract_load_tool: ETLTools.extract_load]
        ETLToolNode --> ToolTransform[transform_load_tool: ETLTools.execute_code]
        ToolExtract --> WebAPI[(External Web API)]
        ToolTransform --> FileStore[(Local Disk /data/)]
        ETLToolNode --> ETLLLMNode
        ETLCheckEdge -- Finished --> ETLEnd([End ETL Graph])
    end

    RepresentAns --> Output([Formatted Final Response])
    CancelSQLNode --> Output
    ETLEnd --> Output
```

---

## 🔄 2. SQL Analyst Sub-Graph Flow

```mermaid
stateDiagram-v2
    [*] --> curate_ques
    curate_ques --> prompt_query_context : Question Curated
    prompt_query_context --> generate_sql : Schema Context Attached
    generate_sql --> is_safe_sql : SQL Query Generated
    
    state is_safe_sql_eval <<choice>>
    is_safe_sql --> is_safe_sql_eval
    
    is_safe_sql_eval --> execute_sql : is_safe == 'Yes'
    is_safe_sql_eval --> canceled_sql : is_safe == 'No'
    
    execute_sql --> represent_final_answer : SQL Results Fetched
    canceled_sql --> [*]
    represent_final_answer --> [*]
```

---

## ⚙️ 3. ETL Analyst Sub-Graph Flow

```mermaid
stateDiagram-v2
    [*] --> llm_node
    
    state is_tool_call_eval <<choice>>
    llm_node --> is_tool_call_eval
    
    is_tool_call_eval --> tool_node : Has Tool Calls
    tool_node --> llm_node : Return ToolMessage Observation
    
    is_tool_call_eval --> [*] : No Tool Calls (Finished)
```
