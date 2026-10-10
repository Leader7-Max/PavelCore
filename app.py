import sys
import os
import re
import calendar
import json
import base64
import streamlit as st
import streamlit.components.v1 as components
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

# Dossier local pour le stockage des fichiers uploadés
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploaded_files")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Gestionnaire d'État Global
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Sombre Nuit"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "direct_agenda" not in st.session_state:
    st.session_state.direct_agenda = False

if "agenda_active_tab" not in st.session_state:
    st.session_state.agenda_active_tab = "vue"

if "agenda_events" not in st.session_state:
    st.session_state.agenda_events = []

if "saved_prompts_library" not in st.session_state:
    st.session_state.saved_prompts_library = [
        {
            "title": "Flyer Événement Afro/DJ Ultra Réaliste",
            "category": "🎨 Génération d'images (Midjourney, DALL-E, Flux)",
            "prompt": "High-energy promotional flyer for an Afro-Fusion DJ event, neon magenta and deep violet lighting, gold accents, professional typography, cinematic atmosphere, 8k resolution, photorealistic, octane render --ar 4:5"
        },
        {
            "title": "Inpainting - Modification de fond de flyer",
            "category": "✏️ Modification & Retouche d'images",
            "prompt": "Isolate subject, replace background with a dark futuristic DJ booth filled with glowing purple lasers and subtle smoke machine haze, smooth blending"
        },
        {
            "title": "Refactoring Application Python Streamlit",
            "category": "🤖 Développement & Code AI",
            "prompt": "Refactor the following Python Streamlit code to use a modular architecture with separate views, clean session state initialization, and CSS Grid layout for responsiveness."
        },
        {
            "title": "Chanson Afrobeat / Bikutsi Anniversaire",
            "category": "🎵 Création Musicale & Paroles (Suno, Udio)",
            "prompt": "[Style: Afrobeat, Bikutsi, Uptempo 120 BPM, Energetic Brass, Lead Guitar, Cheerful Choirs]\n[Verse 1]\nAujourd'hui c'est la fête, on célèbre avec joie,\nLa famille rassemblée, pour chanter avec toi...\n[Chorus]\nJoyeux anniversaire, santé et bonheur !"
        }
    ]

if "saved_code_snippets" not in st.session_state:
    st.session_state.saved_code_snippets = []

if "saved_ideas" not in st.session_state:
    st.session_state.saved_ideas = []

if "saved_current_projects" not in st.session_state:
    st.session_state.saved_current_projects = []

if "saved_future_projects" not in st.session_state:
    st.session_state.saved_future_projects = []

if "saved_links" not in st.session_state:
    st.session_state.saved_links = []

if "saved_media_files" not in st.session_state:
    st.session_state.saved_media_files = []

if "saved_api_keys" not in st.session_state:
    st.session_state.saved_api_keys = []

if "saved_user_credentials" not in st.session_state:
    st.session_state.saved_user_credentials = []

if "saved_contacts" not in st.session_state:
    st.session_state.saved_contacts = []

if "saved_email_templates" not in st.session_state:
    st.session_state.saved_email_templates = []

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
    bg_app = "#090114"
    text_color = "#F8FAFC"
    card_bg = "linear-gradient(135deg, #1A0B36 0%, #120524 100%)"
    card_border = "rgba(139, 92, 246, 0.25)"
    card_gradient = "linear-gradient(135deg, #1F0D3D 0%, #100421 100%)"
    header_box_bg = "#1E0A3C"
    header_box_text = "#A78BFA"
    desc_color = "#CBD5E1"
    sub_title_color = "#FFF"
    hero_bg = "linear-gradient(135deg, rgba(236, 72, 153, 0.18) 0%, rgba(139, 92, 246, 0.18) 100%)"

