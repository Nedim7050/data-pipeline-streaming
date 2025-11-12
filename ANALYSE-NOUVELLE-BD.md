# 📊 Comment Analyser une Nouvelle Base de Données

## 🎯 Objectif

Ce guide vous explique comment créer et analyser une nouvelle base de données avec plus ou moins de transactions.

## 🔄 Option 1: Créer une Nouvelle Base de Données (Local)

### Méthode 1: Utiliser le Script Python

```powershell
# Activer l'environnement virtuel
.\.venv\Scripts\Activate.ps1

# Créer une nouvelle base de données avec 1000 transactions
python load_new_database.py --rows 1000 --reset

# Créer une nouvelle base de données avec 5000 transactions
python load_new_database.py --rows 5000 --reset

# Créer une nouvelle base de données dans un fichier spécifique
python load_new_database.py --rows 2000 --db data/my_new_database.db --reset
```

### Méthode 2: Utiliser create_database.py Directement

```powershell
# Activer l'environnement virtuel
.\.venv\Scripts\Activate.ps1

# Créer une nouvelle base de données avec 1000 transactions
python -c "from create_database import main; from pathlib import Path; main(rows=1000, db_path=Path('data/transactions.db'))"
```

### Méthode 3: Utiliser le Dashboard Streamlit

1. **Lancer le dashboard:**
   ```powershell
   streamlit run streamlit_app.py
   ```

2. **Dans la sidebar, cliquer sur "🔄 Créer la base de données"**
   - Cela créera une base de données avec 500 transactions par défaut

3. **Pour générer plus de données:**
   - Cliquer sur "➕ Générer 500 transactions" dans la sidebar
   - Cela ajoutera 500 transactions supplémentaires

## 🔄 Option 2: Utiliser une Base de Données Existante

### Méthode 1: Remplacer la Base de Données

```powershell
# Supprimer l'ancienne base de données
Remove-Item data/transactions.db -ErrorAction SilentlyContinue

# Créer une nouvelle base de données
python load_new_database.py --rows 2000 --reset
```

### Méthode 2: Utiliser une Autre Base de Données

1. **Créer une nouvelle base de données:**
   ```powershell
   python load_new_database.py --rows 3000 --db data/my_analysis.db --reset
   ```

2. **Modifier streamlit_app.py pour utiliser cette base:**
   ```python
   # Dans streamlit_app.py, changer:
   db_path = project_root / "data" / "my_analysis.db"
   ```

## 📊 Option 3: Analyser les Données avec Filtres

Le dashboard Streamlit permet d'analyser les données avec des filtres:

1. **Lancer le dashboard:**
   ```powershell
   streamlit run streamlit_app.py
   ```

2. **Utiliser les filtres dans la sidebar:**
   - **Nombre de transactions:** Slider pour limiter le nombre de transactions affichées
   - **Période:** Sélectionner une plage de dates
   - **Catégories:** Sélectionner des catégories spécifiques
   - **Villes:** Sélectionner des villes spécifiques
   - **Statuts:** Sélectionner des statuts spécifiques
   - **Montant:** Sélectionner une plage de montants

3. **Visualiser les résultats:**
   - Les graphiques se mettent à jour automatiquement
   - Le tableau affiche les transactions filtrées
   - Les métriques sont calculées sur les données filtrées

## 🔧 Option 4: Créer une Base de Données Personnalisée

### Créer un Script Personnalisé

```python
# my_custom_analysis.py
from create_database import main as create_db
from pathlib import Path

# Créer une base de données avec 5000 transactions
db_path = Path("data/my_custom_analysis.db")
success = create_db(rows=5000, db_path=db_path)

if success:
    print(f"✅ Base de données créée: {db_path}")
    print("Pour analyser cette base, modifiez streamlit_app.py pour utiliser ce chemin")
else:
    print("❌ Échec de la création")
```

## 📊 Option 5: Analyser les Données avec Pandas

### Script d'Analyse Python

```python
# analyze_data.py
import sqlite3
import pandas as pd
from pathlib import Path

# Connexion à la base de données
db_path = Path("data/transactions.db")
conn = sqlite3.connect(str(db_path))

# Charger les données
df = pd.read_sql("SELECT * FROM transactions_flat", conn)
conn.close()

# Analyses
print(f"Total transactions: {len(df)}")
print(f"Montant total: {df['amount'].sum():,.2f} €")
print(f"Montant moyen: {df['amount'].mean():,.2f} €")
print(f"Transactions approuvées: {len(df[df['status'] == 'APPROVED'])}")

# Analyse par catégorie
print("\n📊 Analyse par catégorie:")
print(df.groupby('category')['amount'].sum().sort_values(ascending=False))

# Analyse par ville
print("\n📊 Analyse par ville:")
print(df.groupby('city').size().sort_values(ascending=False))

# Analyse par marchand
print("\n📊 Top 10 marchands:")
print(df.groupby('merchant')['amount'].sum().sort_values(ascending=False).head(10))
```

## 🌐 Option 6: Utiliser sur Streamlit Cloud

### Créer une Nouvelle Base de Données

1. **Dans Streamlit Cloud, utiliser le bouton "🔄 Créer la base de données"**
   - Cela créera une base de données avec 500 transactions

2. **Pour générer plus de données:**
   - Cliquer sur "➕ Générer 500 transactions" dans la sidebar
   - Cela ajoutera 500 transactions supplémentaires

### Modifier le Nombre de Transactions

Pour modifier le nombre de transactions générées:

1. **Modifier streamlit_app.py:**
   ```python
   # Changer le nombre de transactions
   success = create_db(rows=1000, db_path=db_path)  # Au lieu de 500
   ```

2. **Pousser les changements vers GitHub:**
   ```bash
   git add streamlit_app.py
   git commit -m "Increase number of transactions to 1000"
   git push origin main
   ```

3. **Streamlit Cloud redéploiera automatiquement**

## 📚 Exemples d'Analyses

### Analyse 1: Transactions par Catégorie

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/transactions.db")
df = pd.read_sql("SELECT * FROM transactions_flat", conn)
conn.close()

# Analyse par catégorie
category_analysis = df.groupby('category').agg({
    'amount': ['sum', 'mean', 'count'],
    'transaction_id': 'count'
}).round(2)

print(category_analysis)
```

### Analyse 2: Transactions par Ville

```python
# Analyse par ville
city_analysis = df.groupby('city').agg({
    'amount': ['sum', 'mean', 'count'],
    'transaction_id': 'count'
}).round(2)

print(city_analysis)
```

### Analyse 3: Transactions par Statut

```python
# Analyse par statut
status_analysis = df.groupby('status').agg({
    'amount': ['sum', 'mean', 'count'],
    'transaction_id': 'count'
}).round(2)

print(status_analysis)
```

## 🔧 Configuration

### Variables d'Environnement

Vous pouvez configurer le chemin de la base de données via des variables d'environnement:

```powershell
# Windows
$env:SQLITE_DB_PATH = "data/my_database.db"

# Linux/Mac
export SQLITE_DB_PATH="data/my_database.db"
```

### Modifier le Nombre de Transactions par Défaut

Dans `streamlit_app.py`, modifiez:

```python
# Changer de 500 à 1000
success = create_db(rows=1000, db_path=db_path)
```

## 📚 Documentation

- [README.md](README.md) - Documentation principale
- [QUICKSTART.md](QUICKSTART.md) - Démarrage rapide
- [GUIDE-SIMPLE.md](GUIDE-SIMPLE.md) - Guide simple

---

**✅ Vous pouvez maintenant créer et analyser de nouvelles bases de données!**

