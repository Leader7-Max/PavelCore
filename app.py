import sys
import os
import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import streamlit.components.v1 as components

# Configuration de la page
st.set_page_config(
    page_title="PavelCore — Workspace & Agenda Premium",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from assets.styles import inject_custom_design
inject_custom_design()

# Global State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Initialisation des bases de données de sauvegarde
if "agenda_events" not in st.session_state:
    st.session_state.agenda_events = [
        {"title": "Lancement Application PavelCore", "date": date(2026, 10, 25), "time": time(10, 0), "category": "Projet", "desc": "Mise en ligne sur Streamlit", "ringtone": "Alarme Digitale", "notified": False}
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
    # Header Supérieur
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

    # Navigation horizontale tactile
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
            "📦 Fichiers ZIP"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 15px 0 20px 0;'>", unsafe_allow_html=True)

    # ====================================================
    # 📆 MODULE AGENDA ULTRA PREMIUM
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
            
            st.components.v1.html("""
                <audio autoplay>
                    <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
                </audio>
            """, height=0)

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
                    ringtone = st.selectbox("Sonnerie & Notification", ["Alarme Digitale", "Bip Futurg", "Douce Mélodie", "Silence"])

                desc = st.text_area("Description / Notes supplémentaires")

                if st.form_submit_button("🔔 Enregistrer dans l'Agenda"):
                    if title:
                        st.session_state.agenda_events.append({
                            "title": title, "date": event_date, "time": event_time,
                            "category": category, "desc": desc, "ringtone": ringtone, "notified": False
                        })
                        st.success("Événement ajouté avec succès !")
                        st.rerun()

        with tab_view:
            st.markdown("### Événements Planifiés")
            if st.session_state.agenda_events:
                for idx, ev in enumerate(st.session_state.agenda_events):
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
            else:
                st.info("Aucun événement enregistré dans l'agenda.")

    # ====================================================
    # 🤖 PROMPTS AI CODES
    # ====================================================
    elif menu == "🤖 Prompts AI Code":
        st.markdown("## 🤖 Mes Prompts AI Code (ChatGPT, Copilot, Cursor)")
        with st.form("form_ai_code"):
            title = st.text_input("Titre du Prompt Code")
            language = st.selectbox("Langage / Framework ciblé", ["Python", "JavaScript", "React", "SQL", "HTML/CSS", "Flutter / Flet", "Autre"])
            prompt = st.text_area("Contenu du Prompt AI", height=150)
            tags = st.text_input("Mots-clés (séparés par des virgules)", placeholder="ex: backend, api, auth")
            if st.form_submit_button("Enregistrer le Prompt AI Code"):
                if title and prompt:
                    st.session_state.saved_ai_prompts.append({"title": title, "lang": language, "prompt": prompt, "tags": tags})
                    st.rerun()

        for p in st.session_state.saved_ai_prompts:
            st.markdown(f"""
                <div class="zapio-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="margin:0; color:#FF3B30;">{p['title']}</h3>
                        <span class="zapio-badge">{p['lang']}</span>
                    </div>
                    <div class="code-box" style="margin-top:10px;">{p['prompt']}</div>
                    <span style="color:#8E8E93; font-size:0.75rem; margin-top:5px; display:block;">Tags: {p['tags']}</span>
                </div>
            """, unsafe_allow_html=True)

    # ====================================================
    # 🧠 PROMPTS CLAUDE
    # ====================================================
    elif menu == "🧠 Prompts Claude":
        st.markdown("## 🧠 Mes Prompts Spécialisés Claude (Anthropic)")
        with st.form("form_claude"):
            title = st.text_input("Titre de la consigne / Prompt")
            system_prompt = st.text_area("System Prompt / Instructions de rôle", height=100)
            user_prompt = st.text_area("User Prompt / Message principal", height=150)
            artifacts = st.text_input("Format de sortie / Artifacts attendus", placeholder="ex: SVG, Document React, Code complet")
            if st.form_submit_button("Enregistrer le Prompt Claude"):
                if title:
                    st.session_state.saved_claude_prompts.append({"title": title, "sys": system_prompt, "user": user_prompt, "artifacts": artifacts})
                    st.rerun()

        for c in st.session_state.saved_claude_prompts:
            st.markdown(f"""
                <div class="zapio-card">
                    <h3 style="color:#FF3B30; margin:0;">{c['title']}</h3>
                    <p style="color:#8E8E93; font-size:0.85rem; margin-top:5px;"><b>System:</b> {c['sys']}</p>
                    <div class="code-box">{c['user']}</div>
                    <span class="zapio-badge-green" style="margin-top:8px;">Artifact: {c['artifacts']}</span>
                </div>
            """, unsafe_allow_html=True)

    # ====================================================
    # 💻 CODES (HTML / CSS / JS)
    # ====================================================
    elif menu == "💻 Codes (HTML/CSS/JS)":
        st.markdown("## 💻 Mes Snippets de Code (HTML, CSS, JS, Python)")
        with st.form("form_code"):
            title = st.text_input("Nom de la fonction / Snippet")
            type_code = st.selectbox("Type de code", ["HTML5", "CSS3 / TailWind", "JavaScript / ES6", "Python / Streamlit", "PHP / WordPress"])
            code_content = st.text_area("Code source", height=180)
            usage_note = st.text_input("Note d'utilisation / Emplacement")
            if st.form_submit_button("Enregistrer le Snippet"):
                if title and code_content:
                    st.session_state.saved_code_snippets.append({"title": title, "type": type_code, "code": code_content, "note": usage_note})
                    st.rerun()

        for cd in st.session_state.saved_code_snippets:
            st.markdown(f"""
                <div class="zapio-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="margin:0; color:#FFF;">{cd['title']}</h3>
                        <span class="zapio-badge">{cd['type']}</span>
                    </div>
                    <p style="color:#8E8E93; font-size:0.8rem; margin:5px 0;">{cd['note']}</p>
                    <div class="code-box">{cd['code']}</div>
                </div>
            """, unsafe_allow_html=True)

    # ====================================================
    # 🎨 PROMPTS IMAGES
    # ====================================================
    elif menu == "🎨 Prompts Images":
        st.markdown("## 🎨 Mes Prompts d'Images (Midjourney, DALL-E, Flux)")
        with st.form("form_img_prompt"):
            title = st.text_input("Titre / Concept Visuel")
            generator = st.selectbox("Générateur", ["Midjourney v6", "DALL-E 3", "Flux.1", "Stable Diffusion"])
            prompt_text = st.text_area("Prompt complet / Description détaillée", height=120)
            aspect_ratio = st.selectbox("Format d'image (--ar)", ["1:1 (Carré)", "16:9 (Flyer / Ecran)", "9:16 (Story / Kakemono)", "4:5 (Instagram)"])
            negative_prompt = st.text_input("Prompt négatif / Éléments à exclure")
            if st.form_submit_button("Enregistrer le Prompt Image"):
                if title and prompt_text:
                    st.session_state.saved_image_prompts.append({
                        "title": title, "gen": generator, "prompt": prompt_text, "ar": aspect_ratio, "neg": negative_prompt
                    })
                    st.rerun()

        for img in st.session_state.saved_image_prompts:
            st.markdown(f"""
                <div class="zapio-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="margin:0; color:#FF3B30;">{img['title']}</h3>
                        <span class="zapio-badge">{img['gen']}</span>
                    </div>
                    <div class="code-box" style="margin-top:10px;">{img['prompt']}</div>
                    <div style="margin-top:8px; font-size:0.8rem; color:#8E8E93;">
                        <span>Format: <b>{img['ar']}</b></span> | <span>Exclure: <b>{img['neg']}</b></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # ====================================================
    # 💡 BOÎTE À IDÉES
    # ====================================================
    elif menu == "💡 Idées":
        st.markdown("## 💡 Boîte à Idées & Concepts")
        with st.form("form_ideas"):
            title = st.text_input("Titre de l'idée")
            category = st.selectbox("Domaine", ["Business & E-commerce", "Développement Web & App", "Événementiel & DJ", "Personnel"])
            description = st.text_area("Description détaillée de l'idée", height=120)
            impact = st.select_slider("Niveau d'impact estimé", options=["Faible", "Moyen", "Fort", "Révolutionnaire !"])
            if st.form_submit_button("Sauvegarder l'Idée"):
                if title:
                    st.session_state.saved_ideas.append({"title": title, "cat": category, "desc": description, "impact": impact})
                    st.rerun()

        for id_item in st.session_state.saved_ideas:
            st.markdown(f"""
                <div class="zapio-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="margin:0; color:#FFF;">{id_item['title']}</h3>
                        <span class="zapio-badge">{id_item['cat']}</span>
                    </div>
                    <p style="color:#A0A0AB; margin-top:10px;">{id_item['desc']}</p>
                    <span class="zapio-badge-green">Impact: {id_item['impact']}</span>
                </div>
            """, unsafe_allow_html=True)

    # ====================================================
    # 🚀 PROJETS EN COURS
    # ====================================================
    elif menu == "🚀 Projets en cours":
        st.markdown("## 🚀 Suivi des Projets Actifs")
        with st.form("form_curr_proj"):
            name = st.text_input("Nom du projet")
            client = st.text_input("Client / Marque ciblé")
            progress = st.slider("Avancement (%)", 0, 100, 25)
            next_step = st.text_input("Prochaine action critique")
            deadline = st.date_input("Date limite visée")
            if st.form_submit_button("Enregistrer le projet actif"):
                if name:
                    st.session_state.saved_current_projects.append({
                        "name": name, "client": client, "progress": progress, "next": next_step, "deadline": str(deadline)
                    })
                    st.rerun()

        for cp in st.session_state.saved_current_projects:
            st.markdown(f"""
                <div class="zapio-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="margin:0; color:#FF3B30;">{cp['name']}</h3>
                        <span style="color:#FFF;">Client: <b>{cp['client']}</b></span>
                    </div>
                    <p style="margin:10px 0; color:#8E8E93;">Prochaine étape: <b>{cp['next']}</b></p>
                    <div style="font-size:0.85rem; color:#FFF;">Avancement : {cp['progress']}% | Échéance : {cp['deadline']}</div>
                </div>
            """, unsafe_allow_html=True)

    # ====================================================
    # 🔮 PROJETS FUTURS
    # ====================================================
    elif menu == "🔮 Projets futurs":
        st.markdown("## 🔮 Projets Futurs & Vision")
        with st.form("form_fut_proj"):
            name = st.text_input("Nom du projet futur")
            horizon = st.selectbox("Horizon de lancement", ["Court terme (1-3 mois)", "Moyen terme (6 mois)", "Long terme (1 an et +)"])
            resources = st.text_area("Ressources nécessaires (Budget, Compétences, Outils)", height=100)
            goal = st.text_input("Objectif principal")
            if st.form_submit_button("Ajouter à la vision"):
                if name:
                    st.session_state.saved_future_projects.append({"name": name, "horizon": horizon, "resources": resources, "goal": goal})
                    st.rerun()

        for fp in st.session_state.saved_future_projects:
            st.markdown(f"""
                <div class="zapio-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="margin:0; color:#FFF;">{fp['name']}</h3>
                        <span class="zapio-badge">{fp['horizon']}</span>
                    </div>
                    <p style="color:#A0A0AB; margin-top:10px;"><b>Objectif:</b> {fp['goal']}</p>
                    <p style="color:#8E8E93; font-size:0.85rem;"><b>Ressources requises:</b> {fp['resources']}</p>
                </div>
            """, unsafe_allow_html=True)

    # ====================================================
    # 🔗 MES LIENS
