import sys
import os
import json
import streamlit as st
from datetime import datetime, date

# Correctif pour Streamlit Cloud
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration de la page
st.set_page_config(
    page_title="PavelCore — Workspace & Agenda Premium",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import des styles et des vues modulaires
try:
    from assets.styles import inject_custom_design
    inject_custom_design()
except ImportError:
    pass

try:
    from views.agenda_view import render_agenda_module
    from views.projets_view import render_projets_module
    from views.dev_ia_view import render_dev_ia_module
except ImportError as e:
    st.error(f"Erreur d'importation des modules de vue : {e}")

# Initialisation robuste de l'État Global (Session State)
defaults = {
    "theme_mode": "Sombre Nuit",
    "app_lang": "FR",
    "authenticated": False,
    "direct_agenda": False,
    "agenda_active_tab": "vue",
    "agenda_events": [],
    "saved_ai_prompts": [],
    "saved_claude_prompts": [],
    "saved_code_snippets": [],
    "saved_image_prompts": [],
    "saved_ideas": [],
    "saved_current_projects": [],
    "saved_future_projects": [],
    "saved_links": [],
    "saved_zip_files": [],
    "saved_api_keys": [],
    "saved_user_credentials": [],
    "current_view": "home"
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Gestion des liens directs (ex: ?app=agenda)
query_params = st.query_params
is_direct_agenda_link = query_params.get("app", None) == "agenda"

if is_direct_agenda_link or st.session_state.get("direct_agenda", False):
    render_agenda_module()

elif not st.session_state.authenticated:
    st.markdown('<div style="text-align: center; margin-top: 30px; margin-bottom: 25px;"><h1 style="font-size: 2.8rem; margin-bottom: 5px;"><span style="color: #F8FAFC;">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 10px; border-radius: 8px; font-size: 2rem; margin-left: 6px;">CORE</span></h1><div style="margin-top: 15px;"><span class="zapio-badge">🔮 Espace Sécurisé & Workspace</span></div></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            email = st.text_input("Adresse Email", placeholder="nom@exemple.com")
            master_key = st.text_input("Clé Maîtresse / PIN", type="password", placeholder="••••••••")
            if st.form_submit_button("Se connecter au Workspace"):
                if master_key != "":
                    st.session_state.authenticated = True
                    st.toast("🔓 Connexion réussie au Workspace.", icon="✨")
                    st.rerun()
                else:
                    st.error("Veuillez saisir votre clé d'accès.")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📅 Accéder directement à l'Agenda (Offline)", use_container_width=True, type="secondary"):
            st.session_state.direct_agenda = True
            st.rerun()

else:
    col_logo, col_logout = st.columns([3, 1])
    with col_logo:
        st.markdown('<h1 style="font-size: 1.3rem; margin: 0; display: flex; align-items: center; gap: 4px;"><span style="color: #F8FAFC;">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 5px; border-radius: 6px; font-size: 0.85rem;">CORE</span><span class="zapio-badge-green" style="font-size: 0.55rem;">● Live</span></h1>', unsafe_allow_html=True)
    with col_logout:
        if st.button("🔒 Déconnexion", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.current_view = "home"
            st.toast("🔒 Déconnexion effectuée.", icon="👋")
            st.rerun()

    st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 15px 0 25px 0;'>", unsafe_allow_html=True)

    if st.session_state.current_view == "home":
        st.markdown('''
            <div class="pavel-hero-banner">
                <span class="zapio-badge" style="margin-bottom: 10px; display: inline-block;">🚀 WORKSPACE CENTRALISÉ</span>
                <h2 style="font-size: 2.2rem; color: #FFF; margin: 10px 0 5px 0;">Tableau de Bord Principal</h2>
                <p style="color: #CBD5E1; font-size: 1rem; margin: 0;">Sélectionnez ci-dessous l'espace de travail ou l'outil à lancer</p>
            </div>
        ''', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="pavel-card-grid"><h3 style="color:#FFF; font-size: 1.1rem;">📅 Agenda & Planning</h3><p style="color: #CBD5E1; font-size: 0.8rem;">Calendrier et mode hors-ligne.</p></div>', unsafe_allow_html=True)
            if st.button("Ouvrir l'Agenda", use_container_width=True, type="primary"):
                st.session_state.current_view = "Agenda"
                st.rerun()

            st.markdown('<div class="pavel-card-grid" style="margin-top: 20px;"><h3 style="color:#FFF; font-size: 1.1rem;">💻 Code & IA</h3><p style="color: #CBD5E1; font-size: 0.8rem;">Prompts IA et snippets.</p></div>', unsafe_allow_html=True)
            if st.button("Ouvrir Dev & IA", use_container_width=True):
                st.session_state.current_view = "Dev & IA"
                st.rerun()

        with c2:
            st.markdown('<div class="pavel-card-grid"><h3 style="color:#FFF; font-size: 1.1rem;">🚀 Projets & Idées</h3><p style="color: #CBD5E1; font-size: 0.8rem;">Projets actifs et idées.</p></div>', unsafe_allow_html=True)
            if st.button("Ouvrir Projets", use_container_width=True):
                st.session_state.current_view = "Projets"
                st.rerun()

        # Sauvegarde globale JSON
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("⚙️ Gestion & Sauvegarde Globale du Workspace (Backup JSON)"):
            workspace_data = {
                "agenda_events": [
                    {
                        "title": e["title"],
                        "date": e["date"].strftime("%Y-%m-%d"),
                        "time": e["time"].strftime("%H:%M"),
                        "category": e["category"],
                        "desc": e["desc"],
                        "ringtone": e["ringtone"]
                    } for e in st.session_state.agenda_events
                ],
                "saved_ai_prompts": st.session_state.saved_ai_prompts,
                "saved_claude_prompts": st.session_state.saved_claude_prompts,
                "saved_code_snippets": st.session_state.saved_code_snippets,
                "saved_ideas": st.session_state.saved_ideas,
                "saved_current_projects": st.session_state.saved_current_projects,
                "saved_future_projects": st.session_state.saved_future_projects,
            }
            json_str = json.dumps(workspace_data, indent=4, ensure_ascii=False)
            st.download_button(
                label="📥 Exporter tout le Workspace (.json)",
                data=json_str,
                file_name=f"pavelcore_backup_{date.today().strftime('%Y-%m-%d')}.json",
                mime="application/json",
                use_container_width=True
            )

    else:
        current = st.session_state.current_view
        if st.button("← Retour au Tableau de Bord", key="back_to_home_universal"):
            st.session_state.current_view = "home"
            st.rerun()
            
        st.markdown(f"<h2 style='color: #EC4899; margin-top: 15px;'>Espace : {current}</h2>", unsafe_allow_html=True)

        if current == "Agenda":
            render_agenda_module()
        elif current == "Projets":
            render_projets_module()
        elif current == "Dev & IA":
            render_dev_ia_module()
