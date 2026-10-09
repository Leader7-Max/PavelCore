import sys
import os
import re
import calendar
import json
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

# Gestionnaire d'État Global (Thème, Langue, Modaux)
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Sombre Nuit"

if "app_lang" not in st.session_state:
    st.session_state.app_lang = "FR"

if "show_settings_modal" not in st.session_state:
    st.session_state.show_settings_modal = False

if "show_help_modal" not in st.session_state:
    st.session_state.show_help_modal = False

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

# Définition dynamique des couleurs selon le thème choisi (Indépendant de Streamlit)
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
    capsule_bg = "rgba(15, 23, 42, 0.04)"
    capsule_border = "rgba(15, 23, 42, 0.1)"
    capsule_btn_bg = "#FFFFFF"
else:  # Sombre Nuit
    bg_app = "#0E031C"
    text_color = "#F8FAFC"
    card_bg = "#170A2E"
    card_border = "#2B1552"
    card_gradient = "linear-gradient(135deg, #1A0B36 0%, #120524 100%)"
    header_box_bg = "#1E0A3C"
    header_box_text = "#A78BFA"
    desc_color = "#CBD5E1"
    sub_title_color = "#FFF"
    capsule_bg = "rgba(0, 0, 0, 0.35)"
    capsule_border = "rgba(255, 255, 255, 0.12)"
    capsule_btn_bg = "rgba(25, 10, 45, 0.6)"

