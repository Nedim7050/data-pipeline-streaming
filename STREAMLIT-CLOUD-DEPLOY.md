# 🌐 Déployer sur Streamlit Cloud

## ✅ Étape 1: Vérifier GitHub

Votre projet est maintenant sur GitHub:
- **URL:** https://github.com/Nedim7050/data-pipeline-streaming
- **Branche:** `main`
- **Fichiers:** 41 fichiers poussés avec succès

## 🚀 Étape 2: Déployer sur Streamlit Cloud

### 2.1. Créer un Compte Streamlit Cloud

1. **Aller sur [Streamlit Cloud](https://streamlit.io/cloud)**
2. **Cliquer sur "Sign up"**
3. **Se connecter avec GitHub**
4. **Autoriser Streamlit Cloud à accéder à vos repositories**

### 2.2. Déployer l'Application

1. **Cliquer sur "New app"**
2. **Remplir les informations:**
   - **Repository:** `Nedim7050/data-pipeline-streaming`
   - **Branch:** `main`
   - **Main file:** `streamlit_app.py` (recommandé)
   - **Python version:** `3.11`
3. **Cliquer sur "Deploy!"**

### 2.3. Attendre le Déploiement

Le déploiement peut prendre 2-3 minutes. Vous verrez:
- ✅ "Building app..."
- ✅ "App is ready!"
- ✅ URL de votre application

## 🔧 Étape 3: Configuration (Optionnel)

### Variables d'environnement

Si vous avez besoin de variables d'environnement:

1. **Aller dans "Settings" de votre app**
2. **Cliquer sur "Secrets"**
3. **Ajouter vos variables d'environnement:**
   ```toml
   SQLITE_DB_PATH = "data/transactions.db"
   ```

## ✅ Étape 4: Vérifier le Déploiement

1. **Aller sur votre app Streamlit Cloud**
2. **Vérifier que le dashboard s'affiche**
3. **Si la base de données n'existe pas, cliquer sur le bouton "Créer la base de données"**
4. **Vérifier que les données sont chargées**

## 🐛 Dépannage

### Problème: "Module not found"

**Solution:** Vérifier que `requirements.txt` contient toutes les dépendances nécessaires.

### Problème: "Database not found"

**Solution:** Cliquer sur le bouton "Créer la base de données" dans le dashboard.

### Problème: "Streamlit app not found"

**Solution:** Vérifier que le fichier principal est `streamlit_app.py` dans les settings de Streamlit Cloud.

## 📚 Ressources

- [Documentation Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Documentation GitHub](https://docs.github.com)

## 🎉 Félicitations!

Votre application est maintenant déployée sur Streamlit Cloud!

**URL de votre application:** `https://votre-app-name.streamlit.app`

