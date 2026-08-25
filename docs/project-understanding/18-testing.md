# 18 — Testing

This document inspects test coverage, test scripts, and recommendations for implementing test suites in **Agentic AI - Data Agent**.

---

## 🧪 Current Test Status

* **Automated Unit Tests (`pytest` / `unittest`)**: **Not Implemented**. There is no `tests/` directory in the repository.
* **Integration Tests**: Standalone script blocks inside `if __name__ == "__main__":` blocks serve as manual developer integration tests.

---

## 📄 Existing Verification & Script Entry Points

### 1. `main.py`
Serves as an integration test for the top-level `data_agent` graph with a sample API extraction prompt:
```python
if __name__ == "__main__":
    response = data_agent.invoke(
        {"messages":[HumanMessage(content="I want to extract the data from the API endpoint 'https://pokeapi.co/api/v2/pokemon' and save it to data/extract folder in the csv format")],
         "route_response": ""}
    )
    print(response)
```

### 2. `agents/sql_analyst.py`
Contains a manual test harness executing a SQL query against PostgreSQL:
```python
if __name__ == "__main__":
    input_schema = {
        "messages": [],
        "user_question": "What are the different types of Payment Methods we have in our database",
        ...
    }
    sql_analyst_response = sql_analyst.invoke(input_schema)
    print(sql_analyst_response['generated_sql_query'])
```

### 3. `agents/etl_analyst.py`
Contains a manual test harness calling `etl_analyst.invoke()` with sample prompts.

---

## 🚀 Recommended Unit & Integration Test Plan

To bring the project to production standards, implement pytest suites:

1. **`tests/test_router.py`**: Mock `pick_llm` and verify `router_node` correctly returns `"sql"` for database prompts and `"etl"` for file prompts.
2. **`tests/test_sql_judge.py`**: Test `is_safe_sql` against known dangerous SQL queries (`DROP TABLE users;`, `DELETE FROM rides;`) to verify rejections.
3. **`tests/test_etl_tools.py`**: Unit test `extract_load` and `transform_load_context` using `unittest.mock.patch('requests.get')`.
4. **`tests/test_database.py`**: Test PostgreSQL schema extraction and connection handling against a test database instance.
