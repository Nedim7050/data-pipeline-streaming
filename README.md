# Data Pipeline Streaming

Pipeline de données de bout-en-bout illustrant la génération, l'ingestion, la transformation et la visualisation de transactions financières synthétiques.

## 🚀 Démarrage Rapide

### Option 1: Version Simplifiée (Sans Docker) - **RECOMMANDÉ**

```powershell
# 1. Installer les dépendances
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-simple.txt

# 2. Créer la base de données et générer des données
python create_database.py

# 3. Lancer le dashboard
streamlit run dashboard_working.py
```

### Option 2: Version Complète (Avec Docker)

```bash
# 1. Démarrer l'écosystème
docker compose up -d

# 2. Activer le DAG dans Airflow UI (http://localhost:8080)

# 3. Produire des événements
python producer/producer.py --rows 10000 --rate 100

# 4. Visualiser
streamlit run analytics/streamlit_dashboard.py
```

## 📊 Architecture

- **Producteur** (`producer/producer.py`) génère des événements JSON et les publie sur Kafka
- **Kafka & Zookeeper** gèrent le transport des événements
- **Airflow** orchestre l'ETL micro-batch (Kafka → Postgres) via le DAG `transactions_etl`
- **Postgres** stocke les tables raw/curated et les vues matérialisées
- **Streamlit** visualise en quasi temps réel les transactions agrégées

## 🌐 Déploiement

### Déployer sur Streamlit Cloud

1. **Pousser le projet sur GitHub**
2. **Aller sur [Streamlit Cloud](https://streamlit.io/cloud)**
3. **Connecter votre repository GitHub**
4. **Configurer le déploiement:**
   - **Main file:** `streamlit_app.py` (recommandé) ou `dashboard_working.py`
   - **Python version:** `3.11`
5. **Déployer!**

Voir [DEPLOY.md](DEPLOY.md) pour plus de détails.

### Déployer sur GitHub

```bash
# 1. Initialiser Git
git init

# 2. Ajouter les fichiers
git add .

# 3. Commit
git commit -m "Initial commit"

# 4. Créer un repository sur GitHub et pousser
git remote add origin https://github.com/votre-username/data-pipeline-streaming.git
git branch -M main
git push -u origin main
```

## 📁 Structure du Projet

```
data-pipeline-streaming/
├── producer/          # Générateur de transactions
├── consumers/         # Consumer Kafka → Postgres/SQLite
├── airflow_dags/      # DAGs Airflow
├── analytics/         # Dashboard Streamlit
├── scripts/           # Scripts utilitaires
├── sql/               # Schémas SQL
├── docker/            # Configuration Docker
├── requirements.txt   # Dépendances (Docker)
├── requirements-simple.txt  # Dépendances (Local)
└── README.md
```

## 🔧 Configuration

### Variables d'environnement

```bash
# Kafka
KAFKA_BOOTSTRAP_SERVER=localhost:29092
KAFKA_TOPIC=transactions

# Postgres
POSTGRES_CONN_URI=postgresql+psycopg2://airflow:airflow@localhost:5432/transactions

# SQLite (Version simplifiée)
SQLITE_DB_PATH=data/transactions.db
```

## 📊 Fonctionnalités

- ✅ Génération de transactions synthétiques
- ✅ Ingestion Kafka ou fichiers JSONL
- ✅ Transformation ETL (Airflow ou script Python)
- ✅ Stockage Postgres ou SQLite
- ✅ Visualisation Streamlit avec graphiques et métriques
- ✅ Export CSV pour PowerBI/Tableau

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Démarrage rapide
- [DEPLOY.md](DEPLOY.md) - Guide de déploiement
- [GITHUB-DEPLOY.md](GITHUB-DEPLOY.md) - Guide complet GitHub et Streamlit Cloud
- [README-CLOUD.md](README-CLOUD.md) - Déploiement cloud
- [START-HERE.md](START-HERE.md) - Guide de démarrage détaillé

## 📄 Licence

Projet sous licence MIT (voir `LICENSE`).
