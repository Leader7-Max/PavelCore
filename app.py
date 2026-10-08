import streamlit as st
from assets.styles import inject_custom_design

st.set_page_config(
    page_title="PavelCore — Coffre-Fort & Workspace",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_design()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- ECRAN DE CONNEXION ---
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
            
            # Email lisible
            email = st.text_input("Adresse Email", placeholder="exemple@domaine.com")
            
            # Mot de passe masqué
            master_key = st.text_input("Clé Maîtresse / PIN", type="password", placeholder="••••••••")
            
            submit = st.form_submit_button("Déverrouiller le Coffre", use_container_width=True)

            if submit:
                if master_key != "":
                    st.session_state.authenticated = True
                    st.success("Accès accordé.")
                    st.rerun()
                else:
                    st.error("Saisis ta clé d'accès.")

# --- APPLICATION PRINCIPALE ---
else:
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

    if menu == "Dashboard":
        st.markdown("## 🚀 Dashboard")
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
        from modules.prompts import render_prompts_module
        render_prompts_module()

    elif menu == "Projets & Agenda":
        from modules.projects_agenda import render_projects_agenda
        render_projects_agenda()

    elif menu == "Boîte à Idées":
        from modules.ideas import render_ideas
        render_ideas()

    elif menu == "Coffre-Fort Docs":
        from modules.vault import render_vault
        render_vault()
