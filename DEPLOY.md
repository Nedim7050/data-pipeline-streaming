# 🚀 Guide de Déploiement - GitHub et Streamlit Cloud

## 📋 Prérequis

- Compte GitHub
- Compte Streamlit Cloud (gratuit)
- Git installé sur votre machine

## 🔧 Étape 1: Nettoyer le Projet

Les fichiers inutiles ont été nettoyés. Le projet est prêt pour GitHub.

## 📤 Étape 2: Pousser vers GitHub

### 2.1. Initialiser Git

```bash
# Initialiser Git (si pas déjà fait)
git init

# Vérifier le statut
git status
```

### 2.2. Créer un Repository sur GitHub

1. **Aller sur [GitHub](https://github.com)**
2. **Cliquer sur "New repository"**
3. **Remplir les informations:**
   - **Repository name:** `data-pipeline-streaming`
   - **Description:** `Data pipeline with Kafka, Airflow, Postgres, and Streamlit`
   - **Visibility:** Public ou Private
   - **Ne PAS** initialiser avec README, .gitignore, ou license (on a déjà tout)
4. **Cliquer sur "Create repository"**

### 2.3. Pousser le Code

```bash
# Ajouter tous les fichiers
git add .

# Commit
git commit -m "Initial commit: Data pipeline with Streamlit dashboard"

# Ajouter le remote (remplacez par votre URL)
git remote add origin https://github.com/votre-username/data-pipeline-streaming.git

# Pousser vers GitHub
git branch -M main
git push -u origin main
```

## 🌐 Étape 3: Déployer sur Streamlit Cloud

### 3.1. Créer un Compte Streamlit Cloud

1. **Aller sur [Streamlit Cloud](https://streamlit.io/cloud)**
2. **Cliquer sur "Sign up"**
3. **Se connecter avec GitHub**
4. **Autoriser Streamlit Cloud à accéder à vos repositories**

### 3.2. Déployer l'Application

1. **Cliquer sur "New app"**
2. **Remplir les informations:**
   - **Repository:** Sélectionner `votre-username/data-pipeline-streaming`
   - **Branch:** `main`
   - **Main file:** `streamlit_app.py` (recommandé) ou `dashboard_working.py`
   - **Python version:** `3.11`
3. **Cliquer sur "Deploy!"**

**Note:** `streamlit_app.py` est recommandé car il gère automatiquement la création de la base de données avec un bouton dans l'interface.

### 3.3. Configuration (Optionnel)

Si vous avez besoin de variables d'environnement:

1. **Aller dans "Settings" de votre app**
2. **Cliquer sur "Secrets"**
3. **Ajouter vos variables d'environnement:**
   ```toml
   SQLITE_DB_PATH = "data/transactions.db"
   ```

## 🔧 Étape 4: Adapter pour Streamlit Cloud

### 4.1. Créer un Dashboard pour Streamlit Cloud

Le fichier `dashboard_working.py` est déjà adapté pour Streamlit Cloud.

### 4.2. Générer des Données (Optionnel)

Si vous voulez générer des données dans Streamlit Cloud:

1. **Créer un script d'initialisation:**
   ```python
   # scripts/init_streamlit_cloud.py
   from producer.producer_to_file import produce_transactions_to_file
   from pathlib import Path
   
   # Générer des données
   output_file = Path("data/queue/transactions.jsonl")
   output_file.parent.mkdir(parents=True, exist_ok=True)
   produce_transactions_to_file(rows=1000, rate=50, output_file=output_file)
   ```

2. **Appeler ce script dans le dashboard:**
   ```python
   # Dans dashboard_working.py
   if not db_path.exists():
       # Générer des données
       import subprocess
       subprocess.run(["python", "create_database.py"])
   ```

## ✅ Vérification

### Vérifier le Déploiement

1. **Aller sur votre app Streamlit Cloud**
2. **Vérifier que le dashboard s'affiche**
3. **Vérifier que les données sont chargées**

### Vérifier GitHub

1. **Aller sur votre repository GitHub**
2. **Vérifier que tous les fichiers sont présents**
3. **Vérifier que le README.md est à jour**

## 🐛 Dépannage

### Problème: "Module not found"

**Solution:** Vérifier que `requirements.txt` ou `requirements-simple.txt` contient toutes les dépendances.

### Problème: "Database not found"

**Solution:** Vérifier que la base de données est créée ou générer des données.

### Problème: "Streamlit app not found"

**Solution:** Vérifier que le fichier principal est `dashboard_working.py` ou configurer le bon fichier dans Streamlit Cloud.

## 📚 Ressources

- [Documentation Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Documentation GitHub](https://docs.github.com)
- [Documentation Git](https://git-scm.com/doc)

## 🎉 Félicitations!

Votre application est maintenant déployée sur Streamlit Cloud et accessible à tous!

