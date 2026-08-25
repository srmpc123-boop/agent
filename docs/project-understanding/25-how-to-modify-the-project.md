# 25 — How to Modify the Project

This document provides step-by-step developer recipes for extending or modifying **Agentic AI - Data Agent**.

---

## 🛠️ Recipe 1: Add a New Agent (e.g., Visualization Agent)

To add a new specialized agent (such as a Matplotlib/Seaborn Chart Generator):

1. **Define State Schema**:
   In [Models/schema.py](file:///e:/AI_Data_Agent-main/Models/schema.py), add `VizAgentSchema` and update `RouterSchema` options:
   ```python
   class RouterSchema(BaseModel):
       answer: Literal["sql", "etl", "viz"] = Field(...)
   ```
2. **Build Agent Graph**:
   Create `agents/viz_analyst.py` defining nodes for generating chart Python code and saving image files.
3. **Update Router Node**:
   In [agents/data_agent.py](file:///e:/AI_Data_Agent-main/agents/data_agent.py):
   - Add `viz_node(state)`
   - Add node to `data_agent_graph.add_node("viz_node", viz_node)`
   - Update `route_edge` conditional map to route `"viz"` -> `"viz_node"`.

---

## 🛠️ Recipe 2: Add a New Tool to ETL Agent

To add a file conversion tool (e.g. Parquet-to-CSV converter):

1. **Add Utility Method**:
   In [utils/etl_tools.py](file:///e:/AI_Data_Agent-main/utils/etl_tools.py), implement `convert_parquet_to_csv(self, src, dst)`.
2. **Decorate `@tool`**:
   In [agents/etl_analyst.py](file:///e:/AI_Data_Agent-main/agents/etl_analyst.py):
   ```python
   @tool
   def convert_parquet_to_csv_tool(src_path: str, dst_path: str) -> str:
       """Converts a Parquet file to CSV format."""
       etl_tools = ETLTools()
       return etl_tools.convert_parquet_to_csv(src_path, dst_path)
   ```
3. **Register Tool**:
   Add tool to `tools` list in `agents/etl_analyst.py`:
   ```python
   tools = [extract_load_tool, transform_load_tool, convert_parquet_to_csv_tool]
   ```

---

## 🛠️ Recipe 3: Change LLM Model Provider or Tiers

To update model providers or tier mappings:
1. Open [utils/llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L6-L34).
2. Modify `model_name` parameters inside `pick_llm(level)` (e.g. change `"gpt-5.6-luna"` to `"gpt-4o-mini"` or `"claude-sonnet-5"` to `"claude-3-5-sonnet-20240620"`).

---

## 🛠️ Recipe 4: Add a New Table to PostgreSQL Database

1. Open [feed_db.py](file:///e:/AI_Data_Agent-main/feed_db.py).
2. Add table creation DDL inside `create_tables_sql` (e.g., `CREATE TABLE public.promotions (...)`).
3. Add a `load_csv()` call targeting your CSV file.
4. Run `python feed_db.py`.
5. The `prompt_query_context` node in `sql_analyst.py` will automatically detect the new table via `DatabaseUtil.schema_details("public")` on the next run!
