# 📊 Data Pipeline Streaming

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Nedim7050-black.svg)](https://github.com/Nedim7050)

> **Pipeline de données de bout-en-bout** pour la génération, l'ingestion, la transformation et la visualisation de transactions financières synthétiques en temps réel.

## 👤 Auteur

**Nedim Mejri**  
📧 [GitHub Profile](https://github.com/Nedim7050) | 🚀 [Repository](https://github.com/Nedim7050/data-pipeline-streaming)

---

## 🎯 Vue d'ensemble

Ce projet implémente un **pipeline de données complet** (end-to-end) qui simule le traitement de transactions financières en temps réel. Il démontre les concepts modernes de traitement de données avec :

- 🔄 **Génération de données** : Transactions financières synthétiques réalistes
- 📥 **Ingestion** : Kafka ou fichiers JSONL
- 🔧 **Transformation ETL** : Apache Airflow ou scripts Python
- 💾 **Stockage** : PostgreSQL ou SQLite
- 📊 **Visualisation** : Dashboard Streamlit interactif

### ✨ Caractéristiques principales

- ✅ Architecture modulaire et extensible
- ✅ Support Docker pour déploiement facile
- ✅ Version simplifiée sans Docker (SQLite)
- ✅ Dashboard interactif avec filtres avancés
- ✅ Export des données (CSV)
- ✅ Documentation complète et guides détaillés

---

## 🚀 Démarrage Rapide

### Option 1 : Version Simplifiée (Sans Docker) ⭐ **RECOMMANDÉ**

Parfait pour démarrer rapidement sans configuration complexe.

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

Le dashboard sera accessible sur `http://localhost:8501`

### Option 2 : Version Complète (Avec Docker)

Pour une architecture complète avec Kafka, Airflow et PostgreSQL.

```bash
# 1. Démarrer l'écosystème (Kafka, Zookeeper, Airflow, Postgres)
docker compose up -d

# 2. Accéder à l'interface Airflow (http://localhost:8080)
# Activer le DAG 'transactions_etl'

# 3. Produire des événements
python producer/producer.py --rows 10000 --rate 100

# 4. Visualiser dans le dashboard
streamlit run analytics/streamlit_dashboard.py
```

---

## 📊 Architecture

Le pipeline suit une architecture modulaire en plusieurs étapes :

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│  Producer   │────▶│  Kafka/JSONL │────▶│    ETL      │────▶│  Database   │
│  (Python)   │     │  (Queue)     │     │ (Airflow)   │     │ (Postgres/  │
│             │     │              │     │             │     │  SQLite)    │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
                                                                      │
                                                                      ▼
                                                              ┌─────────────┐
                                                              │  Streamlit  │
                                                              │  Dashboard  │
                                                              └─────────────┘
```

### Composants

| Composant | Description | Technologie |
|-----------|-------------|-------------|
| **Producteur** | Génère des transactions synthétiques | Python |
| **Queue** | Système de messagerie distribué | Kafka / JSONL |
| **ETL** | Transformation et chargement des données | Airflow / Python |
| **Base de données** | Stockage structuré | PostgreSQL / SQLite |
| **Dashboard** | Visualisation interactive | Streamlit |

---

## 📁 Structure du Projet

```
data-pipeline-streaming/
├── producer/              # Générateur de transactions synthétiques
│   ├── producer.py        # Producteur Kafka
│   └── producer_to_file.py # Producteur fichier JSONL
├── consumers/             # Consumers Kafka → Database
│   ├── kafka_to_postgres.py
│   └── file_queue_to_sqlite.py
├── airflow_dags/          # DAGs Apache Airflow
│   └── etl_dag.py
├── analytics/             # Dashboards Streamlit
│   ├── streamlit_dashboard.py
│   └── streamlit_dashboard_sqlite.py
├── scripts/               # Scripts utilitaires
├── sql/                   # Schémas de base de données
├── docker/                # Configuration Docker
├── notebooks/             # Notebooks d'exploration
├── create_database.py     # Script de création de base de données
├── dashboard_working.py   # Dashboard Streamlit principal
├── streamlit_app.py       # App Streamlit pour Cloud
├── requirements.txt       # Dépendances (version complète)
└── requirements-simple.txt # Dépendances (version simplifiée)
```

---

## 🔧 Configuration

### Variables d'environnement

```bash
# Kafka
KAFKA_BOOTSTRAP_SERVER=localhost:29092
KAFKA_TOPIC=transactions

# PostgreSQL (version complète)
POSTGRES_CONN_URI=postgresql+psycopg2://airflow:airflow@localhost:5432/transactions

# SQLite (version simplifiée)
SQLITE_DB_PATH=data/transactions.db
```

---

## 📊 Fonctionnalités du Dashboard

Le dashboard Streamlit offre :

- 📈 **Métriques en temps réel** : Montants, transactions, statistiques
- 📊 **Graphiques interactifs** : Visualisations des données
- 🔍 **Filtres avancés** : Catégorie, ville, statut, montant, date
- 📥 **Export CSV** : Export des données pour analyse externe
- 🎨 **Interface intuitive** : Design moderne et responsive

---

## 🌐 Déploiement

### Déploiement sur Streamlit Cloud

✅ **Le projet est déjà disponible sur GitHub** : [Nedim7050/data-pipeline-streaming](https://github.com/Nedim7050/data-pipeline-streaming)

1. **Aller sur [Streamlit Cloud](https://streamlit.io/cloud)**
2. **Se connecter avec GitHub**
3. **Cliquer sur "New app"**
4. **Configurer le déploiement :**
   - **Repository :** `Nedim7050/data-pipeline-streaming`
   - **Branch :** `main`
   - **Main file :** `streamlit_app.py`
   - **Python version :** `3.11`
5. **Cliquer sur "Deploy!"**

📖 Voir [DEPLOY.md](DEPLOY.md) ou [GITHUB-DEPLOY.md](GITHUB-DEPLOY.md) pour plus de détails.

---

## 📚 Documentation

- 📖 [PRESENTATION.md](PRESENTATION.md) - Présentation complète du projet, objectifs et cas d'usage
- ⚡ [QUICKSTART.md](QUICKSTART.md) - Guide de démarrage rapide
- 📊 [GUIDE-ANALYSE-NOUVELLE-BD.md](GUIDE-ANALYSE-NOUVELLE-BD.md) - Guide pour analyser une nouvelle base de données
- 🚀 [DEPLOY.md](DEPLOY.md) - Guide de déploiement détaillé
- 🌐 [GITHUB-DEPLOY.md](GITHUB-DEPLOY.md) - Guide complet GitHub et Streamlit Cloud
- 🎯 [START-HERE.md](START-HERE.md) - Guide de démarrage pour débutants
- ✨ [AMELIORATIONS-PROJET.md](AMELIORATIONS-PROJET.md) - Améliorations et fonctionnalités futures

---

## 🛠️ Technologies Utilisées

- **Python 3.11** - Langage principal
- **Streamlit** - Dashboard interactif
- **Apache Kafka** - Système de messagerie distribué
- **Apache Airflow** - Orchestration de workflows
- **PostgreSQL** - Base de données relationnelle
- **SQLite** - Base de données légère
- **Docker** - Containerisation
- **Pandas** - Manipulation de données
- **Plotly** - Visualisations interactives

---

## 📊 Cas d'Usage

- 🎓 **Étudiants** : Apprendre les concepts de pipelines de données
- 💼 **Développeurs** : Prototyper des systèmes de traitement de données
- 🏢 **Entreprises** : Démonstration de concepts de data engineering
- 📚 **Formateurs** : Matériel pédagogique pour cours de données

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- 🐛 Signaler des bugs
- 💡 Proposer de nouvelles fonctionnalités
- 📝 Améliorer la documentation
- 🔧 Soumettre des pull requests

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👤 Auteur

**Nedim Mejri**

- 🌐 GitHub : [@Nedim7050](https://github.com/Nedim7050)
- 📦 Repository : [data-pipeline-streaming](https://github.com/Nedim7050/data-pipeline-streaming)

---

## ⭐ Support

Si ce projet vous a été utile, n'hésitez pas à lui donner une ⭐ sur GitHub !

---

<div align="center">

**Fait avec ❤️ par Nedim Mejri**

[⬆ Retour en haut](#-data-pipeline-streaming)

</div>
