# 🚀 Guide de Démarrage Rapide - Windows (Sans Docker)

Bienvenue ! Ce guide vous permet de démarrer votre pipeline de données **sans installer Docker**.

## ⚡ Démarrage en 5 Minutes

### Étape 1 : Installer Python (si pas déjà fait)

1. Télécharger Python 3.11+ depuis https://www.python.org/downloads/
2. **Important** : Cocher "Add Python to PATH" lors de l'installation
3. Vérifier l'installation :
   ```powershell
   python --version
   ```

### Étape 2 : Installer les Dépendances

#### Option A : Installation Automatique (Recommandé)

```powershell
# Utiliser le script d'installation automatique
.\scripts\install_windows.ps1
```

#### Option B : Installation Manuelle

**Si vous utilisez Python 3.11 ou 3.12** (recommandé) :
```powershell
# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement virtuel
.\.venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements-simple.txt
```

**Si vous utilisez Python 3.14 alpha** :
```powershell
# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement virtuel
.\.venv\Scripts\Activate.ps1

# Installer Pillow et PyArrow d'abord (binaires pour Python 3.14)
pip install --upgrade pip
pip install pillow --upgrade --only-binary :all:
pip install pyarrow --only-binary :all: --no-deps

# Installer les autres dépendances
pip install sqlalchemy pandas streamlit python-dotenv click tqdm altair greenlet --no-deps
pip install altair blinker cachetools packaging protobuf requests tenacity toml typing-extensions watchdog gitpython pydeck tornado numpy python-dateutil pytz tzdata colorama jinja2 jsonschema narwhals gitdb six charset-normalizer idna urllib3 certifi smmap markupsafe attrs jsonschema-specifications referencing rpds-py mdurl pygments
pip install greenlet "altair<6,>=4.0"
```

💡 **Note** : Si vous utilisez Python 3.14 alpha, vous devrez peut-être installer certaines dépendances manuellement. Consultez la section "Problèmes Courants" ci-dessous.

### Étape 3 : Tester l'Installation

```powershell
# Exécuter les tests
python scripts/test_simple.py
```

Ou utiliser le script PowerShell :
```powershell
.\scripts\test_simple.ps1
```

### Étape 4 : Générer des Données

```powershell
python producer/producer_to_file.py --rows 10000 --rate 100
```

Cela génère 10 000 transactions dans `data/queue/transactions.jsonl`.

### Étape 5 : Traiter les Données

**✅ Solution Simple (Recommandé)**

```powershell
python create_database.py
```

Ce script va créer la base de données et insérer les données automatiquement.

**Option B: Utiliser le Consumer Directement**

```powershell
python consumers/file_queue_to_sqlite.py --input data/queue/transactions.jsonl --db data/transactions.db --batch-size 500
```

### Étape 6 : Visualiser avec Streamlit

```powershell
streamlit run analytics/streamlit_dashboard_sqlite.py
```

Ouvrez http://localhost:8501 dans votre navigateur.

## 🎯 Workflow Complet

### Option A : Traitement Manuel

1. **Générer des données** :
   ```powershell
   python producer/producer_to_file.py --rows 10000 --rate 100
   ```

2. **Traiter les données** :
   ```powershell
   python consumers/file_queue_to_sqlite.py --input data/queue/transactions.jsonl --db data/transactions.db
   ```

3. **Visualiser** :
   ```powershell
   streamlit run analytics/streamlit_dashboard_sqlite.py
   ```

### Option B : Traitement Automatique (Scheduler)

Pour traiter automatiquement les données toutes les 30 secondes :

```powershell
python scripts/run_simple_etl.py data/queue/transactions.jsonl data/transactions.db 500 30
```

Dans un autre terminal, générez des données en continu :

```powershell
python producer/producer_to_file.py --rows 0 --rate 50
```

## 📊 Fonctionnalités du Dashboard

Le dashboard Streamlit affiche :
- ✅ Dernières transactions
- ✅ Volume horaire (graphiques)
- ✅ Top marchands
- ✅ Heatmap Ville vs Catégorie
- ✅ Export CSV pour PowerBI/Tableau

## 🔧 Configuration

Vous pouvez modifier les chemins par défaut via des variables d'environnement :

```powershell
$env:SQLITE_DB_PATH = "data/transactions.db"
$env:INPUT_FILE = "data/queue/transactions.jsonl"
```

## 📁 Structure des Fichiers

```
data/
├── queue/
│   └── transactions.jsonl    # Fichier d'entrée (simule Kafka)
└── transactions.db            # Base SQLite (simule Postgres)
```

## 🆘 Résolution de Problèmes

### Erreur : "Python n'est pas reconnu"
- Vérifier que Python est installé
- Vérifier que Python est dans le PATH
- Redémarrer PowerShell

### Erreur : "Module not found"
- Activer l'environnement virtuel : `.\.venv\Scripts\Activate.ps1`
- Installer les dépendances : `pip install -r requirements-simple.txt`

### Erreur : "Permission denied"
- Exécuter PowerShell en tant qu'administrateur
- Vérifier les permissions du dossier `data/`

### Dashboard ne charge pas
- Vérifier que la base SQLite existe : `data/transactions.db`
- Vérifier que des données ont été traitées
- Vérifier les logs dans la console

## 📚 Ressources

- [QUICKSTART.md](QUICKSTART.md) - Démarrage rapide
- [DEPLOY.md](DEPLOY.md) - Guide de déploiement
- [README.md](README.md) - Documentation complète du projet

## 🎉 Prochaines Étapes

1. ✅ Tester la version simplifiée localement
2. 🔄 Explorer le dashboard Streamlit
3. ☁️ Déployer sur Streamlit Cloud (voir [DEPLOY.md](DEPLOY.md))
4. 🚀 Passer à la version complète avec Docker (voir [README.md](README.md))

## 💡 Conseils

- **Générer plus de données** : Augmentez `--rows` pour plus de transactions
- **Traiter en continu** : Utilisez `scripts/run_simple_etl.py` avec un intervalle court
- **Exporter les données** : Utilisez le bouton "Export CSV" dans le dashboard
- **Explorer les données** : Utilisez le notebook `notebooks/exploration.ipynb`

---

**Besoin d'aide ?** Consultez les autres fichiers README ou ouvrez une issue sur GitHub.


