#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script simple pour creer la base de donnees SQLite."""

import sys
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


def generate_transaction():
    """Generate a synthetic transaction payload."""
    import random
    import uuid
    
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


def main(rows: Optional[int] = 500, db_path: Optional[Path] = None) -> bool:
    """
    Crée la base de données SQLite avec des données de test.
    
    Args:
        rows: Nombre de transactions à générer (défaut: 500)
        db_path: Chemin de la base de données (défaut: data/transactions.db)
    
    Returns:
        True si la création a réussi, False sinon
    """
    try:
        # Chemins
        project_root = Path(__file__).parent.resolve()
        if db_path is None:
            db_path = project_root / "data" / "transactions.db"
        else:
            db_path = Path(db_path)
        
        data_dir = db_path.parent
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Supprimer la base existante si elle existe
        if db_path.exists():
            db_path.unlink()
        
        # Créer la base de données
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Créer les tables
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
        
        # Créer les index
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_flat_user_id 
            ON transactions_flat (user_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_flat_event_ts 
            ON transactions_flat (event_ts)
        """)
        
        conn.commit()
        conn.close()
        
        # Générer et insérer les données
        ingested_at = datetime.now(timezone.utc).isoformat()
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        inserted_count = 0
        for i in range(rows):
            try:
                # Générer une transaction
                record = generate_transaction()
                
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
                
                # Déterminer le bucket
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
                inserted_count += 1
            except Exception as e:
                print(f"Erreur transaction {i}: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        # Vérifier
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM transactions_flat")
        count = cursor.fetchone()[0]
        conn.close()
        
        if count > 0:
            print(f"SUCCESS: Base de données créée avec succès! {count} transactions insérées.")
            return True
        else:
            print("ERREUR: Base vide!")
            return False
            
    except Exception as e:
        print(f"ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Pour l'exécution en ligne de commande
    project_root = Path(__file__).parent.resolve()
    db_path = project_root / "data" / "transactions.db"
    
    print("=" * 60)
    print("Creation de la base de donnees SQLite")
    print("=" * 60)
    
    success = main(rows=500, db_path=db_path)
    
    if success:
        print(f"Base: {db_path}")
        print("Pour lancer Streamlit:")
        print("   streamlit run dashboard_working.py")
    else:
        print("Échec de la création de la base de données")
        sys.exit(1)
    
    print("=" * 60)
