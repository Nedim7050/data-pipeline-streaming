# Script d'installation automatique pour Windows (Python 3.14)

Write-Host "🚀 Installation de data-pipeline-streaming pour Windows..." -ForegroundColor Green
Write-Host ""

# Vérifier Python
Write-Host "1. Vérification de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✅ Python détecté: $pythonVersion" -ForegroundColor Green
    
    if ($pythonVersion -match "Python 3\.14") {
        Write-Host "   ⚠️  Python 3.14 alpha détecté - installation spéciale requise" -ForegroundColor Yellow
        $useSpecialInstall = $true
    } else {
        Write-Host "   ✅ Version Python stable détectée" -ForegroundColor Green
        $useSpecialInstall = $false
    }
} catch {
    Write-Host "   ❌ Python n'est pas installé ou n'est pas dans le PATH" -ForegroundColor Red
    exit 1
}

# Créer l'environnement virtuel
Write-Host ""
Write-Host "2. Création de l'environnement virtuel..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "   ⚠️  Environnement virtuel existe déjà" -ForegroundColor Yellow
} else {
    python -m venv .venv
    Write-Host "   ✅ Environnement virtuel créé" -ForegroundColor Green
}

# Activer l'environnement virtuel
Write-Host ""
Write-Host "3. Activation de l'environnement virtuel..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "   ✅ Environnement virtuel activé" -ForegroundColor Green

# Mettre à jour pip
Write-Host ""
Write-Host "4. Mise à jour de pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
Write-Host "   ✅ pip mis à jour" -ForegroundColor Green

# Installer les dépendances
Write-Host ""
Write-Host "5. Installation des dépendances..." -ForegroundColor Yellow

if ($useSpecialInstall) {
    Write-Host "   Installation spéciale pour Python 3.14..." -ForegroundColor Cyan
    
    # Installer Pillow et PyArrow d'abord
    Write-Host "   - Installation de Pillow..." -ForegroundColor White
    pip install pillow --upgrade --only-binary :all: 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "     ✅ Pillow installé" -ForegroundColor Green
    } else {
        Write-Host "     ❌ Erreur lors de l'installation de Pillow" -ForegroundColor Red
    }
    
    Write-Host "   - Installation de PyArrow..." -ForegroundColor White
    pip install pyarrow --only-binary :all: --no-deps 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "     ✅ PyArrow installé" -ForegroundColor Green
    } else {
        Write-Host "     ❌ Erreur lors de l'installation de PyArrow" -ForegroundColor Red
    }
    
    # Installer les autres dépendances
    Write-Host "   - Installation des autres dépendances..." -ForegroundColor White
    pip install sqlalchemy pandas streamlit python-dotenv click tqdm altair greenlet --no-deps 2>&1 | Out-Null
    pip install altair blinker cachetools packaging protobuf requests tenacity toml typing-extensions watchdog gitpython pydeck tornado numpy python-dateutil pytz tzdata colorama jinja2 jsonschema narwhals gitdb six charset-normalizer idna urllib3 certifi smmap markupsafe attrs jsonschema-specifications referencing rpds-py mdurl pygments 2>&1 | Out-Null
    pip install greenlet "altair<6,>=4.0" 2>&1 | Out-Null
    
} else {
    Write-Host "   Installation standard..." -ForegroundColor Cyan
    pip install -r requirements-simple.txt 2>&1 | Out-Null
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Dépendances installées" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Certaines dépendances peuvent avoir des problèmes" -ForegroundColor Yellow
    Write-Host "   💡 Consultez INSTALL-WINDOWS.md pour plus d'informations" -ForegroundColor Cyan
}

# Vérifier l'installation
Write-Host ""
Write-Host "6. Vérification de l'installation..." -ForegroundColor Yellow
try {
    python -c "import streamlit; import pandas; import sqlalchemy; print('OK')" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Installation réussie!" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Erreur lors de la vérification" -ForegroundColor Red
    }
} catch {
    Write-Host "   ❌ Erreur lors de la vérification" -ForegroundColor Red
}

# Résumé
Write-Host ""
Write-Host "✅ Installation terminée!" -ForegroundColor Green
Write-Host ""
Write-Host "📚 Prochaines étapes:" -ForegroundColor Cyan
Write-Host "   1. Générer des données: python producer/producer_to_file.py --rows 100" -ForegroundColor White
Write-Host "   2. Traiter les données: python consumers/file_queue_to_sqlite.py" -ForegroundColor White
Write-Host "   3. Lancer le dashboard: streamlit run analytics/streamlit_dashboard_sqlite.py" -ForegroundColor White
Write-Host ""
Write-Host "💡 Pour plus d'informations, consultez START-HERE.md" -ForegroundColor Cyan

