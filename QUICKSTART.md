# 🚀 Démarrage Rapide

## Installation Locale

```bash
# 1. Installer les dépendances
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate    # Linux/Mac
pip install -r requirements-simple.txt

# 2. Créer la base de données
python create_database.py

# 3. Lancer le dashboard
streamlit run dashboard_working.py
```

## Déployer sur GitHub

```bash
# 1. Initialiser Git
git init

# 2. Ajouter les fichiers
git add .

# 3. Commit
git commit -m "Initial commit"

# 4. Créer un repository sur GitHub et pousser
git remote add origin https://github.com/VOTRE-USERNAME/data-pipeline-streaming.git
git branch -M main
git push -u origin main
```

## Déployer sur Streamlit Cloud

1. **Aller sur [Streamlit Cloud](https://streamlit.io/cloud)**
2. **Se connecter avec GitHub**
3. **Cliquer sur "New app"**
4. **Sélectionner votre repository**
5. **Main file:** `streamlit_app.py`
6. **Python version:** `3.11`
7. **Cliquer sur "Deploy!"**

Voir [DEPLOY.md](DEPLOY.md) ou [GITHUB-DEPLOY.md](GITHUB-DEPLOY.md) pour plus de détails.

