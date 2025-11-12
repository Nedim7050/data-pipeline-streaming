# 📊 Data Pipeline Streaming - Présentation du Projet

## 🎯 Qu'est-ce que c'est ?

**Data Pipeline Streaming** est un **pipeline de données de bout-en-bout** (end-to-end data pipeline) qui illustre le processus complet de traitement de données financières, de la **génération** à la **visualisation**. 

Ce projet simule un système de traitement de transactions en temps réel avec des données synthétiques, démontrant les concepts essentiels du traitement de données modernes.

---

## 🚀 À quoi ça sert ?

### 1. **Génération de Données** 📝
- ✅ Génère des **transactions financières synthétiques** réalistes
- ✅ Simule un flux de données en temps réel
- ✅ Montants, catégories, marchands, villes, statuts variés
- ✅ Permet de tester et démontrer des pipelines sans données réelles

### 2. **Ingestion de Données** 🔄
- ✅ Collecte les transactions depuis différentes sources
- ✅ Support de **Kafka** (messagerie distribuée) ou **fichiers JSONL**
- ✅ Gère le flux de données de manière fiable et scalable
- ✅ Support de différents formats de données

### 3. **Transformation de Données (ETL)** 🔧
- ✅ Transforme les données brutes en données structurées
- ✅ Applique des **règles de qualité de données**
- ✅ Enrichit les données avec des métadonnées (dates, heures, buckets de montants)
- ✅ Nettoie et valide les données
- ✅ Support de **Apache Airflow** pour l'orchestration

### 4. **Stockage de Données** 💾
- ✅ Stocke les données dans une base de données
- ✅ Support de **SQLite** (version simplifiée) et **PostgreSQL** (version complète)
- ✅ Maintient une version brute et une version transformée
- ✅ Crée des index pour des requêtes rapides
- ✅ Support de vues matérialisées pour des agrégations

### 5. **Visualisation et Analyse** 📈
- ✅ **Dashboard interactif** avec Streamlit
- ✅ Graphiques et métriques en temps réel
- ✅ **Filtres avancés** (catégorie, ville, statut, montant, date)
- ✅ Export des données pour analyse externe (CSV)
- ✅ Analyses statistiques (montants, tendances, top marchands)

### 6. **Cas d'Usage Réels** 🎯

#### Pour les Étudiants
- 📚 Apprendre les concepts de traitement de données
- 📚 Comprendre les pipelines de données
- 📚 Pratiquer avec les technologies modernes

#### Pour les Développeurs
- 💼 Démonstration de compétences techniques
- 💼 Prototypage rapide de solutions
- 💼 Base pour des projets plus complexes

#### Pour les Data Engineers
- 🔧 Exemple de pipeline de données complet
- 🔧 Référence pour des projets similaires
- 🔧 Démonstration de best practices

#### Pour les Analystes de Données
- 📊 Analyse de données financières
- 📊 Visualisation interactive
- 📊 Export de données pour PowerBI, Tableau, etc.

---

## 🛠️ Technologies Utilisées

### **🔷 Backend & Données**

#### 1. **Python 3.11+** 🐍
- Langage de programmation principal
- Utilisé pour tous les scripts de traitement de données
- Bibliothèques : Pandas, SQLAlchemy, Kafka-Python

#### 2. **Apache Kafka** (Optionnel) 📨
- Système de messagerie distribuée
- Gère le flux de données en temps réel
- Permet la communication asynchrone entre services
- Utilisé pour l'ingestion de données en streaming

#### 3. **Zookeeper** (Optionnel) 🐘
- Service de coordination pour Kafka
- Gère la configuration et la synchronisation
- Utilisé avec Kafka pour la gestion des clusters

#### 4. **SQLite** (Version Simplifiée) 🗄️
- Base de données légère et embarquée
- Stocke les transactions et les métadonnées
- Pas besoin de serveur séparé
- Idéal pour le développement et les démonstrations

#### 5. **PostgreSQL** (Version Complète) 🐘
- Base de données relationnelle robuste
- Stocke les données brutes et transformées
- Supporte des requêtes complexes
- Utilisé dans la version Docker complète

#### 6. **Apache Airflow** (Optionnel) 🌊
- Orchestrateur de workflows
- Gère l'exécution des tâches ETL
- Planifie et surveille les pipelines
- Interface web pour la gestion des DAGs (Directed Acyclic Graphs)

### **🔷 Frontend & Visualisation**

#### 7. **Streamlit** 🎨
- Framework Python pour créer des applications web
- Dashboard interactif et responsive
- Graphiques et visualisations intégrés
- Filtres et contrôles utilisateur
- Déploiement facile sur Streamlit Cloud

#### 8. **Pandas** 📊
- Bibliothèque Python pour l'analyse de données
- Manipulation et transformation de données
- Agrégations et calculs statistiques
- Export de données (CSV, JSON, etc.)

