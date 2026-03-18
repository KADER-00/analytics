import streamlit as st
import hashlib
import json
import os
import base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("assets/LOGO_KOMAFIN.png")

# Fichier pour stocker les utilisateurs (en production, utiliser une vraie base de données)
USERS_FILE = "users.json"

def hash_password(password):
    """Hachage du mot de passe"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Chargement des utilisateurs depuis le fichier"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    """Sauvegarde des utilisateurs dans le fichier"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def create_default_users():
    """Création d'utilisateurs par défaut"""
    users = load_users()
    if not users:
        default_users = {
            "admin": {
                "password": hash_password("admin123"),
                "email": "admin@analysepme.com",
                "role": "admin"
            },
            "demo": {
                "password": hash_password("demo123"),
                "email": "demo@analysepme.com",
                "role": "user"
            }
        }
        save_users(default_users)
        return default_users
    return users

def authenticate_user(username, password):
    """Authentification de l'utilisateur"""
    users = load_users()
    if username in users:
        if users[username]["password"] == hash_password(password):
            return True, users[username]
    return False, None

def register_user(username, password, email):
    """Inscription d'un nouvel utilisateur"""
    users = load_users()
    if username in users:
        return False, "Nom d'utilisateur déjà existant"
    
    users[username] = {
        "password": hash_password(password),
        "email": email,
        "role": "user"
    }
    save_users(users)
    return True, "Utilisateur créé avec succès"

def check_authentication():
    """Vérification de l'état d'authentification"""
    return st.session_state.get('authenticated', False)