# INJECTION DES STYLES (Contrôle total sur l'apparence, les cartes et la capsule en ligne)
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_app} !important;
        color: {text_color} !important;
    }}
    .pavel-card-grid {{
        background: {card_gradient};
        border: 1px solid {card_border};
        border-radius: 14px;
        padding: 25px;
        text-align: center;
        transition: all 0.25s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }}
    .pavel-card-grid:hover {{
        transform: translateY(-3px);
        border-color: #EC4899;
        box-shadow: 0 8px 30px rgba(236, 72, 153, 0.12);
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
    .calendar-header-box {{
        background: {header_box_bg};
        color: {header_box_text};
        text-align: center;
        padding: 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
        border: 1px solid {card_border};
    }}
    .calendar-day-box {{
        min-height: 90px;
        border-radius: 8px;
        padding: 6px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }}
    .calendar-event-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 10px;
        padding: 12px;
        display: flex;
        gap: 15px;
        margin-bottom: 10px;
        align-items: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }}
    .calendar-date-box {{
        background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%);
        color: #FFF;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        min-width: 65px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        font-weight: 800;
    }}
    /* Style de la capsule de contrôle horizontale unifiée */
    .reference-capsule-wrapper {{
        background: {capsule_bg};
        border: 1px solid {capsule_border};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 30px;
        padding: 3px 6px;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 3px;
        justify-content: flex-end;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        width: 100%;
    }}
    .reference-capsule-wrapper [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 2px !important;
    }}
    .reference-capsule-wrapper [data-testid="column"] {{
        width: auto !important;
        flex: 1 1 auto !important;
        min-width: 0 !important;
        padding: 0 !important;
    }}
    .reference-capsule-wrapper button {{
        background: {capsule_btn_bg} !important;
        border: 1px solid {capsule_border} !important;
        color: {text_color} !important;
        border-radius: 20px !important;
        padding: 2px 6px !important;
        font-size: 0.75rem !important;
        min-height: 24px !important;
        max-height: 28px !important;
        line-height: 1 !important;
        width: 100% !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }}
    .reference-capsule-wrapper button:hover {{
        border-color: #EC4899 !important;
        color: #EC4899 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Enregistrement du Service Worker PWA via st.markdown
pwa_offline_script = """
<script>
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js').then(function(reg) {
            console.log('PWA ServiceWorker actif:', reg.scope);
        }).catch(function(err) {
            console.log('Erreur SW:', err);
        });
    });
}
function syncAgendaToOfflineStorage(eventsData) {
    try {
        localStorage.setItem('pavelcore_offline_agenda', JSON.stringify(eventsData));
    } catch(e) {
        console.error('Erreur LocalStorage', e);
    }
}
</script>
"""
st.markdown(pwa_offline_script, unsafe_allow_html=True)

# Détecteur automatique de langage
def detect_language(code):
    if not code or not isinstance(code, str):
        return "python"
    code_lower = code.lower().strip()
    if re.search(r'<!doctype html>|<html|<div|<span|<body|<p>|<a href', code_lower):
        return "html"
    elif re.search(r'\{\s*color:|margin:|padding:|background-color:|font-family:|border-radius:', code_lower):
        return "css"
    elif re.search(r'\b(select|insert into|update|delete from|create table|where|group by|order by|join)\b', code_lower):
        return "sql"
    elif re.search(r'\b(const|let|var|function|console\.log|document\.|window\.|export default|import react)\b', code_lower):
        return "javascript"
    elif "<?php" in code_lower or re.search(r'\$[a-zA-Z_][a-zA-Z0-9_]*\s*=', code):
        return "php"
    elif code_lower.startswith("{") and code_lower.endswith("}") and ":" in code_lower:
        return "json"
    elif re.search(r'\b(def |import |from |st\.|print\(|self\.|elif |class )\b', code_lower):
        return "python"
    return "python"

LANG_MAP = {
    "Python": "python",
    "Détection Automatique": "auto",
    "JavaScript / React": "javascript",
    "HTML5": "html",
    "CSS3 / TailWind": "css",
    "SQL": "sql",
    "PHP / WordPress": "php",
    "Flutter / Flet": "python",
    "JSON / Config": "json"
}

MONTH_NAMES_FR = [
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]

def sync_offline():
    serializable_events = [
        {
            "title": e["title"],
            "date": e["date"].strftime("%Y-%m-%d"),
            "time": e["time"].strftime("%H:%M"),
            "category": e["category"],
            "desc": e["desc"],
            "ringtone": e["ringtone"]
        } for e in st.session_state.agenda_events
    ]
    js_sync = f"<script>if(typeof syncAgendaToOfflineStorage === 'function'){{ syncAgendaToOfflineStorage({json.dumps(serializable_events)}); }}</script>"
    st.markdown(js_sync, unsafe_allow_html=True)

def render_agenda_module():
    st.markdown(f'<div style="margin-bottom: 20px;"><span class="zapio-badge">📅 AGENDA AUTONOME & HORS-LIGNE</span><h2 style="margin-top: 10px; font-size: 2rem; color: {sub_title_color};">Agenda & Calendrier Interactif</h2></div>', unsafe_allow_html=True)

    col_btn1, col_btn2, col_clear = st.columns([2.3, 2.5, 2])
    
    with col_btn1:
        if st.button("📅 Vue Calendrier Mensuel", type="primary" if st.session_state.agenda_active_tab == "vue" else "secondary", use_container_width=True, key="nav_btn_vue"):
            st.session_state.agenda_active_tab = "vue"
            st.rerun()

    with col_btn2:
        if st.button("➕ Programmer un Événement", type="primary" if st.session_state.agenda_active_tab == "add" else "secondary", use_container_width=True, key="nav_btn_add"):
            st.session_state.agenda_active_tab = "add"
            st.rerun()

    with col_clear:
        if st.session_state.agenda_events:
            if st.button("🗑️ Vider tout l'agenda", key="clear_all_events"):
                st.session_state.agenda_events = []
                sync_offline()
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
        days_header = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        cols_h = st.columns(7)
        for idx, h in enumerate(days_header):
            cols_h[idx].markdown(f'<div class="calendar-header-box">{h}</div>', unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)
        events_by_day = {}
        for ev in st.session_state.agenda_events:
            if ev['date'].month == selected_month_idx and ev['date'].year == selected_year:
                day_num = ev['date'].day
                if day_num not in events_by_day:
                    events_by_day[day_num] = []
                events_by_day[day_num].append(ev)

        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(selected_year, selected_month_idx)

        for week in month_days:
            cols_w = st.columns(7)
            for day_idx, day_num in enumerate(week):
                if day_num == 0:
                    cols_w[day_idx].markdown('<div class="calendar-day-box" style="background:rgba(100,100,100,0.1); border:1px solid rgba(100,100,100,0.2); opacity:0.3;"></div>', unsafe_allow_html=True)
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
                        event_html += f'<div style="background:#F43F5E; color:#FFF; font-size:0.6rem; font-weight:800; border-radius:3px; padding:1px 3px; margin-top:3px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">⏰ {ev_item["time"].strftime("%H:%M")} - {ev_item["title"]}</div>'

                    if hidden_count > 0:
                        event_html += f'<div style="background:#A78BFA; color:#1E0A3C; font-size:0.55rem; font-weight:800; border-radius:3px; padding:1px 2px; margin-top:2px; text-align:center;">+{hidden_count}</div>'

                    day_marker = '📌' if is_today else ''
                    day_color = '#EC4899' if is_today else text_color
                    
                    cols_w[day_idx].markdown(
                        f'<div class="calendar-day-box" style="background:{bg_color}; border:1px solid {border_color};">'
                        f'<div style="display:flex; justify-content:space-between; align-items:center;">'
                        f'<span class="calendar-day-number" style="font-weight:800; font-size:0.85rem; color:{day_color};">{day_num} {day_marker}</span>'
                        f'</div>{event_html}</div>', 
                        unsafe_allow_html=True
                    )

        st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 25px 0 15px 0;'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: {sub_title_color};'>📋 Liste chronologique ({MONTH_NAMES_FR[selected_month_idx-1]} {selected_year})</h3>", unsafe_allow_html=True)
        
        month_events = [ev for ev in st.session_state.agenda_events if ev['date'].month == selected_month_idx and ev['date'].year == selected_year]
        if month_events:
            sorted_events = sorted(month_events, key=lambda x: (x['date'], x['time']))
            for idx, ev in enumerate(sorted_events):
                desc_text = ev['desc'] if ev['desc'] else '<i>Aucune note</i>'
                c_card, c_del = st.columns([5, 1])
                with c_card:
                    st.markdown(f'<div class="calendar-event-card"><div class="calendar-date-box"><span style="font-size: 0.75rem; text-transform: uppercase;">{MONTH_NAMES_FR[ev["date"].month-1][:3].upper()}</span><span style="font-size: 1.5rem; line-height: 1;">{ev["date"].strftime("%d")}</span><span style="font-size: 0.8rem; margin-top: 3px; opacity: 0.95;">{ev["time"].strftime("%H:%M")}</span></div><div style="flex-grow: 1;"><div style="display:flex; justify-content:space-between; align-items:flex-start;"><h3 style="margin:0; color:{sub_title_color}; font-size: 1.2rem;">{ev["title"]}</h3><span class="zapio-badge">{ev["category"]}</span></div><p style="color:{desc_color}; margin: 6px 0; font-size: 0.85rem;">{desc_text}</p><div style="font-size: 0.8rem; color: #A78BFA;">🔔 Notification : <b style="color:{text_color};">{ev["ringtone"]}</b></div></div></div>', unsafe_allow_html=True)
                with c_del:
                    if st.button("🗑️ Supprimer", key=f"del_ev_{idx}"):
                        st.session_state.agenda_events.remove(ev)
                        sync_offline()
                        st.rerun()
        else:
            st.info(f"Aucun événement pour {MONTH_NAMES_FR[selected_month_idx-1]} {selected_year}.")

    elif st.session_state.agenda_active_tab == "add":
        with st.form("add_event_form"):
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
                    sync_offline()
                    st.session_state.agenda_active_tab = "vue"
                    st.success("Événement enregistré !")
                    st.rerun()

# CONTRÔLE D'ACCÈS ET NAVIGATION
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
                    st.rerun()
                else:
                    st.error("Veuillez saisir votre clé d'accès.")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📅 Accéder directement à l'Agenda (Offline)", use_container_width=True, type="secondary"):
            st.session_state.direct_agenda = True
            st.rerun()

else:
    # EN-TÊTE SUPÉRIEUR : Logo à gauche, Capsule intégrale unifiée à droite sur une seule ligne
    col_logo, col_spacer, col_capsule = st.columns([1.2, 0.2, 3.6])
    
    with col_logo:
        st.markdown(f'<h1 style="font-size: 1.3rem; margin: 0; display: flex; align-items: center; gap: 4px;"><span style="color: {text_color};">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 5px; border-radius: 6px; font-size: 0.85rem;">CORE</span><span class="zapio-badge-green" style="font-size: 0.55rem;">● Live</span></h1>', unsafe_allow_html=True)
    
    with col_capsule:
        st.markdown('<div class="reference-capsule-wrapper">', unsafe_allow_html=True)
        c_th, c_set, c_hlp, c_lng, c_out = st.columns(5)
        
        with c_th:
            theme_icon = "☀️" if st.session_state.theme_mode == "Sombre Nuit" else "🌙"
            if st.button(theme_icon, use_container_width=True, key="btn_toggle_theme"):
                st.session_state.theme_mode = "Blanc Épuré" if st.session_state.theme_mode == "Sombre Nuit" else "Sombre Nuit"
                st.rerun()
                
        with c_set:
            if st.button("⚙️", use_container_width=True, key="btn_settings_toggle"):
                st.session_state.show_settings_modal = not st.session_state.show_settings_modal
                st.rerun()
                
        with c_hlp:
            if st.button("❓", use_container_width=True, key="btn_help_toggle"):
                st.session_state.show_help_modal = not st.session_state.show_help_modal
                st.rerun()
                
        with c_lng:
            lang_label = "EN" if st.session_state.app_lang == "FR" else "FR"
            if st.button(lang_label, use_container_width=True, key="btn_toggle_lang"):
                st.session_state.app_lang = "EN" if st.session_state.app_lang == "FR" else "FR"
                st.rerun()

        with c_out:
            if st.button("🔒", use_container_width=True, key="btn_nav_logout_capsule"):
                st.session_state.authenticated = False
                st.session_state.current_view = "home"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # MODAL / PANNEAU PARAMÈTRES (⚙️)
    if st.session_state.show_settings_modal:
        st.markdown(f'<div class="zapio-card" style="border-color: #EC4899; margin-top: 15px;"><h3 style="color:{sub_title_color};">⚙️ Panneau de Paramètres Avancés</h3><p style="color:{desc_color};">Personnalisez votre espace PavelCore selon vos préférences.</p></div>', unsafe_allow_html=True)
        c_set1, c_set2 = st.columns(2)
        with c_set1:
            st.selectbox("Mode d'affichage par défaut", ["Grille de cartes", "Liste compacte"], key="pref_display_mode")
        with c_set2:
            st.selectbox("Fréquence de synchro Cloud/Offline", ["Temps réel", "Toutes les heures", "Manuel uniquement"], key="pref_sync_freq")
        if st.button("Fermer les paramètres", key="close_settings"):
            st.session_state.show_settings_modal = False
            st.rerun()

    # MODAL / PANNEAU AIDE (❓)
    if st.session_state.show_help_modal:
        st.markdown(f'<div class="zapio-card" style="border-color: #8B5CF6; margin-top: 15px;"><h3 style="color:{sub_title_color};">❓ Centre d\'Aide & Support PavelCore</h3><p style="color:{desc_color};"><b>Mode Hors-Ligne (PWA) :</b> Vos données d\'agenda sont automatiquement enregistrées dans le cache local de votre navigateur.</p><p style="color:{desc_color};"><b>Sécurité :</b> Vos clés API et mots de passe sont stockés localement et chiffrés dans votre session.</p></div>', unsafe_allow_html=True)
        if st.button("Fermer l'aide", key="close_help"):
            st.session_state.show_help_modal = False
            st.rerun()

    st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 15px 0 25px 0;'>", unsafe_allow_html=True)

    # VUE ACCUEIL : GRILLE DE CARTES PREMIUM
    if st.session_state.current_view == "home":
        st.markdown(f'<div style="text-align: center; margin-bottom: 25px;"><h2 style="font-size: 1.8rem; color: {sub_title_color};">Tableau de Bord Principal</h2><p style="color: {desc_color}; font-size: 0.9rem;">Sélectionnez un espace de travail</p></div>', unsafe_allow_html=True)
        
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

    # SOUS-PÔLES DÉTAILLÉS (AVEC BOUTON DE RETOUR UNIFIÉ)
    else:
        current = st.session_state.current_view
        
        if st.button("← Retour au Tableau de Bord", key="back_to_home_universal"):
            st.session_state.current_view = "home"
            st.rerun()
            
        st.markdown(f"<h2 style='color: #EC4899; margin-top: 15px;'>Espace : {current}</h2>", unsafe_allow_html=True)

        if current == "Agenda":
            render_agenda_module()

        elif current == "Projets":
            sub_tab = st.radio("Navigation Projets", ["🚀 Projets en cours", "🔮 Projets futurs", "💡 Idées"], horizontal=True)
            st.markdown("<hr style='border-color: rgba(236,72,153,0.2);'>", unsafe_allow_html=True)
            
            if sub_tab == "🚀 Projets en cours":
                with st.form("form_curr_proj"):
                    name = st.text_input("Nom du projet")
                    client = st.text_input("Client / Marque")
                    priority = st.selectbox("Priorité", ["🔴 Haute", "🟠 Moyenne", "🟢 Basse"])
                    next_step = st.text_input("Prochaine étape")
                    deadline = st.date_input("Date limite")
                    project_desc = st.text_area("Description")
                    if st.form_submit_button("Enregistrer"):
                        if name:
                            st.session_state.saved_current_projects.append({"name": name, "client": client, "priority": priority, "next": next_step, "deadline": str(deadline), "desc": project_desc})
                            st.rerun()
                for cp in st.session_state.saved_current_projects:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{cp["name"]}</h3><p style="color:{desc_color};">Client: {cp["client"]} | Échéance: {cp["deadline"]}</p></div>', unsafe_allow_html=True)

            elif sub_tab == "🔮 Projets futurs":
                with st.form("form_fut_proj"):
                    name = st.text_input("Nom du projet futur")
                    horizon = st.selectbox("Horizon", ["Court terme", "Moyen terme", "Long terme"])
                    resources = st.text_area("Ressources requises")
                    goal = st.text_input("Objectif")
                    if st.form_submit_button("Ajouter"):
                        if name:
                            st.session_state.saved_future_projects.append({"name": name, "horizon": horizon, "resources": resources, "goal": goal})
                            st.rerun()
                for fp in st.session_state.saved_future_projects:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{fp["name"]}</h3><p style="color:{desc_color};">Objectif: {fp["goal"]}</p></div>', unsafe_allow_html=True)

            elif sub_tab == "💡 Idées":
                with st.form("form_ideas"):
                    title = st.text_input("Titre de l'idée")
                    category = st.selectbox("Domaine", ["Business", "Tech", "DJ", "Personnel"])
                    description = st.text_area("Description")
                    impact = st.select_slider("Impact", options=["Faible", "Moyen", "Fort", "Révolutionnaire !"])
                    if st.form_submit_button("Sauvegarder"):
                        if title:
                            st.session_state.saved_ideas.append({"title": title, "cat": category, "desc": description, "impact": impact})
                            st.rerun()
                for id_item in st.session_state.saved_ideas:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{id_item["title"]}</h3><p style="color:{desc_color};">{id_item["desc"]}</p></div>', unsafe_allow_html=True)

        elif current == "Dev & IA":
            sub_tab = st.radio("Navigation Dev", ["🤖 Prompts AI Code", "🧠 Prompts Claude", "💻 Snippets Code"], horizontal=True)
            st.markdown("<hr style='border-color: rgba(236,72,153,0.2);'>", unsafe_allow_html=True)
            
            if sub_tab == "🤖 Prompts AI Code":
                with st.form("form_ai_code"):
                    title = st.text_input("Titre")
                    selected_lang = st.selectbox("Langage", list(LANG_MAP.keys()))
                    prompt = st.text_area("Contenu du Prompt")
                    tags = st.text_input("Tags")
                    if st.form_submit_button("Enregistrer"):
                        if title and prompt:
                            final_lang = LANG_MAP[selected_lang]
                            if final_lang == "auto":
                                final_lang = detect_language(prompt)
                            st.session_state.saved_ai_prompts.append({"title": title, "lang_label": selected_lang, "lang": final_lang, "prompt": prompt, "tags": tags})
                            st.rerun()
                for p in st.session_state.saved_ai_prompts:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{p["title"]}</h3>', unsafe_allow_html=True)
                    st.code(p['prompt'], language=p['lang'])
                    st.markdown('</div>', unsafe_allow_html=True)

            elif sub_tab == "🧠 Prompts Claude":
                with st.form("form_claude"):
                    title = st.text_input("Titre")
                    system_prompt = st.text_area("System Prompt")
                    selected_lang = st.selectbox("Langage", list(LANG_MAP.keys()))
                    user_prompt = st.text_area("User Prompt")
                    artifacts = st.text_input("Artifacts")
                    if st.form_submit_button("Sauvegarder"):
                        if title and user_prompt:
                            final_lang = LANG_MAP[selected_lang]
                            if final_lang == "auto":
                                final_lang = detect_language(user_prompt)
                            st.session_state.saved_claude_prompts.append({"title": title, "sys": system_prompt, "user": user_prompt, "artifacts": artifacts, "lang_label": selected_lang, "lang": final_lang})
                            st.rerun()
                for c in st.session_state.saved_claude_prompts:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{c["title"]}</h3>', unsafe_allow_html=True)
                    st.code(c['user'], language=c.get('lang', 'python'))
                    st.markdown('</div>', unsafe_allow_html=True)

            elif sub_tab == "💻 Snippets Code":
                with st.form("form_code"):
                    title = st.text_input("Nom")
                    selected_lang = st.selectbox("Langage", list(LANG_MAP.keys()))
                    code_content = st.text_area("Code")
                    usage_note = st.text_input("Note")
                    if st.form_submit_button("Enregistrer"):
                        if title and code_content:
                            final_lang = LANG_MAP[selected_lang]
                            if final_lang == "auto":
                                final_lang = detect_language(code_content)
                            st.session_state.saved_code_snippets.append({"title": title, "type_label": selected_lang, "type": final_lang, "code": code_content, "note": usage_note})
                            st.rerun()
                for cd in st.session_state.saved_code_snippets:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{cd["title"]}</h3>', unsafe_allow_html=True)
                    st.code(cd['code'], language=cd['type'])
                    st.markdown('</div>', unsafe_allow_html=True)

        elif current == "Ressources":
            sub_tab = st.radio("Navigation Ressources", ["🎨 Prompts Images", "🔗 Liens Utiles", "📦 Fichiers ZIP"], horizontal=True)
            st.markdown("<hr style='border-color: rgba(236,72,153,0.2);'>", unsafe_allow_html=True)
            
            if sub_tab == "🎨 Prompts Images":
                with st.form("form_img_prompt"):
                    title = st.text_input("Titre")
                    generator = st.selectbox("Générateur", ["Midjourney", "DALL-E 3", "Flux.1"])
                    prompt_text = st.text_area("Prompt")
                    aspect_ratio = st.selectbox("Format", ["1:1", "16:9", "9:16"])
                    negative_prompt = st.text_input("Négatif")
                    if st.form_submit_button("Enregistrer"):
                        if title and prompt_text:
                            st.session_state.saved_image_prompts.append({"title": title, "gen": generator, "prompt": prompt_text, "ar": aspect_ratio, "neg": negative_prompt})
                            st.rerun()
                for img in st.session_state.saved_image_prompts:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{img["title"]}</h3><p style="color:{desc_color};">{img["prompt"]}</p></div>', unsafe_allow_html=True)

            elif sub_tab == "🔗 Liens Utiles":
                with st.form("form_links"):
                    title = st.text_input("Nom")
                    url = st.text_input("URL")
                    category = st.selectbox("Catégorie", ["Doc", "Outils", "Business"])
                    note = st.text_input("Note")
                    if st.form_submit_button("Enregistrer"):
                        if title and url:
                            st.session_state.saved_links.append({"title": title, "url": url, "cat": category, "note": note})
                            st.rerun()
                for lk in st.session_state.saved_links:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{lk["title"]}</h3><a href="{lk["url"]}" target="_blank">{lk["url"]}</a></div>', unsafe_allow_html=True)

            elif sub_tab == "📦 Fichiers ZIP":
                with st.form("form_zip"):
                    title = st.text_input("Nom")
                    cloud_link = st.text_input("Lien")
                    version = st.text_input("Version", value="v1.0")
                    contents = st.text_area("Contenu")
                    if st.form_submit_button("Enregistrer"):
                        if title and cloud_link:
                            st.session_state.saved_zip_files.append({"title": title, "link": cloud_link, "version": version, "contents": contents})
                            st.rerun()
                for zp in st.session_state.saved_zip_files:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{zp["title"]}</h3><a href="{zp["link"]}" target="_blank">Télécharger ZIP</a></div>', unsafe_allow_html=True)

        elif current == "Coffre-Fort":
            sub_tab = st.radio("Navigation Sécurité", ["🔑 Clés API", "🔐 Mots de passe"], horizontal=True)
            st.markdown("<hr style='border-color: rgba(236,72,153,0.2);'>", unsafe_allow_html=True)
            
            if sub_tab == "🔑 Clés API":
                with st.form("form_api_key"):
                    service_name = st.text_input("Service")
                    api_key_val = st.text_input("Clé API", type="password")
                    provider_env = st.selectbox("Environnement", ["Production", "Test"])
                    notes = st.text_input("Notes")
                    if st.form_submit_button("Sauvegarder"):
                        if service_name and api_key_val:
                            st.session_state.saved_api_keys.append({"service": service_name, "key": api_key_val, "env": provider_env, "notes": notes})
                            st.rerun()
                for ak in st.session_state.saved_api_keys:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">🔑 {ak["service"]}</h3>', unsafe_allow_html=True)
                    st.code(ak['key'], language="text")
                    st.markdown('</div>', unsafe_allow_html=True)

            elif sub_tab == "🔐 Mots de passe":
                with st.form("form_user_cred"):
                    platform_name = st.text_input("Plateforme")
                    username_val = st.text_input("Identifiant")
                    password_val = st.text_input("Mot de passe / PIN", type="password")
                    cred_type = st.selectbox("Type", ["Web", "PIN", "Serveur"])
                    cred_notes = st.text_input("Notes")
                    if st.form_submit_button("Sauvegarder"):
                        if platform_name:
                            st.session_state.saved_user_credentials.append({"platform": platform_name, "username": username_val, "password": password_val, "type": cred_type, "notes": cred_notes})
                            st.rerun()
                for cred in st.session_state.saved_user_credentials:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">🔐 {cred["platform"]}</h3><p style="color:{desc_color};">User: {cred["username"]}</p>', unsafe_allow_html=True)
                    st.code(cred['password'], language="text")
                    st.markdown('</div>', unsafe_allow_html=True)