#### 9. **Altair** (via Streamlit) 📈
- Bibliothèque de visualisation de données
- Graphiques interactifs
- Intégration native avec Streamlit
- Support de différents types de graphiques (barres, lignes, etc.)

### **🔷 Infrastructure & Déploiement**

#### 10. **Docker & Docker Compose** (Optionnel) 🐳
- Conteneurisation des services
- Orchestration de plusieurs services (Kafka, Zookeeper, Postgres, Airflow)
- Facilite le déploiement et la mise à l'échelle
- Environnement de développement reproductible

#### 11. **Git & GitHub** 📦
- Contrôle de version
- Collaboration et partage de code
- Historique des modifications
- Intégration avec Streamlit Cloud

#### 12. **Streamlit Cloud** ☁️
- Plateforme de déploiement pour Streamlit
- Déploiement automatique depuis GitHub
- Hosting gratuit
- Mise à jour automatique

### **🔷 Outils & Bibliothèques**

#### 13. **SQLAlchemy** 🔗
- ORM (Object-Relational Mapping) pour Python
- Abstraction de la base de données
- Support de SQLite et PostgreSQL
- Requêtes SQL simplifiées

#### 14. **Kafka-Python** 📨
- Client Kafka pour Python
- Production et consommation de messages
- Gestion des topics et partitions
- Support des consumers et producers

#### 15. **Click** 🖱️
- Framework CLI pour Python
- Création de commandes en ligne de commande
- Arguments et options personnalisables
- Interface utilisateur intuitive

#### 16. **TQDM** 📊
- Barre de progression pour Python
- Affichage du progrès des tâches
- Estimation du temps restant
- Amélioration de l'expérience utilisateur

#### 17. **Python-dotenv** 🔐
- Gestion des variables d'environnement
- Configuration sécurisée
- Support des fichiers .env
- Séparation des configurations

---

## 📊 Architecture du Projet

### **Version Simplifiée (Sans Docker) - RECOMMANDÉ**

```
┌─────────────────────┐
│   Producer          │ → Génère des transactions synthétiques
│   (Python)          │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   Fichier JSONL     │ → Stockage temporaire des transactions
│   (data/queue/)     │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   ETL Script        │ → Transformation des données
│   (Python)          │   - Validation
│                     │   - Enrichissement
│                     │   - Nettoyage
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   SQLite DB         │ → Stockage des données
│   (data/)           │   - raw_transactions
│                     │   - transactions_flat
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   Streamlit         │ → Visualisation et analyse
│   Dashboard         │   - Graphiques
│                     │   - Filtres
│                     │   - Export CSV
└─────────────────────┘
```

### **Version Complète (Avec Docker)**

```
┌─────────────────────┐
│   Producer          │ → Génère des transactions synthétiques
│   (Python)          │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   Kafka             │ → Messagerie distribuée
│   + Zookeeper       │   - Topics
│   (Docker)          │   - Partitions
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   Airflow           │ → Orchestration ETL
│   (DAGs)            │   - Planification
│   (Docker)          │   - Surveillance
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   PostgreSQL        │ → Base de données
│   (Docker)          │   - raw_transactions
│                     │   - transactions_flat
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   Streamlit         │ → Visualisation et analyse
│   Dashboard         │   - Graphiques
│                     │   - Filtres
│                     │   - Export CSV
└─────────────────────┘
```

---

## 🎓 Compétences Développées

### **Techniques** 🔧
- ✅ **Traitement de données** : ETL, transformation, nettoyage
- ✅ **Bases de données** : SQL, SQLite, PostgreSQL
- ✅ **Streaming de données** : Kafka, messages en temps réel
- ✅ **Orchestration** : Airflow, DAGs, workflows
- ✅ **Visualisation** : Streamlit, graphiques, dashboards
- ✅ **Déploiement** : Docker, Streamlit Cloud, GitHub

### **Concepts** 💡
- ✅ **Pipeline de données** : Flux de données de bout-en-bout
- ✅ **Temps réel** : Traitement en streaming
- ✅ **Micro-batch** : Traitement par lots
- ✅ **Data Quality** : Validation et nettoyage des données
- ✅ **Data Warehousing** : Stockage et organisation des données
- ✅ **Business Intelligence** : Analyse et visualisation

---

## 📈 Fonctionnalités Principales

### **1. Génération de Données** 📝
- ✅ Transactions synthétiques réalistes
- ✅ Multiples catégories (grocery, electronics, travel, etc.)
- ✅ Différents marchands (Amazon, Uber, Carrefour, etc.)
- ✅ Différentes villes (Paris, Lyon, Marseille, etc.)
- ✅ Statuts variés (APPROVED, DECLINED, PENDING, REFUNDED)
- ✅ Montants variables (5€ à 750€)
- ✅ Timestamps réalistes

