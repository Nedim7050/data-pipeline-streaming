import json
import logging
import random
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

import click
from kafka import KafkaProducer
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
LOGGER = logging.getLogger("transaction-producer")


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


def _build_producer(bootstrap_server: str) -> KafkaProducer:
    """Instantiate a Kafka producer with sane defaults."""
    return KafkaProducer(
        bootstrap_servers=bootstrap_server,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        linger_ms=100,
        batch_size=32_768,
        retries=5,
        acks="all",
    )


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


def _rate_limiter(rate: Optional[int]) -> Iterable[None]:
    """Yield control to respect the target rate (events per second)."""
    if not rate or rate <= 0:
        while True:
            yield
    interval = 1.0 / rate
    last_emit = time.perf_counter()
    while True:
        now = time.perf_counter()
        elapsed = now - last_emit
        if elapsed < interval:
            time.sleep(interval - elapsed)
        last_emit = time.perf_counter()
        yield


def _send_transactions(
    producer: KafkaProducer,
    topic: str,
    rows: Optional[int],
    rate: Optional[int],
) -> None:
    limiter = _rate_limiter(rate)
    sent = 0
    with tqdm(
        total=rows if rows and rows > 0 else None,
        unit="event",
        desc="Producing transactions",
    ) as progress:
        while True:
            limiter.__next__()
            payload = generate_transaction()
            producer.send(topic, value=payload)
            sent += 1
            if progress.total:
                progress.update(1)
            if rows and rows > 0 and sent >= rows:
                break
    producer.flush()
    LOGGER.info("Sent %s events to topic %s", sent, topic)


def produce_transactions(
    rows: Optional[int],
    rate: Optional[int],
    topic: str,
    bootstrap_server: str,
) -> None:
    producer = _build_producer(bootstrap_server)
    try:
        _send_transactions(producer, topic, rows=rows or None, rate=rate or None)
    finally:
        producer.flush()
        producer.close()


@click.command()
@click.option("--rows", type=int, default=0, help="Nombre d'événements à produire (0 = infini)")
@click.option("--rate", type=int, default=50, help="Débit cible en événements/seconde (0 = sans limite)")
@click.option("--topic", type=str, default="transactions", show_default=True, help="Topic Kafka cible")
@click.option(
    "--bootstrap-server",
    "bootstrap_server",
    type=str,
    default="localhost:29092",
    show_default=True,
    help="Adresse du cluster Kafka",
)
def main(rows: int, rate: int, topic: str, bootstrap_server: str) -> None:
    """Entrée CLI principale pour générer et envoyer des transactions vers Kafka."""
    LOGGER.info(
        "Starting producer rows=%s rate=%s topic=%s bootstrap=%s",
        rows,
        rate,
        topic,
        bootstrap_server,
    )
    try:
        produce_transactions(rows=rows or None, rate=rate or None, topic=topic, bootstrap_server=bootstrap_server)
    except KeyboardInterrupt:
        LOGGER.warning("Interruption utilisateur, arrêt du producteur.")
    finally:
        LOGGER.info("Producteur arrêté proprement.")


if __name__ == "__main__":
    main()

