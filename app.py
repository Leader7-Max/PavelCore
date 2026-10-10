import sys
import os
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

# Import de l'état global modulaire
from modules.state import init_session_state
init_session_state()

# Import et injection du design CSS global
from assets.styles import inject_custom_design
inject_custom_design()

# Import de toutes les vues modulaires
from views.agenda_view import render_agenda_view
from views.dev_ia_view import render_dev_ia_view
from views.projets_view import render_projets_view
from views.media_view import render_media_view
from views.vault_contacts_view import render_vault_view, render_contacts_view

# Dossier local pour le stockage des fichiers uploadés
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploaded_files")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Définition sécurisée des couleurs pour les variables de texte
theme_mode = st.session_state.get("theme_mode", "Sombre Nuit")
if theme_mode == "Blanc Épuré":
    text_color = "#0F172A"
    sub_title_color = "#0F172A"
    desc_color = "#475569"
    header_box_bg = "#F1F5F9"
    header_box_text = "#475569"
    card_border = "#E2E8F0"
    card_bg = "#FFFFFF"
else:
    text_color = "#F8FAFC"
    sub_title_color = "#FFF"
    desc_color = "#CBD5E1"
    header_box_bg = "#1E0A3C"
    header_box_text = "#A78BFA"
    card_border = "#2B1552"
    card_bg = "#170A2E"

def render_global_search():
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
    search_query = st.text_input("⚡ Recherche Rapide Universelle", placeholder="🔍 Tapez un mot-clé (ex: Flyer, Python, DJ, Client, Prompt...)", key="global_search_input")
    
    if search_query.strip():
        q = search_query.strip().lower()
        results_count = 0
        st.markdown(f"### 🔎 Résultats de recherche pour : *'{search_query}'*")

        # 1. Prompts
        matched_prompts = [p for p in st.session_state.saved_prompts_library if q in p["title"].lower() or q in p["prompt"].lower() or q in p["category"].lower()]
        if matched_prompts:
            st.markdown("#### 🧠 Prompts & IA")
            for item in matched_prompts:
                results_count += 1
                st.markdown(f'<div class="zapio-card"><span class="zapio-badge">{item["category"]}</span><h4 style="margin-top:5px;">{item["title"]}</h4>', unsafe_allow_html=True)
                st.code(item["prompt"], language="markdown")
                st.markdown('</div>', unsafe_allow_html=True)

        # 2. Fichiers & Médias
        matched_files = [f for f in st.session_state.saved_media_files if q in f["title"].lower() or q in f.get("filename", "").lower() or q in f.get("type", "").lower() or q in f.get("desc", "").lower()]
        if matched_files:
            st.markdown("#### 📁 Médias & Fichiers")
            for item in matched_files:
                results_count += 1
                st.markdown(f'<div class="zapio-card"><span class="zapio-badge">{item["type"]}</span><h4 style="margin-top:5px;">{item["title"]}</h4></div>', unsafe_allow_html=True)

        # 3. Événements Agenda
        matched_events = [e for e in st.session_state.agenda_events if q in e["title"].lower() or q in e.get("desc", "").lower() or q in e.get("category", "").lower()]
        if matched_events:
            st.markdown("#### 📅 Agenda & Événements")
            for item in matched_events:
                results_count += 1
                st.markdown(f'<div class="zapio-card"><span class="zapio-badge">{item["category"]}</span><h4 style="margin-top:5px;">{item["title"]}</h4><p>Date: {item["date"]} à {item["time"]}</p></div>', unsafe_allow_html=True)

        # 4. Contacts
        matched_contacts = [c for c in st.session_state.saved_contacts if q in c["name"].lower() or q in c.get("email", "").lower() or q in c.get("phone", "").lower() or q in c.get("notes", "").lower()]
        if matched_contacts:
            st.markdown("#### 🎴 Contacts")
            for item in matched_contacts:
                results_count += 1
                st.markdown(f'<div class="zapio-card"><span class="zapio-badge">{item["cat"]}</span><h4 style="margin-top:5px;">{item["name"]}</h4><p>📧 {item["email"]} | 📞 {item["phone"]}</p></div>', unsafe_allow_html=True)

        # 5. Projets & Idées
        matched_projects = [p for p in st.session_state.saved_current_projects + st.session_state.saved_future_projects if q in p["name"].lower() or q in p.get("desc", "").lower() or q in p.get("client", "").lower()]
        if matched_projects:
            st.markdown("#### 🚀 Projets")
            for item in matched_projects:
                results_count += 1
                st.markdown(f'<div class="zapio-card"><h4 style="margin-top:5px;">{item["name"]}</h4></div>', unsafe_allow_html=True)

        if results_count == 0:
            st.warning("Aucun élément ne correspond à votre recherche.")
        st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 25px 0;'>", unsafe_allow_html=True)

# AUTH & NAVIGATION
query_params = st.query_params
is_direct_agenda_link = query_params.get("app", None) == "agenda"

if is_direct_agenda_link or st.session_state.get("direct_agenda", False):
    render_agenda_view(sub_title_color, card_bg, card_border, header_box_bg, header_box_text, text_color)

elif not st.session_state.get("authenticated", False):
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

    st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 15px 0 15px 0;'>", unsafe_allow_html=True)
    
    # Barre de Recherche Rapide
    render_global_search()

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

            st.markdown(f'<div class="pavel-card-grid" style="margin-top: 20px;"><h3 style="color:{sub_title_color}; font-size: 1.1rem;">🤖 Prompts & IA</h3><p style="color: {desc_color}; font-size: 0.8rem;">Bibliothèque complète de prompts IA.</p></div>', unsafe_allow_html=True)
            if st.button("Ouvrir Prompts & IA", use_container_width=True):
                st.session_state.current_view = "Prompts & IA"
                st.rerun()

            st.markdown(f'<div class="pavel-card-grid" style="margin-top: 20px;"><h3 style="color:{sub_title_color}; font-size: 1.1rem;">📁 Médias & Fichiers</h3><p style="color: {desc_color}; font-size: 0.8rem;">Images, ZIP, APK, PDFs et Documents.</p></div>', unsafe_allow_html=True)
            if st.button("Ouvrir Médias & Fichiers", use_container_width=True):
                st.session_state.current_view = "Médias & Fichiers"
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

            st.markdown(f'<div class="pavel-card-grid" style="margin-top: 20px;"><h3 style="color:{sub_title_color}; font-size: 1.1rem;">🎴 Contacts & Emails</h3><p style="color: {desc_color}; font-size: 0.8rem;">Répertoire et templates d\'emails.</p></div>', unsafe_allow_html=True)
            if st.button("Ouvrir Contacts & Emails", use_container_width=True):
                st.session_state.current_view = "Contacts & Emails"
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
            render_agenda_view(sub_title_color, card_bg, card_border, header_box_bg, header_box_text, text_color)

        elif current == "Prompts & IA":
            render_dev_ia_view(sub_title_color)

        elif current == "Projets":
            render_projets_view(sub_title_color, desc_color)

        elif current == "Médias & Fichiers":
            render_media_view(sub_title_color, UPLOADS_DIR)

        elif current == "Coffre-Fort":
            render_vault_view(sub_title_color, desc_color)

        elif current == "Contacts & Emails":
            render_contacts_view(sub_title_color, desc_color)
