"""
Kafka consumer & ETL helpers to move transactions from Kafka into Postgres.

This module exposes composable functions that can be orchestrated either from
Airflow (see `airflow_dags/etl_dag.py`) or executed manually as a standalone
batch consumer (`python consumers/kafka_to_postgres.py --help`).
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import List, Optional, Sequence

import click
import pandas as pd
from kafka import KafkaConsumer
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

LOGGER = logging.getLogger("kafka-to-postgres")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)


@dataclass
class ETLConfig:
    """Typed configuration for the ETL flow."""

    kafka_bootstrap_server: str
    kafka_topic: str
    kafka_group_id: str = "transactions-etl"
    batch_size: int = 500
    poll_timeout_ms: int = 5_000
    postgres_conn_uri: str = "postgresql+psycopg2://airflow:airflow@localhost:5432/transactions"


def load_config(
    kafka_bootstrap_server: Optional[str] = None,
    kafka_topic: Optional[str] = None,
    postgres_uri: Optional[str] = None,
    batch_size: Optional[int] = None,
) -> ETLConfig:
    """Load configuration, overriding defaults with environment variables."""

    cfg = ETLConfig(
        kafka_bootstrap_server=kafka_bootstrap_server
        or os.getenv("KAFKA_BOOTSTRAP_SERVER", "localhost:29092"),
        kafka_topic=kafka_topic or os.getenv("KAFKA_TOPIC", "transactions"),
        kafka_group_id=os.getenv("KAFKA_GROUP_ID", "transactions-etl"),
        batch_size=batch_size or int(os.getenv("BATCH_SIZE", "500")),
        poll_timeout_ms=int(os.getenv("POLL_TIMEOUT_MS", "5000")),
        postgres_conn_uri=postgres_uri
        or os.getenv(
            "POSTGRES_CONN_URI",
            "postgresql+psycopg2://airflow:airflow@localhost:5432/transactions",
        ),
    )
    LOGGER.debug("Loaded config: %s", cfg)
    return cfg


def build_consumer(cfg: ETLConfig) -> KafkaConsumer:
    """Instantiate a Kafka consumer configured for batch processing."""
    consumer = KafkaConsumer(
        cfg.kafka_topic,
        bootstrap_servers=cfg.kafka_bootstrap_server,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id=cfg.kafka_group_id,
        max_poll_records=cfg.batch_size,
    )
    return consumer


def fetch_batch(consumer: KafkaConsumer, batch_size: int, timeout_ms: int) -> List[dict]:
    """Fetch a bounded batch of records from Kafka."""
    records: List[dict] = []
    raw_messages = consumer.poll(timeout_ms=timeout_ms, max_records=batch_size)
    for partition, messages in raw_messages.items():
        LOGGER.debug("Fetched %s messages from partition %s", len(messages), partition)
        for message in messages:
            records.append(message.value)
    LOGGER.info("Fetched %s messages from Kafka", len(records))
    return records


def derive_amount_bucket(amount: float) -> str:
    """Simple bucketing logic used for aggregate reporting."""
    if amount < 20:
        return "<20"
    if amount < 100:
        return "20-100"
    if amount < 250:
        return "100-250"
    if amount < 500:
        return "250-500"
    return ">=500"


def transform(records: Sequence[dict]) -> pd.DataFrame:
    """Apply data quality and transformation rules on the batch."""
    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    df["event_ts"] = pd.to_datetime(df.get("event_ts"), utc=True, errors="coerce")
    df["amount"] = pd.to_numeric(df.get("amount"), errors="coerce")
    df["ingested_at"] = datetime.now(timezone.utc)
    df["amount_bucket"] = df["amount"].map(lambda x: derive_amount_bucket(x or 0.0))
    df["event_date"] = df["event_ts"].dt.date
    df["event_hour"] = df["event_ts"].dt.hour
    df["event_dayofweek"] = df["event_ts"].dt.day_name()

    mandatory_columns = ["transaction_id", "user_id", "amount", "event_ts"]
    nulls = df[mandatory_columns].isnull().any()
    if nulls.any():
        bad_columns = ", ".join(nulls[nulls].index.tolist())
        raise ValueError(f"Null values detected in mandatory columns: {bad_columns}")
    return df


def build_engine(uri: str) -> Engine:
    """Return a SQLAlchemy engine that can be reused across batches."""
    engine = create_engine(uri, pool_pre_ping=True, future=True)
    return engine


def insert_raw_records(engine: Engine, df: pd.DataFrame) -> int:
    if df.empty:
        return 0

    payloads = [
        {
            "transaction_id": row["transaction_id"],
            "event_ts": row["event_ts"],
            "payload": json.dumps(
                {
                    key: (
                        value.isoformat()
                        if isinstance(value, (datetime, pd.Timestamp, date))
                        else value
                    )
                    for key, value in df.loc[idx]
                    .drop(labels=["ingested_at"])
                    .to_dict()
                    .items()
                }
            ),
            "ingested_at": row["ingested_at"],
        }
        for idx, row in df.iterrows()
    ]

    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO raw_transactions (transaction_id, event_ts, payload, ingested_at)
                VALUES (:transaction_id, :event_ts, CAST(:payload AS JSONB), :ingested_at)
                ON CONFLICT (transaction_id) DO NOTHING
                """
            ),
            payloads,
        )
    return len(payloads)


