import streamlit as st
import base64
@st.cache_data
def get_img_as_base64(file):
    """Encode une image locale en Base64 pour l'intégrer en CSS/HTML."""
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
def setup_page_config():
    """Configuration de la page Streamlit"""
    st.set_page_config(
        page_title="KOMAFIN CONSULTING",
        page_icon="assets/LOGO_KOMAFIN.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    """Application du CSS personnalisé"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables CSS */
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #A23B72;
        --accent-color: #F18F01;
        --success-color: #06D6A0;
        --warning-color: #FFD23F;
        --error-color: #F72585;
        --background-color: white;
        --card-background: #FFFFFF;
        --text-primary: #1E293B;
        --text-secondary: #64748B;
        --border-color: #E2E8F0;
    }
    
    /* Style général */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: var(--background-color);
        border-radius: 20px;
        margin: 1rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* Header personnalisé */
    .custom-header {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .custom-header h1 {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .custom-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    
    /* Boutons personnalisés */
    .stButton > button {
        background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Cards styling */
    .metric-card {
        background: var(--card-background);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 4px solid var(--primary-color);
        margin: 1rem 0;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: var(--card-background);
        border: 2px dashed var(--primary-color);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: var(--accent-color);
        background: rgba(46, 134, 171, 0.05);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    }
    
    /* Alerts styling */
    .stAlert {
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Navigation tabs */
    .nav-tab {
        background: var(--card-background);
        border: 2px solid var(--border-color);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        font-weight: 600;
    }
    
    .nav-tab:hover {
        border-color: var(--primary-color);
        background: rgba(46, 134, 171, 0.05);
    }
    
    .nav-tab.active {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .custom-header h1 {
            font-size: 2rem;
        }
        
        .block-container {
            margin: 0.5rem;
            padding: 1rem;
        }
    }
    
    </style>
    """, unsafe_allow_html=True)

def show_header():
    """Affichage de l'en-tête personnalisé"""
    icon_base64 = get_img_as_base64("assets/LOGO_KOMAFIN.png")
    st.markdown(f"""
    <div class="custom-header">
        <div style="display: flex; align-items: center; justify-content: center; gap: 20px;">
            <img src="data:image/png;base64,{icon_base64}" style="width: 100px; height: 100px;">
            <h1 style="font-size: 3rem; margin: 0;">KOMAFIN CONSULTING</h1>
        </div>
        <p>Bienvenue, {st.session_state.username} | Plateforme d'analyse intelligente des données</p>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Création de la barre latérale de navigation"""
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        # Bouton de déconnexion
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.data = None
            st.session_state.cleaned_data = None
            st.session_state.recommendations = []
            st.session_state.file_uploaded = False
            st.rerun()
        
        st.markdown("---")
        
        # Navigation principale
        pages = ["Importer", "Visualiser", "Exporter"]
        icons = ["📁", "📈", "📄"]
        
        selected_page = st.radio(
            "Choisissez une section:",
            pages,
            format_func=lambda x: f"{icons[pages.index(x)]} {x}",
            key="navigation"
        )
        
        st.markdown("---")
        
        # Informations sur les données
        if st.session_state.file_uploaded and st.session_state.cleaned_data is not None:
            st.markdown("###  Données chargées")
            st.metric("Lignes", st.session_state.cleaned_data.shape[0])
            st.metric("Colonnes", st.session_state.cleaned_data.shape[1])
            st.metric("Opérations de Nettoyage", len(st.session_state.get('cleaning_log', [])))
        else:
            st.info("Aucune donnée chargée")
        
        st.markdown("---")
        st.markdown("### ℹ️ À propos")
        st.markdown("""
        **KOMAFIN CONSULTING** v1.0
        
        Plateforme d'analyse de données pour petites et moyennes entreprises.
        
        Fonctionnalités:
        -   Import CSV/Excel
        - 🧹 Nettoyage automatique
        - 💡 Recommandations Intelligentes
        - 📈 Visualisations
        - 📄 Export PDF 
        """)
    
    return selected_page

def create_metric_card(title, value, delta=None, delta_color="normal"):
    """Création d'une carte métrique personnalisée"""
    delta_html = ""
    if delta:
        color = "green" if delta_color == "normal" else "red"
        delta_html = f'<p style="color: {color}; margin: 0; font-size: 0.9rem;">Δ {delta}</p>'
    
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin: 0; color: var(--text-primary);">{title}</h3>
        <h2 style="margin: 0.5rem 0; color: var(--primary-color);">{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)
