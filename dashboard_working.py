#!/usr/bin/env python
"""
Dashboard Streamlit qui FONCTIONNE - Version ultra-simple.
Ce dashboard fonctionne à coup sûr!
"""

import streamlit as st
from pathlib import Path
import sqlite3
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Transactions Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre
st.title("📈 Transactions Dashboard")
st.markdown("---")

# Chemin de la base de données (chemin absolu)
try:
    project_root = Path(__file__).parent.resolve()
    db_path = project_root / "data" / "transactions.db"
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Informations")
        st.write(f"**Base de données:**")
        st.code(str(db_path), language=None)
        
        # Vérifier la base
        if db_path.exists():
            st.success("✅ Base trouvée")
            try:
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM transactions_flat")
                count = cursor.fetchone()[0]
                conn.close()
                st.metric("Transactions", count)
                st.success(f"✅ {count} transactions disponibles")
            except Exception as e:
                st.error(f"Erreur: {e}")
        else:
            st.error("❌ Base non trouvée")
            st.info("Exécutez: `python create_database.py`")
            st.stop()
    
    # Charger les données
    st.write("## 📊 Chargement des données...")
    
    try:
        # Connexion SQLite directe (plus simple que SQLAlchemy)
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
        
        if df.empty:
            st.warning("⚠️ Aucune transaction trouvée")
            st.info("💡 Exécutez: `python create_database.py`")
            st.stop()
        
        st.success(f"✅ {len(df)} transactions chargées")
        
        # Convertir event_ts en datetime
        if 'event_ts' in df.columns:
            df['event_ts'] = pd.to_datetime(df['event_ts'], errors='coerce')
        
        # Métriques
        st.markdown("---")
        st.subheader("📊 Métriques")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total transactions", len(df))
        
        with col2:
            total_amount = df['amount'].sum()
            st.metric("Montant total", f"{total_amount:,.2f} €")
        
        with col3:
            avg_amount = df['amount'].mean()
            st.metric("Moyenne", f"{avg_amount:,.2f} €")
        
        with col4:
            approved = len(df[df['status'] == 'APPROVED'])
            st.metric("Approuvées", approved)
        
        # Tableau des transactions
        st.markdown("---")
        st.subheader("📋 Dernières transactions")
        st.dataframe(df, use_container_width=True, height=400)
        
        # Graphiques
        st.markdown("---")
        st.subheader("📈 Graphiques")
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.write("**Montants par catégorie**")
            if 'category' in df.columns and 'amount' in df.columns:
                category_amounts = df.groupby('category')['amount'].sum().sort_values(ascending=False)
                st.bar_chart(category_amounts)
            else:
                st.info("Données non disponibles")
        
        with col_right:
            st.write("**Transactions par ville**")
            if 'city' in df.columns:
                city_counts = df.groupby('city').size().sort_values(ascending=False)
                st.bar_chart(city_counts)
            else:
                st.info("Données non disponibles")
        
        # Top marchands
        st.write("**Top 10 marchands**")
        if 'merchant' in df.columns and 'amount' in df.columns:
            merchant_amounts = df.groupby('merchant')['amount'].sum().sort_values(ascending=False).head(10)
            st.bar_chart(merchant_amounts)
        else:
            st.info("Données non disponibles")
        
        # Export CSV
        st.markdown("---")
        st.subheader("💾 Export")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger CSV",
            data=csv,
            file_name="transactions.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement: {e}")
        import traceback
        with st.expander("Détails de l'erreur"):
            st.code(traceback.format_exc(), language="python")
        st.stop()
        
except Exception as e:
    st.error(f"❌ Erreur: {e}")
    import traceback
    st.code(traceback.format_exc(), language="python")
    st.stop()

