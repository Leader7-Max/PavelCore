import streamlit as st
from assets.styles import inject_custom_design

# Configuration de la page
st.set_page_config(
    page_title="PavelCore — Coffre-Fort & Workspace",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injection du design CSS Ultra Premium
inject_custom_design()

# Gestion de la session
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ----------------------------------------------------
# ECRAN DE CONNEXION / ACCÈS SÉCURISÉ
# ----------------------------------------------------
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <h1 style="background: linear-gradient(90deg, #00F2FE, #4F46E5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0;">PavelCore</h1>
                <p style="color: #8E9BAE; font-size: 0.95rem;">Espace Ultra-Sécurisé & Second Brain</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            st.subheader("Authentification")
            
            # Saisie de l'email MASQUÉE dans la barre pour des raisons de confidentialité
            email = st.text_input("Adresse Email", type="password", placeholder="••••••••••••••••")
            
            # Mot de passe / Code Master
            master_key = st.text_input("Clé Maîtresse / PIN", type="password", placeholder="••••••••")
            
            submit = st.form_submit_button("Déverrouiller le Coffre", use_container_width=True)

            if submit:
                # Logique de vérification (à coupler avec votre base de données)
                if master_key != "":
                    st.session_state.authenticated = True
                    st.success("Accès accordé.")
                    st.rerun()
                else:
                    st.error("Identifiants incorrects.")

# ----------------------------------------------------
# APPLICATION PRINCIPALE (Abonnement / Coffre)
# ----------------------------------------------------
else:
    # Sidebar de navigation
    with st.sidebar:
        st.markdown("<h2 style='color: #00F2FE;'>PavelCore</h2>", unsafe_allow_html=True)
        st.markdown('<span class="badge">Session Sécurisée</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        menu = st.radio(
            "Navigation",
            ["Dashboard", "Mes Prompts & Code", "Projets & Agenda", "Boîte à Idées", "Coffre-Fort Docs"],
            index=0
        )
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.button("Verrouiller la session", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # Contenu principal
    st.markdown(f"## 🚀 {menu}")
    
    if menu == "Dashboard":
        # Cartes statistiques stylisées
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
                <div class="glass-card">
                    <h4 style="color: #8E9BAE; margin:0;">Projets Actifs</h4>
                    <h1 style="color: #00F2FE; margin:10px 0;">08</h1>
                    <span class="badge">En progression</span>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
                <div class="glass-card">
                    <h4 style="color: #8E9BAE; margin:0;">Prompts & Snippets</h4>
                    <h1 style="color: #4F46E5; margin:10px 0;">142</h1>
                    <span class="badge">Sauvegardés</span>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
                <div class="glass-card">
                    <h4 style="color: #8E9BAE; margin:0;">Échéances Proches</h4>
                    <h1 style="color: #FF007A; margin:10px 0;">03</h1>
                    <span class="badge" style="color:#FF007A; border-color:#FF007A;">Aujourd'hui</span>
                </div>
            """, unsafe_allow_html=True)

    elif menu == "Mes Prompts & Code":
        st.markdown("""
            <div class="glass-card">
                <h3>Ajouter un nouveau Snippet / Prompt</h3>
            </div>
        """, unsafe_allow_html=True)
        
        title = st.text_input("Titre du prompt ou code")
        language = st.selectbox("Langage / Catégorie", ["Python", "JavaScript", "SQL", "Prompt Midjourney", "Prompt LLM"])
        code_content = st.text_area("Contenu du Code / Prompt", height=180)
        
        if st.button("Enregistrer au Coffre"):
            st.toast("Snippet sauvegardé avec succès !", icon="🔐")