def insert_curated_records(engine: Engine, df: pd.DataFrame) -> int:
    if df.empty:
        return 0

    curated = df[
        [
            "transaction_id",
            "event_ts",
            "event_date",
            "event_hour",
            "event_dayofweek",
            "user_id",
            "amount",
            "amount_bucket",
            "merchant",
            "category",
            "city",
            "status",
            "payment_method",
            "currency",
            "ingested_at",
        ]
    ].to_dict(orient="records")

    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO transactions_flat (
                    transaction_id,
                    event_ts,
                    event_date,
                    event_hour,
                    event_dayofweek,
                    user_id,
                    amount,
                    amount_bucket,
                    merchant,
                    category,
                    city,
                    status,
                    payment_method,
                    currency,
                    ingested_at
                )
                VALUES (
                    :transaction_id,
                    :event_ts,
                    :event_date,
                    :event_hour,
                    :event_dayofweek,
                    :user_id,
                    :amount,
                    :amount_bucket,
                    :merchant,
                    :category,
                    :city,
                    :status,
                    :payment_method,
                    :currency,
                    :ingested_at
                )
                ON CONFLICT (transaction_id) DO UPDATE
                SET
                    event_ts = EXCLUDED.event_ts,
                    event_date = EXCLUDED.event_date,
                    event_hour = EXCLUDED.event_hour,
                    event_dayofweek = EXCLUDED.event_dayofweek,
                    user_id = EXCLUDED.user_id,
                    amount = EXCLUDED.amount,
                    amount_bucket = EXCLUDED.amount_bucket,
                    merchant = EXCLUDED.merchant,
                    category = EXCLUDED.category,
                    city = EXCLUDED.city,
                    status = EXCLUDED.status,
                    payment_method = EXCLUDED.payment_method,
                    currency = EXCLUDED.currency,
                    ingested_at = EXCLUDED.ingested_at
                """
            ),
            curated,
        )
    return len(curated)


def run_etl(config: ETLConfig) -> int:
    """Entry point to fetch-transform-load a single micro-batch."""
    consumer = build_consumer(config)
    engine = build_engine(config.postgres_conn_uri)
    try:
        records = fetch_batch(
            consumer,
            batch_size=config.batch_size,
            timeout_ms=config.poll_timeout_ms,
        )
        if not records:
            LOGGER.info("No new records to process.")
            return 0

        transformed = transform(records)
        raw_count = insert_raw_records(engine, transformed)
        curated_count = insert_curated_records(engine, transformed)
        consumer.commit()
        LOGGER.info(
            "Batch processed - raw inserted: %s, curated upserted: %s",
            raw_count,
            curated_count,
        )
        return curated_count
    finally:
        consumer.close()
        engine.dispose()


@click.command()
@click.option("--bootstrap-server", default=None, help="Adresse du cluster Kafka")
@click.option("--topic", default=None, help="Topic à consommer")
@click.option("--postgres-uri", default=None, help="URI SQLAlchemy pour Postgres")
@click.option("--batch-size", type=int, default=None, help="Nombre max d'événements à traiter")
def cli(
    bootstrap_server: Optional[str],
    topic: Optional[str],
    postgres_uri: Optional[str],
    batch_size: Optional[int],
) -> None:
    """CLI pour lancer le traitement d'un micro-batch."""
    config = load_config(
        kafka_bootstrap_server=bootstrap_server,
        kafka_topic=topic,
        postgres_uri=postgres_uri,
        batch_size=batch_size,
    )
    processed = run_etl(config)
    LOGGER.info("Traitement terminé (%s événements).", processed)


if __name__ == "__main__":
    cli()

