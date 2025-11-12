#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script simple pour creer la base de donnees SQLite."""

import sys
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone

print("=" * 60)
print("Creation de la base de donnees SQLite")
print("=" * 60)

# Chemins
project_root = Path(__file__).parent.resolve()
data_dir = project_root / "data"
db_path = data_dir / "transactions.db"
input_file = data_dir / "queue" / "transactions.jsonl"

print(f"\n1. Verification des chemins...")
print(f"   Projet: {project_root}")
print(f"   Data: {data_dir}")
print(f"   DB: {db_path}")
print(f"   Input: {input_file}")

# Creer le repertoire data
data_dir.mkdir(parents=True, exist_ok=True)
print(f"   OK: Repertoire data cree")

# Verifier le fichier d'entree
if not input_file.exists():
    print(f"\n2. Generation de donnees...")
    try:
        sys.path.insert(0, str(project_root))
        from producer.producer_to_file import produce_to_file
        produce_to_file(rows=200, rate=50, output_file=input_file)
        print(f"   OK: {input_file.stat().st_size} bytes generes")
    except Exception as e:
        print(f"   ERREUR: {e}")
        sys.exit(1)
else:
    print(f"\n2. Fichier d'entree trouve: {input_file.stat().st_size} bytes")

# Supprimer la base existante
if db_path.exists():
    print(f"\n3. Suppression de la base existante...")
    db_path.unlink()
    print(f"   OK: Base supprimee")

# Creer la base de donnees
print(f"\n4. Creation de la base de donnees...")
try:
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Creer les tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_transactions (
            transaction_id TEXT PRIMARY KEY,
            event_ts TEXT NOT NULL,
            payload TEXT NOT NULL,
            ingested_at TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
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
    """)
    
    # Creer les index
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_flat_user_id 
        ON transactions_flat (user_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_flat_event_ts 
        ON transactions_flat (event_ts)
    """)
    
    conn.commit()
    print(f"   OK: Tables creees")
    conn.close()
    
except Exception as e:
    print(f"   ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Lire et inserer les donnees
print(f"\n5. Lecture et insertion des donnees...")
try:
    # Lire les donnees
    records = []
    with input_file.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= 500:  # Limite a 500 transactions
                break
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"   ERREUR ligne {i}: {e}")
                continue
    
    print(f"   OK: {len(records)} transactions lues")
    
    if not records:
        print("   ERREUR: Aucune transaction a inserer")
        sys.exit(1)
    
    # Inserer les donnees
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    ingested_at = datetime.now(timezone.utc).isoformat()
    
    for record in records:
        try:
            # Insertion dans raw_transactions
            cursor.execute("""
                INSERT OR IGNORE INTO raw_transactions 
                (transaction_id, event_ts, payload, ingested_at)
                VALUES (?, ?, ?, ?)
            """, (
                record.get("transaction_id"),
                record.get("event_ts"),
                json.dumps(record),
                ingested_at
            ))
            
            # Transformer pour transactions_flat
            event_ts = datetime.fromisoformat(record.get("event_ts").replace("Z", "+00:00"))
            amount = float(record.get("amount", 0))
            
            # Determiner le bucket
            if amount < 20:
                amount_bucket = "<20"
            elif amount < 100:
                amount_bucket = "20-100"
            elif amount < 250:
                amount_bucket = "100-250"
            elif amount < 500:
                amount_bucket = "250-500"
            else:
                amount_bucket = ">=500"
            
            # Insertion dans transactions_flat
            cursor.execute("""
                INSERT OR REPLACE INTO transactions_flat (
                    transaction_id, event_ts, event_date, event_hour, event_dayofweek,
                    user_id, amount, amount_bucket, merchant, category, city, status,
                    payment_method, currency, ingested_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.get("transaction_id"),
                record.get("event_ts"),
                event_ts.date().isoformat(),
                event_ts.hour,
                event_ts.strftime("%A"),
                int(record.get("user_id", 0)),
                amount,
                amount_bucket,
                record.get("merchant", ""),
                record.get("category", ""),
                record.get("city", ""),
                record.get("status", ""),
                record.get("payment_method", ""),
                record.get("currency", "EUR"),
                ingested_at
            ))
        except Exception as e:
            print(f"   ERREUR transaction {record.get('transaction_id')}: {e}")
            continue
    
    conn.commit()
    print(f"   OK: Donnees inserees")
    conn.close()
    
except Exception as e:
    print(f"   ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Verifier
print(f"\n6. Verification...")
try:
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"   Tables: {tables}")
    
    cursor.execute("SELECT COUNT(*) FROM transactions_flat")
    count = cursor.fetchone()[0]
    print(f"   Transactions dans transactions_flat: {count}")
    
    cursor.execute("SELECT COUNT(*) FROM raw_transactions")
    raw_count = cursor.fetchone()[0]
    print(f"   Transactions dans raw_transactions: {raw_count}")
    
    conn.close()
    
    print("\n" + "=" * 60)
    if count > 0:
        print("SUCCESS: Base de donnees creee avec succes!")
        print(f"Base: {db_path}")
        print(f"Transactions: {count}")
        print("\nPour lancer Streamlit:")
        print("   streamlit run analytics/streamlit_dashboard_sqlite.py")
    else:
        print("ERREUR: Base vide!")
        sys.exit(1)
        
except Exception as e:
    print(f"   ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)