### **2. Transformation de Données** 🔧
- ✅ Validation des données
- ✅ Enrichissement des données
- ✅ Calcul de métriques (buckets de montants, heures, jours)
- ✅ Extraction de métadonnées
- ✅ Nettoyage et normalisation

### **3. Visualisation** 📊
- ✅ Dashboard interactif
- ✅ Graphiques en temps réel
- ✅ Filtres avancés (catégorie, ville, statut, montant, date)
- ✅ Métriques clés (total, moyenne, approuvées)
- ✅ Export de données (CSV)

### **4. Analyse** 📈
- ✅ Analyse par catégorie
- ✅ Analyse par ville
- ✅ Analyse par marchand
- ✅ Analyse par statut
- ✅ Analyse par période
- ✅ Top 10 marchands
- ✅ Tendances temporelles

---

## 🌟 Points Forts du Projet

### **1. Flexibilité** 🔄
- ✅ Version simplifiée (sans Docker) - **RECOMMANDÉ**
- ✅ Version complète (avec Docker)
- ✅ Déploiement local ou cloud
- ✅ Support de multiples bases de données (SQLite, PostgreSQL)

### **2. Facilité d'Utilisation** 🎯
- ✅ Interface utilisateur intuitive
- ✅ Scripts en ligne de commande
- ✅ Documentation complète
- ✅ Exemples et guides

### **3. Scalabilité** 📈
- ✅ Support de grandes quantités de données
- ✅ Traitement par lots
- ✅ Optimisation des requêtes
- ✅ Index sur les colonnes importantes

### **4. Extensibilité** 🔧
- ✅ Architecture modulaire
- ✅ Facile à étendre
- ✅ Support de nouvelles fonctionnalités
- ✅ Intégration avec d'autres outils

---

## 🚀 Démarrage Rapide

### **Version Simplifiée (Sans Docker) - RECOMMANDÉ**

```powershell
# 1. Installer les dépendances
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-simple.txt

# 2. Créer la base de données et générer des données
python create_database.py

# 3. Lancer le dashboard
streamlit run streamlit_app.py
```

### **Version Complète (Avec Docker)**

```bash
# 1. Démarrer l'écosystème
docker compose up -d

# 2. Activer le DAG dans Airflow UI (http://localhost:8080)

# 3. Produire des événements
python producer/producer.py --rows 10000 --rate 100

# 4. Visualiser
streamlit run analytics/streamlit_dashboard.py
```

---

## 📚 Ressources

### **Documentation** 📖
- [README.md](README.md) - Documentation principale
- [GUIDE-ANALYSE-NOUVELLE-BD.md](GUIDE-ANALYSE-NOUVELLE-BD.md) - Guide d'analyse
- [QUICKSTART.md](QUICKSTART.md) - Démarrage rapide
- [DEPLOY.md](DEPLOY.md) - Guide de déploiement
- [AMELIORATIONS-PROJET.md](AMELIORATIONS-PROJET.md) - Améliorations

### **Code Source** 💻
- **GitHub Repository**: https://github.com/Nedim7050/data-pipeline-streaming
- **Streamlit Cloud**: https://streamlit.io/cloud

### **Technologies** 🛠️
- [Python](https://www.python.org/) - Langage de programmation
- [Streamlit](https://streamlit.io/) - Framework de visualisation
- [Kafka](https://kafka.apache.org/) - Messagerie distribuée
- [Airflow](https://airflow.apache.org/) - Orchestration
- [PostgreSQL](https://www.postgresql.org/) - Base de données
- [SQLite](https://www.sqlite.org/) - Base de données légère

---

## 🎉 Conclusion

**Data Pipeline Streaming** est un projet complet qui démontre les concepts essentiels du traitement de données modernes. Il combine des technologies puissantes pour créer un pipeline de données fonctionnel, de la génération à la visualisation.

### **Pourquoi ce projet ?**
- ✅ **Apprendre** : Comprendre les pipelines de données
- ✅ **Démontrer** : Montrer des compétences techniques
- ✅ **Prototyper** : Tester rapidement des idées
- ✅ **Analyser** : Analyser des données financières

### **Qui peut l'utiliser ?**
- 📚 **Étudiants** : Apprentissage des concepts
- 💼 **Développeurs** : Démonstration de compétences
- 🔧 **Data Engineers** : Exemple de pipeline
- 📊 **Analystes** : Analyse de données

---

**🚀 Prêt à commencer ?** Consultez le [README.md](README.md) pour les instructions de démarrage !

**📊 Voir le projet en action :** Déployez sur [Streamlit Cloud](https://streamlit.io/cloud) pour une démonstration live !

---

*Dernière mise à jour : Décembre 2024*
