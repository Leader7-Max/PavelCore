import sys
import os
import re
import calendar
import json
import base64
import streamlit as st
import pandas as pd
from datetime import datetime, date, time

# Correctif pour Streamlit Cloud
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration de la page
st.set_page_config(
    page_title="PavelCore — Workspace & Agenda Premium",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

try:
    from assets.styles import inject_custom_design
    inject_custom_design()
except ImportError:
    pass

# Gestionnaire d'État Global (Initialisation robuste)
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Sombre Nuit"

if "app_lang" not in st.session_state:
    st.session_state.app_lang = "FR"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "direct_agenda" not in st.session_state:
    st.session_state.direct_agenda = False

if "agenda_active_tab" not in st.session_state:
    st.session_state.agenda_active_tab = "vue"

if "agenda_events" not in st.session_state:
    st.session_state.agenda_events = []

if "saved_ai_prompts" not in st.session_state:
    st.session_state.saved_ai_prompts = []

if "saved_claude_prompts" not in st.session_state:
    st.session_state.saved_claude_prompts = []

if "saved_code_snippets" not in st.session_state:
    st.session_state.saved_code_snippets = []

if "saved_image_prompts" not in st.session_state:
    st.session_state.saved_image_prompts = []

if "saved_ideas" not in st.session_state:
    st.session_state.saved_ideas = []

if "saved_current_projects" not in st.session_state:
    st.session_state.saved_current_projects = []

if "saved_future_projects" not in st.session_state:
    st.session_state.saved_future_projects = []

if "saved_links" not in st.session_state:
    st.session_state.saved_links = []

if "saved_zip_files" not in st.session_state:
    st.session_state.saved_zip_files = []

if "saved_api_keys" not in st.session_state:
    st.session_state.saved_api_keys = []

if "saved_user_credentials" not in st.session_state:
    st.session_state.saved_user_credentials = []

if "current_view" not in st.session_state:
    st.session_state.current_view = "home"

# Couleurs dynamiques
if st.session_state.theme_mode == "Blanc Épuré":
    bg_app = "#F8FAFC"
    text_color = "#0F172A"
    card_bg = "#FFFFFF"
    card_border = "#E2E8F0"
    card_gradient = "linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%)"
    header_box_bg = "#F1F5F9"
    header_box_text = "#475569"
    desc_color = "#475569"
    sub_title_color = "#0F172A"
    hero_bg = "linear-gradient(135deg, rgba(236, 72, 153, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%)"
else:
    bg_app = "#0E031C"
    text_color = "#F8FAFC"
    card_bg = "#170A2E"
    card_border = "#2B1552"
    card_gradient = "linear-gradient(135deg, #1A0B36 0%, #120524 100%)"
    header_box_bg = "#1E0A3C"
    header_box_text = "#A78BFA"
    desc_color = "#CBD5E1"
    sub_title_color = "#FFF"
    hero_bg = "linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%)"

# Styles CSS (Grille CSS fluide pour le calendrier)
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_app} !important;
        color: {text_color} !important;
    }}
    .pavel-hero-banner {{
        background: {hero_bg};
        border: 1px solid rgba(236, 72, 153, 0.25);
        border-radius: 18px;
        padding: 30px 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }}
    .sub-section-header {{
        background: {hero_bg};
        border-left: 5px solid #EC4899;
        padding: 15px 20px;
        border-radius: 0 12px 12px 0;
        margin-bottom: 25px;
        margin-top: 10px;
    }}
    .pavel-card-grid {{
        background: {card_gradient};
        border: 1px solid {card_border};
        border-radius: 14px;
        padding: 25px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        margin-bottom: 15px;
    }}
    .pavel-card-grid:hover {{
        transform: translateY(-4px);
        border-color: #EC4899;
        box-shadow: 0 10px 35px rgba(236, 72, 153, 0.18);
    }}
    .zapio-badge {{
        background: rgba(236, 72, 153, 0.1);
        color: #DB2777;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid rgba(236, 72, 153, 0.2);
    }}
    .zapio-badge-green {{
        background: rgba(16, 185, 129, 0.1);
        color: #059669;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }}
    .zapio-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.03);
    }}
    .calendar-grid-container {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 6px;
        width: 100%;
    }}
    .calendar-header-box {{
        background: {header_box_bg};
        color: {header_box_text};
        text-align: center;
        padding: 8px 2px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        border: 1px solid {card_border};
    }}
    .calendar-day-box {{
        min-height: 85px;
        border-radius: 8px;
        padding: 6px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        box-sizing: border-box;
    }}
    div[data-testid="stPills"] button {{
        background-color: {card_bg} !important;
        border: 1px solid {card_border} !important;
        color: {text_color} !important;
        border-radius: 8px !important;
        font-weight: 500;
    }}
    div[data-testid="stPills"] button[aria-selected="true"] {{
        background-color: #EC4899 !important;
        border-color: #EC4899 !important;
        color: #FFF !important;
    }}
    </style>
