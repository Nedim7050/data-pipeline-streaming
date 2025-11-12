import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List

import click

from producer.producer import generate_transaction, produce_transactions  # type: ignore


def generate_transactions(rows: int, seed: int) -> List[dict]:
    random.seed(seed)
    base_time = datetime.now(timezone.utc) - timedelta(days=7)
    transactions = []
    for _ in range(rows):
        tx = generate_transaction()
        tx["event_ts"] = (base_time + timedelta(seconds=random.randint(0, 7 * 24 * 3600))).isoformat()
        transactions.append(tx)
    return transactions


def write_csv(transactions: List[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as csvfile:
        fieldnames = transactions[0].keys() if transactions else ["transaction_id"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        if transactions:
            writer.writerows(transactions)


@click.command()
@click.option("--rows", type=int, default=1000, show_default=True, help="Nombre de transactions à générer")
@click.option("--seed", type=int, default=42, show_default=True, help="Graine aléatoire pour la reproductibilité")
@click.option("--output", type=click.Path(path_type=Path), default=Path("data/synthetic_transactions.csv"), show_default=True)
@click.option("--publish", is_flag=True, default=False, help="Publier également vers Kafka via producer.py")
@click.option("--rate", type=int, default=None, help="Débit d'envoi Kafka (events/sec)")
@click.option("--bootstrap-server", default="localhost:29092", show_default=True, help="Serveur Kafka pour la publication optionnelle")
@click.option("--topic", default="transactions", show_default=True, help="Topic Kafka pour la publication optionnelle")
def cli(rows: int, seed: int, output: Path, publish: bool, rate: int, bootstrap_server: str, topic: str) -> None:
    """Génère un dataset synthétique pour la pipeline et optionally le publie vers Kafka."""
    transactions = generate_transactions(rows, seed)
    write_csv(transactions, output)
    click.echo(f"Fichier généré: {output} ({len(transactions)} lignes)")

    if publish:
        click.echo("Publication vers Kafka...")
        produce_transactions(
            rows=rows,
            rate=rate,
            topic=topic,
            bootstrap_server=bootstrap_server,
        )


if __name__ == "__main__":
    cli()

