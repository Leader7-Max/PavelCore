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

# Import des fonctions base de données utilisateurs
from modules.database import create_user_db, authenticate_user_db

# Import de toutes les vues modulaires
from views.home_view import render_home_view
from views.agenda_view import render_agenda_view
from views.dev_ia_view import render_dev_ia_view
from views.projets_view import render_projets_view
from views.media_view import render_media_view
from views.vault_contacts_view import render_vault_view, render_contacts_view
from views.backup_view import render_backup_view

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
    st.markdown(f'<div style="text-align: center; margin-top: 25px; margin-bottom: 20px;"><h1 style="font-size: 2.8rem; margin-bottom: 5px;"><span style="color: {text_color};">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 10px; border-radius: 8px; font-size: 2rem; margin-left: 6px;">CORE</span></h1><div style="margin-top: 10px;"><span class="zapio-badge">🔮 Workspace Centralisé & Sécurisé</span></div></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if "auth_mode" not in st.session_state:
            st.session_state.auth_mode = "login"

        # CSS anti-empilement mobile pour forcer ces 2 colonnes à rester côte à côte
        st.markdown("""
            <style>
                @media (max-width: 640px) {
                    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                        width: 50% !important;
                        flex: 1 1 50% !important;
                        min-width: unset !important;
                    }
                }
            </style>
        """, unsafe_allow_html=True)

        # Boutons natifs instantanés (Zéro latence réseau via WebSocket)
        auth_col1, auth_col2 = st.columns(2)
        with auth_col1:
            if st.button("🔑 Connexion", use_container_width=True, type="primary" if st.session_state.auth_mode == "login" else "secondary"):
                st.session_state.auth_mode = "login"
                st.rerun()
        with auth_col2:
            if st.button("✨ Inscription", use_container_width=True, type="primary" if st.session_state.auth_mode == "signup" else "secondary"):
                st.session_state.auth_mode = "signup"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Bouton d'accès direct à l'Agenda remonté ici (juste après les onglets)
        if st.button("📅 Accéder directement à l'Agenda (Hors-ligne / Démo)", use_container_width=True, type="secondary"):
            st.session_state.direct_agenda = True
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.auth_mode == "login":
            with st.form("login_form"):
                email = st.text_input("Adresse Email", placeholder="votre.email@exemple.com", key="login_email")
                password = st.text_input("Mot de passe", type="password", placeholder="••••••••", key="login_pass")
                submit_login = st.form_submit_button("Se connecter au Workspace", use_container_width=True)
                
                if submit_login:
                    ok, res = authenticate_user_db(email, password)
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res
                        st.toast(f"🔓 Bienvenue, {res['email']} !", icon="✨")
                        st.rerun()
                    else:
                        st.error(res)
        else:
            with st.form("signup_form"):
                new_email = st.text_input("Adresse Email", placeholder="nom@exemple.com", key="signup_email")
                new_pass = st.text_input("Créer un mot de passe", type="password", placeholder="••••••••", key="signup_pass")
                confirm_pass = st.text_input("Confirmer le mot de passe", type="password", placeholder="••••••••", key="signup_confirm_pass")
                submit_signup = st.form_submit_button("S'inscrire et rejoindre PavelCore", use_container_width=True)
                
                if submit_signup:
                    if new_pass != confirm_pass:
                        st.error("Les deux mots de passe ne correspondent pas.")
                    elif len(new_pass) < 6:
                        st.warning("Le mot de passe doit contenir au moins 6 caractères.")
                    else:
                        ok, msg = create_user_db(new_email, new_pass)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)

else:
    col_logo, col_user, col_logout = st.columns([2, 2, 1])
    
    with col_logo:
        st.markdown(f'<h1 style="font-size: 1.3rem; margin: 0; display: flex; align-items: center; gap: 6px;"><span style="color: {text_color};">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding: 2px 6px; border-radius: 6px; font-size: 0.85rem;">CORE</span><span class="zapio-badge-green" style="font-size: 0.55rem;">● Live</span></h1>', unsafe_allow_html=True)
    
    with col_user:
        current_email = st.session_state.get("user_info", {}).get("email", "Session Active") if st.session_state.get("user_info") else "Membre"
        st.markdown(f'<div style="text-align: center; color: {desc_color}; font-size: 0.85rem; padding-top: 5px;">👤 Connecté en tant que : <strong style="color: {sub_title_color};">{current_email}</strong></div>', unsafe_allow_html=True)

    with col_logout:
        if st.button("🔒 Déconnexion", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.session_state.current_view = "home"
            st.toast("🔒 Déconnexion effectuée.", icon="👋")
            st.rerun()

    st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 15px 0 15px 0;'>", unsafe_allow_html=True)
    
    render_global_search()

    if st.session_state.current_view == "home":
        render_home_view()
        render_backup_view(sub_title_color)
    else:
        current = st.session_state.current_view
        
        if st.button("← Retour au Tableau de Bord", key="back_to_home_universal", type="secondary"):
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
        elif current == "Sauvegarde":
            render_backup_view(sub_title_color)
