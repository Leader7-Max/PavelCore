import sys
import os
import re
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

# Global State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "agenda_events" not in st.session_state:
    st.session_state.agenda_events = [
        {"title": "Lancement Application PavelCore", "date": date(2026, 10, 25), "time": time(10, 0), "category": "Dev & Tech", "desc": "Mise en ligne globale sur Streamlit Cloud", "ringtone": "Alarme Digitale"},
        {"title": "Session DJ & Mixing Event", "date": date(2026, 10, 28), "time": time(21, 30), "category": "Événement DJ / Prestation", "desc": "Préparation set Afrobeat & Zouglou", "ringtone": "Bip Futuriste"}
    ]

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


# ----------------------------------------------------
# 1. AUTHENTIFICATION
# ----------------------------------------------------
if not st.session_state.authenticated:
    auth_header = """<div style="text-align: center; margin-top: 30px; margin-bottom: 25px;"><h1 style="font-size: 2.8rem; margin-bottom: 5px;"><span style="color: #FFFFFF;">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 10px; border-radius: 8px; font-size: 2rem; margin-left: 6px;">CORE</span></h1><div style="margin-top: 15px;"><span class="zapio-badge">🔮 Espace Sécurisé & Workspace</span></div></div>"""
    st.markdown(auth_header, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            email = st.text_input("Adresse Email", placeholder="nom@exemple.com")
            master_key = st.text_input("Clé Maîtresse / PIN", type="password", placeholder="••••••••")
            
            submit = st.form_submit_button("Se connecter / Sign in")

            if submit:
                if master_key != "":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Veuillez saisir votre clé d'accès.")

# ----------------------------------------------------
# 2. APPLICATION PRINCIPALE
# ----------------------------------------------------
else:
    col_logo, col_logout = st.columns([3, 1])
    
    with col_logo:
        logo_html = """<h1 style="font-size: 2rem; margin: 0; display: flex; align-items: center; gap: 8px;"><span style="color: #FFF;">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 8px; border-radius: 6px; font-size: 1.4rem;">CORE</span><span class="zapio-badge-green" style="font-size: 0.75rem;">● Connecté</span></h1>"""
        st.markdown(logo_html, unsafe_allow_html=True)
        
    with col_logout:
        if st.button("Déconnexion", key="top_logout"):
            st.session_state.authenticated = False
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    menu = st.radio(
        "Navigation",
        [
            "📆 Agenda Premium", 
            "🤖 Prompts AI Code", 
            "🧠 Prompts Claude", 
            "💻 Codes (HTML/CSS/JS)", 
            "🎨 Prompts Images", 
            "💡 Idées", 
            "🚀 Projets en cours", 
            "🔮 Projets futurs", 
            "🔗 Liens Utiles", 
            "📦 Fichiers ZIP",
            "🔑 Mes Clés API",
            "🔐 Mes Accès & Mots de passe"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 15px 0 20px 0;'>", unsafe_allow_html=True)

    # ====================================================
    # 📆 AGENDA PREMIUM (Grille Mensuelle Interactive Pro)
    # ====================================================
    if menu == "📆 Agenda Premium":
        st.markdown("""<div style="margin-bottom: 20px;"><span class="zapio-badge">📅 DESIGN CALENDAR TEMPLATE</span><h2 style="margin-top: 10px; font-size: 2rem;">Agenda & Calendrier Interactif</h2></div>""", unsafe_allow_html=True)

        tab_cal, tab_add = st.tabs(["📅 Vue Calendrier Mensuel", "➕ Programmer un Événement"])

        with tab_cal:
            col_m1, col_m2, col_m3 = st.columns([1, 2, 1])
            with col_m2:
                selected_month = st.selectbox(
                    "Mois",
                    ["Octobre 2026", "Novembre 2026", "Décembre 2026"],
                    index=0,
                    label_visibility="collapsed"
                )

            # Entête des jours de la semaine
            days_header = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
            cols_h = st.columns(7)
            for idx, h in enumerate(days_header):
                cols_h[idx].markdown(f"""<div style="text-align:center; font-weight:800; color:#EC4899; padding:8px; background:#261245; border-radius:8px; border:1px solid #5B21B6;">{h}</div>""", unsafe_allow_html=True)

            st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)

            # Événements du mois (Octobre 2026)
            events_by_day = {}
            for ev in st.session_state.agenda_events:
                if ev['date'].month == 10 and ev['date'].year == 2026:
                    day_num = ev['date'].day
                    if day_num not in events_by_day:
                        events_by_day[day_num] = []
                    events_by_day[day_num].append(ev)

            # Octobre 2026 commence un Jeudi (offset = 3)
            start_day_offset = 3 
            total_days = 31
            current_day = 1

            for week in range(5):
                cols_w = st.columns(7)
                for day_idx in range(7):
                    if week == 0 and day_idx < start_day_offset:
                        cols_w[day_idx].markdown("""<div style="background:rgba(20,9,35,0.4); border:1px solid #261245; border-radius:12px; min-height:85px; padding:6px; opacity:0.3;"></div>""", unsafe_allow_html=True)
                    elif current_day > total_days:
                        cols_w[day_idx].markdown("""<div style="background:rgba(20,9,35,0.4); border:1px solid #261245; border-radius:12px; min-height:85px; padding:6px; opacity:0.3;"></div>""", unsafe_allow_html=True)
                    else:
                        is_today = (current_day == 9)
                        day_events = events_by_day.get(current_day, [])
                        
                        border_color = "#EC4899" if is_today else "#5B21B6"
                        bg_color = "linear-gradient(135deg, #3B1578 0%, #261245 100%)" if is_today else "#1E0A3C"
                        
                        # Tronquage automatique : Max 2 puces visibles par case
                        max_visible_events = 2
                        visible_events = day_events[:max_visible_events]
                        hidden_count = len(day_events) - max_visible_events

                        event_html = ""
                        for ev_item in visible_events:
                            event_html += f"""<div style="background:#F43F5E; color:#FFF; font-size:0.65rem; font-weight:800; border-radius:4px; padding:2px 4px; margin-top:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">⏰ {ev_item['time'].strftime('%H:%M')} - {ev_item['title']}</div>"""

                        if hidden_count > 0:
                            event_html += f"""<div style="background:#A78BFA; color:#1E0A3C; font-size:0.6rem; font-weight:800; border-radius:4px; padding:1px 4px; margin-top:3px; text-align:center;">+{hidden_count} de plus</div>"""

                        pin_str = "📌" if is_today else ""
                        day_color_str = "#EC4899" if is_today else "#FFF"
                        
                        card_inner = f"""<div style="background:{bg_color}; border:1px solid {border_color}; border-radius:12px; min-height:85px; max-height:115px; padding:6px; overflow:hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.3);"><div style="display:flex; justify-content:space-between; align-items:center;"><span style="font-weight:800; font-size:0.85rem; color:{day_color_str};">{current_day} {pin_str}</span></div>{event_html}</div>"""
                        cols_w[day_idx].markdown(card_inner, unsafe_allow_html=True)
                        
                        current_day += 1

            st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 25px 0 15px 0;'>", unsafe_allow_html=True)

            # Liste détaillée chronologique sous le calendrier
            st.subheader("📋 Liste chronologique des événements")
            if st.session_state.agenda_events:
                sorted_events = sorted(st.session_state.agenda_events, key=lambda x: (x['date'], x['time']))
                for ev in sorted_events:
                    desc_val = ev['desc'] if ev['desc'] else '<i>Aucune note fournie</i>'
                    st.markdown(f"""<div class="calendar-event-card"><div class="calendar-date-box"><span style="font-size: 0.75rem; text-transform: uppercase;">{ev['date'].strftime('%b').upper()}</span><span style="font-size: 1.5rem; line-height: 1;">{ev['date'].strftime('%d')}</span><span style="font-size: 0.8rem; margin-top: 3px; opacity: 0.95;">{ev['time'].strftime('%H:%M')}</span></div><div style="flex-grow: 1;"><div style="display:flex; justify-content:space-between; align-items:flex-start;"><h3 style="margin:0; color:#FFFFFF; font-size: 1.2rem;">{ev['title']}</h3><span class="zapio-badge">{ev['category']}</span></div><p style="color:#CBD5E1; margin: 6px 0; font-size: 0.85rem;">{desc_val}</p><div style="font-size: 0.8rem; color: #A78BFA;">🔔 Notification : <b style="color:#FFF;">{ev['ringtone']}</b></div></div></div>""", unsafe_allow_html=True)
            else:
                st.info("Aucun événement dans l'agenda.")

        with tab_add:
            with st.form("add_event_form"):
                st.subheader("Planifier une nouvelle date")
                title = st.text_input("Titre de l'événement / Rappel", placeholder="Ex: Concert / Réunion PavelCore")
                
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
                        st.success("Événement ajouté sur le calendrier !")
                        st.rerun()

    # ====================================================
    # 🤖 PROMPTS AI CODES
    # ====================================================
    elif menu == "🤖 Prompts AI Code":
        st.subheader("🤖 Mes Prompts AI Code")
        with st.form("form_ai_code"):
            title = st.text_input("Titre du Prompt Code")
            selected_lang = st.selectbox("Langage / Framework ciblé", list(LANG_MAP.keys()))
            prompt = st.text_area("Contenu du Prompt AI / Code", height=160)
            tags = st.text_input("Mots-clés / Tags", placeholder="ex: backend, api, auth")
            
            if st.form_submit_button("Enregistrer"):
                if title and prompt:
                    final_lang = LANG_MAP[selected_lang]
                    if final_lang == "auto":
                        final_lang = detect_language(prompt)
                    
                    st.session_state.saved_ai_prompts.append({
                        "title": title, "lang_label": selected_lang, "lang": final_lang, "prompt": prompt, "tags": tags
                    })
                    st.rerun()

        for p in st.session_state.saved_ai_prompts:
            st.markdown(f"""<div class="zapio-card"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;"><h3 style="margin:0; color:#EC4899;">{p['title']}</h3><span class="zapio-badge">{p.get('lang_label', p['lang'].upper())}</span></div>""", unsafe_allow_html=True)
            st.code(p['prompt'], language=p['lang'])
            st.markdown(f"""<span style="color:#A78BFA; font-size:0.75rem;">Tags: {p['tags']}</span></div>""", unsafe_allow_html=True)

    # ====================================================
    # 🧠 PROMPTS CLAUDE
    # ====================================================
    elif menu == "🧠 Prompts Claude":
        st.subheader("🧠 Mes Prompts Spécialisés Claude")
        
        with st.form("form_claude"):
            title = st.text_input("Titre de la consigne", placeholder="Ex: Refactoring React Component")
            system_prompt = st.text_area("System Prompt / Instructions de rôle", height=100, placeholder="Ex: Tu es un expert Senior Python...")
            selected_lang = st.selectbox("Langage / Format principal du Code", list(LANG_MAP.keys()))
            user_prompt = st.text_area("User Prompt / Code collé", height=150, placeholder="Collez le code ou la consigne ici...")
            artifacts = st.text_input("Artifacts attendus", placeholder="ex: Application React, Script Python")
            
            if st.form_submit_button("Sauvegarder le Prompt Claude"):
                if title and user_prompt:
                    final_lang = LANG_MAP[selected_lang]
                    if final_lang == "auto":
                        final_lang = detect_language(user_prompt)

                    st.session_state.saved_claude_prompts.append({
                        "title": title, "sys": system_prompt, "user": user_prompt, "artifacts": artifacts, "lang_label": selected_lang, "lang": final_lang
                    })
                    st.success("Prompt enregistré !")
                    st.rerun()

        for c in st.session_state.saved_claude_prompts:
            st.markdown(f"""<div class="zapio-card"><div style="display:flex; justify-content:space-between; align-items:center;"><h3 style="color:#EC4899; margin:0;">{c['title']}</h3><span class="zapio-badge">{c.get('lang_label', 'Python')}</span></div><p style="color:#CBD5E1; font-size:0.85rem; margin-top:5px;"><b>System:</b> {c['sys']}</p>""", unsafe_allow_html=True)
            st.code(c['user'], language=c.get('lang', 'python'))
            st.markdown(f"""<span class="zapio-badge-green">Artifact: {c['artifacts']}</span></div>""", unsafe_allow_html=True)

    # ====================================================
    # 💻 CODES (HTML/CSS/JS)
    # ====================================================
    elif menu == "💻
