# 13 — Testing Audit

This audit evaluates test coverage, test infrastructure, edge-case validation, and provides a recommended test plan for **Agentic AI - Data Agent**.

---

## 📊 Current Test Coverage Assessment

* **Testing Score**: **1.0 / 10**
* **Automated Unit Tests**: None (0% code coverage).
* **Integration Tests**: None.
* **Test Suite Framework**: No `pytest` or `unittest` configuration files (`pytest.ini`, `conftest.py`, `tests/` directory).

Developer verification currently relies entirely on manual execution of `if __name__ == "__main__":` blocks at the bottom of source files.

---

## 🚀 Top 10 Recommended Unit & Integration Tests

To make the codebase production-ready, implement the following tests inside a `tests/` directory:

1. **`test_router_node`**: Mock `llm_router.invoke` and verify `router_node` routes SQL prompts to `"sql_node"` and ETL prompts to `"etl_node"`.
2. **`test_sql_judge_safe`**: Verify `is_safe_sql` returns `"Yes"` for valid `SELECT` queries with `JOIN` and `GROUP BY`.
3. **`test_sql_judge_unsafe`**: Verify `is_safe_sql` returns `"No"` for dangerous queries containing `DROP TABLE`, `DELETE FROM`, or `UPDATE`.
4. **`test_database_schema_introspection`**: Test `DatabaseUtil.schema_details("public")` against a mock PostgreSQL database to verify formatted table context output.
5. **`test_database_connection_reuse`**: Verify calling `schema_details()` followed by `execute_sql()` on the same `DatabaseUtil` instance does not raise `psycopg2.InterfaceError`.
6. **`test_extract_load_tool_csv`**: Mock `requests.get` returning JSON data and verify `extract_load_tool` correctly creates CSV output files.
7. **`test_extract_load_tool_error`**: Mock `requests.get` raising `requests.exceptions.HTTPError` and verify tool returns clean error string.
8. **`test_transform_load_context`**: Verify `ETLTools.transform_load_context()` correctly reads top 3 preview rows from CSV files.
9. **`test_end_to_end_sql_flow`**: Integration test invoking `data_agent.invoke()` with a synthetic database prompt.
10. **`test_end_to_end_etl_flow`**: Integration test invoking `data_agent.invoke()` with an API extraction prompt.
