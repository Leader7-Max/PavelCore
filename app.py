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
        st.markdown('<h1 style="font-size: 2rem; margin: 0; display: flex; align-items: center; gap: 8px;"><span style="color: #FFF;">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 8px; border-radius: 6px; font-size: 1.4rem;">CORE</span><span class="zapio-badge-green" style="font-size: 0.75rem;">● Connecté / Offline Ready</span></h1>', unsafe_allow_html=True)
        
    with col_logout:
        if st.button("Déconnexion", key="top_logout"):
            st.session_state.authenticated = False
            st.session_state.direct_agenda = False
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

    if menu == "📆 Agenda Premium":
        render_agenda_module()

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
            lang_txt = p.get('lang_label', p['lang'].upper())
            st.markdown(f'<div class="zapio-card"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;"><h3 style="margin:0; color:#EC4899;">{p["title"]}</h3><span class="zapio-badge">{lang_txt}</span></div>', unsafe_allow_html=True)
            st.code(p['prompt'], language=p['lang'])
            st.markdown(f'<span style="color:#A78BFA; font-size:0.75rem;">Tags: {p["tags"]}</span></div>', unsafe_allow_html=True)

    elif menu == "🧠 Prompts Claude":
        st.subheader("🧠 Mes Prompts Spécialisés Claude")
        with st.form("form_claude"):
            title = st.text_input("Titre de la consigne", placeholder="Ex: Refactoring React Component")
            system_prompt = st.text_area("System Prompt / Instructions de rôle", height=100)
            selected_lang = st.selectbox("Langage / Format principal du Code", list(LANG_MAP.keys()))
            user_prompt = st.text_area("User Prompt / Code collé", height=150)
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
            lang_label = c.get('lang_label', 'Python')
            st.markdown(f'<div class="zapio-card"><div style="display:flex; justify-content:space-between; align-items:center;"><h3 style="color:#EC4899; margin:0;">{c["title"]}</h3><span class="zapio-badge">{lang_label}</span></div><p style="color:#CBD5E1; font-size:0.85rem; margin-top:5px;"><b>System:</b> {c["sys"]}</p>', unsafe_allow_html=True)
            st.code(c['user'], language=c.get('lang', 'python'))
            st.markdown(f'<span class="zapio-badge-green">Artifact: {c["artifacts"]}</span></div>', unsafe_allow_html=True)

    elif menu == "💻 Codes (HTML/CSS/JS)":
        st.subheader("💻 Mes Snippets de Code")
        with st.form("form_code"):
            title = st.text_input("Nom de la fonction / Snippet")
            selected_lang = st.selectbox("Langage du Snippet", list(LANG_MAP.keys()))
            code_content = st.text_area("Collez votre code ici", height=180)
            usage_note = st.text_input("Note d'utilisation")
            if st.form_submit_button("Enregistrer le Code"):
                if title and code_content:
                    final_lang = LANG_MAP[selected_lang]
                    if final_lang == "auto":
                        final_lang = detect_language(code_content)
                    st.session_state.saved_code_snippets.append({
                        "title": title, "type_label": selected_lang, "type": final_lang, "code": code_content, "note": usage_note
                    })
                    st.rerun()

        for cd in st.session_state.saved_code_snippets:
            type_lbl = cd.get('type_label', cd['type'].upper())
            st.markdown(f'<div class="zapio-card"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;"><h3 style="margin:0; color:#FFF;">{cd["title"]}</h3><span class="zapio-badge">{type_lbl}</span></div><p style="color:#CBD5E1; font-size:0.8rem; margin:2px 0;">{cd["note"]}</p>', unsafe_allow_html=True)
            st.code(cd['code'], language=cd['type'])
            st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "🎨 Prompts Images":
        st.subheader("🎨 Mes Prompts d'Images")
        with st.form("form_img_prompt"):
            title = st.text_input("Titre / Concept Visuel")
            generator = st.selectbox("Générateur", ["Midjourney v6", "DALL-E 3", "Flux.1", "Stable Diffusion"])
            prompt_text = st.text_area("Prompt complet", height=120)
            aspect_ratio = st.selectbox("Format d'image", ["1:1 (Carré)", "16:9 (Ecran)", "9:16 (Story/Kakemono)", "4:5 (Instagram)"])
            negative_prompt = st.text_input("Prompt négatif")
            if st.form_submit_button("Enregistrer"):
                if title and prompt_text:
                    st.session_state.saved_image_prompts.append({
                        "title": title, "gen": generator, "prompt": prompt_text, "ar": aspect_ratio, "neg": negative_prompt
                    })
                    st.rerun()

        for img in st.session_state.saved_image_prompts:
            st.markdown(f'<div class="zapio-card"><div style="display:flex; justify-content:space-between; align-items:center;"><h3 style="margin:0; color:#EC4899;">{img["title"]}</h3><span class="zapio-badge">{img["gen"]}</span></div>', unsafe_allow_html=True)
            st.code(img['prompt'], language="text")
            st.markdown(f'<div style="font-size:0.8rem; color:#A78BFA;">Format: <b>{img["ar"]}</b> | Exclure: <b>{img["neg"]}</b></div></div>', unsafe_allow_html=True)

    elif menu == "💡 Idées":
        st.subheader("💡 Boîte à Idées")
        with st.form("form_ideas"):
            title = st.text_input("Titre de l'idée")
            category = st.selectbox("Domaine", ["Business & E-commerce", "Développement Web & App", "Événementiel & DJ", "Personnel"])
            description = st.text_area("Description de l'idée", height=120)
            impact = st.select_slider("Niveau d'impact", options=["Faible", "Moyen", "Fort", "Révolutionnaire !"])
            if st.form_submit_button("Sauvegarder"):
                if title:
                    st.session_state.saved_ideas.append({"title": title, "cat": category, "desc": description, "impact": impact})
                    st.rerun()

        for id_item in st.session_state.saved_ideas:
            st.markdown(f'<div class="zapio-card"><div style="display:flex; justify-content:space-between; align-items:center;"><h3 style="margin:0; color:#FFF;">{id_item["title"]}</h3><span class="zapio-badge">{id_item["cat"]}</span></div><p style="color:#CBD5E1; margin-top:10px;">{id_item["desc"]}</p><span class="zapio-badge-green">Impact: {id_item["impact"]}</span></div>', unsafe_allow_html=True)

    elif menu == "🚀 Projets en cours":
        st.subheader("🚀 Suivi des Projets Actifs")
        with st.form("form_curr_proj"):
            name = st.text_input("Nom du projet")
            client = st.text_input("Client / Marque")
            priority = st.selectbox("Priorité / Urgence", ["🔴 Haute / Urgente", "🟠 Moyenne", "🟢 Basse"])
            next_step = st.text_input("Prochaine étape")
            deadline = st.date_input("Date limite")
            project_desc = st.text_area("Description / Notes détaillées du projet", height=120)
            if st.form_submit_button("Enregistrer le Projet"):
                if name:
                    st.session_state.saved_current_projects.append({
                        "name": name, "client": client, "priority": priority, "next": next_step, "deadline": str(deadline), "desc": project_desc
                    })
                    st.rerun()

        for cp in st.session_state.saved_current_projects:
            priority_val = cp.get('priority', '🔴 Haute')
            desc_val = cp.get('desc', '')
            st.markdown(f'<div class="zapio-card"><div style="display:flex; justify-content:space-between; align-items:center;"><h3 style="margin:0; color:#EC4899;">{cp["name"]}</h3><div><span class="zapio-badge" style="margin-right:8px;">{priority_val}</span><span style="color:#FFF; font-size:0.9rem;">Client: <b>{cp["client"]}</b></span></div></div><p style="margin:12px 0 8px 0; color:#E2E8F0;">{desc_val}</p><div style="font-size:0.85rem; color:#A78BFA; display:flex; gap:20px; margin-top:8px;"><span>🎯 Prochaine étape : <b style="color:#FFF;">{cp["next"]}</b></span><span>⏰ Échéance : <b style="color:#FFF;">{cp["deadline"]}</b></span></div></div>', unsafe_allow_html=True)

    elif menu == "🔮 Projets futurs":
        st.subheader("🔮 Projets Futurs")
        with st.form("form_fut_proj"):
            name = st.text_input("Nom du projet futur")
            horizon = st.selectbox("Horizon", ["Court terme (1-3 mois)", "Moyen terme (6 mois)", "Long terme (1 an et +)"])
            resources = st.text_area("Ressources requises", height=100)
            goal = st.text_input("Objectif principal")
            if st.form_submit_button("Ajouter à la vision"):
                if name:
                    st.session_state.saved_future_projects.append({"name": name, "horizon": horizon, "resources": resources, "goal": goal})
                    st.rerun()

        for fp in st.session_state.saved_future_projects:
            st.markdown(f'<div class="zapio-card"><div style="display:flex; justify-content:space-between; align-items:center;"><h3 style="margin:0; color:#FFF;">{fp["name"]}</h3><span class="zapio-badge">{fp["horizon"]}</span></div><p style="color:#CBD5E1; margin-top:10px;"><b>Objectif:</b> {fp["goal"]}</p><p style="color:#A78BFA; font-size:0.85rem;"><b>Ressources:</b> {fp["resources"]}</p></div>', unsafe_allow_html=True)

    elif menu == "🔗 Liens Utiles":
        st.subheader("🔗 Sauvegarde de Liens Web")
        with st.form("form_links"):
            title = st.text_input("Nom du site / Application")
            url = st.text_input("Lien URL (https://...)")
            category = st.selectbox("Catégorie", ["Doc Tech & API", "Outils Design & AI", "Téléchargement d'Apps & Logiciels", "Sites Web Utiles & Services", "Ressources & Banques d'Images", "E-commerce & Business", "Inspiration / Modèles", "Administration / Finance"])
            note = st.text_input("Note")
            if st.form_submit_button("Enregistrer le Lien"):
                if title and url:
                    st.session_state.saved_links.append({"title": title, "url": url, "cat": category, "note": note})
                    st.rerun()

        for lk in st.session_state.saved_links:
            st.markdown(f'<div class="zapio-card"><div style="display:flex; justify-content:space-between; align-items:center;"><h3 style="margin:0; color:#EC4899;">{lk["title"]}</h3><span class="zapio-badge">{lk["cat"]}</span></div><a href="{lk["url"]}" target="_blank" style="color:#38BDF8; display:block; margin:8px 0;">{lk["url"]}</a><span style="color:#A78BFA; font-size:0.8rem;">{lk["note"]}</span></div>', unsafe_allow_html=True)

    elif menu == "📦 Fichiers ZIP":
        st.subheader("📦 Banque de Fichiers ZIP")
        with st.form("form_zip"):
            title = st.text_input("Nom du projet / Archive")
            cloud_link = st.text_input("Lien de Téléchargement")
            version = st.text_input("Version", value="v1.0")
            contents = st.text_area("Contenu détaillé du dossier ZIP", height=100)
            if st.form_submit_button("Enregistrer"):
                if title and cloud_link:
                    st.session_state.saved_zip_files.append({"title": title, "link": cloud_link, "version": version, "contents": contents})
                    st.rerun()

        for zp in st.session_state.saved_zip_files:
            st.markdown(f'<div class="zapio-card"><div style="display:flex; justify-content:space-between; align-items:center;"><h3 style="margin:0; color:#FFF;">{zp["title"]} <span style="font-size:0.8rem; color:#A78BFA;">({zp["version"]})</span></h3><a href="{zp["link"]}" target="_blank" class="zapio-badge-green" style="text-decoration:none;">📥 Télécharger ZIP</a></div><p style="color:#CBD5E1; margin-top:10px; font-size:0.85rem;"><b>Contenu:</b> {zp["contents"]}</p></div>', unsafe_allow_html=True)

    elif menu == "🔑 Mes Clés API":
        st.subheader("🔑 Sauvegarde Sécurisée de Clés API")
        with st.form("form_api_key"):
            service_name = st.text_input("Service / Plateforme")
            api_key_val = st.text_input("Clé API / Secret Token", type="password")
            provider_env = st.selectbox("Environnement", ["Production", "Développement / Test", "Staging"])
            notes = st.text_input("Notes / Projet associé")
            if st.form_submit_button("🔑 Sauvegarder la clé API"):
                if service_name and api_key_val:
                    st.session_state.saved_api_keys.append({"service": service_name, "key": api_key_val, "env": provider_env, "notes": notes})
                    st.success("Clé API enregistrée !")
                    st.rerun()

        for ak in st.session_state.saved_api_keys:
            note_txt = ak['notes'] if ak['notes'] else 'Aucune note'
            st.markdown(f'<div class="zapio-card"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;"><h3 style="margin:0; color:#EC4899;">🔑 {ak["service"]}</h3><span class="zapio-badge">{ak["env"]}</span></div><p style="color:#CBD5E1; font-size:0.85rem; margin: 4px 0;"><b>Notes:</b> {note_txt}</p>', unsafe_allow_html=True)
            st.code(ak['key'], language="text")
            st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "🔐 Mes Accès & Mots de passe":
        st.subheader("🔐 Coffre-Fort d'Accès, PIN & Mots de Passe")
        with st.form("form_user_cred"):
            platform_name = st.text_input("Plateforme / Site / Application")
            username_val = st.text_input("Identifiant / Email")
            password_val = st.text_input("Mot de passe / PIN", type="password")
            cred_type = st.selectbox("Type d'accès", ["Compte Web / Service", "Code PIN / Sécurité", "Serveur / SSH / BDD", "Application Mobile"])
            cred_notes = st.text_input("Notes & URL de connexion")
            if st.form_submit_button("🔐 Enregistrer les Identifiants"):
                if platform_name and (username_val or password_val):
                    st.session_state.saved_user_credentials.append({"platform": platform_name, "username": username_val, "password": password_val, "type": cred_type, "notes": cred_notes})
                    st.success("Accès enregistré !")
                    st.rerun()

        for cred in st.session_state.saved_user_credentials:
            user_txt = cred['username'] if cred['username'] else 'N/A'
            notes_txt = cred['notes'] if cred['notes'] else 'Aucune note'
            st.markdown(f'<div class="zapio-card"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;"><h3 style="margin:0; color:#EC4899;">🔐 {cred["platform"]}</h3><span class="zapio-badge">{cred["type"]}</span></div><p style="color:#FFFFFF; font-size:0.9rem; margin: 4px 0;"><b>User :</b> {user_txt}</p><p style="color:#CBD5E1; font-size:0.85rem; margin: 4px 0;"><b>Notes / URL :</b> {notes_txt}</p>', unsafe_allow_html=True)
            st.code(cred['password'], language="text")
            st.markdown('</div>', unsafe_allow_html=True)
