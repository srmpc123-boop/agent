# 10 — Free Stack System Architecture

This document presents the target system architecture of **Agentic AI Data Agent** running completely on the **Free Groq + Local Infrastructure Stack**.

---

## 🏛️ Free Stack Architectural Diagram

```mermaid
graph TD
    Client([User Prompt / CLI]) --> Main[main.py]
    Main --> DataAgent[agents/data_agent.py: data_agent]
    
    subgraph Free LLM Inference Layer (Groq LPU API)
        DataAgent --> RouterNode[router_node]
        RouterNode --> GroqRouter[ChatGroq: llama-3.3-70b-versatile]
        GroqRouter --> RouterSchema[RouterSchema Output]
    end

    RouterSchema --> RouteEdge{route_edge}

    subgraph Free Text-to-SQL Pipeline
        RouteEdge -- "sql" --> SQLNode[sql_node]
        SQLNode --> Curate[curate_ques]
        Curate --> GroqCurate[ChatGroq: llama-3.1-8b-instant]
        
        Context[prompt_query_context] --> LocalPG[(Local PostgreSQL Database)]
        LocalPG --> SchemaText[Schema & Sample Context]
        
        SchemaText --> GenSQL[generate_sql]
        GenSQL --> GroqSQL[ChatGroq: llama-3.3-70b-versatile]
        
        GroqSQL --> Judge[is_safe_sql]
        Judge --> GroqJudge[ChatGroq: llama-3.3-70b-versatile + JudgeSchema]
        
        GroqJudge -- safe == 'Yes' --> ExecSQL[execute_sql: DatabaseUtil]
        ExecSQL --> LocalPG
        ExecSQL --> FormatAns[represent_final_answer]
        FormatAns --> GroqFormat[ChatGroq: llama-3.1-8b-instant]
    end

    subgraph Free ETL Tool Pipeline
        RouteEdge -- "etl" --> ETLNode[etl_node]
        ETLNode --> ETLLLM[llm_node]
        ETLLLM --> GroqETL[ChatGroq: llama-3.3-70b-versatile.bind_tools]
        
        GroqETL --> ToolCheck{is_tool_call}
        ToolCheck -- tool_calls --> ETLTools[tool_node]
        ETLTools --> ToolExtract[extract_load_tool: requests HTTP GET]
        ETLTools --> ToolTransform[transform_load_tool: Pandas + exec]
        
        ToolExtract --> ExtractedData[(data/extract/extracted_data.csv)]
        ToolTransform --> TransformedData[(data/transform/)]
    end

    GroqFormat --> Output([Final Natural Language Response])
    ETLTools --> Output
```

---

## ⚡ Component Summary

1. **LLM Engine**: Groq LPU Cloud API (`langchain-groq`). Zero API costs under the developer tier.
2. **Database Engine**: Local PostgreSQL (`psycopg2-binary`). Zero database hosting costs.
3. **Data Storage**: Local filesystem storage under `data/`. Zero cloud storage costs.
4. **Agent Framework**: LangGraph + LangChain Core. Zero framework licensing costs.