def show_login_form():
    """Affichage du formulaire de connexion"""
    # Créer les utilisateurs par défaut
    create_default_users()
   
    # CSS pour le design divisé moderne
    st.markdown("""
     <style>
     .main > div {
         padding: 0 !important;
         max-width: 100% !important;
     }
     
     .split-container {
         display: flex;
         min-height: 100vh;
         margin: 0;
         padding: 0;
     }
     
     .left-panel {
         background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 50%, #1e40af 100%);
         width: 50%;
         padding: 3rem;
         color: white;
         position: relative;
         overflow: hidden;
         display: flex;
         align-items: center;
         justify-content: center;
     }
     
     .left-panel::before {
         content: '';
         position: absolute;
         top: 20%;
         left: 20%;
         width: 200px;
         height: 200px;
         background: rgba(59, 130, 246, 0.3);
         border-radius: 50%;
         filter: blur(40px);
     }
     
     .left-panel::after {
         content: '';
         position: absolute;
         bottom: 20%;
         right: 20%;
         width: 300px;
         height: 300px;
         background: rgba(147, 197, 253, 0.2);
         border-radius: 50%;
         filter: blur(60px);
     }
     
     .left-content {
         position: relative;
         z-index: 10;
         max-width: 400px;
     }
     
     .left-content h1 {
         font-size: 2.5rem;
         font-weight: 700;
         margin-bottom: 1.5rem;
         line-height: 1.2;
     }
     
     .left-content p {
         font-size: 1.1rem;
         color: rgba(255, 255, 255, 0.9);
         margin-bottom: 2rem;
         line-height: 1.6;
     }
     
     .feature-list {
         list-style: none;
         padding: 0;
         margin: 0;
     }
     
     .feature-item {
         display: flex;
         align-items: flex-start;
         margin-bottom: 1.5rem;
     }
     
     .feature-number {
         background: rgba(59, 130, 246, 0.8);
         color: white;
         width: 24px;
         height: 24px;
         border-radius: 50%;
         display: flex;
         align-items: center;
         justify-content: center;
         font-size: 0.875rem;
         font-weight: 600;
         margin-right: 1rem;
         flex-shrink: 0;
     }
     
     .feature-text {
         color: rgba(255, 255, 255, 0.9);
         font-size: 0.95rem;
     }
     
     .right-panel {
         width: 50%;
         background: #f8fafc;
         display: flex;
         align-items: center;
         justify-content: center;
         padding: 2rem;
     }
     
     .form-container {
         background: white;
         padding: 2.5rem;
         border-radius: 16px;
         box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
         width: 100%;
         max-width: 400px;
     }
     
     .form-header {
         text-align: center;
         margin-bottom: 2rem;
     }
     
     .form-header h2 {
         font-size: 1.875rem;
         font-weight: 700;
         color: #1f2937;
         margin-bottom: 0.5rem;
     }
     
     .form-header p {
         color: #6b7280;
         font-size: 0.95rem;
     }
     
     .stTextInput > div > div > input {
         border-radius: 8px !important;
         border: 1px solid #d1d5db !important;
         padding: 0.75rem 1rem !important;
         font-size: 0.95rem !important;
         transition: all 0.2s ease !important;
     }
     
     .stTextInput > div > div > input:focus {
         border-color: #2563eb !important;
         box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
     }
     
     .stButton > button {
         background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
         color: white !important;
         border: none !important;
         border-radius: 8px !important;
         padding: 0.75rem 1.5rem !important;
         font-weight: 600 !important;
         width: 100% !important;
         transition: all 0.2s ease !important;
         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
     }
     
     .stButton > button:hover {
         transform: translateY(-1px) !important;
         box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
     }
     
     .stTabs [data-baseweb="tab-list"] {
         gap: 0 !important;
         background: #f3f4f6 !important;
         border-radius: 8px !important;
         padding: 4px !important;
     }
     
     .stTabs [data-baseweb="tab"] {
         background: transparent !important;
         border-radius: 6px !important;
         color: #6b7280 !important;
         font-weight: 500 !important;
         padding: 0.5rem 1rem !important;
     }
     
     .stTabs [aria-selected="true"] {
         background: white !important;
         color: #2563eb !important;
         box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1) !important;
     }
     
     .demo-info {
         background: #eff6ff;
         border: 1px solid #bfdbfe;
         border-radius: 8px;
         padding: 1rem;
         margin-top: 1.5rem;
     }
     
     .demo-info h4 {
         color: #1e40af;
         font-weight: 600;
         margin-bottom: 0.5rem;
     }
     
     .demo-account {
         background: white;
         border-radius: 6px;
         padding: 0.75rem;
         margin: 0.5rem 0;
         border-left: 3px solid #2563eb;
     }
     
     .toggle-text {
         text-align: center;
         margin-top: 1.5rem;
         color: #6b7280;
         font-size: 0.9rem;
     }
     
     .toggle-link {
         color: #2563eb;
         font-weight: 600;
         text-decoration: none;
         cursor: pointer;
     }
     
     .toggle-link:hover {
         text-decoration: underline;
     }
     
     @media (max-width: 1024px) {
         .split-container {
             flex-direction: column;
         }
         
         .left-panel, .right-panel {
             width: 100%;
         }
         
         .left-panel {
             min-height: 40vh;
             padding: 2rem;
         }
         
         .left-content h1 {
             font-size: 2rem;
         }
     }
     </style>
     """, unsafe_allow_html=True)
     
     # Structure HTML pour le design divisé

    st.markdown(f""" 
        <style>
            .left-panel {{
                display: flex;
                justify-content: center;  /* centre horizontalement */
                align-items: center;      /* centre verticalement */
                height: 100vh;
                background: linear-gradient(to bottom right, #1e3a8a, #3b82f6);
            }}
            .left-content {{
                max-width: 800px;
                padding: 2rem;
            }}
        </style>

        <div class="split-container">
            <div class="left-panel">
                <div class="left-content">
                    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 1.5rem;">
                        <img src="data:image/png;base64,{logo_base64}" style="width: 100px; height: 100px;">
                        <h1 style="font-size: 3.5rem; margin: 0; color: #ffffff;">KOMAFIN CONSULTING</h1>
                    </div>
                    <p style="font-size: 1.4rem; line-height: 2rem; color: rgba(255,255,255,0.95); margin-bottom: 1.5rem;">
                        Analysez vos données d'entreprise en toute simplicité.
                    </p>
                    <p style="font-size: 1.2rem; line-height: 1.9rem; color: rgba(255,255,255,0.9); margin-bottom: 2rem;">
                        Notre plateforme vous aide à nettoyer, analyser et interpréter vos données
                        pour prendre des décisions éclairées et stratégiques.
                    </p>
                    <ul class="feature-list" style="padding-left: 0;">
                        <li class="feature-item" style="display: flex; align-items: center; margin-bottom: 1rem;">
                            <div class="feature-number" style="background: #3b82f6; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; font-weight: 600; margin-right: 1rem;">1</div>
                            <div class="feature-text" style="font-size: 1.1rem; color: rgba(255,255,255,0.9);">Importez vos données CSV ou Excel</div>
                        </li>
                        <li class="feature-item" style="display: flex; align-items: center; margin-bottom: 1rem;">
                            <div class="feature-number" style="background: #2563eb; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; font-weight: 600; margin-right: 1rem;">2</div>
                            <div class="feature-text" style="font-size: 1.1rem; color: rgba(255,255,255,0.9);">Nettoyage et traitement automatique</div>
                        </li>
                        <li class="feature-item" style="display: flex; align-items: center;">
                            <div class="feature-number" style="background: #1e40af; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; font-weight: 600; margin-right: 1rem;">3</div>
                            <div class="feature-text" style="font-size: 1.1rem; color: rgba(255,255,255,0.9);">Obtenez des recommandations intelligentes</div>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="right-panel">
    """, unsafe_allow_html=True)

     # Conteneur du formulaire
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
     
     # En-tête du formulaire
    st.markdown("""
     <div class="form-header">
         <h2>Connexion</h2>
         <p>Connectez-vous pour accéder à votre tableau de bord</p>
     </div>
     """, unsafe_allow_html=True)
     
    tab1, tab2 = st.tabs(["Connexion", "Inscription"])
     
    with tab1:
         with st.form("login_form"):
             username = st.text_input("Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur", label_visibility="collapsed")
             st.markdown('<div style="margin-bottom: 1rem;"></div>', unsafe_allow_html=True)
             password = st.text_input("Mot de passe", type="password", placeholder="Entrez votre mot de passe", label_visibility="collapsed")
             st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)
             
             login_button = st.form_submit_button("Se connecter", use_container_width=True)
             
             if login_button:
                 if username and password:
                     is_valid, user_data = authenticate_user(username, password)
                     if is_valid:
                         st.session_state.authenticated = True
                         st.session_state.username = username
                         st.success("✅ Connexion réussie!")
                         st.rerun()
                     else:
                         st.error("❌ Nom d'utilisateur ou mot de passe incorrect")
                 else:
                     st.warning("⚠️ Veuillez remplir tous les champs")
         
        #  # Informations de démonstration
        #  st.markdown("""
        #  <div class="demo-info">
        #      <h4>🎯 Comptes de démonstration</h4>
        #      <div class="demo-account">
        #          <strong>Administrateur:</strong><br>
        #          Utilisateur: admin | Mot de passe: admin123
        #      </div>
        #      <div class="demo-account">
        #          <strong>Utilisateur demo:</strong><br>
        #          Utilisateur: demo | Mot de passe: demo123
        #      </div>
        #  </div>
        #  """, unsafe_allow_html=True)

    with tab2:
         with st.form("register_form"):
             new_username = st.text_input("Nom d'utilisateur", placeholder="Choisissez un nom d'utilisateur", label_visibility="collapsed", key="reg_username")
             st.markdown('<div style="margin-bottom: 1rem;"></div>', unsafe_allow_html=True)
             new_email = st.text_input("Email", placeholder="votre.email@exemple.com", label_visibility="collapsed")
             st.markdown('<div style="margin-bottom: 1rem;"></div>', unsafe_allow_html=True)
             new_password = st.text_input("Mot de passe", type="password", placeholder="Choisissez un mot de passe", label_visibility="collapsed", key="reg_password")
             st.markdown('<div style="margin-bottom: 1rem;"></div>', unsafe_allow_html=True)
             confirm_password = st.text_input("Confirmer le mot de passe", type="password", placeholder="Confirmez votre mot de passe", label_visibility="collapsed")
             st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)
             
             register_button = st.form_submit_button("S'inscrire", use_container_width=True)
             
             if register_button:
                 if new_username and new_email and new_password and confirm_password:
                     if new_password == confirm_password:
                         if len(new_password) >= 6:
                             success, message = register_user(new_username, new_password, new_email)
                             if success:
                                 st.success(f"✅ {message}")
                                 st.info("Vous pouvez maintenant vous connecter avec vos identifiants")
                             else:
                                 st.error(f"❌ {message}")
                         else:
                             st.error("❌ Le mot de passe doit contenir au moins 6 caractères")
                     else:
                        st.error("❌ Les mots de passe ne correspondent pas")
                 else:
                     st.warning("⚠️ Veuillez remplir tous les champs")

     # Fermeture des conteneurs
    st.markdown('</div>', unsafe_allow_html=True)  # form-container
    st.markdown('</div>', unsafe_allow_html=True)  # right-panel
    st.markdown('</div>', unsafe_allow_html=True)  # split-container
     
     # Footer
    st.markdown("---")
    st.markdown("""
     <div style="text-align: center; color: #64748B; padding: 1rem;">
         <p>© 2026 Analyse PME - Plateforme d'analyse de données pour entreprises</p>
     <div style="position: fixed; bottom: 0; left: 0; right: 0; background: white; border-top: 1px solid #e5e7eb; padding: 0.75rem; text-align: center; z-index: 1000;">
         <p style="margin: 0; color: #6b7280; font-size: 0.75rem;">
            Analyse PME — Version Desktop 1.0 — Appuyez sur Entrée pour vous connecter rapidement
        </p>
      </div>
      """, unsafe_allow_html=True)
