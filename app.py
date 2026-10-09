import sys
import os
import re
import calendar
import json
import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import streamlit.components.v1 as components

# Correctif pour Streamlit Cloud
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration de la page
st.set_page_config(
    page_title="PavelCore — Workspace & Agenda Premium",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Sécurisation de l'import des styles personnalisés
try:
    from assets.styles import inject_custom_design
    inject_custom_design()
except ImportError:
    pass

# Script PWA + Synchronisation Hors-Ligne dans le LocalStorage
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
components.html(pwa_offline_script, height=0, width=0)

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

# State Management Global
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

# Synchronisation JS pour stockage hors-ligne
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
    js_sync = f"<script>syncAgendaToOfflineStorage({json.dumps(serializable_events)});</script>"
    components.html(js_sync, height=0, width=0)

# Fonction d'affichage du calendrier dynamique
def render_agenda_module():
    # Barre supérieure avec bouton de retour
    col_header, col_back = st.columns([3, 1])
    with col_header:
        st.markdown(
            '<h1 style="font-size: 1.8rem; margin: 0; display: flex; align-items: center; gap: 8px;">'
            '<span style="color: #FFF;">pavel</span>'
            '<span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 8px; border-radius: 6px; font-size: 1.2rem;">CORE</span>'
            '<span class="zapio-badge-green" style="font-size: 0.75rem;">● Agenda Offline</span>'
            '</h1>', 
            unsafe_allow_html=True
        )
    with col_back:
        btn_label = "🔒 Déconnexion" if st.session_state.authenticated else "🔒 Connexion Workspace"
        if st.button(btn_label, key="back_to_login", use_container_width=True, type="secondary"):
            st.session_state.direct_agenda = False
            st.session_state.authenticated = False
            st.query_params.clear()
            st.rerun()

    st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 15px 0 20px 0;'>", unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 20px;"><span class="zapio-badge">📅 AGENDA AUTONOME & HORS-LIGNE</span><h2 style="margin-top: 10px; font-size: 2rem;">Agenda & Calendrier Interactif</h2></div>', unsafe_allow_html=True)

    col_btn1, col_btn2, col_clear = st.columns([2.3, 2.5, 2])
    
    with col_btn1:
        btn_vue = st.button(
            "📅 Vue Calendrier Mensuel", 
            type="primary" if st.session_state.agenda_active_tab == "vue" else "secondary",
            use_container_width=True,
            key="nav_btn_vue"
        )
        if btn_vue:
            st.session_state.agenda_active_tab = "vue"
            st.rerun()

    with col_btn2:
        btn_add = st.button(
            "➕ Programmer un Événement", 
            type="primary" if st.session_state.agenda_active_tab == "add" else "secondary",
            use_container_width=True,
            key="nav_btn_add"
        )
        if btn_add:
            st.session_state.agenda_active_tab = "add"
            st.rerun()

    with col_clear:
        if st.session_state.agenda_events:
            if st.button("🗑️ Vider tout l'agenda", key="clear_all_events"):
                st.session_state.agenda_events = []
                sync_offline()
                st.rerun()

    st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

    # VUE CALENDRIER MENSUEL MULTI-ANNÉES AUTOMATIQUE
    if st.session_state.agenda_active_tab == "vue":
        today = date.today()
        current_year = today.year
        
        available_years = list(range(2025, current_year + 15))
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            selected_month_idx = st.selectbox(
                "Mois",
                range(1, 13),
                format_func=lambda x: MONTH_NAMES_FR[x-1],
                index=today.month - 1
            )
        with col_m2:
            default_year_idx = available_years.index(current_year) if current_year in available_years else 1
            selected_year = st.selectbox(
                "Année",
                available_years,
                index=default_year_idx
            )

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
                    cols_w[day_idx].markdown('<div class="calendar-day-box" style="background:rgba(20,9,35,0.4); border:1px solid #261245; opacity:0.3;"></div>', unsafe_allow_html=True)
                else:
                    is_today = (day_num == today.day and selected_month_idx == today.month and selected_year == today.year)
                    day_events = events_by_day.get(day_num, [])
                    
                    border_color = "#EC4899" if is_today else "#5B21B6"
                    bg_color = "linear-gradient(135deg, #3B1578 0%, #261245 100%)" if is_today else "#1E0A3C"
                    
                    max_visible_events = 2
                    visible_events = day_events[:max_visible_events]
                    hidden_count = len(day_events) - max_visible_events

                    event_html = ""
                    for ev_item in visible_events:
                        event_html += f'<div style="background:#F43F5E; color:#FFF; font-size:0.6rem; font-weight:800; border-radius:3px; padding:1px 3px; margin-top:3px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">⏰ {ev_item["time"].strftime("%H:%M")} - {ev_item["title"]}</div>'

                    if hidden_count > 0:
                        event_html += f'<div style="background:#A78BFA; color:#1E0A3C; font-size:0.55rem; font-weight:800; border-radius:3px; padding:1px 2px; margin-top:2px; text-align:center;">+{hidden_count}</div>'

                    day_marker = '📌' if is_today else ''
                    day_color = '#EC4899' if is_today else '#FFF'
                    
                    cols_w[day_idx].markdown(
                        f'<div class="calendar-day-box" style="background:{bg_color}; border:1px solid {border_color};">'
                        f'<div style="display:flex; justify-content:space-between; align-items:center;">'
                        f'<span class="calendar-day-number" style="font-weight:800; font-size:0.85rem; color:{day_color};">{day_num} {day_marker}</span>'
                        f'</div>{event_html}</div>', 
                        unsafe_allow_html=True
                    )

        st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 25px 0 15px 0;'>", unsafe_allow_html=True)

        st.subheader(f"📋 Liste chronologique des événements ({MONTH_NAMES_FR[selected_month_idx-1]} {selected_year})")
        
        month_events = [ev for ev in st.session_state.agenda_events if ev['date'].month == selected_month_idx and ev['date'].year == selected_year]
        
        if month_events:
            sorted_events = sorted(month_events, key=lambda x: (x['date'], x['time']))
            for idx, ev in enumerate(sorted_events):
                desc_text = ev['desc'] if ev['desc'] else '<i>Aucune note fournie</i>'
                
                c_card, c_del = st.columns([5, 1])
                with c_card:
                    st.markdown(f'<div class="calendar-event-card"><div class="calendar-date-box"><span style="font-size: 0.75rem; text-transform: uppercase;">{MONTH_NAMES_FR[ev["date"].month-1][:3].upper()}</span><span style="font-size: 1.5rem; line-height: 1;">{ev["date"].strftime("%d")}</span><span style="font-size: 0.8rem; margin-top: 3px; opacity: 0.95;">{ev["time"].strftime("%H:%M")}</span></div><div style="flex-grow: 1;"><div style="display:flex; justify-content:space-between; align-items:flex-start;"><h3 style="margin:0; color:#FFFFFF; font-size: 1.2rem;">{ev["title"]}</h3><span class="zapio-badge">{ev["category"]}</span></div><p style="color:#CBD5E1; margin: 6px 0; font-size: 0.85rem;">{desc_text}</p><div style="font-size: 0.8rem; color: #A78BFA;">🔔 Notification : <b style="color:#FFF;">{ev["ringtone"]}</b></div></div></div>', unsafe_allow_html=True)
                with c_del:
                    if st.button("🗑️ Supprimer", key=f"del_ev_{idx}"):
                        st.session_state.agenda_events.remove(ev)
                        sync_offline()
                        st.rerun()
        else:
            st.info(f"Aucun événement enregistré pour {MONTH_NAMES_FR[selected_month_idx-1]} {selected_year}.")

    # PROGRAMMER UN ÉVÉNEMENT
    elif st.session_state.agenda_active_tab == "add":
        with st.form("add_event_form"):
            st.subheader("Planifier une nouvelle date")
            title = st.text_input("Titre de l'événement / Rappel", placeholder="Ex: Prestation DJ 2027 / Réunion PavelCore")
            
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
                    st.session_state.agenda_events.append({
                        "title": title, "date": event_date, "time": event_time,
                        "category": category, "desc": desc, "ringtone": ringtone
                    })
                    sync_offline()
                    st.session_state.agenda_active_tab = "vue"
                    st.success("Événement enregistré et sauvegardé hors-ligne !")
                    st.rerun()


# CONTROLE D'ACCÈS / NAVIGATION
query_params = st.query_params
is_direct_agenda_link = query_params.get("app", None) == "agenda"

if is_direct_agenda_link or st.session_state.get("direct_agenda", False):
    render_agenda_module()

elif not st.session_state.authenticated:
    st.markdown('<div style="text-align: center; margin-top: 30px; margin-bottom: 25px;"><h1 style="font-size: 2.8rem; margin-bottom: 5px;"><span style="color: #FFFFFF;">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 10px; border-radius: 8px; font-size: 2rem; margin-left: 6px;">CORE</span></h1><div style="margin-top: 15px;"><span class="zapio-badge">🔮 Espace Sécurisé & Workspace</span></div></div>', unsafe_allow_html=True)

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
        if st.button("📅 Accéder directement à l'Agenda (Mode Rapide & Offline)", use_container_width=True, type="secondary"):
            st.session_state.direct_agenda = True
            st.rerun()

else:
    col_logo, col_logout = st.columns([3, 1])
    
    with col_logo:
        st.markdown('<h1 style="font-size: 2rem; margin: 0; display: flex; align-items: center; gap: 8px;"><span style="color: #FFF;">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 8px
