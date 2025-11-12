"""
Script de test pour la version simplifiée (sans Docker).

Ce script teste rapidement que tous les composants fonctionnent.
"""

import sys
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from consumers.file_queue_to_sqlite import SimpleETLConfig, init_sqlite_db, run_etl
from producer.producer_to_file import produce_to_file


def test_producer():
    """Teste la génération de transactions."""
    print("🧪 Test 1: Génération de transactions...")
    output_file = Path("data/queue/transactions.jsonl")
    produce_to_file(rows=100, rate=50, output_file=output_file)
    assert output_file.exists(), "Le fichier de transactions n'a pas été créé"
    assert output_file.stat().st_size > 0, "Le fichier de transactions est vide"
    print("✅ Test 1 réussi: Transactions générées")


def test_consumer():
    """Teste le traitement des transactions."""
    print("🧪 Test 2: Traitement des transactions...")
    input_file = Path("data/queue/transactions.jsonl")
    db_path = Path("data/transactions.db")

    if not input_file.exists():
        print("⚠️  Le fichier d'entrée n'existe pas. Génération de données de test...")
        produce_to_file(rows=100, rate=50, output_file=input_file)

    config = SimpleETLConfig(
        input_file=input_file,
        db_path=db_path,
        batch_size=100,
    )
    processed = run_etl(config)
    assert processed > 0, "Aucune transaction n'a été traitée"
    assert db_path.exists(), "La base de données n'a pas été créée"
    print(f"✅ Test 2 réussi: {processed} transactions traitées")


def test_database():
    """Teste l'accès à la base de données."""
    print("🧪 Test 3: Accès à la base de données...")
    from sqlalchemy import create_engine, text

    db_path = Path("data/transactions.db")
    if not db_path.exists():
        print("⚠️  La base de données n'existe pas. Création...")
        init_sqlite_db(db_path)

    engine = create_engine(f"sqlite:///{db_path}")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM transactions_flat"))
        count = result.scalar()
        print(f"✅ Test 3 réussi: {count} transactions dans la base de données")
    engine.dispose()


def main():
    """Exécute tous les tests."""
    print("🚀 Démarrage des tests de la version simplifiée...\n")

    try:
        test_producer()
        print()
        test_consumer()
        print()
        test_database()
        print()
        print("✅ Tous les tests sont passés avec succès!")
        print("\n📊 Prochaines étapes:")
        print("   1. Lancer le dashboard: streamlit run analytics/streamlit_dashboard_sqlite.py")
        print("   2. Générer plus de données: python producer/producer_to_file.py --rows 10000")
        print("   3. Traiter les données: python consumers/file_queue_to_sqlite.py")
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


