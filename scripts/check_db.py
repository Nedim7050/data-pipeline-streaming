"""Script pour vérifier la base de données SQLite."""

from pathlib import Path
import sqlite3

db_path = Path("data/transactions.db")

if db_path.exists():
    print(f"✅ Base de données trouvée: {db_path}")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Vérifier les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"✅ Tables trouvées: {[t[0] for t in tables]}")
    
    # Compter les transactions
    try:
        cursor.execute("SELECT COUNT(*) FROM transactions_flat")
        count = cursor.fetchone()[0]
        print(f"✅ Nombre de transactions dans transactions_flat: {count}")
    except sqlite3.OperationalError as e:
        print(f"⚠️  Erreur lors de la lecture des transactions: {e}")
    
    # Compter les raw transactions
    try:
        cursor.execute("SELECT COUNT(*) FROM raw_transactions")
        count = cursor.fetchone()[0]
        print(f"✅ Nombre de transactions dans raw_transactions: {count}")
    except sqlite3.OperationalError as e:
        print(f"⚠️  Erreur lors de la lecture des raw transactions: {e}")
    
    conn.close()
else:
    print(f"❌ Base de données non trouvée: {db_path}")
    print("💡 Exécutez d'abord: python consumers/file_queue_to_sqlite.py")

