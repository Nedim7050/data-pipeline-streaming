"""
Script simple pour orchestrer l'ETL sans Airflow.

Ce script simule un scheduler simple qui exécute l'ETL toutes les X secondes.
"""

import logging
import time
from pathlib import Path

from consumers.file_queue_to_sqlite import SimpleETLConfig, run_etl

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
LOGGER = logging.getLogger("simple-etl-scheduler")


def main(
    input_file: Path = Path("data/queue/transactions.jsonl"),
    db_path: Path = Path("data/transactions.db"),
    batch_size: int = 500,
    interval_seconds: int = 30,
    max_iterations: int = None,
) -> None:
    """Exécute l'ETL en boucle toutes les X secondes."""
    config = SimpleETLConfig(
        input_file=input_file,
        db_path=db_path,
        batch_size=batch_size,
    )

    iteration = 0
    LOGGER.info(
        "Démarrage du scheduler ETL - intervalle: %s secondes, batch_size: %s",
        interval_seconds,
        batch_size,
    )

    try:
        while True:
            iteration += 1
            LOGGER.info("=== Itération %s ===", iteration)

            try:
                processed = run_etl(config)
                LOGGER.info("Traitement terminé: %s événements", processed)
            except Exception as e:
                LOGGER.error("Erreur lors du traitement: %s", e, exc_info=True)

            if max_iterations and iteration >= max_iterations:
                LOGGER.info("Nombre maximum d'itérations atteint.")
                break

            LOGGER.info("Attente de %s secondes avant la prochaine itération...", interval_seconds)
            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        LOGGER.info("Arrêt demandé par l'utilisateur.")
    finally:
        LOGGER.info("Scheduler arrêté.")


if __name__ == "__main__":
    import sys

    input_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/queue/transactions.jsonl")
    db_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("data/transactions.db")
    batch_size = int(sys.argv[3]) if len(sys.argv) > 3 else 500
    interval = int(sys.argv[4]) if len(sys.argv) > 4 else 30

    main(
        input_file=input_file,
        db_path=db_path,
        batch_size=batch_size,
        interval_seconds=interval,
    )


