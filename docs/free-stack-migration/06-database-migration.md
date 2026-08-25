# 06 — Database & Storage Migration Plan

This document audits relational database and file storage dependencies in **Agentic AI Data Agent**.

---

## 🗄️ Relational Database Audit & Status

* **Current Engine**: **PostgreSQL** (`psycopg2-binary`).
* **Deployment Model**: Local or self-hosted PostgreSQL instance running on `localhost:5432`.
* **Cost**: **$0.00 (100% Free & Open Source)**.
* **Migration Needed**: **No**. Local PostgreSQL is fully open source and free.

---

## 📁 Storage Audit & Status

* **Current Storage**: Local filesystem storage inside the `data/` directory:
  - Dataset seeding CSV files: `data/users.csv`, `rides.csv`, `payments.csv`, etc.
  - API extraction folder: `data/extract/`
  - Transformation folder: `data/transform/`
* **Cost**: **$0.00 (Local Disk)**.
* **Migration Needed**: **No**. No AWS S3 or paid blob storage SDKs are used.
