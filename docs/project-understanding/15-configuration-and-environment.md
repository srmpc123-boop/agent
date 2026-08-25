# 15 — Configuration and Environment

This document describes all environment variables, configuration parameters, and secret requirements for **Agentic AI - Data Agent**.

---

## ⚙️ Environment Variables Reference (`.env`)

Configuration is managed via `.env` files loaded using `python-dotenv` ([utils/llm_pick.py:L4](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L4), [feed_db.py:L6](file:///e:/AI_Data_Agent-main/feed_db.py#L6)).

| Variable Name | Required? | Default Value | Description | Consumed In File |
| --- | --- | --- | --- | --- |
| `OPENAI_API_KEY` | Yes (if using OpenAI) | `<secret>` | API Key for OpenAI LLM services | `utils/llm_pick.py` |
| `ANTHROPIC_API_KEY` | Yes (if using Claude) | `<secret>` | API Key for Anthropic Claude LLM services | `utils/llm_pick.py` |
| `host` | Yes | `localhost` | PostgreSQL database host | `feed_db.py`, `agents/sql_analyst.py` |
| `port` | Yes | `5432` | PostgreSQL database port | `feed_db.py`, `agents/sql_analyst.py` |
| `database` | Yes | `postgres` / `data_agent_db` | PostgreSQL database name | `feed_db.py`, `agents/sql_analyst.py` |
| `user` | Yes | `postgres` | PostgreSQL user | `feed_db.py`, `agents/sql_analyst.py` |
| `password` | Yes | `<secret>` | PostgreSQL password | `feed_db.py`, `agents/sql_analyst.py` |

---

## 📄 Configuration Template (`.env.example`)

The codebase includes [.env.example](file:///e:/AI_Data_Agent-main/.env.example):

```env
OPENAI_API_KEY=blabla
ANTHROPIC_API_KEY=blabla

port=5432
database=postgres
host=localhost
user=postgres
password=postgres
```

---

## 🤖 LLM Model Selection Configuration

In [utils/llm_pick.py](file:///e:/AI_Data_Agent-main/utils/llm_pick.py#L16-L32), model selection is configured programmatically via the `level` string:

```python
# Level "low" -> ChatOpenAI(model_name="gpt-5.6-luna", temperature=0)
# Level "medium" -> ChatOpenAI(model_name="gpt-5.6-terra", temperature=0)
# Level "high" -> ChatOpenAI(model_name="gpt-5.6-sol", temperature=0)
# Level "claude" -> ChatAnthropic(model_name="claude-sonnet-5")
```

### Production Recommended Overrides:
To run with real OpenAI and Anthropic accounts, modify `utils/llm_pick.py` to use:
- `"low"`: `gpt-4o-mini`
- `"medium"`: `gpt-4o`
- `"claude"`: `claude-3-5-sonnet-20240620`
