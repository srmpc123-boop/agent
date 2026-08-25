# 09 — Cost Analysis (Before vs. After)

This document provides a comparative financial cost analysis before and after migrating to the **Free Stack (Groq + Open Source)**.

---

## 💰 Cost Comparison Table

| Subsystem Component | Before Migration (Paid Stack) | After Migration (Free Stack) | Estimated Savings |
| --- | --- | --- | --- |
| **Router LLM Inference** | Anthropic Claude 3.5 Sonnet (~$3.00 / 1M input tokens) | Groq Llama 3.3 70B (Free Developer Tier) | **100% Savings** |
| **Text-to-SQL LLM Inference** | OpenAI GPT-4o (~$2.50 / 1M input tokens) | Groq Llama 3.3 70B (Free Developer Tier) | **100% Savings** |
| **SQL Safety Judge LLM** | OpenAI GPT-4o-mini (~$0.15 / 1M input tokens) | Groq Llama 3.1 8B (Free Developer Tier) | **100% Savings** |
| **Pandas Code Generation** | Anthropic Claude 3.5 Sonnet (~$15.00 / 1M output tokens)| Groq Llama 3.3 70B (Free Developer Tier) | **100% Savings** |
| **Database Storage** | Local PostgreSQL ($0.00) | Local PostgreSQL ($0.00) | **No Change ($0.00)** |
| **File Storage** | Local Filesystem ($0.00) | Local Filesystem ($0.00) | **No Change ($0.00)** |
| **TOTAL ESTIMATED MONTHLY COST** | **$15.00 – $100.00+ / month (Usage dependent)** | **$0.00 / month** | **$0.00 Recurring Cost** |

---

## 📌 Free Tier Allowance Summary

Groq provides a generous free tier for developers:
- **`llama-3.1-8b-instant`**: 30 requests per minute (RPM), 14,400 requests per day (RPD), 500,000 tokens per minute (TPM).
- **`llama-3.3-70b-versatile`**: 30 requests per minute (RPM), 14,400 requests per day (RPD), 100,000 tokens per minute (TPM).

This allowance is more than sufficient to run hundreds of natural language data queries per day at **$0 cost**.
