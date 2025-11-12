#!/usr/bin/env python
"""
Dashboard Streamlit pour Streamlit Cloud.
Ce fichier est le point d'entrée principal pour Streamlit Cloud.
Version améliorée avec filtres et analyses avancées.
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

# Chemin de la base de données
try:
    project_root = Path(__file__).parent.resolve()
    db_path = project_root / "data" / "transactions.db"
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Configuration")
        
        # Option pour créer une nouvelle base de données
        st.subheader("🔄 Base de données")
        st.write(f"**Chemin:** `{db_path.name}`")
        
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
                # Essayer de créer la base de données
                if st.button("🔄 Créer la base de données", use_container_width=True, type="primary"):
                    try:
                        with st.spinner("Création de la base de données en cours..."):
                            from create_database import main as create_db
                            success = create_db(rows=500, db_path=db_path, append=False)
                            if success:
                                st.success("✅ Base de données créée!")
                                st.rerun()
                            else:
                                st.error("❌ Échec de la création de la base de données")
                    except Exception as e2:
                        st.error(f"Erreur lors de la création: {e2}")
                        import traceback
                        with st.expander("Détails de l'erreur"):
                            st.code(traceback.format_exc(), language="python")
        else:
            st.error("❌ Base non trouvée")
            st.info("💡 Cliquez sur le bouton ci-dessous pour créer la base de données")
            if st.button("🔄 Créer la base de données", use_container_width=True, type="primary"):
                try:
                    with st.spinner("Création de la base de données en cours..."):
                        from create_database import main as create_db
                        success = create_db(rows=500, db_path=db_path, append=False)
                        if success:
                            st.success("✅ Base de données créée!")
                            st.rerun()
                        else:
                            st.error("❌ Échec de la création de la base de données")
                except Exception as e:
                    st.error(f"Erreur lors de la création: {e}")
                    import traceback
                    with st.expander("Détails de l'erreur"):
                        st.code(traceback.format_exc(), language="python")
            st.stop()
        
        # Options d'analyse
        st.markdown("---")
        st.subheader("⚙️ Options d'analyse")
        
        # Nombre de transactions à afficher
        limit = st.slider("Nombre de transactions", min_value=10, max_value=1000, value=100, step=10)
        
        # Filtres
        st.markdown("---")
        st.subheader("🔍 Filtres")
        
        # Charger les options de filtres
        try:
            conn = sqlite3.connect(str(db_path))
            
            # Catégories
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM transactions_flat WHERE category IS NOT NULL ORDER BY category")
            categories = [row[0] for row in cursor.fetchall()]
            
            # Villes
            cursor.execute("SELECT DISTINCT city FROM transactions_flat WHERE city IS NOT NULL ORDER BY city")
            cities = [row[0] for row in cursor.fetchall()]
            
            # Statuts
            cursor.execute("SELECT DISTINCT status FROM transactions_flat WHERE status IS NOT NULL ORDER BY status")
            statuses = [row[0] for row in cursor.fetchall()]
            
            # Montants
            cursor.execute("SELECT MIN(amount), MAX(amount) FROM transactions_flat")
            amount_range = cursor.fetchone()
            
            # Dates
            cursor.execute("SELECT MIN(event_date), MAX(event_date) FROM transactions_flat")
            date_range = cursor.fetchone()
            
            conn.close()
            
            # Filtres UI
            selected_categories = st.multiselect(
                "Catégories",
                options=categories,
                default=categories if categories else []
            )
            
            selected_cities = st.multiselect(
                "Villes",
                options=cities,
                default=cities if cities else []
            )
            
            selected_statuses = st.multiselect(
                "Statuts",
                options=statuses,
                default=statuses if statuses else []
            )
            
            if amount_range and amount_range[0] is not None and amount_range[1] is not None:
                min_amount = float(amount_range[0])
                max_amount = float(amount_range[1])
                
                amount_range_filter = st.slider(
                    "Montant (€)",
                    min_value=min_amount,
                    max_value=max_amount,
                    value=(min_amount, max_amount),
                    step=10.0
                )
            else:
                amount_range_filter = None
            
            if date_range and date_range[0] and date_range[1]:
                try:
                    min_date = pd.to_datetime(date_range[0]).date()
                    max_date = pd.to_datetime(date_range[1]).date()
                    
                    date_filter = st.date_input(
                        "Période",
                        value=(min_date, max_date),
                        min_value=min_date,
                        max_value=max_date
                    )
                except:
                    date_filter = None
            else:
                date_filter = None
                
        except Exception as e:
            st.error(f"Erreur lors du chargement des filtres: {e}")
            selected_categories = []
            selected_cities = []
            selected_statuses = []
            amount_range_filter = None
            date_filter = None
        
        # Bouton pour générer plus de données
        st.markdown("---")
        st.subheader("➕ Générer des données")
        
        col_add1, col_add2 = st.columns(2)
        
        with col_add1:
            if st.button("➕ Ajouter 500", use_container_width=True):
                try:
                    with st.spinner("Ajout de 500 transactions..."):
                        from create_database import main as create_db
                        success = create_db(rows=500, db_path=db_path, append=True)
                        if success:
                            st.success("✅ 500 transactions ajoutées!")
                            st.rerun()
                        else:
                            st.error("❌ Échec")
                except Exception as e:
                    st.error(f"Erreur: {e}")
        
        with col_add2:
            if st.button("🔄 Nouvelle (1000)", use_container_width=True):
                try:
                    with st.spinner("Création d'une nouvelle base..."):
                        from create_database import main as create_db
                        success = create_db(rows=1000, db_path=db_path, append=False)
                        if success:
                            st.success("✅ Nouvelle base créée!")
                            st.rerun()
                        else:
                            st.error("❌ Échec")
                except Exception as e:
                    st.error(f"Erreur: {e}")
        
        # Option personnalisée
        custom_rows = st.number_input("Nombre de transactions", min_value=100, max_value=10000, value=1000, step=100, key="custom_rows")
        if st.button("🔄 Créer personnalisée", use_container_width=True):
            try:
                with st.spinner(f"Création avec {custom_rows} transactions..."):
                    from create_database import main as create_db
                    success = create_db(rows=custom_rows, db_path=db_path, append=False)
                    if success:
                        st.success(f"✅ Base créée avec {custom_rows} transactions!")
                        st.rerun()
                    else:
                        st.error("❌ Échec")
            except Exception as e:
                st.error(f"Erreur: {e}")
    
    # Charger les données
    st.write("## 📊 Analyse des transactions")
    
    try:
        # Connexion SQLite directe
        conn = sqlite3.connect(str(db_path))
        
        # Construire la requête avec les filtres
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
            WHERE 1=1
        """
        
        params = []
        
        # Appliquer les filtres
        if selected_categories:
            placeholders = ','.join(['?' for _ in selected_categories])
            query += f" AND category IN ({placeholders})"
            params.extend(selected_categories)
        
        if selected_cities:
            placeholders = ','.join(['?' for _ in selected_cities])
            query += f" AND city IN ({placeholders})"
            params.extend(selected_cities)
        
        if selected_statuses:
            placeholders = ','.join(['?' for _ in selected_statuses])
            query += f" AND status IN ({placeholders})"
            params.extend(selected_statuses)
        
        if amount_range_filter:
            query += " AND amount >= ? AND amount <= ?"
            params.extend([amount_range_filter[0], amount_range_filter[1]])
        
        if date_filter and len(date_filter) == 2:
            query += " AND event_date >= ? AND event_date <= ?"
            params.extend([date_filter[0].isoformat(), date_filter[1].isoformat()])
        
        query += f" ORDER BY event_ts DESC LIMIT {limit}"
        
        df = pd.read_sql(query, conn, params=params)
        conn.close()
        
        if df.empty:
            st.warning("⚠️ Aucune transaction trouvée avec ces filtres")
            st.info("💡 Modifiez les filtres dans la sidebar")
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
        st.subheader("📋 Transactions")
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
        
        # Analyses supplémentaires
        st.markdown("---")
        st.subheader("📊 Analyses supplémentaires")
        
        col_analysis1, col_analysis2 = st.columns(2)
        
        with col_analysis1:
            st.write("**Statuts des transactions**")
            if 'status' in df.columns:
                status_counts = df['status'].value_counts()
                st.bar_chart(status_counts)
        
        with col_analysis2:
            st.write("**Méthodes de paiement**")
            if 'payment_method' in df.columns:
                payment_counts = df['payment_method'].value_counts()
                st.bar_chart(payment_counts)
        
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
