# Bookshop Data Platform (Scaffold)

This repository is a **minimal, vendor-agnostic scaffold** generated from `config/datasources.json`.  
It includes:
- **Airflow DAG** for batch ingestion and transform steps
- **dbt** project skeleton for ELT modeling
- **Great Expectations** stub for quality checks
- Simple **config parser** mapping your sources by `namespace_name` and `oddrn`
- Optional **Docker Compose** to bring up a local Postgres + MinIO (S3) sandbox

> Replace placeholders with your real connection strings, credentials, and models.

## Quick Start

1. Create a Python virtual environment and install requirements:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Export environment variables (see `.env.example`) for connectors (Postgres, Snowflake, S3, Kafka, etc.).

3. (Optional) Start local sandbox services:
   ```bash
   docker compose -f infrastructure/docker-compose.yml up -d
   ```

4. Run the **config lister** to see detected assets:
   ```bash
   python tools/list_config.py
   ```

5. For Airflow (local dev), set envs and place `orchestrations/airflow/dags` in your `$AIRFLOW_HOME/dags` (or mount via Compose).

6. For dbt, edit `transformations/dbt_project/dbt_project.yml` + `profiles.yml` and add models in `models/`.

7. For Great Expectations, define expectations in `quality/great_expectations/expectations/` and run checkpoints.

---

## Sources detected from `datasources.json`
We grouped sources by `namespace_name` and parsed `oddrn` to infer the tech family (postgresql, redshift, snowflake, airflow, kafka, s3, kinesis, etc.).

- Namespaces present: ['Data Lake', 'Data Quality', 'ETL', 'Messaging', 'Samples', 'Transactional']

---

### Notes
- This scaffold is intentionally lightweight to be portable. Replace stubs with your vendor SDKs (e.g., `psycopg2`, `snowflake-connector-python`, `boto3`, `confluent-kafka`, etc.).
- The Airflow DAG demonstrates **orchestration patterns**: upstream dependencies, SLAs, retries, and quality gates.
- The dbt skeleton shows where to put **staging (stg_)** and **marts** models.
- Great Expectations folders are prepared; wire them up to your data lake/warehouse.
