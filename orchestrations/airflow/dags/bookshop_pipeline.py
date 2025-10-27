from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os, json, pathlib

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[3]
CONFIG_PATH = PROJECT_ROOT / 'config' / 'datasources.json'

default_args = {
    'owner': 'data-platform',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'sla': timedelta(hours=2),
}

def load_sources():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_postgres(**_):
    sources = load_sources()
    pg = [s for s in sources if s.get('oddrn','').startswith('//postgresql')]
    # TODO: connect using psycopg2 and export tables to S3 (parquet/csv)
    print('Found Postgres sources:', [s['name'] for s in pg])

def extract_snowflake(**_):
    sources = load_sources()
    sf = [s for s in sources if s.get('oddrn','').startswith('//snowflake')]
    # TODO: query Snowflake and land results to S3 / stage
    print('Found Snowflake sources:', [s['name'] for s in sf])

def land_streaming(**_):
    sources = load_sources()
    streams = [s for s in sources if s.get('oddrn','').startswith('//kafka') or s.get('oddrn','').startswith('//kinesis')]
    # TODO: consume topics/streams and land to S3 raw zone
    print('Found streaming sources:', [s['name'] for s in streams])

def quality_checks(**_):
    # TODO: call Great Expectations checkpoint(s)
    print('Run Great Expectations checkpoints (stub)')

def run_dbt(**_):
    # TODO: dbt run + dbt test (invoke via subprocess)
    print('Run dbt transformations (stub)')

with DAG(
    dag_id='bookshop_batch_pipeline',
    start_date=datetime(2025, 1, 1),
    schedule_interval='0 2 * * *',  # daily at 02:00
    catchup=False,
    default_args=default_args,
    description='Batch pipeline generated from datasources.json',
    tags=['bookshop','data-platform'],
) as dag:

    t_extract_pg = PythonOperator(task_id='extract_postgres', python_callable=extract_postgres)
    t_extract_sf = PythonOperator(task_id='extract_snowflake', python_callable=extract_snowflake)
    t_stream_land = PythonOperator(task_id='land_streaming_raw', python_callable=land_streaming)
    t_quality = PythonOperator(task_id='quality_checks', python_callable=quality_checks)
    t_dbt = PythonOperator(task_id='dbt_transform', python_callable=run_dbt)

    # Orchestration: raw -> quality -> transform
    [t_extract_pg, t_extract_sf, t_stream_land] >> t_quality >> t_dbt
