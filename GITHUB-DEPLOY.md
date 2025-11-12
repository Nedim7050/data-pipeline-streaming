# 🚀 Guide Complet - Déployer sur GitHub et Streamlit Cloud

## 📋 Prérequis

- Compte GitHub (gratuit)
- Compte Streamlit Cloud (gratuit)
- Git installé sur votre machine

## 🧹 Étape 1: Vérifier le Nettoyage

Les fichiers inutiles ont été nettoyés. Vérifiez que vous avez seulement:

### Fichiers de Documentation
- ✅ README.md
- ✅ PRESENTATION.md
- ✅ DEPLOY.md
- ✅ START-HERE.md
- ✅ GUIDE-SIMPLE.md
- ✅ QUICKSTART.md
- ✅ LICENSE

### Fichiers de Code
- ✅ producer/
- ✅ consumers/
- ✅ analytics/
- ✅ airflow_dags/
- ✅ scripts/
- ✅ sql/
- ✅ docker/
- ✅ notebooks/

### Fichiers de Configuration
- ✅ requirements.txt
- ✅ requirements-simple.txt
- ✅ .gitignore
- ✅ .streamlit/config.toml
- ✅ docker-compose.yml
- ✅ Makefile

### Scripts Principaux
- ✅ create_database.py
- ✅ dashboard_working.py
- ✅ streamlit_app.py

## 📤 Étape 2: Initialiser Git

```bash
# Initialiser Git (si pas déjà fait)
git init

# Vérifier le statut
git status
```

## 📦 Étape 3: Créer un Repository sur GitHub

1. **Aller sur [GitHub](https://github.com)**
2. **Cliquer sur "New repository" (ou le bouton + en haut à droite)**
3. **Remplir les informations:**
   - **Repository name:** `data-pipeline-streaming`
   - **Description:** `Data pipeline with Kafka, Airflow, Postgres, and Streamlit`
   - **Visibility:** Public (recommandé pour Streamlit Cloud) ou Private
   - **Ne PAS** cocher "Add a README file" (on a déjà README.md)
   - **Ne PAS** cocher "Add .gitignore" (on a déjà .gitignore)
   - **Ne PAS** cocher "Choose a license" (on a déjà LICENSE)
4. **Cliquer sur "Create repository"**

## 🚀 Étape 4: Pousser le Code vers GitHub

```bash
# 1. Ajouter tous les fichiers
git add .

# 2. Commit
git commit -m "Initial commit: Data pipeline with Streamlit dashboard"

# 3. Ajouter le remote (remplacez VOTRE-USERNAME par votre nom d'utilisateur GitHub)
git remote add origin https://github.com/VOTRE-USERNAME/data-pipeline-streaming.git

# 4. Renommer la branche en main (si nécessaire)
git branch -M main

# 5. Pousser vers GitHub
git push -u origin main
```

**Note:** Si vous avez déjà un remote, utilisez:
```bash
git remote set-url origin https://github.com/VOTRE-USERNAME/data-pipeline-streaming.git
```

## 🌐 Étape 5: Déployer sur Streamlit Cloud

### 5.1. Créer un Compte Streamlit Cloud

1. **Aller sur [Streamlit Cloud](https://streamlit.io/cloud)**
2. **Cliquer sur "Sign up"**
3. **Se connecter avec GitHub**
4. **Autoriser Streamlit Cloud à accéder à vos repositories**

### 5.2. Déployer l'Application

1. **Cliquer sur "New app"**
2. **Remplir les informations:**
   - **Repository:** Sélectionner `VOTRE-USERNAME/data-pipeline-streaming`
   - **Branch:** `main`
   - **Main file:** `dashboard_working.py` ou `streamlit_app.py`
   - **Python version:** `3.11`
3. **Cliquer sur "Deploy!"**

### 5.3. Configuration (Optionnel)

Si vous avez besoin de variables d'environnement:

1. **Aller dans "Settings" de votre app**
2. **Cliquer sur "Secrets"**
3. **Ajouter vos variables d'environnement:**
   ```toml
   SQLITE_DB_PATH = "data/transactions.db"
   ```

## ✅ Étape 6: Vérifier le Déploiement

### Vérifier GitHub

1. **Aller sur votre repository GitHub:** `https://github.com/VOTRE-USERNAME/data-pipeline-streaming`
2. **Vérifier que tous les fichiers sont présents**
3. **Vérifier que le README.md s'affiche correctement**

### Vérifier Streamlit Cloud

1. **Aller sur votre app Streamlit Cloud**
2. **Vérifier que le dashboard s'affiche**
3. **Vérifier que les données sont chargées**

**Note:** Si la base de données n'existe pas, le dashboard affichera un bouton pour créer la base de données.

## 🔧 Étape 7: Générer des Données (Si Nécessaire)

Si vous voulez générer des données dans Streamlit Cloud:

1. **Le dashboard affiche un bouton "Créer la base de données"**
2. **Cliquez sur le bouton**
3. **Attendez que la base de données soit créée**
4. **Rafraîchissez la page**

## 🐛 Dépannage

### Problème: "Module not found"

**Solution:** Vérifier que `requirements.txt` contient toutes les dépendances nécessaires.

### Problème: "Database not found"

**Solution:** Cliquer sur le bouton "Créer la base de données" dans le dashboard.

### Problème: "Streamlit app not found"

**Solution:** Vérifier que le fichier principal est `dashboard_working.py` ou `streamlit_app.py` dans les settings de Streamlit Cloud.

### Problème: "Git push rejected"

**Solution:** 
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## 📚 Ressources

- [Documentation Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Documentation GitHub](https://docs.github.com)
- [Documentation Git](https://git-scm.com/doc)

## 🎉 Félicitations!

Votre application est maintenant déployée sur GitHub et Streamlit Cloud!

**Votre application Streamlit Cloud est accessible à l'URL:**
`https://VOTRE-APP-NAME.streamlit.app`

