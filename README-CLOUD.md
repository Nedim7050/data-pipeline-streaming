# Déploiement sur Services Cloud (Sans Docker Local)

Ce guide vous explique comment déployer votre pipeline sur des services cloud gratuits **sans installer Docker** sur votre machine.

## 🌐 Services Cloud Gratuits Recommandés

### 1. **Postgres** (Base de données)
- **Supabase** : https://supabase.com (gratuit jusqu'à 500MB)
- **Render PostgreSQL** : https://render.com (gratuit, avec limitations)
- **Neon** : https://neon.tech (gratuit, serverless Postgres)
- **Railway PostgreSQL** : https://railway.app (crédits gratuits)

### 2. **Kafka** (Message Queue)
- **Upstash Kafka** : https://upstash.com (gratuit jusqu'à 10K messages/jour)
- **Confluent Cloud** : https://confluent.cloud (essai gratuit 30 jours)
- **Redpanda Cloud** : https://redpanda.com (essai gratuit)

### 3. **Orchestration** (Airflow)
- **Astronomer** : https://astronomer.io (essai gratuit)
- **Google Cloud Composer** : https://cloud.google.com/composer (crédits gratuits)
- **Apache Airflow sur Railway/Render** : Déploiement manuel

### 4. **Dashboard** (Streamlit)
- **Streamlit Cloud** : https://streamlit.io/cloud (gratuit, illimité)

---

## 🚀 Guide de Déploiement Étape par Étape

### Étape 1 : Créer une Base Postgres Cloud

**Exemple avec Supabase :**

1. Créer un compte sur https://supabase.com
2. Créer un nouveau projet
3. Noter les identifiants de connexion :
   - Host: `db.xxxxx.supabase.co`
   - Port: `5432`
   - Database: `postgres`
   - User: `postgres`
   - Password: (généré automatiquement)

4. Exécuter le schéma SQL :
   ```sql
   -- Copier le contenu de sql/schema.sql
   -- L'exécuter dans l'éditeur SQL de Supabase
   ```

**Exemple avec Render :**

1. Créer un compte sur https://render.com
2. Créer une nouvelle "PostgreSQL" database
3. Noter l'URL de connexion interne (format: `postgresql://user:password@host:5432/dbname`)

### Étape 2 : Configurer Kafka Cloud

**Exemple avec Upstash Kafka :**

1. Créer un compte sur https://upstash.com
2. Créer un cluster Kafka (gratuit)
3. Créer un topic `transactions`
4. Noter les identifiants :
   - Bootstrap Server: `xxxxx.upstash.io:9092`
   - Username/Password: (générés automatiquement)

### Étape 3 : Modifier la Configuration

Créez un fichier `.env` avec vos identifiants cloud :

```env
# Postgres Cloud (Supabase, Render, etc.)
POSTGRES_CONN_URI=postgresql+psycopg2://postgres:password@db.xxxxx.supabase.co:5432/postgres

# Kafka Cloud (Upstash, Confluent, etc.)
KAFKA_BOOTSTRAP_SERVER=xxxxx.upstash.io:9092
KAFKA_USERNAME=your_username
KAFKA_PASSWORD=your_password
KAFKA_TOPIC=transactions

# Batch size
BATCH_SIZE=500
```

### Étape 4 : Modifier le Code pour Kafka Cloud

Les services Kafka cloud nécessitent souvent une authentification SASL. Modifiez `consumers/kafka_to_postgres.py` :

```python
from kafka import KafkaConsumer
from kafka.errors import KafkaError

def build_consumer(cfg: ETLConfig) -> KafkaConsumer:
    """Instantiate a Kafka consumer with SASL authentication for cloud."""
    consumer = KafkaConsumer(
        cfg.kafka_topic,
        bootstrap_servers=cfg.kafka_bootstrap_server,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id=cfg.kafka_group_id,
        max_poll_records=cfg.batch_size,
        security_protocol="SASL_SSL",
        sasl_mechanism="PLAIN",
        sasl_plain_username=os.getenv("KAFKA_USERNAME", ""),
        sasl_plain_password=os.getenv("KAFKA_PASSWORD", ""),
    )
    return consumer
```

De même pour `producer/producer.py` :

