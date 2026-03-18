import streamlit as st
import sys
import os
from scipy import stats
from itertools import combinations
import numpy as np

# Ajouter le répertoire racine au path pour les imports

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from frontend.ui import setup_page_config, apply_custom_css, create_sidebar, show_header
from backend.authentifat import check_authentication, show_login_form
from backend.datacleaning import clean_data, load_file
from utilisation.recommendation import generate_recommendations
from utilisation.exportpdf import create_pdf_report
from visualisation import create_visualizations

def initialize_session_state():
    """Initialise les variables de session"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'cleaned_data' not in st.session_state:
        st.session_state.cleaned_data = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False

def main():
    """Fonction principale de l'application"""
    # Configuration de la page
    setup_page_config()
    apply_custom_css()
   
    # Initialisation des variables de session
    initialize_session_state()
   
    # Vérification de l'authentification
    if not st.session_state.authenticated:
        show_login_form()
        return
   
    # Interface principale
    show_header()
   
    # Sidebar navigation
    page = create_sidebar()
   
    # Contenu principal selon la page sélectionnée
    if page == "Importer":
        show_import_page()
    elif page == "Visualiser":
        show_visualization_page()
    elif page == "Exporter":
        show_export_page()

def show_import_page():
    """Page d'importation des données"""
    st.markdown("##  Importation des Données")
   
    # Upload de fichier
    uploaded_file = st.file_uploader(
        "Choisissez un fichier CSV ou Excel",
        type=['csv', 'xlsx', 'xls'],
        help="Formats supportés: CSV, Excel (.xlsx, .xls)"
    )
   
    if uploaded_file is not None:
        try:
            # Chargement des données
            with st.spinner("Chargement du fichier..."):
                raw_data = load_file(uploaded_file)
           
            if raw_data is not None:
                st.session_state.data = raw_data
                st.session_state.file_uploaded = True
                st.success(f"✅ Fichier chargé avec succès! ({raw_data.shape[0]} lignes, {raw_data.shape[1]} colonnes)")
                
                st.markdown("### Aperçu des données brutes")
                st.dataframe(raw_data.head(), use_container_width=True)

                st.divider()

                # --- Section de configuration du nettoyage ---
                st.markdown("### ⚙️ Configurez le Nettoyage")
                with st.expander("Afficher les options de nettoyage", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        missing_strategy = st.selectbox(
                            "Stratégie pour les valeurs manquantes :", 
                            ['auto', 'remove_row', 'none'], 
                            index=0,
                            help="Auto: remplace intelligemment (médiane/mode). Remove: supprime les lignes concernées. None: ne fait rien."
                        )
                    with col2:
                        outlier_strategy = st.selectbox(
                            "Stratégie pour les valeurs aberrantes :", 
                            ['flag', 'cap', 'remove', 'none'],
                            index=0,
                            help="Flag: marque sans modifier. Cap: plafonne à la limite. Remove: supprime la ligne. None: ne fait rien."
                        )

                # --- Bouton pour lancer le nettoyage ---
                if st.button(" Lancer le Nettoyage des Données", use_container_width=True, type="primary"):
                    with st.spinner("Nettoyage des données en cours..."):
                        cleaned_df, log_messages = clean_data(
                            st.session_state.data,
                            missing_value_strategy=missing_strategy,
                            outlier_strategy=outlier_strategy
                        )
                        
                        st.session_state.cleaned_data = cleaned_df
                        st.session_state.cleaning_log = log_messages
                    
                    st.success(" Nettoyage terminé !")

                    # --- Affichage des résultats après nettoyage ---
                    if st.session_state.cleaned_data is not None:
                        st.markdown("### Données après nettoyage")
                        st.dataframe(st.session_state.cleaned_data.head(), use_container_width=True)

                        st.markdown("###  Journal des Opérations de Nettoyage")
                        for msg in st.session_state.cleaning_log:
                            if "IMPORTANT" in msg or "AVERTISSEMENT" in msg:
                                st.warning(msg)
                            elif "SUCCÈS" in msg:
                                st.success(msg)
                            else:
                                st.info(msg)
                
                       
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement du fichier: {str(e)}")
    else:
        st.info("📁 Veuillez importer un fichier pour commencer l'analyse")

def show_visualization_page():
    """Page de visualisation des données"""
    st.markdown("## 📈 Visualisation des Données")
   
    if 'cleaned_data' not in st.session_state or st.session_state.cleaned_data is None:
        st.warning("⚠️ Veuillez d'abord importer et nettoyer un fichier dans l'onglet 'Importer'")
        return
    # Création des visualisations
    create_visualizations(st.session_state.cleaned_data)

def show_export_page():
    """Page d'exportation"""
    st.markdown("## 📄 Exportation des Résultats")
   
    if 'cleaned_data' not in st.session_state or st.session_state.cleaned_data is None:
        st.warning("⚠️ Aucune donnée nettoyée à exporter. Veuillez d'abord importer et nettoyer un fichier.")
        return
   
    st.markdown("### Options d'exportation")
   
    col1, col2 = st.columns(2)
   
    with col1:
        csv_data = st.session_state.cleaned_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=" Télécharger les données nettoyées (CSV)",
            data=csv_data,
            file_name="donnees_nettoyees.csv",
            mime="text/csv",
            use_container_width=True
        )
   
    with col2:
    # Le type du bouton reste le même
        if st.button(" Générer rapport PDF", use_container_width=True):
            with st.spinner("Génération du rapport PDF..."):
                
                # --- MODIFICATION ICI ---
                # On retire l'argument 'recommendations' qui n'est plus nécessaire.
                # La nouvelle fonction génère ses propres analyses.
                pdf_buffer = create_pdf_report(
                    st.session_state.cleaned_data,
                    st.session_state.username
                    # Vous pouvez aussi ajouter un thème si vous le souhaitez, ex:
                    # theme_sujet="Analyse des Ventes Mensuelles"
                )
                
                st.download_button(
                    label="📄 Télécharger le Rapport d'Analyse",
                    data=pdf_buffer,
                    file_name="Rapport_Analyse_Exploratoire.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

if __name__ == "__main__":
    main()
