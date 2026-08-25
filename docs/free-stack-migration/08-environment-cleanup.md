# 08 — Environment Variable Cleanup

This document details the environment configuration updates for running **Agentic AI Data Agent** on the free Groq stack.

---

## 🛠️ Environment Variables Matrix

| Variable | Purpose | Required? | Provider | Replacement / Default |
| --- | --- | --- | --- | --- |
| `LLM_PROVIDER` | Selects LLM backend | Yes | Internal | `groq` |
| `GROQ_API_KEY` | Authentication for Groq LPU inference | Yes (if provider is groq) | Groq (Free Tier) | `<your_groq_api_key>` |
| `GROQ_MODEL_LOW` | Fast model for curation/synthesis | Optional | Groq | `llama-3.1-8b-instant` |
| `GROQ_MODEL_MEDIUM`| Model for SQL generation & safety judge | Optional | Groq | `llama-3.3-70b-versatile` |
| `GROQ_MODEL_HIGH` | Model for routing & Pandas code generation | Optional | Groq | `llama-3.3-70b-versatile` |
| `OPENAI_API_KEY` | OpenAI authentication | No | OpenAI | Optional fallback |
| `ANTHROPIC_API_KEY`| Anthropic authentication | No | Anthropic | Optional fallback |
| `host` | PostgreSQL host | Yes | Local | `localhost` |
| `port` | PostgreSQL port | Yes | Local | `5432` |
| `database` | PostgreSQL database name | Yes | Local | `postgres` |
| `user` | PostgreSQL user | Yes | Local | `postgres` |
| `password` | PostgreSQL password | Yes | Local | `postgres` |

---

## 📄 Updated Template (`.env.example`)

```env
# Primary Free LLM Configuration (Groq)
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_free_groq_api_key_here

# Groq Model Selection
GROQ_MODEL_LOW=llama-3.1-8b-instant
GROQ_MODEL_MEDIUM=llama-3.3-70b-versatile
GROQ_MODEL_HIGH=llama-3.3-70b-versatile

# Optional Paid Provider Fallbacks
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Local PostgreSQL Database Configuration
port=5432
database=postgres
host=localhost
user=postgres
password=postgres
```
