"""
Dashboard Streamlit qui lit depuis SQLite au lieu de Postgres.

Usage:
    streamlit run analytics/streamlit_dashboard_sqlite.py
"""

import os
from pathlib import Path

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(page_title="Transactions Streaming Analytics (SQLite)", layout="wide")


@st.cache_resource
def get_engine():
    """Crée une connexion SQLite."""
    # Utiliser le chemin absolu depuis le répertoire du projet
    project_root = Path(__file__).parent.parent.resolve()
    db_path_obj = project_root / "data" / "transactions.db"
    
    # Afficher le chemin pour debug
    st.sidebar.info(f"📁 Base: `{db_path_obj}`")
    
    if not db_path_obj.exists():
        st.error(f"❌ Base de données SQLite non trouvée: {db_path_obj}")
        st.info("💡 Veuillez d'abord créer la base de données:")
        st.code("""
# Activer l'environnement virtuel
.\\\\.venv\\\\.Scripts\\\\.Activate.ps1

# Créer la base de données
python create_database.py
        """, language="bash")
        st.stop()
    
    # Vérifier que la base contient des données
    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path_obj))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM transactions_flat")
        count = cursor.fetchone()[0]
        conn.close()
        
        if count == 0:
            st.warning("⚠️ La base de données existe mais est vide!")
            st.info("💡 Exécutez `python create_database.py` pour insérer des données")
            st.stop()
    except Exception as e:
        st.error(f"❌ Erreur lors de la vérification de la base: {e}")
        st.stop()
    
    uri = f"sqlite:///{db_path_obj}"
    try:
        engine = create_engine(uri, pool_pre_ping=True)
        return engine
    except Exception as e:
        st.error(f"❌ Erreur lors de la création de la connexion: {e}")
        st.stop()


@st.cache_data(ttl=60)
def load_transactions(limit: int = 5000) -> pd.DataFrame:
    """Charge les dernières transactions."""
    try:
        engine = get_engine()
        
        # SQLite avec pandas: utiliser f-string pour la limite (sécurisé car limit est un int)
        query = f"""
            SELECT
                transaction_id,
                event_ts,
                user_id,
                amount,
                amount_bucket,
                merchant,
                category,
                city,
                status,
                payment_method,
                currency
            FROM transactions_flat
            ORDER BY event_ts DESC
            LIMIT {limit}
        """
        
        df = pd.read_sql(query, engine)
        
        if not df.empty and "event_ts" in df.columns:
            df["event_ts"] = pd.to_datetime(df["event_ts"], errors="coerce")
        
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des transactions: {e}")
        import traceback
        st.code(traceback.format_exc(), language="python")
        return pd.DataFrame()


@st.cache_data(ttl=120)
def load_time_series(window_days: int = 7) -> pd.DataFrame:
    """Charge les séries temporelles."""
    query = f"""
        SELECT
            strftime('%Y-%m-%d %H:00:00', event_ts) AS hour_bucket,
            COUNT(*) AS tx_count,
            SUM(amount) AS tx_amount
        FROM transactions_flat
        WHERE datetime(event_ts) >= datetime('now', '-{window_days} days')
        GROUP BY hour_bucket
        ORDER BY hour_bucket
    """
    engine = get_engine()
    try:
        df = pd.read_sql(query, engine)
        if not df.empty and "hour_bucket" in df.columns:
            df["hour_bucket"] = pd.to_datetime(df["hour_bucket"])
        return df
    except Exception as e:
        st.warning(f"Erreur lors du chargement des séries temporelles: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=300)
def load_summary_by_merchants() -> pd.DataFrame:
    """Charge le résumé par marchands."""
    query = """
        SELECT merchant, COUNT(*) AS tx_count, SUM(amount) AS total_amount
        FROM transactions_flat
        GROUP BY merchant
        ORDER BY total_amount DESC
        LIMIT 10
    """
    try:
        engine = get_engine()
        return pd.read_sql(query, engine)
    except Exception as e:
        st.warning(f"Erreur lors du chargement des marchands: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=300)
def load_heatmap_data() -> pd.DataFrame:
    """Charge les données pour le heatmap."""
    query = """
        SELECT city, category, SUM(amount) AS total_amount
        FROM transactions_flat
        GROUP BY city, category
        ORDER BY city, category
    """
    try:
        engine = get_engine()
        return pd.read_sql(query, engine)
    except Exception as e:
        st.warning(f"Erreur lors du chargement du heatmap: {e}")
        return pd.DataFrame()


def render_download(df: pd.DataFrame) -> None:
    """Affiche un bouton de téléchargement CSV."""
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Export CSV pour PowerBI / Tableau",
        data=csv,
        file_name="transactions_flat.csv",
        mime="text/csv",
    )


def main() -> None:
    """Point d'entrée principal du dashboard."""
    st.title("📈 Transactions Streaming Dashboard (SQLite)")
    st.write(
        "Suivez en temps réel les flux de transactions ingérées depuis un fichier et stockées dans SQLite."
    )

    # Vérifier la connexion dès le début
    try:
        engine = get_engine()
        st.sidebar.success("✅ Connexion à la base de données réussie")
    except Exception as e:
        st.error(f"❌ Erreur de connexion: {e}")
        st.info("💡 Assurez-vous que la base de données existe:")
        st.code("python create_database.py", language="bash")
        st.stop()

    with st.sidebar:
        st.header("Filtres")
        limit = st.slider("Nombre de lignes affichées", min_value=100, max_value=10000, value=1000, step=100)
        window_days = st.slider("Fenêtre temporelle (jours)", min_value=1, max_value=30, value=7)

    try:
        transactions = load_transactions(limit=limit)
        
        if transactions.empty:
            st.warning("⚠️ Aucune transaction trouvée dans la base de données.")
            st.info("💡 Veuillez d'abord générer et traiter des données:")
            st.code("""
# 1. Générer des données
python producer/producer_to_file.py --rows 1000 --rate 50

# 2. Traiter les données
python consumers/file_queue_to_sqlite.py --input data/queue/transactions.jsonl --db data/transactions.db
            """, language="bash")
            return
        
        time_series = load_time_series(window_days=window_days)
        merchants = load_summary_by_merchants()
        heatmap = load_heatmap_data()

        st.subheader("Dernières transactions")
        st.dataframe(transactions, use_container_width=True)
        render_download(transactions)

        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("Volume horaire (nombre de transactions)")
            if not time_series.empty:
                st.line_chart(time_series.set_index("hour_bucket")["tx_count"])
            else:
                st.info("Pas encore de données temporelles suffisantes.")

        with col_right:
            st.subheader("Montants agrégés par heure")
            if not time_series.empty:
                st.area_chart(time_series.set_index("hour_bucket")["tx_amount"])
            else:
                st.info("Pas encore de données temporelles suffisantes.")

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Top marchands (total des montants)")
            if not merchants.empty:
                st.bar_chart(merchants.set_index("merchant")["total_amount"])
            else:
                st.info("Pas encore de données agrégées.")

        with col_b:
            st.subheader("Heatmap Ville vs Catégorie")
            if not heatmap.empty:
                pivot = heatmap.pivot(index="city", columns="category", values="total_amount").fillna(0)
                st.dataframe(pivot.style.background_gradient(cmap="Blues"), use_container_width=True)
            else:
                st.info("Pas encore de données agrégées.")
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        st.info("Assurez-vous que la base SQLite existe et contient des données.")


if __name__ == "__main__":
    main()


