# data-pipeline-streaming - Version Simplifiée (Sans Docker)

Cette version simplifiée fonctionne **sans Docker** en utilisant :
- **SQLite** au lieu de Postgres
- **Fichiers JSONL** au lieu de Kafka
- **Script Python simple** au lieu d'Airflow

## 🚀 Démarrage Rapide

### 1. Installation des dépendances

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-simple.txt
```

### 2. Générer des données de test

```powershell
python producer/producer_to_file.py --rows 10000 --rate 100 --output data/queue/transactions.jsonl
```

### 3. Traiter les données (ETL)

**Option A : Traitement manuel (une fois)**
```powershell
python consumers/file_queue_to_sqlite.py --input data/queue/transactions.jsonl --db data/transactions.db --batch-size 500
```

**Option B : Traitement automatique (scheduler simple)**
```powershell
python scripts/run_simple_etl.py data/queue/transactions.jsonl data/transactions.db 500 30
```
Ce script traite les données toutes les 30 secondes.

### 4. Visualiser avec Streamlit

```powershell
streamlit run analytics/streamlit_dashboard_sqlite.py
```

Ouvrez http://localhost:8501 dans votre navigateur.

## 📁 Structure des Fichiers

```
data/
├── queue/
│   └── transactions.jsonl    # Fichier d'entrée (simule Kafka)
└── transactions.db            # Base SQLite (simule Postgres)
```

## 🔄 Workflow Complet

1. **Générer des transactions** → `producer/producer_to_file.py`
2. **Traiter les transactions** → `consumers/file_queue_to_sqlite.py` ou `scripts/run_simple_etl.py`
3. **Visualiser** → `analytics/streamlit_dashboard_sqlite.py`

## 📊 Exporter les Données

Le dashboard Streamlit permet d'exporter un CSV pour PowerBI/Tableau.

## 🔧 Configuration

Vous pouvez modifier les chemins par défaut via des variables d'environnement :

```powershell
$env:SQLITE_DB_PATH = "data/transactions.db"
$env:INPUT_FILE = "data/queue/transactions.jsonl"
```

## 🆚 Comparaison avec la Version Complète

| Composant | Version Complète | Version Simplifiée |
|-----------|------------------|-------------------|
| Message Queue | Kafka | Fichier JSONL |
| Base de données | Postgres | SQLite |
| Orchestration | Airflow | Script Python |
| Déploiement | Docker Compose | Local |

## 📝 Notes

- La version simplifiée est idéale pour le développement et les tests locaux
- Pour la production, utilisez la version complète avec Docker ou des services cloud
- SQLite peut gérer des millions de lignes, mais Postgres est recommandé pour de gros volumes

## 🚀 Déploiement sur Streamlit Cloud

Pour déployer le dashboard sur Streamlit Cloud :

1. **Pousser votre code sur GitHub**
2. **Créer une app sur https://share.streamlit.io**
3. **Configurer les secrets** (si vous utilisez Postgres cloud) :
   ```
   POSTGRES_CONN_URI = postgresql://user:password@host:5432/db
   ```
4. **Point d'entrée** : `analytics/streamlit_dashboard_sqlite.py`

**Note** : Streamlit Cloud ne peut pas accéder à des fichiers locaux. Pour déployer cette version, vous devrez :
- Soit utiliser une base Postgres cloud (voir section "Services Cloud" ci-dessous)
- Soit héberger SQLite sur un service de stockage accessible (S3, etc.)


