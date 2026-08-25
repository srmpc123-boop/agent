# 01 — LLM Provider Migration Plan (Groq)

This document details the migration plan from paid proprietary LLM APIs (OpenAI & Anthropic) to **Groq (`langchain-groq`)** for zero-cost, ultra-fast LLM inference.

---

## 🧠 Groq Capability Matching & Model Mapping

Groq provides extremely fast LPU-powered inference with a generous free tier for developers. We map existing paid model tiers to high-performance open-weight models on Groq:

| Tier Name | Existing Paid Model | Groq Replacement Model | Functionality Supported |
| --- | --- | --- | --- |
| **`"low"`** | `gpt-3.5-turbo` / `gpt-4o-mini` | `llama-3.1-8b-instant` | Chat, Structured Outputs, Question Curation, Natural Text Synthesis |
| **`"medium"`** | `gpt-4-turbo` / `gpt-4o` | `llama-3.3-70b-versatile` | Complex SQL Generation, SQL Safety Judging (`JudgeSchema`), Schema Context Reasoning |
| **`"high"` / `"claude"`** | `claude-3-opus` / `claude-3-5-sonnet` | `llama-3.3-70b-versatile` | Intent Routing (`RouterSchema`), Tool Calling (`bind_tools`), Python Pandas Code Generation |

---

## ⚡ Capability Verification Checklist

- **Tool Calling (`bind_tools`)**: `ChatGroq` natively supports LangChain tool binding for `extract_load_tool` and `transform_load_tool`.
- **Structured Output (`with_structured_output`)**: `ChatGroq` supports Pydantic structured output validation for `RouterSchema` and `JudgeSchema`.
- **System & Human Messages**: Fully compatible with `HumanMessage`, `AIMessage`, and `ToolMessage`.

---

## 🛠️ Refactored Provider Architecture (`utils/llm_pick.py`)

The LLM factory is refactored to support `LLM_PROVIDER=groq` as default, while remaining fully configurable via environment variables:

```python
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

load_dotenv()

def pick_llm(level: str):
    provider = os.getenv("LLM_PROVIDER", "groq").lower()
    
    if provider == "groq":
        groq_api_key = os.getenv("GROQ_API_KEY")
        if level.lower() == "low":
            model = os.getenv("GROQ_MODEL_LOW", "llama-3.1-8b-instant")
            return ChatGroq(model_name=model, temperature=0, groq_api_key=groq_api_key)
        elif level.lower() == "medium":
            model = os.getenv("GROQ_MODEL_MEDIUM", "llama-3.3-70b-versatile")
            return ChatGroq(model_name=model, temperature=0, groq_api_key=groq_api_key)
        elif level.lower() in ["high", "claude"]:
            model = os.getenv("GROQ_MODEL_HIGH", "llama-3.3-70b-versatile")
            return ChatGroq(model_name=model, temperature=0, groq_api_key=groq_api_key)
        else:
            return ChatGroq(model_name="llama-3.1-8b-instant", temperature=0, groq_api_key=groq_api_key)
    elif provider == "openai":
        return ChatOpenAI(model_name=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
    elif provider == "anthropic":
        return ChatAnthropic(model_name=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620"), temperature=0)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
```

---

## 🔑 Environment Variable Changes

Old `.env` requirements:
```env
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
```

New Free-Stack `.env` requirements:
```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_free_groq_api_key_here
GROQ_MODEL_LOW=llama-3.1-8b-instant
GROQ_MODEL_MEDIUM=llama-3.3-70b-versatile
GROQ_MODEL_HIGH=llama-3.3-70b-versatile
```
