import sys
import os
import re
import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import streamlit.components.v1 as components

# Correction du chemin d'importation pour Streamlit Cloud
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration de la page
st.set_page_config(
    page_title="PavelCore — Workspace & Agenda Premium",
    page_icon="🔴",
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
    "JavaScript / React": "javascript",
    "HTML5": "html",
    "CSS3 / TailWind": "css",
    "SQL": "sql",
    "PHP / WordPress": "php",
    "Flutter / Flet": "python",
    "JSON / Config": "json",
    "Détection Automatique": "auto"
}

# Global State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "agenda_events" not in st.session_state:
    st.session_state.agenda_events = [
        {"title": "Lancement Application PavelCore", "date": date(2026, 10, 25), "time": time(10, 0), "category": "Projet", "desc": "Mise en ligne sur Streamlit", "ringtone": "Alarme Digitale"}
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


# ----------------------------------------------------
# 1. AUTHENTIFICATION
# ----------------------------------------------------
if not st.session_state.authenticated:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 25px;">
                <h1 style="font-size: 2.5rem; margin-bottom: 5px;">
                    <span style="color: #FFFFFF;">pavel</span><span style="background: #FF3B30; color: #FFF; padding: 2px 10px; border-radius: 8px; font-size: 1.8rem; margin-left: 4px;">CORE</span>
                </h1>
                <div style="margin-top: 15px;">
                    <span class="zapio-badge">🔴 Espace Sécurisé & Workspace</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Adresse Email", placeholder="nom@exemple.com")
            master_key = st.text_input("Clé Maîtresse / PIN", type="password", placeholder="••••••••")
            
            st.markdown("<br>", unsafe_allow_html=True)
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
        st.markdown("""
            <h2 style="font-size: 1.8rem; margin: 0; display: flex; align-items: center; gap: 10px;">
                <span style="color: #FFF;">pavel</span><span style="background: #FF3B30; color: #FFF; padding: 2px 8px; border-radius: 6px; font-size: 1.2rem;">CORE</span>
                <span class="zapio-badge-green" style="font-size: 0.75rem;">● Connecté</span>
            </h2>
        """, unsafe_allow_html=True)
        
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
            "🔑 Mes Clés API"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 15px 0 20px 0;'>", unsafe_allow_html=True)

    # ====================================================
    # 📆 AGENDA PREMIUM (Avec Lecteur d'Alarme Fiable)
    # ====================================================
    if menu == "📆 Agenda Premium":
        st.markdown("""
            <div style="margin-bottom: 20px;">
                <span class="zapio-badge">🔴 Gestionnaire Temporel & Rappels Sonores</span>
                <h1 style="margin-top: 10px;">Agenda Ultra Premium</h1>
            </div>
        """, unsafe_allow_html=True)

        today = date.today()
        today_events = [e for e in st.session_state.agenda_events if e['date'] == today]

        if today_events:
            st.markdown(f"""
                <div class="zapio-card" style="border-color: #FF3B30;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="zapio-badge">🔔 ALERTE ÉVÉNEMENT AUJOURD'HUI</span>
                        <span style="color:#8E8E93; font-size:0.85rem;">{today.strftime('%d/%m/%Y')}</span>
                    </div>
                    <h3 style="color:#FFF; margin-top:10px;">Vous avez {len(today_events)} événement(s) prévu(s) aujourd'hui !</h3>
                </div>
            """, unsafe_allow_html=True)
            
            components.html("""
                <div style="text-align: center; background: #16161E; padding: 12px; border-radius: 12px; border: 1px solid #FF3B30;">
                    <p style="color: #FFF; font-family: sans-serif; font-weight: bold; font-size: 0.9rem; margin-bottom: 8px;">
                        🔊 RAPPEL SONORE ACTIF
                    </p>
                    <button onclick="playAlarm()" style="background: #FF3B30; color: white; border: none; padding: 8px 18px; border-radius: 20px; font-weight: bold; cursor: pointer; font-size: 0.85rem;">
                        🔔 Déclencher / Tester la Sonnerie
                    </button>
                    <audio id="alarmAudio" src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" preload="auto"></audio>
                    <script>
                        function playAlarm() {
                            var audio = document.getElementById('alarmAudio');
                            audio.play().catch(function(error) {
                                console.log("Autoplay bloqué par le navigateur");
                            });
                        }
                        window.onload = function() {
                            playAlarm();
                        };
                    </script>
                </div>
            """, height=100)

        tab_add, tab_view = st.tabs(["➕ Ajouter un Événement", "📅 Vue Calendrier & Liste"])

        with tab_add:
            with st.form("add_event_form"):
                st.subheader("Planifier un événement")
                title = st.text_input("Titre de l'événement / Rappel", placeholder="Ex: Réunion projet Reborn Beauty")
                
                c_date, c_time = st.columns(2)
                with c_date:
                    event_date = st.date_input("Date (Jour / Mois / Année)", value=date.today())
                with c_time:
                    event_time = st.time_input("Heure de l'événement", value=time(12, 0))

                c_cat, c_ring = st.columns(2)
                with c_cat:
                    category = st.selectbox("Catégorie", ["Business / Travail", "Dev & Tech", "Personnel", "Rendez-vous Urgent", "Événement DJ / Event"])
                with c_ring:
                    ringtone = st.selectbox("Sonnerie & Notification", ["Alarme Digitale", "Bip Futuriste", "Douce Mélodie", "Silence"])

                desc = st.text_area("Description / Notes supplémentaires")

                if st.form_submit_button("🔔 Enregistrer dans l'Agenda"):
                    if title:
                        st.session_state.agenda_events.append({
                            "title": title, "date": event_date, "time": event_time,
                            "category": category, "desc": desc, "ringtone": ringtone
                        })
                        st.success("Événement ajouté avec succès !")
                        st.rerun()

        with tab_view:
            if st.session_state.agenda_events:
                for ev in st.session_state.agenda_events:
                    st.markdown(f"""
                        <div class="zapio-card">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <h3 style="margin:0; color:#FF3B30;">{ev['title']}</h3>
                                <span class="zapio-badge">{ev['category']}</span>
                            </div>
                            <p style="color:#A0A0AB; margin:10px 0;">{ev['desc']}</p>
                            <div style="font-size:0.85rem; color:#FFF; display:flex; gap:20px;">
                                <span>📅 Date : <b>{ev['date'].strftime('%d/%m/%Y')}</b></span>
                                <span>⏰ Heure : <b>{ev['time'].strftime('%H:%M')}</b></span>
                                <span>🔔 Sonnerie : <b>{ev['ringtone']}</b></span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    # ====================================================
    # 🤖 PROMPTS AI CODES
    # ====================================================
    elif menu == "🤖 Prompts AI Code":
        st.markdown("## 🤖 Mes Prompts AI Code")
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