# Styles CSS globaux : Effets de lueurs néons, fonds travaillés et design mobile sur-mesure
st.markdown(f"""
    <style>
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(6px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .stApp {{
        background-color: {bg_app} !important;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(139, 92, 246, 0.12) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(236, 72, 153, 0.12) 0%, transparent 40%) !important;
        background-attachment: fixed !important;
        color: {text_color} !important;
        animation: fadeIn 0.3s ease-in-out;
    }}
    .block-container {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 2rem !important;
        max-width: 100% !important;
    }}
    .pavel-hero-banner {{
        background: {hero_bg};
        border: 1px solid rgba(236, 72, 153, 0.35);
        border-radius: 18px;
        padding: 22px 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.15);
        backdrop-filter: blur(10px);
    }}
    .sub-section-header {{
        background: {hero_bg};
        border-left: 4px solid #EC4899;
        padding: 12px 15px;
        border-radius: 0 10px 10px 0;
        margin-bottom: 20px;
        margin-top: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    .pavel-card-grid {{
        background: {card_gradient};
        border: 1px solid {card_border};
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        margin-bottom: 12px;
        backdrop-filter: blur(5px);
    }}
    .pavel-card-grid:hover {{
        transform: translateY(-4px);
        border-color: #EC4899;
        box-shadow: 0 12px 30px rgba(236, 72, 153, 0.3);
    }}
    .zapio-badge {{
        background: rgba(236, 72, 153, 0.15);
        color: #F472B6;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid rgba(236, 72, 153, 0.3);
    }}
    .zapio-badge-green {{
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    .zapio-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.25s ease;
    }}
    .zapio-card:hover {{
        border-color: #8B5CF6;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.25);
    }}
    div[data-testid="stPills"] button {{
        background-color: #170A2E !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        color: {text_color} !important;
        border-radius: 8px !important;
        font-weight: 500;
        font-size: 0.85rem !important;
    }}
    div[data-testid="stPills"] button[aria-selected="true"] {{
        background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
        border-color: transparent !important;
        color: #FFF !important;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4);
    }}
    /* Boutons modernes avec dégradé subtil */
    .stButton button {{
        width: 100% !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        background: linear-gradient(135deg, #1E0A3C 0%, #2A1052 100%) !important;
        border: 1px solid rgba(139, 92, 246, 0.4) !important;
        color: #F8FAFC !important;
        transition: all 0.3s ease !important;
    }}
    .stButton button:hover {{
        background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
        border-color: #EC4899 !important;
        box-shadow: 0 5px 20px rgba(236, 72, 153, 0.4);
    }}
    </style>
""", unsafe_allow_html=True)

MONTH_NAMES_FR = [
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]

PROMPT_CATEGORIES = [
    "🎨 Génération d'images (Midjourney, DALL-E, Flux)",
    "✏️ Modification & Retouche d'images",
    "🤖 Développement & Code AI",
    "🧠 System Prompts (Claude & ChatGPT)",
    "🎵 Création Musicale & Paroles (Suno, Udio)",
    "📝 Rédaction de Contenu & Marketing"
]

def render_global_search():
    st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)
    search_query = st.text_input("⚡ Recherche Rapide Universelle", placeholder="🔍 Mot-clé (ex: Flyer, Python, DJ, Client...)", key="global_search_input")
    
    if search_query.strip():
        q = search_query.strip().lower()
        results_count = 0
        st.markdown(f"### 🔎 Résultats : *'{search_query}'*")

        matched_prompts = [p for p in st.session_state.saved_prompts_library if q in p["title"].lower() or q in p["prompt"].lower() or q in p["category"].lower()]
        if matched_prompts:
            st.markdown("#### 🧠 Prompts & IA")
            for item in matched_prompts:
                results_count += 1
                st.markdown(f'<div class="zapio-card"><span class="zapio-badge">{item["category"]}</span><h4 style="margin-top:5px;">{item["title"]}</h4>', unsafe_allow_html=True)
                st.code(item["prompt"], language="markdown")
                st.markdown('</div>', unsafe_allow_html=True)

        matched_files = [f for f in st.session_state.saved_media_files if q in f["title"].lower() or q in f.get("filename", "").lower() or q in f.get("type", "").lower() or q in f.get("desc", "").lower()]
        if matched_files:
            st.markdown("#### 📁 Médias & Fichiers")
            for item in matched_files:
                results_count += 1
                st.markdown(f'<div class="zapio-card"><span class="zapio-badge">{item["type"]}</span><h4 style="margin-top:5px;">{item["title"]}</h4></div>', unsafe_allow_html=True)

        matched_events = [e for e in st.session_state.agenda_events if q in e["title"].lower() or q in e.get("desc", "").lower() or q in e.get("category", "").lower()]
        if matched_events:
            st.markdown("#### 📅 Agenda & Événements")
            for item in matched_events:
                results_count += 1
                st.markdown(f'<div class="zapio-card"><span class="zapio-badge">{item["category"]}</span><h4 style="margin-top:5px;">{item["title"]}</h4><p>Date: {item["date"]} à {item["time"]}</p></div>', unsafe_allow_html=True)

        matched_contacts = [c for c in st.session_state.saved_contacts if q in c["name"].lower() or q in c.get("email", "").lower() or q in c.get("phone", "").lower() or q in c.get("notes", "").lower()]
        if matched_contacts:
            st.markdown("#### 🎴 Contacts")
            for item in matched_contacts:
                results_count += 1
                st.markdown(f'<div class="zapio-card"><span class="zapio-badge">{item["cat"]}</span><h4 style="margin-top:5px;">{item["name"]}</h4><p>📧 {item["email"]} | 📞 {item["phone"]}</p></div>', unsafe_allow_html=True)

        matched_projects = [p for p in st.session_state.saved_current_projects + st.session_state.saved_future_projects if q in p["name"].lower() or q in p.get("desc", "").lower() or q in p.get("client", "").lower()]
        if matched_projects:
            st.markdown("#### 🚀 Projets")
            for item in matched_projects:
                results_count += 1
                st.markdown(f'<div class="zapio-card"><h4 style="margin-top:5px;">{item["name"]}</h4></div>', unsafe_allow_html=True)

        if results_count == 0:
            st.warning("Aucun élément ne correspond à votre recherche.")
        st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 20px 0;'>", unsafe_allow_html=True)

