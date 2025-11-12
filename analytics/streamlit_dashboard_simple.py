"""
Dashboard Streamlit SIMPLE - Version minimale qui fonctionne.
Usage:
    streamlit run analytics/streamlit_dashboard_simple.py
"""

import streamlit as st
from pathlib import Path
import sqlite3
import pandas as pd

st.set_page_config(page_title="Transactions Dashboard", layout="wide")

# Titre
st.title("📈 Transactions Dashboard")
st.write("Version simple du dashboard")

# Chemin de la base de données
project_root = Path(__file__).parent.parent.resolve()
db_path = project_root / "data" / "transactions.db"

st.sidebar.write(f"**Base de données:**")
st.sidebar.write(f"`{db_path}`")

# Vérifier que la base existe
if not db_path.exists():
    st.error(f"❌ Base de données non trouvée: {db_path}")
    st.info("💡 Exécutez: `python create_database.py`")
    st.stop()

st.sidebar.success("✅ Base de données trouvée")

# Vérifier que la base contient des données
try:
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Compter les transactions
    cursor.execute("SELECT COUNT(*) FROM transactions_flat")
    count = cursor.fetchone()[0]
    
    st.sidebar.write(f"**Transactions:** {count}")
    
    if count == 0:
        st.warning("⚠️ La base de données est vide!")
        st.info("💡 Exécutez: `python create_database.py`")
        conn.close()
        st.stop()
    
    conn.close()
    st.sidebar.success(f"✅ {count} transactions dans la base")
    
except Exception as e:
    st.error(f"❌ Erreur lors de la vérification: {e}")
    st.stop()

# Charger les données
try:
    st.write("## 📊 Chargement des données...")
    
    conn = sqlite3.connect(str(db_path))
    
    # Charger les transactions
    query = """
        SELECT
            transaction_id,
            event_ts,
            user_id,
            amount,
            merchant,
            category,
            city,
            status,
            payment_method
        FROM transactions_flat
        ORDER BY event_ts DESC
        LIMIT 100
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    
    st.success(f"✅ {len(df)} transactions chargées")
    
    # Afficher les données
    if not df.empty:
        st.write("### Dernières transactions")
        st.dataframe(df, use_container_width=True)
        
        # Statistiques
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total transactions", len(df))
        
        with col2:
            st.metric("Montant total", f"{df['amount'].sum():.2f} EUR")
        
        with col3:
            st.metric("Montant moyen", f"{df['amount'].mean():.2f} EUR")
        
        with col4:
            st.metric("Transactions approuvées", len(df[df['status'] == 'APPROVED']))
        
        # Graphiques simples
        st.write("### Graphiques")
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.write("**Montants par catégorie**")
            category_amounts = df.groupby('category')['amount'].sum().sort_values(ascending=False)
            st.bar_chart(category_amounts)
        
        with col_right:
            st.write("**Transactions par ville**")
            city_counts = df.groupby('city').size().sort_values(ascending=False)
            st.bar_chart(city_counts)
        
        # Top marchands
        st.write("### Top 10 marchands")
        merchant_amounts = df.groupby('merchant')['amount'].sum().sort_values(ascending=False).head(10)
        st.bar_chart(merchant_amounts)
        
        # Export CSV
        st.write("### Export")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger CSV",
            data=csv,
            file_name="transactions.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Aucune transaction trouvée")
        
except Exception as e:
    st.error(f"❌ Erreur lors du chargement: {e}")
    import traceback
    st.code(traceback.format_exc(), language="python")