""", unsafe_allow_html=True)

MONTH_NAMES_FR = [
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]

def render_agenda_module():
    query_params = st.query_params
    if st.session_state.get("direct_agenda", False) or query_params.get("app", None) == "agenda":
        if st.button("← Retour / Quitter l'Agenda", key="back_from_direct_agenda", type="secondary"):
            st.session_state.direct_agenda = False
            st.rerun()

    st.markdown(f'<div style="margin-top: 10px; margin-bottom: 20px;"><span class="zapio-badge">📅 AGENDA AUTONOME & HORS-LIGNE</span><h2 style="margin-top: 10px; font-size: 2rem; color: {sub_title_color};">Agenda & Calendrier Interactif</h2></div>', unsafe_allow_html=True)
    col_btn1, col_btn2, col_clear = st.columns([2.3, 2.5, 2])
    
    with col_btn1:
        if st.button("📅 Vue Calendrier", type="primary" if st.session_state.agenda_active_tab == "vue" else "secondary", use_container_width=True, key="nav_btn_vue"):
            st.session_state.agenda_active_tab = "vue"
            st.rerun()

    with col_btn2:
        if st.button("➕ Programmer", type="primary" if st.session_state.agenda_active_tab == "add" else "secondary", use_container_width=True, key="nav_btn_add"):
            st.session_state.agenda_active_tab = "add"
            st.rerun()

    with col_clear:
        if st.session_state.agenda_events:
            if st.button("🗑️ Vider tout", key="clear_all_events"):
                st.session_state.agenda_events = []
                st.toast("🗑️ Agenda vidé avec succès.", icon="ℹ️")
                st.rerun()

    st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

    if st.session_state.agenda_active_tab == "vue":
        today = date.today()
        current_year = today.year
        available_years = list(range(2025, current_year + 15))
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            selected_month_idx = st.selectbox("Mois", range(1, 13), format_func=lambda x: MONTH_NAMES_FR[x-1], index=today.month - 1)
        with col_m2:
            default_year_idx = available_years.index(current_year) if current_year in available_years else 1
            selected_year = st.selectbox("Année", available_years, index=default_year_idx)

        st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
        
        # En-têtes des jours en Grid pur aligné mobile
        days_header = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        header_html = "".join([f'<div class="calendar-header-box">{h}</div>' for h in days_header])

        events_by_day = {}
        for ev in st.session_state.agenda_events:
            if ev['date'].month == selected_month_idx and ev['date'].year == selected_year:
                day_num = ev['date'].day
                if day_num not in events_by_day:
                    events_by_day[day_num] = []
                events_by_day[day_num].append(ev)

        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(selected_year, selected_month_idx)

        cells_html = ""
        for week in month_days:
            for day_num in week:
                if day_num == 0:
                    cells_html += '<div class="calendar-day-box" style="background:rgba(100,100,100,0.05); opacity:0.15; border:1px solid transparent;"></div>'
                else:
                    is_today = (day_num == today.day and selected_month_idx == today.month and selected_year == today.year)
                    day_events = events_by_day.get(day_num, [])
                    border_color = "#EC4899" if is_today else "#8B5CF6"
                    bg_color = "linear-gradient(135deg, #3B1578 0%, #261245 100%)" if is_today else card_bg
                    
                    max_visible_events = 2
                    visible_events = day_events[:max_visible_events]
                    hidden_count = len(day_events) - max_visible_events

                    event_html = ""
                    for ev_item in visible_events:
                        event_html += f'<div style="background:#F43F5E; color:#FFF; font-size:0.55rem; font-weight:800; border-radius:3px; padding:1px 3px; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">⏰ {ev_item["time"].strftime("%H:%M")} - {ev_item["title"]}</div>'
                    if hidden_count > 0:
                        event_html += f'<div style="background:#A78BFA; color:#1E0A3C; font-size:0.5rem; font-weight:800; border-radius:3px; padding:1px; margin-top:1px; text-align:center;">+{hidden_count}</div>'

                    day_marker = '📌' if is_today else ''
                    day_color = '#EC4899' if is_today else text_color
                    
                    cells_html += f'''
                        <div class="calendar-day-box" style="background:{bg_color}; border:1px solid {border_color};">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span style="font-weight:800; font-size:0.8rem; color:{day_color};">{day_num} {day_marker}</span>
                            </div>
                            {event_html}
                        </div>
                    '''

        # Rendu unifié Grid pour un alignement parfait sur smartphone et PC
        st.markdown(f'''
            <div class="calendar-grid-container" style="margin-bottom: 6px;">
                {header_html}
            </div>
            <div class="calendar-grid-container">
                {cells_html}
            </div>
        ''', unsafe_allow_html=True)

    elif st.session_state.agenda_active_tab == "add":
        with st.form("add_event_form", clear_on_submit=True):
            st.markdown(f"<h3 style='color: {sub_title_color};'>Planifier une nouvelle date</h3>", unsafe_allow_html=True)
            title = st.text_input("Titre de l'événement / Rappel", placeholder="Ex: Prestation DJ / Réunion")
            c_date, c_time = st.columns(2)
            with c_date:
                event_date = st.date_input("Date", value=date.today())
            with c_time:
                event_time = st.time_input("Heure exacte", value=time(12, 0))
            c_cat, c_ring = st.columns(2)
            with c_cat:
                category = st.selectbox("Catégorie", ["Business / Travail", "Dev & Tech", "Personnel", "Rendez-vous Urgent", "Événement DJ / Prestation"])
            with c_ring:
                ringtone = st.selectbox("Sonnerie", ["Alarme Digitale", "Bip Futuriste", "Douce Mélodie", "Silence"])
            desc = st.text_area("Notes complémentaires")
            if st.form_submit_button("🔔 Ajouter au Calendrier"):
                if title:
                    st.session_state.agenda_events.append({"title": title, "date": event_date, "time": event_time, "category": category, "desc": desc, "ringtone": ringtone})
                    st.session_state.agenda_active_tab = "vue"
                    st.toast("✅ Événement ajouté avec succès dans l'agenda !", icon="🎉")
                    st.rerun()
                else:
                    st.warning("Veuillez saisir un titre pour l'événement.")

# AUTH & NAVIGATION
query_params = st.query_params
is_direct_agenda_link = query_params.get("app", None) == "agenda"

if is_direct_agenda_link or st.session_state.get("direct_agenda", False):
    render_agenda_module()

elif not st.session_state.authenticated:
    st.markdown(f'<div style="text-align: center; margin-top: 30px; margin-bottom: 25px;"><h1 style="font-size: 2.8rem; margin-bottom: 5px;"><span style="color: {text_color};">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 10px; border-radius: 8px; font-size: 2rem; margin-left: 6px;">CORE</span></h1><div style="margin-top: 15px;"><span class="zapio-badge">🔮 Espace Sécurisé & Workspace</span></div></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            email = st.text_input("Adresse Email", placeholder="nom@exemple.com")
            master_key = st.text_input("Clé Maîtresse / PIN", type="password", placeholder="••••••••")
            submit = st.form_submit_button("Se connecter au Workspace")
            if submit:
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
        st.markdown(f'<h1 style="font-size: 1.3rem; margin: 0; display: flex; align-items: center; gap: 4px;"><span style="color: {text_color};">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 5px; border-radius: 6px; font-size: 0.85rem;">CORE</span><span class="zapio-badge-green" style="font-size: 0.55rem;">● Live</span></h1>', unsafe_allow_html=True)
    with col_logout:
        if st.button("🔒 Déconnexion", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.current_view = "home"
            st.toast("🔒 Déconnexion effectuée.", icon="👋")
            st.rerun()

    st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 15px 0 25px 0;'>", unsafe_allow_html=True)

    if st.session_state.current_view == "home":
        st.markdown(f'''
            <div class="pavel-hero-banner">
                <span class="zapio-badge" style="margin-bottom: 10px; display: inline-block;">🚀 WORKSPACE CENTRALISÉ</span>
                <h2 style="font-size: 2.2rem; color: {sub_title_color}; margin: 10px 0 5px 0;">Tableau de Bord Principal</h2>
                <p style="color: {desc_color}; font-size: 1rem; margin: 0;">Sélectionnez ci-dessous l'espace de travail ou l'outil à lancer</p>
            </div>
        ''', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="pavel-card-grid"><h3 style="color:{sub_title_color}; font-size: 1.1rem;">📅 Agenda & Planning</h3><p style="color: {desc_color}; font-size: 0.8rem;">Calendrier et mode hors-ligne.</p></div>', unsafe_allow_html=True)
            if st.button("Ouvrir l'Agenda", use_container_width=True, type="primary"):
                st.session_state.current_view = "Agenda"
                st.rerun()

            st.markdown(f'<div class="pavel-card-grid" style="margin-top: 20px;"><h3 style="color:{sub_title_color}; font-size: 1.1rem;">💻 Code & IA</h3><p style="color: {desc_color}; font-size: 0.8rem;">Prompts IA et snippets.</p></div>', unsafe_allow_html=True)
            if st.button("Ouvrir Dev & IA", use_container_width=True):
                st.session_state.current_view = "Dev & IA"
                st.rerun()

            st.markdown(f'<div class="pavel-card-grid" style="margin-top: 20px;"><h3 style="color:{sub_title_color}; font-size: 1.1rem;">🎨 Médias & Ressources</h3><p style="color: {desc_color}; font-size: 0.8rem;">Images, liens et ZIP.</p></div>', unsafe_allow_html=True)
            if st.button("Ouvrir Ressources", use_container_width=True):
                st.session_state.current_view = "Ressources"
                st.rerun()

        with c2:
            st.markdown(f'<div class="pavel-card-grid"><h3 style="color:{sub_title_color}; font-size: 1.1rem;">🚀 Projets & Idées</h3><p style="color: {desc_color}; font-size: 0.8rem;">Projets actifs et idées.</p></div>', unsafe_allow_html=True)
            if st.button("Ouvrir Projets", use_container_width=True):
                st.session_state.current_view = "Projets"
                st.rerun()

            st.markdown(f'<div class="pavel-card-grid" style="margin-top: 20px;"><h3 style="color:{sub_title_color}; font-size: 1.1rem;">🔐 Coffre-Fort Sécurisé</h3><p style="color: {desc_color}; font-size: 0.8rem;">Clés API et mots de passe.</p></div>', unsafe_allow_html=True)
            if st.button("Ouvrir le Coffre-Fort", use_container_width=True):
                st.session_state.current_view = "Coffre-Fort"
                st.rerun()

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
                "saved_image_prompts": st.session_state.saved_image_prompts,
                "saved_ideas": st.session_state.saved_ideas,
                "saved_current_projects": st.session_state.saved_current_projects,
                "saved_future_projects": st.session_state.saved_future_projects,
                "saved_links": st.session_state.saved_links,
                "saved_zip_files": st.session_state.saved_zip_files,
                "saved_api_keys": st.session_state.saved_api_keys,
                "saved_user_credentials": st.session_state.saved_user_credentials
            }
            json_str = json.dumps(workspace_data, indent=4, ensure_ascii=False)
            
            c_exp, c_imp = st.columns(2)
            with c_exp:
                st.download_button(
                    label="📥 Exporter tout le Workspace (.json)",
                    data=json_str,
                    file_name=f"pavelcore_backup_{date.today().strftime('%Y-%m-%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            with c_imp:
                uploaded_backup = st.file_uploader("📤 Restaurer une sauvegarde (.json)", type=["json"], key="backup_uploader")
                if uploaded_backup is not None:
                    try:
                        imported_data = json.load(uploaded_backup)
                        st.session_state.saved_ai_prompts = imported_data.get("saved_ai_prompts", [])
                        st.session_state.saved_claude_prompts = imported_data.get("saved_claude_prompts", [])
                        st.session_state.saved_code_snippets = imported_data.get("saved_code_snippets", [])
                        st.session_state.saved_image_prompts = imported_data.get("saved_image_prompts", [])
                        st.session_state.saved_ideas = imported_data.get("saved_ideas", [])
                        st.session_state.saved_current_projects = imported_data.get("saved_current_projects", [])
                        st.session_state.saved_future_projects = imported_data.get("saved_future_projects", [])
                        st.session_state.saved_links = imported_data.get("saved_links", [])
                        st.session_state.saved_zip_files = imported_data.get("saved_zip_files", [])
                        st.session_state.saved_api_keys = imported_data.get("saved_api_keys", [])
                        st.session_state.saved_user_credentials = imported_data.get("saved_user_credentials", [])
                        
                        restored_events = []
                        for ev in imported_data.get("agenda_events", []):
                            restored_events.append({
                                "title": ev["title"],
                                "date": datetime.strptime(ev["date"], "%Y-%m-%d").date(),
                                "time": datetime.strptime(ev["time"], "%H:%M").time(),
                                "category": ev["category"],
                                "desc": ev["desc"],
                                "ringtone": ev["ringtone"]
                            })
                        st.session_state.agenda_events = restored_events
                        st.toast("✅ Restauration du Workspace réussie !", icon="🎉")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur lors de l'importation du fichier : {e}")

    else:
        current = st.session_state.current_view
        if st.button("← Retour au Tableau de Bord", key="back_to_home_universal"):
            st.session_state.current_view = "home"
            st.rerun()
            
        st.markdown(f"<h2 style='color: #EC4899; margin-top: 15px;'>Espace : {current}</h2>", unsafe_allow_html=True)

        if current == "Agenda":
            render_agenda_module()

        elif current == "Projets":
            sub_tab = st.pills(
                "Navigation Projets",
                options=["🚀 Projets en cours", "🔮 Projets futurs", "💡 Idées"],
                default="🚀 Projets en cours",
                label_visibility="collapsed"
            )
            
            if sub_tab == "🚀 Projets en cours":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">SUIVI OPÉRATIONNEL</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🚀 Projets en cours</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_curr_proj", clear_on_submit=True):
                    name = st.text_input("Nom du projet")
                    client = st.text_input("Client / Marque")
                    priority = st.selectbox("Priorité", ["🔴 Haute", "🟠 Moyenne", "🟢 Basse"])
                    next_step = st.text_input("Prochaine étape")
                    deadline = st.date_input("Date limite")
                    project_desc = st.text_area("Description")
                    if st.form_submit_button("Enregistrer"):
                        if name:
                            st.session_state.saved_current_projects.append({"name": name, "client": client, "priority": priority, "next": next_step, "deadline": str(deadline), "desc": project_desc})
                            st.toast("🚀 Projet en cours enregistré avec succès !", icon="✅")
                            st.rerun()
                        else:
                            st.warning("Veuillez renseigner le nom du projet.")
                for cp in st.session_state.saved_current_projects:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{cp["name"]}</h3><p style="color:{desc_color};">Client: {cp["client"]} | Échéance: {cp["deadline"]}</p></div>', unsafe_allow_html=True)

            elif sub_tab == "🔮 Projets futurs":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">VISION & ROADMAP</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🔮 Projets futurs</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_fut_proj", clear_on_submit=True):
                    name = st.text_input("Nom du projet futur")
                    horizon = st.selectbox("Horizon", ["Court terme", "Moyen terme", "Long terme"])
                    resources = st.text_area("Ressources requises")
                    goal = st.text_input("Objectif")
                    if st.form_submit_button("Ajouter"):
                        if name:
                            st.session_state.saved_future_projects.append({"name": name, "horizon": horizon, "resources": resources, "goal": goal})
                            st.toast("🔮 Projet futur ajouté avec succès !", icon="✨")
                            st.rerun()
                        else:
                            st.warning("Veuillez renseigner le nom du projet futur.")
                for fp in st.session_state.saved_future_projects:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{fp["name"]}</h3><p style="color:{desc_color};">Objectif: {fp["goal"]}</p></div>', unsafe_allow_html=True)

            elif sub_tab == "💡 Idées":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">INSPIRATION & CONCEPTS</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">💡 Boîte à Idées</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_ideas", clear_on_submit=True):
                    title = st.text_input("Titre de l'idée")
                    category = st.selectbox("Domaine", ["Business", "Tech", "DJ", "Personnel"])
                    description = st.text_area("Description")
                    impact = st.select_slider("Impact", options=["Faible", "Moyen", "Fort", "Révolutionnaire !"])
                    if st.form_submit_button("Sauvegarder"):
                        if title:
                            st.session_state.saved_ideas.append({"title": title, "cat": category, "desc": description, "impact": impact})
                            st.toast("💡 Idée sauvegardée avec succès !", icon="💡")
                            st.rerun()
                        else:
                            st.warning("Veuillez renseigner un titre.")
                for id_item in st.session_state.saved_ideas:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{id_item["title"]}</h3><p style="color:{desc_color};">{id_item["desc"]}</p></div>', unsafe_allow_html=True)

        elif current == "Dev & IA":
            sub_tab = st.pills(
                "Navigation Dev",
                options=["🤖 Prompts AI Code", "🧠 Prompts Claude", "💻 Snippets Code"],
                default="🤖 Prompts AI Code",
                label_visibility="collapsed"
            )
            if sub_tab == "🤖 Prompts AI Code":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">INTELLIGENCE ARTIFICIELLE</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🤖 Prompts AI Code</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_ai_code", clear_on_submit=True):
                    title = st.text_input("Titre")
                    prompt = st.text_area("Contenu du Prompt")
                    if st.form_submit_button("Enregistrer"):
                        if title and prompt:
                            st.session_state.saved_ai_prompts.append({"title": title, "lang": "python", "prompt": prompt})
                            st.toast("🤖 Prompt IA enregistré !", icon="✅")
                            st.rerun()
                        else:
                            st.warning("Veuillez remplir tous les champs.")
                for p in st.session_state.saved_ai_prompts:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{p["title"]}</h3>', unsafe_allow_html=True)
                    st.code(p['prompt'], language=p['lang'])
                    st.markdown('</div>', unsafe_allow_html=True)

            elif sub_tab == "🧠 Prompts Claude":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">EXPERTISE & SYSTEM PROMPTS</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🧠 Prompts Claude</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_claude", clear_on_submit=True):
                    title = st.text_input("Titre")
                    user_prompt = st.text_area("User Prompt")
                    if st.form_submit_button("Sauvegarder"):
                        if title and user_prompt:
                            st.session_state.saved_claude_prompts.append({"title": title, "user": user_prompt})
                            st.toast("🧠 Prompt Claude sauvegardé !", icon="✅")
                            st.rerun()
                        else:
                            st.warning("Veuillez remplir tous les champs.")
                for c in st.session_state.saved_claude_prompts:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{c["title"]}</h3>', unsafe_allow_html=True)
                    st.code(c['user'], language='python')
                    st.markdown('</div>', unsafe_allow_html=True)

            elif sub_tab == "💻 Snippets Code":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">BIBLIOTHÈQUE DE CODE</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">💻 Snippets de Code</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_code", clear_on_submit=True):
                    title = st.text_input("Nom")
                    code_content = st.text_area("Code")
                    if st.form_submit_button("Enregistrer"):
                        if title and code_content:
                            st.session_state.saved_code_snippets.append({"title": title, "code": code_content})
                            st.toast("💻 Snippet de code enregistré !", icon="✅")
                            st.rerun()
                        else:
                            st.warning("Veuillez remplir tous les champs.")
                for cd in st.session_state.saved_code_snippets:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{cd["title"]}</h3>', unsafe_allow_html=True)
                    st.code(cd['code'], language='python')
                    st.markdown('</div>', unsafe_allow_html=True)
