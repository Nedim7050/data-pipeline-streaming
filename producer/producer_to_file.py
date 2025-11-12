"""
Version simplifiée du producer qui écrit dans un fichier JSONL au lieu de Kafka.

Usage:
    python producer/producer_to_file.py --rows 10000 --rate 100 --output data/queue/transactions.jsonl
"""

import json
import logging
import random
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import click
from tqdm import tqdm

# Constantes pour la génération de transactions
CATEGORIES = [
    "grocery",
    "electronics",
    "travel",
    "fashion",
    "restaurants",
    "entertainment",
    "health",
]
STATUSES = ["APPROVED", "DECLINED", "PENDING", "REFUNDED"]
CITIES = [
    "Paris",
    "Lyon",
    "Marseille",
    "Toulouse",
    "Bordeaux",
    "Nice",
    "Nantes",
]
MERCHANTS = [
    "Amazon",
    "Uber",
    "Carrefour",
    "Fnac",
    "Airbnb",
    "Zara",
    "Decathlon",
]


def generate_transaction() -> Dict[str, Any]:
    """Generate a synthetic transaction payload."""
    amount = round(random.uniform(5.0, 750.0), 2)
    created_at = datetime.now(timezone.utc).isoformat()
    return {
        "transaction_id": str(uuid.uuid4()),
        "event_ts": created_at,
        "user_id": random.randint(1, 5_000),
        "amount": amount,
        "merchant": random.choice(MERCHANTS),
        "category": random.choice(CATEGORIES),
        "city": random.choice(CITIES),
        "status": random.choices(STATUSES, weights=[0.75, 0.1, 0.1, 0.05])[0],
        "payment_method": random.choice(["card", "wallet", "bank_transfer"]),
        "currency": "EUR",
    }

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
LOGGER = logging.getLogger("transaction-producer-file")


def _rate_limiter(rate: Optional[int]) -> None:
    """Attend pour respecter le débit cible (événements par seconde)."""
    if not rate or rate <= 0:
        return
    interval = 1.0 / rate
    time.sleep(interval)


def produce_to_file(
    rows: Optional[int],
    rate: Optional[int],
    output_file: Path,
) -> None:
    """Génère des transactions et les écrit dans un fichier JSONL."""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    sent = 0
    with output_file.open("a", encoding="utf-8") as f, tqdm(
        total=rows if rows and rows > 0 else None,
        unit="event",
        desc="Producing transactions",
    ) as progress:
        while True:
            _rate_limiter(rate)
            payload = generate_transaction()
            f.write(json.dumps(payload) + "\n")
            f.flush()  # Écriture immédiate
            sent += 1
            if progress.total:
                progress.update(1)
            if rows and rows > 0 and sent >= rows:
                break
    LOGGER.info("Écrit %s événements dans %s", sent, output_file)


@click.command()
@click.option("--rows", type=int, default=0, help="Nombre d'événements à produire (0 = infini)")
@click.option("--rate", type=int, default=50, help="Débit cible en événements/seconde (0 = sans limite)")
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    default=Path("data/queue/transactions.jsonl"),
    show_default=True,
    help="Fichier de sortie JSONL",
)
def main(rows: int, rate: int, output: Path) -> None:
    """Entrée CLI principale pour générer et écrire des transactions dans un fichier."""
    LOGGER.info("Starting producer rows=%s rate=%s output=%s", rows, rate, output)
    try:
        produce_to_file(rows=rows or None, rate=rate or None, output_file=output)
    except KeyboardInterrupt:
        LOGGER.warning("Interruption utilisateur, arrêt du producteur.")
    finally:
        LOGGER.info("Producteur arrêté proprement.")


if __name__ == "__main__":
    main()

