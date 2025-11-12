#!/bin/bash
# Script pour configurer l'environnement cloud
# Usage: bash scripts/setup_cloud.sh

echo "🔧 Configuration de l'environnement cloud..."

# Créer un fichier .env.example
cat > .env.example << EOF
# Postgres Cloud (Supabase, Render, etc.)
POSTGRES_CONN_URI=postgresql+psycopg2://user:password@host:5432/database

# Kafka Cloud (Upstash, Confluent, etc.)
KAFKA_BOOTSTRAP_SERVER=your-kafka-host:9092
KAFKA_USERNAME=your_username
KAFKA_PASSWORD=your_password
KAFKA_TOPIC=transactions

# Batch size
BATCH_SIZE=500
EOF

echo "✅ Fichier .env.example créé"
echo "📝 Copiez .env.example vers .env et remplissez vos identifiants cloud"
echo "🔒 Ne commitez jamais .env dans Git !"


