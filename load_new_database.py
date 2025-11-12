#!/usr/bin/env python
"""
Script pour charger une nouvelle base de données SQLite.
Permet de créer une base de données avec un nombre personnalisé de transactions.
"""

import sys
from pathlib import Path
from create_database import main as create_db

def load_new_database(rows: int = 1000, db_path: Path = None, reset: bool = False):
    """
    Charge une nouvelle base de données avec des transactions.
    
    Args:
        rows: Nombre de transactions à générer
        db_path: Chemin de la base de données (défaut: data/transactions.db)
        reset: Si True, supprime la base existante avant de créer une nouvelle
    """
    project_root = Path(__file__).parent.resolve()
    if db_path is None:
        db_path = project_root / "data" / "transactions.db"
    else:
        db_path = Path(db_path)
    
    # Supprimer la base existante si reset=True
    if reset and db_path.exists():
        db_path.unlink()
        print(f"✅ Base de données existante supprimée: {db_path}")
    
    # Créer la nouvelle base de données
    print(f"🔄 Création de la base de données avec {rows} transactions...")
    success = create_db(rows=rows, db_path=db_path)
    
    if success:
        print(f"✅ Base de données créée avec succès: {db_path}")
        print(f"   {rows} transactions générées")
        return True
    else:
        print(f"❌ Échec de la création de la base de données")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Charger une nouvelle base de données")
    parser.add_argument("--rows", type=int, default=1000, help="Nombre de transactions à générer")
    parser.add_argument("--db", type=str, default=None, help="Chemin de la base de données")
    parser.add_argument("--reset", action="store_true", help="Supprimer la base existante avant de créer une nouvelle")
    
    args = parser.parse_args()
    
    db_path = Path(args.db) if args.db else None
    success = load_new_database(rows=args.rows, db_path=db_path, reset=args.reset)
    
    sys.exit(0 if success else 1)

