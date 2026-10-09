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

from assets.styles import inject_custom_design
inject_custom_design()

# Script PWA + Synchronisation Hors-Ligne dans le LocalStorage du navigateur
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

# Détecteur automatique de langage de programmation
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

# Managing Global State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

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

# Composant de rendu pour le module Agenda
def render_agenda_module():
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

    # 1. VUE CALENDRIER MENSUEL (2025-2040+)
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
                    bg_color = "linear-gradient(135deg, #3B1578 0%, #261245 100%)" if is_today else "#1E0A3C
