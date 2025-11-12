import os

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

st.set_page_config(page_title="Transactions Streaming Analytics", layout="wide")


@st.cache_resource
def get_engine() -> Engine:
    uri = os.getenv(
        "POSTGRES_CONN_URI",
        "postgresql+psycopg2://airflow:airflow@localhost:5432/transactions",
    )
    return create_engine(uri, pool_pre_ping=True)


@st.cache_data(ttl=60)
def load_transactions(limit: int = 5000) -> pd.DataFrame:
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
    engine = get_engine()
    return pd.read_sql(query, engine)


@st.cache_data(ttl=120)
def load_time_series(window_days: int = 7) -> pd.DataFrame:
    query = f"""
        SELECT
            date_trunc('hour', event_ts) AS hour_bucket,
            COUNT(*) AS tx_count,
            SUM(amount) AS tx_amount
        FROM transactions_flat
        WHERE event_ts >= NOW() - INTERVAL '{window_days} day'
        GROUP BY hour_bucket
        ORDER BY hour_bucket
    """
    engine = get_engine()
    return pd.read_sql(query, engine)


@st.cache_data(ttl=300)
def load_summary_by_merchants() -> pd.DataFrame:
    query = """
        SELECT merchant, COUNT(*) AS tx_count, SUM(amount) AS total_amount
        FROM transactions_flat
        GROUP BY merchant
        ORDER BY total_amount DESC
        LIMIT 10
    """
    engine = get_engine()
    return pd.read_sql(query, engine)


@st.cache_data(ttl=300)
def load_heatmap_data() -> pd.DataFrame:
    query = """
        SELECT city, category, SUM(amount) AS total_amount
        FROM transactions_flat
        GROUP BY city, category
        ORDER BY city, category
    """
    engine = get_engine()
    return pd.read_sql(query, engine)


def render_download(df: pd.DataFrame) -> None:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Export CSV pour PowerBI / Tableau",
        data=csv,
        file_name="transactions_flat.csv",
        mime="text/csv",
    )


def main() -> None:
    st.title("📈 Transactions Streaming Dashboard")
    st.write(
        "Suivez en temps réel les flux de transactions ingérés depuis Kafka et stockés dans Postgres."
    )

    with st.sidebar:
        st.header("Filtres")
        limit = st.slider("Nombre de lignes affichées", min_value=100, max_value=10000, value=1000, step=100)
        window_days = st.slider("Fenêtre temporelle (jours)", min_value=1, max_value=30, value=7)

    transactions = load_transactions(limit=limit)
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


if __name__ == "__main__":
    main()

