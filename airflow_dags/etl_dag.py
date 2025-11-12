import io
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

from airflow import DAG
from airflow.models import Variable
from sqlalchemy import text
import pandas as pd
from airflow.operators.python import PythonOperator

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from consumers.kafka_to_postgres import ETLConfig, build_engine, build_consumer, fetch_batch, insert_curated_records, insert_raw_records, load_config, transform  # noqa: E402

LOGGER = logging.getLogger("airflow.etl_dag")


def airflow_config() -> ETLConfig:
    """Resolve configuration combining Airflow Variables and defaults."""
    kafka_bootstrap = Variable.get("KAFKA_BOOTSTRAP_SERVER", default_var="kafka:9092")
    kafka_topic = Variable.get("KAFKA_TOPIC", default_var="transactions")
    postgres_conn_uri = Variable.get(
        "POSTGRES_CONN_URI",
        default_var="postgresql+psycopg2://airflow:airflow@postgres:5432/transactions",
    )
    batch_size = int(Variable.get("BATCH_SIZE", default_var="500"))
    return load_config(
        kafka_bootstrap_server=kafka_bootstrap,
        kafka_topic=kafka_topic,
        postgres_uri=postgres_conn_uri,
        batch_size=batch_size,
    )


def fetch_from_kafka(**context) -> List[Dict[str, Any]]:
    cfg = airflow_config()
    consumer = build_consumer(cfg)
    try:
        batch = fetch_batch(
            consumer,
            batch_size=cfg.batch_size,
            timeout_ms=cfg.poll_timeout_ms,
        )
        context["ti"].xcom_push(key="kafka_partition_offsets", value=str(consumer.assignment()))
        return batch
    finally:
        consumer.close()


def transform_records(**context) -> str:
    records = context["ti"].xcom_pull(task_ids="fetch_from_kafka")
    df = transform(records or [])
    payload = df.to_json(orient="records", date_format="iso")
    return payload


def load_to_postgres(**context) -> Dict[str, int]:
    cfg = airflow_config()
    engine = build_engine(cfg.postgres_conn_uri)
    records_json = context["ti"].xcom_pull(task_ids="transform_records")
    if not records_json:
        LOGGER.info("No transformed records found.")
        return {"raw_inserted": 0, "curated_upserted": 0}

    df = pd.read_json(io.StringIO(records_json), orient="records", convert_dates=False)
    if df.empty:
        LOGGER.info("Transformed dataframe is empty.")
        return {"raw_inserted": 0, "curated_upserted": 0}

    df["event_ts"] = pd.to_datetime(df["event_ts"], utc=True)
    df["ingested_at"] = pd.to_datetime(df["ingested_at"], utc=True)
    if "event_date" in df.columns:
        df["event_date"] = pd.to_datetime(df["event_date"]).dt.date

    if df.empty:
        LOGGER.info("Transformed dataframe is empty.")
        return {"raw_inserted": 0, "curated_upserted": 0}

    raw_count = insert_raw_records(engine, df)
    curated_count = insert_curated_records(engine, df)
    engine.dispose()
    return {"raw_inserted": raw_count, "curated_upserted": curated_count}


def quality_checks(**context) -> None:
    cfg = airflow_config()
    engine = build_engine(cfg.postgres_conn_uri)
    with engine.connect() as conn:
        total = conn.execute(
            text("SELECT COUNT(*) FROM transactions_flat WHERE event_ts >= NOW() - INTERVAL '1 day'")
        ).scalar()
        if total is None or total <= 0:
            raise ValueError("Quality check failed: aucune ligne chargée dans transactions_flat.")

        nulls = conn.execute(
            text(
                """
            SELECT COUNT(*) FROM transactions_flat
            WHERE transaction_id IS NULL OR user_id IS NULL
            """
            )
        ).scalar()
        if nulls and nulls > 0:
            raise ValueError("Quality check failed: valeurs nulles détectées sur des colonnes clés.")
    engine.dispose()


default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
}

with DAG(
    dag_id="transactions_etl",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=timedelta(minutes=5),
    catchup=False,
    max_active_runs=1,
    tags=["streaming", "transactions"],
) as dag:
    fetch_task = PythonOperator(
        task_id="fetch_from_kafka",
        python_callable=fetch_from_kafka,
        provide_context=True,
    )

    transform_task = PythonOperator(
        task_id="transform_records",
        python_callable=transform_records,
        provide_context=True,
    )

    load_task = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_to_postgres,
        provide_context=True,
    )

    quality_task = PythonOperator(
        task_id="quality_checks",
        python_callable=quality_checks,
        provide_context=True,
    )

    fetch_task >> transform_task >> load_task >> quality_task

