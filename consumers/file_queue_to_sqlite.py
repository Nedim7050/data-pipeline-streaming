"""
Version simplifiée du consumer qui lit depuis un fichier JSON (simule Kafka)
et écrit dans SQLite (simule Postgres).

Usage:
    python consumers/file_queue_to_sqlite.py --input data/queue/transactions.jsonl --batch-size 100
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Sequence

import click
import pandas as pd
from sqlalchemy import create_engine, text

LOGGER = logging.getLogger("file-queue-to-sqlite")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)


@dataclass
class SimpleETLConfig:
    """Configuration simplifiée pour l'ETL sans Docker."""

    input_file: Path
    db_path: Path
    batch_size: int = 500
    processed_file: Optional[Path] = None


def load_transactions_from_file(input_file: Path, batch_size: int) -> List[dict]:
    """Lit un fichier JSONL (une transaction par ligne) et retourne un batch."""
    records: List[dict] = []
    if not input_file.exists():
        LOGGER.warning("Fichier d'entrée non trouvé: %s", input_file)
        return records

    with input_file.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= batch_size:
                break
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                LOGGER.error("Erreur de parsing JSON ligne %s: %s", i, e)
    LOGGER.info("Lu %s transactions depuis %s", len(records), input_file)
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


def init_sqlite_db(db_path: Path) -> None:
    """Initialise la base SQLite avec le schéma."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}")

    with engine.connect() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS raw_transactions (
                    transaction_id TEXT PRIMARY KEY,
                    event_ts TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    ingested_at TEXT NOT NULL
                )
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS transactions_flat (
                    transaction_id TEXT PRIMARY KEY,
                    event_ts TEXT NOT NULL,
                    event_date TEXT NOT NULL,
                    event_hour INTEGER NOT NULL,
                    event_dayofweek TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    amount_bucket TEXT NOT NULL,
                    merchant TEXT,
                    category TEXT,
                    city TEXT,
                    status TEXT,
                    payment_method TEXT,
                    currency TEXT,
                    ingested_at TEXT NOT NULL
                )
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS idx_transactions_flat_user_id 
                ON transactions_flat (user_id)
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS idx_transactions_flat_event_ts 
                ON transactions_flat (event_ts)
                """
            )
        )
        conn.commit()
    LOGGER.info("Base SQLite initialisée: %s", db_path)


def insert_raw_records(engine, df: pd.DataFrame) -> int:
    """Insère les enregistrements bruts dans SQLite."""
    if df.empty:
        return 0

    payloads = []
    for idx, row in df.iterrows():
        payloads.append(
            {
                "transaction_id": str(row["transaction_id"]),
                "event_ts": row["event_ts"].isoformat() if pd.notna(row["event_ts"]) else None,
                "payload": json.dumps(
                    {
                        key: (
                            value.isoformat()
                            if isinstance(value, (datetime, pd.Timestamp))
                            else value
                        )
                        for key, value in row.drop(labels=["ingested_at"]).to_dict().items()
                    }
                ),
                "ingested_at": row["ingested_at"].isoformat() if pd.notna(row["ingested_at"]) else None,
            }
        )

    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT OR IGNORE INTO raw_transactions 
                (transaction_id, event_ts, payload, ingested_at)
                VALUES (:transaction_id, :event_ts, :payload, :ingested_at)
                """
            ),
            payloads,
        )
    return len(payloads)


def insert_curated_records(engine, df: pd.DataFrame) -> int:
    """Insère les enregistrements transformés dans SQLite."""
    if df.empty:
        return 0

    curated = []
    for _, row in df.iterrows():
        curated.append(
            {
                "transaction_id": str(row["transaction_id"]),
                "event_ts": row["event_ts"].isoformat() if pd.notna(row["event_ts"]) else None,
                "event_date": str(row["event_date"]) if pd.notna(row["event_date"]) else None,
                "event_hour": int(row["event_hour"]) if pd.notna(row["event_hour"]) else None,
                "event_dayofweek": str(row["event_dayofweek"]) if pd.notna(row["event_dayofweek"]) else None,
                "user_id": int(row["user_id"]) if pd.notna(row["user_id"]) else None,
                "amount": float(row["amount"]) if pd.notna(row["amount"]) else None,
                "amount_bucket": str(row["amount_bucket"]) if pd.notna(row["amount_bucket"]) else None,
                "merchant": str(row.get("merchant", "")),
                "category": str(row.get("category", "")),
                "city": str(row.get("city", "")),
                "status": str(row.get("status", "")),
                "payment_method": str(row.get("payment_method", "")),
                "currency": str(row.get("currency", "EUR")),
                "ingested_at": row["ingested_at"].isoformat() if pd.notna(row["ingested_at"]) else None,
            }
        )

    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT OR REPLACE INTO transactions_flat (
                    transaction_id, event_ts, event_date, event_hour, event_dayofweek,
                    user_id, amount, amount_bucket, merchant, category, city, status,
                    payment_method, currency, ingested_at
                )
                VALUES (
                    :transaction_id, :event_ts, :event_date, :event_hour, :event_dayofweek,
                    :user_id, :amount, :amount_bucket, :merchant, :category, :city, :status,
                    :payment_method, :currency, :ingested_at
                )
                """
            ),
            curated,
        )
    return len(curated)


def run_etl(config: SimpleETLConfig) -> int:
    """Entry point pour traiter un batch depuis un fichier vers SQLite."""
    init_sqlite_db(config.db_path)
    engine = create_engine(f"sqlite:///{config.db_path}")

    try:
        records = load_transactions_from_file(config.input_file, config.batch_size)
        if not records:
            LOGGER.info("Aucun enregistrement à traiter.")
            return 0

        transformed = transform(records)
        raw_count = insert_raw_records(engine, transformed)
        curated_count = insert_curated_records(engine, transformed)

        LOGGER.info(
            "Batch traité - raw insérés: %s, curated upsertés: %s",
            raw_count,
            curated_count,
        )

        # Optionnel: déplacer les lignes traitées vers un fichier "processed"
        if config.processed_file:
            config.processed_file.parent.mkdir(parents=True, exist_ok=True)
            with config.processed_file.open("a", encoding="utf-8") as f:
                for record in records:
                    f.write(json.dumps(record) + "\n")

        return curated_count
    finally:
        engine.dispose()


@click.command()
@click.option("--input", type=click.Path(path_type=Path), default=Path("data/queue/transactions.jsonl"), help="Fichier JSONL d'entrée")
@click.option("--db", type=click.Path(path_type=Path), default=Path("data/transactions.db"), help="Chemin de la base SQLite")
@click.option("--batch-size", type=int, default=500, help="Taille du batch")
@click.option("--processed", type=click.Path(path_type=Path), default=None, help="Fichier pour déplacer les lignes traitées")
def cli(input: Path, db: Path, batch_size: int, processed: Optional[Path]) -> None:
    """CLI pour traiter un batch depuis un fichier vers SQLite."""
    config = SimpleETLConfig(
        input_file=input,
        db_path=db,
        batch_size=batch_size,
        processed_file=processed,
    )
    processed_count = run_etl(config)
    LOGGER.info("Traitement terminé (%s événements).", processed_count)


if __name__ == "__main__":
    cli()


