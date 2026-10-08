import sys
import os
import re
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

# Détecteur automatique de secours
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

# Map pour Streamlit syntax highlighter
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
            "📦 Fichiers ZIP"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 15px 0 20px 0;'>", unsafe_allow_html=True)

    # ====================================================
    # 📆 AGENDA PREMIUM
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

        for p in st.session_state.saved_ai_prompts:
            st.markdown(f"""
                <div class="zapio-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
                        <h3 style="margin:0; color:#FF3B30;">{p['title']}</h3>
                        <span class="zapio-badge">{p.get('lang_label', p['lang'].upper())}</span>
                    </div>
            """, unsafe_allow_html=True)
            st.code(p['prompt'], language=p['lang'])
            st.markdown(f"""<span style="color:#8E8E93; font-size:0.75rem;">Tags: {p['tags']}</span></div>""", unsafe_allow_html=True)

    # ====================================================
    # 🧠 PROMPTS CLAUDE
    # ====================================================
    elif menu == "🧠 Prompts Claude":
        st.markdown("## 🧠 Mes Prompts Spécialisés Claude")
        with st.form("form_claude"):
            title = st.text_input("Titre de la consigne")
            system_prompt = st.text_area("System Prompt / Instructions de rôle", height=100)
            selected_lang = st.selectbox("Langage / Format principal du Code", list(LANG_MAP.keys()))
            user_prompt = st.text_area("User Prompt / Code collé", height=150)
            artifacts = st.text_input("Artifacts attendus", placeholder="ex: Application React, Script Python")
            
            if st.form_submit_button("Enregistrer"):
                if title:
                    final_lang = LANG_MAP[selected_lang]
                    if final_lang == "auto":
                        final_lang = detect_language(user_prompt)

                    st.session_state.saved_claude_prompts.append({
                        "title": title, "sys": system_prompt, "user": user_prompt, "artifacts": artifacts, "lang_label": selected_lang, "lang": final_lang
                    })
                    st.rerun()

        for c in st.session_state.saved_claude_prompts:
            st.markdown(f"""
                <div class="zapio-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="color:#FF3B30; margin:0;">{c['title']}</h3>
                        <span class="zapio-badge">{c.get('lang_label', 'Python')}</span>
                    </div>
                    <p style="color:#8E8E93; font-size:0.85rem; margin-top:5px;"><b>System:</b> {c['sys']}</p>
            """, unsafe_allow_html=True)
            st.code(c['user'], language=c.get('lang', 'python'))
            st.markdown(f"""<span class="zapio-badge-green">Artifact: {c['artifacts']}</span></div>""", unsafe_allow_html=True)

    # ====================================================
    # 💻 CODES (HTML/CSS/JS)
    # ====================================================
    elif menu == "💻 Codes (HTML/CSS/JS)":
        st.markdown("## 💻 Mes Snippets de Code")
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
            st.markdown(f"""
                <div class="zapio-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <h3 style="margin:0; color:#FFF;">{cd['title']}</h3>
                        <span class="zapio-badge">{cd.get('type_label', cd['type'].upper())}</span>
                    </div>
                    <p style="color:#8E8E93; font-size:0.8rem; margin:2px 0;">{cd['note']}</p>
            """, unsafe_allow_html=True)
            st.code(cd['code'], language=cd['type'])
            st.markdown("</div>", unsafe_allow_html=True)

    # ====================================================
    # 🎨 PROMPTS IMAGES
    # ====================================================
    elif menu == "🎨 Prompts Images":
        st.markdown("## 🎨 Mes Prompts d'Images")
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
            st.markdown(f"""
                <div class="zapio-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="margin:0; color:#FF3B30;">{img['title']}</h3>
                        <span class="zapio-badge">{img['gen']}</span>
                    </div>
            """, unsafe_allow_html=True)
            st.code(img['prompt'], language="text")
            st.markdown(f"""<div style="font-size:0.8rem; color:#8E8E93;">Format: <b>{img['ar']}</b> | Exclure: <b>{img['neg']}</b></div></div>""", unsafe_allow_html=True)

    # ====================================================
    # 💡 IDÉES
    # ====================================================
    elif menu == "💡 Idées":
        st.markdown("## 💡 Boîte à Idées")
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
            client = st.text_input("Client / Marque")
            progress = st.slider("Avancement (%)", 0, 100, 25)
            next_step = st.text_input("Prochaine étape")
            deadline = st.date_input("Date limite")
            if st.form_submit_button("Enregistrer"):
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
                    <div style="font-size:0.85rem; color:#FFF;">Avancement: {cp['progress']}% | Échéance: {cp['deadline']}</div>
                </div>
            """, unsafe_allow_html=True)

    # ====================================================
    # 🔮 PROJETS FUTURS
    # ====================================================
    elif menu == "🔮 Projets futurs":
        st.markdown("## 🔮 Projets Futurs")
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
            st.markdown(f"""
                <div class="zapio-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="margin:0; color:#FFF;">{fp['name']}</h3>
                        <span class="zapio-badge">{fp['horizon']}</span>
                    </div>
                    <p style="color:#A0A0AB; margin-top:10px;"><b>Objectif:</b> {fp['goal']}</p>
                    <p style="color:#8E8E93; font-size:0.85rem;"><b>Ressources:</b> {fp['resources']}</p>
                </div>
            """, unsafe_allow_html=True)

    # ====================================================
    # 🔗 LIENS UTILES
    # ====================================================
    elif menu == "🔗 Liens Utiles":
        st.markdown("## 🔗 Sauvegarde de Liens Web")
        with st.form("form_links"):
            title = st.text_input("Nom du site")
            url = st.text_input("Lien URL (https://...)")
            category = st.selectbox("Catégorie", ["Doc Tech & API", "Outils Design & AI", "Inspiration / Modèles", "Administration / Finance"])
            note = st.text_input("Note")
            if st.form_submit_button("Enregistrer"):
                if title and url:
                    st.session_state.saved_links.append({"title": title, "url": url, "cat": category, "note": note})
                    st.rerun()

        for lk in st.session_state.saved_links:
            st.markdown(f"""
                <div class="zapio-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="margin:0; color:#FF3B30;">{lk['title']}</h3>
                        <span class="zapio-badge">{lk['cat']}</span>
                    </div>
                    <a href="{lk['url']}" target="_blank" style="color:#00F2FE; display:block; margin:8px 0;">{lk['url']}</a>
                    <span style="color:#8E8E93; font-size:0.8rem;">{lk['note']}</span>
                </div>
            """, unsafe_allow_html=True)

    # ====================================================
    # 📦 FICHIERS ZIP
    # ====================================================
    elif menu == "📦 Fichiers ZIP":
        st.markdown("## 📦 Banque de Fichiers ZIP")
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
            st.markdown(f"""
                <div class="zapio-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="margin:0; color:#FFF;">{zp['title']} <span style="font-size:0.8rem; color:#8E8E93;">({zp['version']})</span></h3>
                        <a href="{zp['link']}" target="_blank" class="zapio-badge-green" style="text-decoration:none;">📥 Télécharger ZIP</a>
                    </div>
                    <p style="color:#A0A0AB; margin-top:10px; font-size:0.85rem;"><b>Contenu:</b> {zp['contents']}</p>
                </div>
            """, unsafe_allow_html=True)
