# 19 — Deployment and Runtime

This document details how to install, configure, execute, and deploy **Agentic AI - Data Agent**.

---

## 💻 Local Development Setup

### Step 1: Environment & Dependency Installation
Requires Python 3.12+.

```bash
# Clone project and navigate into repository
cd AI_Data_Agent-main

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies via uv or pip
uv pip install -r requirements.txt
# OR
pip install -e .
```

---

### Step 2: PostgreSQL Database Initialization

1. Ensure PostgreSQL service is running on `localhost:5432`.
2. Create target database:
   ```sql
   CREATE DATABASE postgres;
   ```
3. Copy environment configuration:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` to supply database user/password and API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).
5. Populate PostgreSQL tables with sample dataset:
   ```bash
   python feed_db.py
   ```
   *Expected Output*:
   ```text
   Connected to PostgreSQL
   Tables created successfully
   Loaded users.csv
   Loaded vehicles.csv
   Loaded rides.csv
   Loaded payments.csv
   Loaded ratings.csv

   Record counts:
   ----------------------------------------
   users               10,000
   vehicles             1,500
   rides               50,000
   payments            48,500
   ratings             42,000

   Data loaded successfully!
   Transaction committed.
   PostgreSQL connection closed.
   ```

---

### Step 3: Running the Application

Execute `main.py`:
```bash
python main.py
```

---

## 🐳 Production Containerization Roadmap (Docker)

To deploy as a microservice or worker:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```