```python
def _build_producer(bootstrap_server: str) -> KafkaProducer:
    """Instantiate a Kafka producer with SASL authentication for cloud."""
    return KafkaProducer(
        bootstrap_servers=bootstrap_server,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        security_protocol="SASL_SSL",
        sasl_mechanism="PLAIN",
        sasl_plain_username=os.getenv("KAFKA_USERNAME", ""),
        sasl_plain_password=os.getenv("KAFKA_PASSWORD", ""),
        linger_ms=100,
        batch_size=32_768,
        retries=5,
        acks="all",
    )
```

### Étape 5 : Tester Localement avec les Services Cloud

```powershell
# 1. Produire des événements vers Kafka cloud
python producer/producer.py --rows 10000 --rate 100 --topic transactions --bootstrap-server xxxxx.upstash.io:9092

# 2. Consommer et charger dans Postgres cloud
python consumers/kafka_to_postgres.py --bootstrap-server xxxxx.upstash.io:9092 --postgres-uri postgresql+psycopg2://postgres:password@db.xxxxx.supabase.co:5432/postgres --batch-size 500
```

### Étape 6 : Déployer le Dashboard sur Streamlit Cloud

1. **Pousser votre code sur GitHub** (assurez-vous d'inclure `.env.example` mais **pas** `.env`)

2. **Créer une app sur Streamlit Cloud** :
   - Aller sur https://share.streamlit.io
   - Se connecter avec GitHub
   - Cliquer sur "New app"
   - Sélectionner votre repository
   - Point d'entrée : `analytics/streamlit_dashboard.py`

3. **Configurer les secrets** :
   - Dans les settings de votre app Streamlit Cloud
   - Ajouter le secret `POSTGRES_CONN_URI` avec votre URL Postgres cloud

4. **Déployer** : Votre dashboard sera accessible publiquement !

### Étape 7 : Automatiser avec un Scheduler Cloud

**Option A : Utiliser GitHub Actions (gratuit)**

Créez `.github/workflows/etl.yml` :

```yaml
name: ETL Pipeline

on:
  schedule:
    - cron: '*/5 * * * *'  # Toutes les 5 minutes
  workflow_dispatch:

jobs:
  etl:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: |
          python consumers/kafka_to_postgres.py \
            --bootstrap-server ${{ secrets.KAFKA_BOOTSTRAP_SERVER }} \
            --postgres-uri ${{ secrets.POSTGRES_CONN_URI }} \
            --batch-size 500
        env:
          KAFKA_USERNAME: ${{ secrets.KAFKA_USERNAME }}
          KAFKA_PASSWORD: ${{ secrets.KAFKA_PASSWORD }}
```

**Option B : Utiliser un Service de Scheduler Cloud**

- **Render Cron Jobs** : https://render.com (gratuit)
- **Railway Cron** : https://railway.app
- **EasyCron** : https://www.easycron.com (gratuit jusqu'à 2 jobs)

---

## 🔒 Sécurité

- **Ne jamais commiter** vos fichiers `.env` ou secrets
- Utiliser les **secrets** de votre plateforme (Streamlit Cloud, GitHub Actions, etc.)
- Activer le **SSL/TLS** pour toutes les connexions cloud
- Limiter les **IP autorisées** pour Postgres (si possible)

---

## 📊 Coûts Estimés

| Service | Plan Gratuit | Limitations |
|---------|-------------|-------------|
| Supabase Postgres | Gratuit | 500MB, 2GB bandwidth |
| Upstash Kafka | Gratuit | 10K messages/jour |
| Streamlit Cloud | Gratuit | Illimité |
| GitHub Actions | Gratuit | 2000 minutes/mois |
| Render Cron | Gratuit | 750 heures/mois |

**Total estimé : $0/mois** pour un usage modéré !

---

## 🆘 Dépannage

### Erreur de connexion Postgres
- Vérifier que l'IP de votre machine est autorisée (si applicable)
- Vérifier les identifiants dans `.env`
- Vérifier que le SSL est activé

### Erreur de connexion Kafka
- Vérifier l'authentification SASL
- Vérifier le protocole (SASL_SSL)
- Vérifier que le topic existe

### Dashboard Streamlit ne charge pas
- Vérifier les secrets dans Streamlit Cloud
- Vérifier que Postgres est accessible depuis Internet
- Vérifier les logs dans Streamlit Cloud

---

## 📚 Ressources

- [Supabase Documentation](https://supabase.com/docs)
- [Upstash Kafka Documentation](https://docs.upstash.com/kafka)
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)


