# 🚀 Guide Simple - Création de la Base de Données

## ✅ Solution en 3 Étapes

### Étape 1: Générer des Données

```powershell
# Activer l'environnement virtuel
.\.venv\Scripts\Activate.ps1

# Générer des données
python producer/producer_to_file.py --rows 200 --rate 50
```

### Étape 2: Créer la Base de Données et Traiter les Données

**✅ Solution Simple (Recommandé)**

```powershell
# Activer l'environnement virtuel
.\.venv\Scripts\Activate.ps1

# Créer la base de données (script simple qui fonctionne)
python create_database.py
```

Ce script va:
- Créer la base de données SQLite
- Créer les tables nécessaires
- Lire les données depuis le fichier JSONL
- Insérer les données dans la base
- Vérifier que tout fonctionne

**Option B: Utiliser le Consumer Directement**

```powershell
# Supprimer la base existante (si elle existe)
Remove-Item "data/transactions.db" -ErrorAction SilentlyContinue

# Créer et traiter avec le consumer
python consumers/file_queue_to_sqlite.py --input data/queue/transactions.jsonl --db data/transactions.db --batch-size 500
```

### Étape 3: Vérifier la Base de Données

```powershell
python scripts/check_db.py
```

Vous devriez voir:
```
✅ Base de données trouvée: data\transactions.db
✅ Tables trouvées: ['raw_transactions', 'transactions_flat']
✅ Nombre de transactions dans transactions_flat: 200
```

### Étape 4: Lancer Streamlit

```powershell
streamlit run analytics/streamlit_dashboard_sqlite.py
```

Ouvrez http://localhost:8501 dans votre navigateur.

## 🐛 Dépannage

### Erreur: "Base de données vide"

**Solution**: Vérifiez que le fichier de transactions contient des données:
```powershell
# Vérifier le fichier
if (Test-Path "data/queue/transactions.jsonl") {
    $size = (Get-Item "data/queue/transactions.jsonl").Length
    Write-Host "Fichier trouve: $size bytes"
} else {
    Write-Host "Fichier non trouve, generation..."
    python producer/producer_to_file.py --rows 200 --rate 50
}
```

### Erreur: "Connection error" dans Streamlit

**Solution**: 
1. Vérifiez que la base existe: `python scripts/check_db.py`
2. Vérifiez que des données ont été traitées
3. Relancez Streamlit: `streamlit run analytics/streamlit_dashboard_sqlite.py`

## 📚 Documentation

- **[START-HERE.md](START-HERE.md)** - Guide de démarrage complet
- **[QUICKSTART.md](QUICKSTART.md)** - Démarrage rapide
- **[DEPLOY.md](DEPLOY.md)** - Guide de déploiement

