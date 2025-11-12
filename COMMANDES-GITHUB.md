# 🚀 Commandes pour Pousser vers GitHub

## 📤 Commandes Complètes

```bash
# 1. Initialiser Git
git init

# 2. Ajouter tous les fichiers
git add .

# 3. Commit
git commit -m "Initial commit: Data pipeline with Streamlit dashboard"

# 4. Créer un repository sur GitHub (via le site web)
# Aller sur https://github.com et créer un nouveau repository

# 5. Ajouter le remote (remplacez VOTRE-USERNAME par votre nom d'utilisateur)
git remote add origin https://github.com/VOTRE-USERNAME/data-pipeline-streaming.git

# 6. Renommer la branche en main
git branch -M main

# 7. Pousser vers GitHub
git push -u origin main
```

## 🔍 Vérification

```bash
# Vérifier le statut
git status

# Vérifier les remotes
git remote -v

# Vérifier les branches
git branch
```

## 🐛 Si Vous Avez des Problèmes

### Problème: "fatal: not a git repository"

**Solution:** 
```bash
git init
```

### Problème: "remote origin already exists"

**Solution:**
```bash
git remote set-url origin https://github.com/VOTRE-USERNAME/data-pipeline-streaming.git
```

### Problème: "git push rejected"

**Solution:**
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## 📚 Ressources

- [Documentation Git](https://git-scm.com/doc)
- [Documentation GitHub](https://docs.github.com)