def render_agenda_module():
    query_params = st.query_params
    if st.session_state.get("direct_agenda", False) or query_params.get("app", None) == "agenda":
        if st.button("← Retour / Quitter l'Agenda", key="back_from_direct_agenda", type="secondary"):
            st.session_state.direct_agenda = False
            st.rerun()

    st.markdown(f'<div style="margin-top: 10px; margin-bottom: 15px;"><span class="zapio-badge">📅 AGENDA AUTONOME & HORS-LIGNE</span><h2 style="margin-top: 8px; font-size: 1.6rem; color: {sub_title_color};">Agenda & Calendrier Interactif</h2></div>', unsafe_allow_html=True)
    col_btn1, col_btn2, col_clear = st.columns([2, 2, 1.5])
    
    with col_btn1:
        if st.button("📅 Vue", type="primary" if st.session_state.agenda_active_tab == "vue" else "secondary", use_container_width=True, key="nav_btn_vue"):
            st.session_state.agenda_active_tab = "vue"
            st.rerun()

    with col_btn2:
        if st.button("➕ Ajouter", type="primary" if st.session_state.agenda_active_tab == "add" else "secondary", use_container_width=True, key="nav_btn_add"):
            st.session_state.agenda_active_tab = "add"
            st.rerun()

    with col_clear:
        if st.session_state.agenda_events:
            if st.button("🗑️ Vider", key="clear_all_events"):
                st.session_state.agenda_events = []
                st.toast("🗑️ Agenda vidé avec succès.", icon="ℹ️")
                st.rerun()

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

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

        st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)
        
        days_header = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        header_html = "".join([f'<div style="background:{header_box_bg}; color:{header_box_text}; text-align:center; padding:5px 1px; border-radius:4px; font-weight:700; font-size:0.65rem; border:1px solid {card_border}; box-sizing:border-box;">{h}</div>' for h in days_header])

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
                    cells_html += '<div style="min-height:55px; border-radius:5px; padding:3px; background:rgba(100,100,100,0.03); opacity:0.15; border:1px solid transparent; box-sizing:border-box;"></div>'
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
                        event_html += f'<div style="background:#F43F5E; color:#FFF; font-size:0.4rem; font-weight:800; border-radius:2px; padding:1px; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">⏰ {ev_item["time"].strftime("%H:%M")}</div>'
                    if hidden_count > 0:
                        event_html += f'<div style="background:#A78BFA; color:#1E0A3C; font-size:0.35rem; font-weight:800; border-radius:2px; padding:1px; margin-top:1px; text-align:center;">+{hidden_count}</div>'

                    day_marker = '📌' if is_today else ''
                    day_color = '#EC4899' if is_today else text_color
                    
                    cells_html += f'''
                        <div style="min-height:55px; border-radius:5px; padding:3px; background:{bg_color}; border:1px solid {border_color}; display:flex; flex-direction:column; justify-content:flex-start; box-sizing:border-box;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span style="font-weight:800; font-size:0.7rem; color:{day_color};">{day_num} {day_marker}</span>
                            </div>
                            {event_html}
                        </div>
                    '''

        calendar_full_html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    background-color: transparent;
                    margin: 0;
                    padding: 0;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                }}
                .calendar-grid {{
                    display: grid !important;
                    grid-template-columns: repeat(7, 1fr) !important;
                    gap: 3px !important;
                    width: 100% !important;
                    box-sizing: border-box !important;
                }}
            </style>
        </head>
        <body>
            <div class="calendar-grid">
                {header_html}
                {cells_html}
            </div>
        </body>
        </html>
        '''
        components.html(calendar_full_html, height=380, scrolling=False)

    elif st.session_state.agenda_active_tab == "add":
        with st.form("add_event_form", clear_on_submit=True):
            st.markdown(f"<h3 style='color: {sub_title_color}; font-size: 1.3rem;'>Planifier un événement</h3>", unsafe_allow_html=True)
            title = st.text_input("Titre de l'événement / Rappel", placeholder="Ex: Prestation DJ")
            c_date, c_time = st.columns(2)
            with c_date:
                event_date = st.date_input("Date", value=date.today())
            with c_time:
                event_time = st.time_input("Heure", value=time(12, 0))
            category = st.selectbox("Catégorie", ["Business / Travail", "Dev & Tech", "Personnel", "Rendez-vous Urgent", "Événement DJ / Prestation"])
            ringtone = st.selectbox("Sonnerie", ["Alarme Digitale", "Bip Futuriste", "Douce Mélodie", "Silence"])
            desc = st.text_area("Notes complémentaires")
            if st.form_submit_button("🔔 Ajouter au Calendrier"):
                if title:
                    st.session_state.agenda_events.append({"title": title, "date": event_date, "time": event_time, "category": category, "desc": desc, "ringtone": ringtone})
                    st.session_state.agenda_active_tab = "vue"
                    st.toast("✅ Événement ajouté avec succès !", icon="🎉")
                    st.rerun()
                else:
                    st.warning("Veuillez saisir un titre.")

# AUTH & NAVIGATION
query_params = st.query_params
is_direct_agenda_link = query_params.get("app", None) == "agenda"

if is_direct_agenda_link or st.session_state.get("direct_agenda", False):
    render_agenda_module()

elif not st.session_state.authenticated:
    st.markdown(f'<div style="text-align: center; margin-top: 20px; margin-bottom: 20px;"><h1 style="font-size: 2.2rem; margin-bottom: 5px;"><span style="color: {text_color};">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 8px; border-radius: 6px; font-size: 1.6rem; margin-left: 4px;">CORE</span></h1><div><span class="zapio-badge">🔮 Espace Sécurisé & Mobile Ready</span></div></div>', unsafe_allow_html=True)
    with st.form("login_form"):
        email = st.text_input("Adresse Email", placeholder="nom@exemple.com")
        master_key = st.text_input("Clé Maîtresse / PIN", type="password", placeholder="••••••••")
        submit = st.form_submit_button("Se connecter au Workspace")
        if submit:
            if master_key != "":
                st.session_state.authenticated = True
                st.toast("🔓 Connexion réussie.", icon="✨")
                st.rerun()
            else:
                st.error("Veuillez saisir votre clé d'accès.")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📅 Accéder directement à l'Agenda (Offline)", type="secondary"):
        st.session_state.direct_agenda = True
        st.rerun()

else:
    col_logo, col_logout = st.columns([2.5, 1.5])
    with col_logo:
        st.markdown(f'<h1 style="font-size: 1.1rem; margin: 0; display: flex; align-items: center; gap: 4px;"><span style="color: {text_color};">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 4px; border-radius: 4px; font-size: 0.75rem;">CORE</span><span class="zapio-badge-green" style="font-size: 0.5rem;">● Live</span></h1>', unsafe_allow_html=True)
    with col_logout:
        if st.button("🔒 Déco", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.current_view = "home"
            st.toast("🔒 Déconnexion effectuée.", icon="👋")
            st.rerun()

    st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 10px 0 10px 0;'>", unsafe_allow_html=True)
    
    # Barre de Recherche Rapide Universelle Responsive
    render_global_search()

    if st.session_state.current_view == "home":
        st.markdown(f'''
            <div class="pavel-hero-banner">
                <span class="zapio-badge" style="margin-bottom: 6px; display: inline-block;">🚀 WORKSPACE CENTRALISÉ</span>
                <h2 style="font-size: 1.6rem; color: {sub_title_color}; margin: 5px 0 3px 0;">Tableau de Bord</h2>
                <p style="color: {desc_color}; font-size: 0.85rem; margin: 0;">Sélectionnez ci-dessous l'espace de travail</p>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown(f'<div class="pavel-card-grid"><h3 style="color:{sub_title_color}; font-size: 1rem; margin-bottom:5px;">📅 Agenda & Planning</h3><p style="color: {desc_color}; font-size: 0.75rem; margin-bottom:10px;">Calendrier et mode hors-ligne.</p></div>', unsafe_allow_html=True)
        if st.button("Ouvrir l'Agenda", type="primary"):
            st.session_state.current_view = "Agenda"
            st.rerun()

        st.markdown(f'<div class="pavel-card-grid" style="margin-top: 15px;"><h3 style="color:{sub_title_color}; font-size: 1rem; margin-bottom:5px;">🤖 Prompts & IA</h3><p style="color: {desc_color}; font-size: 0.75rem; margin-bottom:10px;">Bibliothèque complète de prompts IA.</p></div>', unsafe_allow_html=True)
        if st.button("Ouvrir Prompts & IA"):
            st.session_state.current_view = "Prompts & IA"
            st.rerun()

        st.markdown(f'<div class="pavel-card-grid" style="margin-top: 15px;"><h3 style="color:{sub_title_color}; font-size: 1rem; margin-bottom:5px;">📁 Médias & Fichiers</h3><p style="color: {desc_color}; font-size: 0.75rem; margin-bottom:10px;">Images, ZIP, APK, PDFs et Documents.</p></div>', unsafe_allow_html=True)
        if st.button("Ouvrir Médias & Fichiers"):
            st.session_state.current_view = "Médias & Fichiers"
            st.rerun()

        st.markdown(f'<div class="pavel-card-grid" style="margin-top: 15px;"><h3 style="color:{sub_title_color}; font-size: 1rem; margin-bottom:5px;">🚀 Projets & Idées</h3><p style="color: {desc_color}; font-size: 0.75rem; margin-bottom:10px;">Projets actifs et idées.</p></div>', unsafe_allow_html=True)
        if st.button("Ouvrir Projets"):
            st.session_state.current_view = "Projets"
            st.rerun()

        st.markdown(f'<div class="pavel-card-grid" style="margin-top: 15px;"><h3 style="color:{sub_title_color}; font-size: 1rem; margin-bottom:5px;">🔐 Coffre-Fort Sécurisé</h3><p style="color: {desc_color}; font-size: 0.75rem; margin-bottom:10px;">Clés API et mots de passe.</p></div>', unsafe_allow_html=True)
        if st.button("Ouvrir le Coffre-Fort"):
            st.session_state.current_view = "Coffre-Fort"
            st.rerun()

        st.markdown(f'<div class="pavel-card-grid" style="margin-top: 15px;"><h3 style="color:{sub_title_color}; font-size: 1rem; margin-bottom:5px;">🎴 Contacts & Emails</h3><p style="color: {desc_color}; font-size: 0.75rem; margin-bottom:10px;">Répertoire et templates d\'emails.</p></div>', unsafe_allow_html=True)
        if st.button("Ouvrir Contacts & Emails"):
            st.session_state.current_view = "Contacts & Emails"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("⚙️ Sauvegarde Globale (Backup JSON)"):
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
                "saved_prompts_library": st.session_state.saved_prompts_library,
                "saved_code_snippets": st.session_state.saved_code_snippets,
                "saved_ideas": st.session_state.saved_ideas,
                "saved_current_projects": st.session_state.saved_current_projects,
                "saved_future_projects": st.session_state.saved_future_projects,
                "saved_links": st.session_state.saved_links,
                "saved_media_files": st.session_state.saved_media_files,
                "saved_api_keys": st.session_state.saved_api_keys,
                "saved_user_credentials": st.session_state.saved_user_credentials,
                "saved_contacts": st.session_state.saved_contacts,
                "saved_email_templates": st.session_state.saved_email_templates
            }
            json_str = json.dumps(workspace_data, indent=4, ensure_ascii=False)
            
            st.download_button(
                label="📥 Exporter (.json)",
                data=json_str,
                file_name=f"pavelcore_backup_{date.today().strftime('%Y-%m-%d')}.json",
                mime="application/json"
            )
            uploaded_backup = st.file_uploader("📤 Restaurer (.json)", type=["json"], key="backup_uploader")
            if uploaded_backup is not None:
                try:
                    imported_data = json.load(uploaded_backup)
                    st.session_state.saved_prompts_library = imported_data.get("saved_prompts_library", [])
                    st.session_state.saved_code_snippets = imported_data.get("saved_code_snippets", [])
                    st.session_state.saved_ideas = imported_data.get("saved_ideas", [])
                    st.session_state.saved_current_projects = imported_data.get("saved_current_projects", [])
                    st.session_state.saved_future_projects = imported_data.get("saved_future_projects", [])
                    st.session_state.saved_links = imported_data.get("saved_links", [])
                    st.session_state.saved_media_files = imported_data.get("saved_media_files", [])
                    st.session_state.saved_api_keys = imported_data.get("saved_api_keys", [])
                    st.session_state.saved_user_credentials = imported_data.get("saved_user_credentials", [])
                    st.session_state.saved_contacts = imported_data.get("saved_contacts", [])
                    st.session_state.saved_email_templates = imported_data.get("saved_email_templates", [])
                    
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
                    st.toast("✅ Restauration réussie !", icon="🎉")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur : {e}")

    else:
        current = st.session_state.current_view
        if st.button("← Retour", key="back_to_home_universal"):
            st.session_state.current_view = "home"
            st.rerun()
            
        st.markdown(f"<h2 style='color: #EC4899; margin-top: 10px; font-size: 1.4rem;'>Espace : {current}</h2>", unsafe_allow_html=True)

        if current == "Agenda":
            render_agenda_module()

        elif current == "Prompts & IA":
            st.markdown(f'''
                <div class="sub-section-header">
                    <span class="zapio-badge">INTELLIGENCE ARTIFICIELLE</span>
                    <h1 style="color: {sub_title_color}; font-size: 1.4rem; margin: 4px 0 0 0;">🧠 Bibliothèque de Prompts</h1>
                </div>
            ''', unsafe_allow_html=True)
            
            with st.form("form_add_prompt", clear_on_submit=True):
                p_title = st.text_input("Titre du Prompt")
                p_cat = st.selectbox("Catégorie", PROMPT_CATEGORIES)
                p_content = st.text_area("Contenu du Prompt")
                if st.form_submit_button("Enregistrer"):
                    if p_title and p_content:
                        st.session_state.saved_prompts_library.append({
                            "title": p_title,
                            "category": p_cat,
                            "prompt": p_content
                        })
                        st.toast("🧠 Prompt enregistré !", icon="✅")
                        st.rerun()
                    else:
                        st.warning("Veuillez remplir les champs.")

            st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 15px 0;'>", unsafe_allow_html=True)
            selected_cat_filter = st.selectbox("🔍 Filtrer :", ["Tous les prompts"] + PROMPT_CATEGORIES)
            
            for pr in st.session_state.saved_prompts_library:
                if selected_cat_filter == "Tous les prompts" or pr["category"] == selected_cat_filter:
                    st.markdown(f'''
                        <div class="zapio-card">
                            <span class="zapio-badge" style="font-size: 0.65rem;">{pr["category"]}</span>
                            <h3 style="color:{sub_title_color}; font-size: 1rem; margin-top: 4px;">{pr["title"]}</h3>
                        </div>
                    ''', unsafe_allow_html=True)
                    st.code(pr["prompt"], language="markdown")

        elif current == "Médias & Fichiers":
            st.markdown(f'''
                <div class="sub-section-header">
                    <span class="zapio-badge">STOCKAGE & RESSOURCES</span>
                    <h1 style="color: {sub_title_color}; font-size: 1.4rem; margin: 4px 0 0 0;">📁 Images, ZIP, APK & Docs</h1>
                </div>
            ''', unsafe_allow_html=True)

            sub_tab = st.pills(
                "Type",
                options=["📤 Envoyer un fichier", "🔗 Lien externe"],
                default="📤 Envoyer un fichier",
                label_visibility="collapsed"
            )

            if sub_tab == "📤 Envoyer un fichier":
                uploaded_file = st.file_uploader(
                    "Fichier (Images, ZIP, APK, PDF...)",
                    type=["png", "jpg", "jpeg", "gif", "zip", "rar", "apk", "pdf", "docx", "txt", "csv"]
                )
                file_title = st.text_input("Nom / Titre personnalisé")
                file_category = st.selectbox("Catégorie", ["🖼️ Images & Visuels", "📦 Fichiers ZIP / Archives", "📱 Applications APK", "📄 Documents & PDFs", "🔗 Liens Utiles"])

                if st.button("💾 Enregistrer"):
                    if uploaded_file is not None and file_title:
                        file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        st.session_state.saved_media_files.append({
                            "title": file_title,
                            "filename": uploaded_file.name,
                            "path": file_path,
                            "size": f"{round(uploaded_file.size / (1024 * 1024), 2)} MB",
                            "type": file_category,
                            "is_local": True
                        })
                        st.toast("📁 Fichier sauvegardé !", icon="✅")
                        st.rerun()
                    else:
                        st.warning("Veuillez charger un fichier et donner un titre.")

            elif sub_tab == "🔗 Lien externe":
                with st.form("form_external_link", clear_on_submit=True):
                    ext_title = st.text_input("Titre")
                    ext_url = st.text_input("URL directe (Drive, Web)")
                    ext_cat = st.selectbox("Catégorie", ["🖼️ Images & Visuels", "📦 Fichiers ZIP / Archives", "📱 Applications APK", "📄 Documents & PDFs", "🔗 Liens Utiles"])
                    ext_desc = st.text_area("Description")
                    if st.form_submit_button("Enregistrer"):
                        if ext_title and ext_url:
                            st.session_state.saved_media_files.append({
                                "title": ext_title,
                                "url": ext_url,
                                "desc": ext_desc,
                                "type": ext_cat,
                                "is_local": False
                            })
                            st.toast("🔗 Lien sauvegardé !", icon="✅")
                            st.rerun()

            st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 20px 0;'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='color:{sub_title_color}; font-size: 1.1rem;'>📚 Fichiers Enregistrés</h3>", unsafe_allow_html=True)

            if not st.session_state.saved_media_files:
                st.info("Aucun fichier pour le moment.")

            for item in st.session_state.saved_media_files:
                st.markdown(f'''
                    <div class="zapio-card">
                        <span class="zapio-badge" style="font-size:0.65rem;">{item["type"]}</span>
                        <h3 style="color:{sub_title_color}; font-size: 1rem; margin-top:4px;">{item["title"]}</h3>
                ''', unsafe_allow_html=True)

                if item.get("is_local", False):
                    st.caption(f"Fichier : {item['filename']} | Taille : {item['size']}")
                    if os.path.exists(item["path"]):
                        with open(item["path"], "rb") as file_data:
                            st.download_button(
                                label=f"📥 Télécharger {item['filename']}",
                                data=file_data,
                                file_name=item["filename"]
                            )
                else:
                    st.write(f"Description : {item.get('desc', '')}")
                    st.markdown(f'<a href="{item["url"]}" target="_blank" style="color:#EC4899; font-weight:600;">🌐 Ouvrir / Télécharger</a>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

        elif current == "Projets":
            sub_tab = st.pills(
                "Navigation Projets",
                options=["🚀 En cours", "🔮 Futurs", "💡 Idées"],
                default="🚀 En cours",
                label_visibility="collapsed"
            )
            
            if sub_tab == "🚀 En cours":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">SUIVI OPÉRATIONNEL</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.4rem; margin: 4px 0 0 0;">🚀 Projets en cours</h1>
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
                            st.toast("🚀 Projet enregistré !", icon="✅")
                            st.rerun()
                        else:
                            st.warning("Veuillez renseigner le nom.")
                for cp in st.session_state.saved_current_projects:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color}; font-size: 1rem;">{cp["name"]}</h3><p style="color:{desc_color}; font-size: 0.8rem;">Client: {cp["client"]} | Échéance: {cp["deadline"]}</p></div>', unsafe_allow_html=True)

            elif sub_tab == "🔮 Futurs":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">VISION & ROADMAP</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.4rem; margin: 4px 0 0 0;">🔮 Projets futurs</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_fut_proj", clear_on_submit=True):
                    name = st.text_input("Nom du projet")
                    horizon = st.selectbox("Horizon", ["Court terme", "Moyen terme", "Long terme"])
                    resources = st.text_area("Ressources requises")
                    goal = st.text_input("Objectif")
                    if st.form_submit_button("Ajouter"):
                        if name:
                            st.session_state.saved_future_projects.append({"name": name, "horizon": horizon, "resources": resources, "goal": goal})
                            st.toast("🔮 Projet ajouté !", icon="✨")
                            st.rerun()
                        else:
                            st.warning("Veuillez renseigner le nom.")
                for fp in st.session_state.saved_future_projects:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color}; font-size: 1rem;">{fp["name"]}</h3><p style="color:{desc_color}; font-size: 0.8rem;">Objectif: {fp["goal"]}</p></div>', unsafe_allow_html=True)

            elif sub_tab == "💡 Idées":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">INSPIRATION & CONCEPTS</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.4rem; margin: 4px 0 0 0;">💡 Boîte à Idées</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_ideas", clear_on_submit=True):
                    title = st.text_input("Titre")
                    category = st.selectbox("Domaine", ["Business", "Tech", "DJ", "Personnel"])
                    description = st.text_area("Description")
                    impact = st.select_slider("Impact", options=["Faible", "Moyen", "Fort", "Révolutionnaire !"])
                    if st.form_submit_button("Sauvegarder"):
                        if title:
                            st.session_state.saved_ideas.append({"title": title, "cat": category, "desc": description, "impact": impact})
                            st.toast("💡 Idée sauvegardée !", icon="💡")
                            st.rerun()
                        else:
                            st.warning("Veuillez renseigner un titre.")
                for id_item in st.session_state.saved_ideas:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color}; font-size: 1rem;">{id_item["title"]}</h3><p style="color:{desc_color}; font-size: 0.8rem;">{id_item["desc"]}</p></div>', unsafe_allow_html=True)

        elif current == "Coffre-Fort":
            sub_tab = st.pills(
                "Navigation Coffre",
                options=["🔐 Clés API", "🔑 Mots de passe"],
                default="🔐 Clés API",
                label_visibility="collapsed"
            )
            if sub_tab == "🔐 Clés API":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">SÉCURITÉ</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.4rem; margin: 4px 0 0 0;">🔐 Clés d'API & Tokens</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_api_keys", clear_on_submit=True):
                    service = st.text_input("Nom du Service (ex: OpenAI, GitHub)")
                    api_key = st.text_input("Clé API / Token", type="password")
                    if st.form_submit_button("🔒 Sauvegarder"):
                        if service and api_key:
                            st.session_state.saved_api_keys.append({"service": service, "key": api_key})
                            st.toast("🔐 Clé API sauvegardée !", icon="✅")
                            st.rerun()
                        else:
                            st.warning("Veuillez remplir les champs.")
                for ak in st.session_state.saved_api_keys:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color}; font-size: 1rem;">{ak["service"]}</h3>', unsafe_allow_html=True)
                    st.code(ak['key'], language='text')
                    st.markdown('</div>', unsafe_allow_html=True)

            elif sub_tab == "🔑 Mots de passe":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">GESTIONNAIRE</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.4rem; margin: 4px 0 0 0;">🔑 Identifiants</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_creds", clear_on_submit=True):
                    site = st.text_input("Plateforme / Site web")
                    username = st.text_input("Identifiant / Email")
                    password = st.text_input("Mot de passe", type="password")
                    if st.form_submit_button("Enregistrer"):
                        if site and username and password:
                            st.session_state.saved_user_credentials.append({"site": site, "user": username, "pass": password})
                            st.toast("🔑 Identifiants enregistrés !", icon="✅")
                            st.rerun()
                        else:
                            st.warning("Veuillez remplir les champs.")
                for uc in st.session_state.saved_user_credentials:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color}; font-size: 1rem;">{uc["site"]}</h3><p style="color:{desc_color}; font-size: 0.8rem;"><b>ID:</b> {uc["user"]}</p>', unsafe_allow_html=True)
                    st.code(uc['pass'], language='text')
                    st.markdown('</div>', unsafe_allow_html=True)

        elif current == "Contacts & Emails":
            sub_tab = st.pills(
                "Navigation Contacts",
                options=["🎴 Contacts", "📧 Modèles d'Emails"],
                default="🎴 Contacts",
                label_visibility="collapsed"
            )
            if sub_tab == "🎴 Contacts":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">RÉPERTOIRE</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.4rem; margin: 4px 0 0 0;">🎴 Carnet de Contacts</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_contacts", clear_on_submit=True):
                    fullname = st.text_input("Nom & Prénom / Entreprise")
                    email_contact = st.text_input("Adresse Email")
                    phone = st.text_input("Numéro de Téléphone")
                    category = st.selectbox("Catégorie", ["Client", "Partenaire / Prestataire", "VIP", "Personnel"])
                    notes = st.text_area("Notes / Rôle")
                    if st.form_submit_button("Ajouter"):
                        if fullname:
                            st.session_state.saved_contacts.append({
                                "name": fullname,
                                "email": email_contact,
                                "phone": phone,
                                "cat": category,
                                "notes": notes
                            })
                            st.toast("🎴 Contact sauvegardé !", icon="✅")
                            st.rerun()
                        else:
                            st.warning("Veuillez saisir au moins le nom.")
                for ct in st.session_state.saved_contacts:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color}; font-size: 1rem;">{ct["name"]} <span class="zapio-badge" style="font-size:0.6rem;">{ct["cat"]}</span></h3><p style="color:{desc_color}; font-size: 0.8rem;">📧 {ct["email"]} | 📞 {ct["phone"]}</p><p style="color:{desc_color}; font-size: 0.75rem;">{ct["notes"]}</p></div>', unsafe_allow_html=True)

            elif sub_tab == "📧 Modèles d'Emails":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">COMMUNICATION</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.4rem; margin: 4px 0 0 0;">📧 Modèles d'Emails & Scripts</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_email_tpl", clear_on_submit=True):
                    title = st.text_input("Titre du modèle")
                    subject = st.text_input("Objet du mail")
                    body = st.text_area("Corps du message")
                    if st.form_submit_button("Sauvegarder"):
                        if title and body:
                            st.session_state.saved_email_templates.append({
                                "title": title,
                                "subject": subject,
                                "body": body
                            })
                            st.toast("📧 Modèle sauvegardé !", icon="✅")
                            st.rerun()
                        else:
                            st.warning("Veuillez remplir les champs.")
                for et in st.session_state.saved_email_templates:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color}; font-size: 1rem;">{et["title"]}</h3><p style="color:{desc_color}; font-size: 0.8rem;"><b>Objet:</b> {et["subject"]}</p>', unsafe_allow_html=True)
                    st.code(et['body'], language='markdown')
                    st.markdown('</div>', unsafe_allow_html=True)
