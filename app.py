import sys
import os
import re
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

# Import de la vue Agenda modulaire
from views.agenda_view import render_agenda_view

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

PROMPT_CATEGORIES = [
    "🎨 Génération d'images (Midjourney, DALL-E, Flux)",
    "✏️ Modification & Retouche d'images",
    "🤖 Développement & Code AI",
    "🧠 System Prompts (Claude & ChatGPT)",
    "🎵 Création Musicale & Paroles (Suno, Udio)",
    "📝 Rédaction de Contenu & Marketing"
]

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
            st.markdown(f'''
                <div class="sub-section-header">
                    <span class="zapio-badge">INTELLIGENCE ARTIFICIELLE</span>
                    <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🧠 Bibliothèque Centrale de Prompts IA</h1>
                </div>
            ''', unsafe_allow_html=True)
            
            with st.form("form_add_prompt", clear_on_submit=True):
                p_title = st.text_input("Titre du Prompt")
                p_cat = st.selectbox("Catégorie", PROMPT_CATEGORIES)
                p_content = st.text_area("Contenu du Prompt / Instruction")
                if st.form_submit_button("Enregistrer le Prompt"):
                    if p_title and p_content:
                        st.session_state.saved_prompts_library.append({
                            "title": p_title,
                            "category": p_cat,
                            "prompt": p_content
                        })
                        st.toast("🧠 Prompt enregistré avec succès !", icon="✅")
                        st.rerun()
                    else:
                        st.warning("Veuillez renseigner un titre et un contenu.")

            st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 20px 0;'>", unsafe_allow_html=True)
            selected_cat_filter = st.selectbox("🔍 Filtrer par catégorie :", ["Tous les prompts"] + PROMPT_CATEGORIES)
            
            for pr in st.session_state.saved_prompts_library:
                if selected_cat_filter == "Tous les prompts" or pr["category"] == selected_cat_filter:
                    st.markdown(f'''
                        <div class="zapio-card">
                            <span class="zapio-badge" style="font-size: 0.7rem;">{pr["category"]}</span>
                            <h3 style="color:{sub_title_color}; margin-top: 5px;">{pr["title"]}</h3>
                        </div>
                    ''', unsafe_allow_html=True)
                    st.code(pr["prompt"], language="markdown")

        elif current == "Médias & Fichiers":
            st.markdown(f'''
                <div class="sub-section-header">
                    <span class="zapio-badge">STOCKAGE & RESSOURCES</span>
                    <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">📁 Images, ZIP, APK & Documents</h1>
                </div>
            ''', unsafe_allow_html=True)

            sub_tab = st.pills(
                "Type de fichier",
                options=["📤 Envoyer un fichier", "🔗 Lien externe (Drive, Web)"],
                default="📤 Envoyer un fichier",
                label_visibility="collapsed"
            )

            UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploaded_files")
            os.makedirs(UPLOADS_DIR, exist_ok=True)

            if sub_tab == "📤 Envoyer un fichier":
                uploaded_file = st.file_uploader(
                    "Choisissez un fichier à sauvegarder (Images, ZIP, APK, PDFs, DOCX, TXT...)",
                    type=["png", "jpg", "jpeg", "gif", "zip", "rar", "apk", "pdf", "docx", "txt", "csv"]
                )
                file_title = st.text_input("Nom / Titre personnalisé pour le fichier")
                file_category = st.selectbox("Catégorie de fichier", ["🖼️ Images & Visuels", "📦 Fichiers ZIP / Archives", "📱 Applications APK", "📄 Documents & PDFs", "🔗 Liens Utiles"])

                if st.button("💾 Enregistrer le fichier"):
                    if uploaded_file is not None and file_title:
                        file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        st.session_state.saved_media_files.append({
                            "title": file_title,
                            "filename": uploaded_file.name,
                            "path": file_path,
                            "size": f"{round(uploaded_file.size / (1024 * 1024), 2)} MB",
                            "type": file_category,
                            "is_local": True
                        })
                        st.toast("📁 Fichier sauvegardé avec succès !", icon="✅")
                        st.rerun()
                    else:
                        st.warning("Veuillez charger un fichier et renseigner un titre.")

            elif sub_tab == "🔗 Lien externe (Drive, Web)":
                with st.form("form_external_link", clear_on_submit=True):
                    ext_title = st.text_input("Titre du lien ou fichier")
                    ext_url = st.text_input("URL directe (ex: Google Drive, Dropbox, Lien web)")
                    ext_cat = st.selectbox("Catégorie", ["🖼️ Images & Visuels", "📦 Fichiers ZIP / Archives", "📱 Applications APK", "📄 Documents & PDFs", "🔗 Liens Utiles"])
                    ext_desc = st.text_area("Description du fichier")
                    if st.form_submit_button("Enregistrer le lien"):
                        if ext_title and ext_url:
                            st.session_state.saved_media_files.append({
                                "title": ext_title,
                                "url": ext_url,
                                "desc": ext_desc,
                                "type": ext_cat,
                                "is_local": False
                            })
                            st.toast("🔗 Lien sauvegardé avec succès !", icon="✅")
                            st.rerun()

            st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 25px 0;'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='color:{sub_title_color};'>📚 Fichiers & Médias Enregistrés</h3>", unsafe_allow_html=True)

            if not st.session_state.saved_media_files:
                st.info("Aucun fichier n'a été enregistré pour le moment.")

            for item in st.session_state.saved_media_files:
                st.markdown(f'''
                    <div class="zapio-card">
                        <span class="zapio-badge" style="font-size:0.7rem;">{item["type"]}</span>
                        <h3 style="color:{sub_title_color}; margin-top:5px;">{item["title"]}</h3>
                ''', unsafe_allow_html=True)

                if item.get("is_local", False):
                    st.caption(f"Fichier : {item['filename']} | Taille : {item['size']}")
                    if os.path.exists(item["path"]):
                        with open(item["path"], "rb") as file_data:
                            st.download_button(
                                label=f"📥 Télécharger {item['filename']}",
                                data=file_data,
                                file_name=item["filename"],
                                use_container_width=True
                            )
                else:
                    st.write(f"Description : {item.get('desc', '')}")
                    st.markdown(f'<a href="{item["url"]}" target="_blank" style="color:#EC4899; font-weight:600;">🌐 Ouvrir / Télécharger via le lien</a>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

        elif current == "Projets":
            sub_tab = st.pills(
                "Navigation Projets",
                options=["🚀 Projets en cours", "🔮 Projets futurs", "💡 Idées"],
                default="🚀 Projets en cours",
                label_visibility="collapsed"
            )
            
            if sub_tab == "🚀 Projets en cours":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">SUIVI OPÉRATIONNEL</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🚀 Projets en cours</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_curr_proj", clear_on_submit=True):
                    name = st.text_input("Nom du projet")
                    client = st.text_input("Client / Marque")
                    priority = st.selectbox("Priorité", ["🔴 Haute", "🟠 Moyenne", "🟢 Basse"])
                    next_step = st.text_input("Prochaine étape")
                    deadline = st.date_input("Date limite")
                    project_desc = st.text_area("Description")
                    if st.form_submit_button("Enregistrer"):
                        if name:
                            st.session_state.saved_current_projects.append({"name": name, "client": client, "priority": priority, "next": next_step, "deadline": str(deadline), "desc": project_desc})
                            st.toast("🚀 Projet en cours enregistré avec succès !", icon="✅")
                            st.rerun()
                        else:
                            st.warning("Veuillez renseigner le nom du projet.")
                for cp in st.session_state.saved_current_projects:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{cp["name"]}</h3><p style="color:{desc_color};">Client: {cp["client"]} | Échéance: {cp["deadline"]}</p></div>', unsafe_allow_html=True)

            elif sub_tab == "🔮 Projets futurs":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">VISION & ROADMAP</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🔮 Projets futurs</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_fut_proj", clear_on_submit=True):
                    name = st.text_input("Nom du projet futur")
                    horizon = st.selectbox("Horizon", ["Court terme", "Moyen terme", "Long terme"])
                    resources = st.text_area("Ressources requises")
                    goal = st.text_input("Objectif")
                    if st.form_submit_button("Ajouter"):
                        if name:
                            st.session_state.saved_future_projects.append({"name": name, "horizon": horizon, "resources": resources, "goal": goal})
                            st.toast("🔮 Projet futur ajouté avec succès !", icon="✨")
                            st.rerun()
                        else:
                            st.warning("Veuillez renseigner le nom du projet futur.")
                for fp in st.session_state.saved_future_projects:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{fp["name"]}</h3><p style="color:{desc_color};">Objectif: {fp["goal"]}</p></div>', unsafe_allow_html=True)

            elif sub_tab == "💡 Idées":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">INSPIRATION & CONCEPTS</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">💡 Boîte à Idées</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_ideas", clear_on_submit=True):
                    title = st.text_input("Titre de l'idée")
                    category = st.selectbox("Domaine", ["Business", "Tech", "DJ", "Personnel"])
                    description = st.text_area("Description")
                    impact = st.select_slider("Impact", options=["Faible", "Moyen", "Fort", "Révolutionnaire !"])
                    if st.form_submit_button("Sauvegarder"):
                        if title:
                            st.session_state.saved_ideas.append({"title": title, "cat": category, "desc": description, "impact": impact})
                            st.toast("💡 Idée sauvegardée avec succès !", icon="💡")
                            st.rerun()
                        else:
                            st.warning("Veuillez renseigner un titre.")
                for id_item in st.session_state.saved_ideas:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{id_item["title"]}</h3><p style="color:{desc_color};">{id_item["desc"]}</p></div>', unsafe_allow_html=True)

        elif current == "Coffre-Fort":
            sub_tab = st.pills(
                "Navigation Coffre-Fort",
                options=["🔐 Clés API", "🔑 Identifiants & Mots de passe"],
                default="🔐 Clés API",
                label_visibility="collapsed"
            )
            if sub_tab == "🔐 Clés API":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">SÉCURITÉ & CREDENTIALS</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🔐 Clés d'API & Tokens</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_api_keys", clear_on_submit=True):
                    service = st.text_input("Nom du Service (ex: OpenAI, GitHub)")
                    api_key = st.text_input("Clé API / Token Secret", type="password")
                    if st.form_submit_button("🔒 Sauvegarder la clé"):
                        if service and api_key:
                            st.session_state.saved_api_keys.append({"service": service, "key": api_key})
                            st.toast("🔐 Clé API sauvegardée en toute sécurité !", icon="✅")
                            st.rerun()
                        else:
                            st.warning("Veuillez remplir tous les champs.")
                for ak in st.session_state.saved_api_keys:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{ak["service"]}</h3>', unsafe_allow_html=True)
                    st.code(ak['key'], language='text')
                    st.markdown('</div>', unsafe_allow_html=True)

            elif sub_tab == "🔑 Identifiants & Mots de passe":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">GESTIONNAIRE D'ACCÈS</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🔑 Identifiants & Mots de passe</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_creds", clear_on_submit=True):
                    site = st.text_input("Plateforme / Site web")
                    username = st.text_input("Identifiant / Email")
                    password = st.text_input("Mot de passe", type="password")
                    if st.form_submit_button("Enregistrer les accès"):
                        if site and username and password:
                            st.session_state.saved_user_credentials.append({"site": site, "user": username, "pass": password})
                            st.toast("🔑 Identifiants enregistrés avec succès !", icon="✅")
                            st.rerun()
                        else:
                            st.warning("Veuillez remplir tous les champs.")
                for uc in st.session_state.saved_user_credentials:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{uc["site"]}</h3><p style="color:{desc_color};"><b>Identifiant:</b> {uc["user"]}</p>', unsafe_allow_html=True)
                    st.code(uc['pass'], language='text')
                    st.markdown('</div>', unsafe_allow_html=True)

        elif current == "Contacts & Emails":
            sub_tab = st.pills(
                "Navigation Contacts",
                options=["🎴 Carnet de Contacts", "📧 Modèles d'Emails & Scripts"],
                default="🎴 Carnet de Contacts",
                label_visibility="collapsed"
            )
            if sub_tab == "🎴 Carnet de Contacts":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">RÉPERTOIRE PROFESSIONNEL</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🎴 Carnet de Contacts</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_contacts", clear_on_submit=True):
                    fullname = st.text_input("Nom & Prénom / Entreprise")
                    email_contact = st.text_input("Adresse Email")
                    phone = st.text_input("Numéro de Téléphone")
                    category = st.selectbox("Catégorie", ["Client", "Partenaire / Prestataire", "VIP", "Personnel"])
                    notes = st.text_area("Notes / Rôle")
                    if st.form_submit_button("Ajouter le contact"):
                        if fullname:
                            st.session_state.saved_contacts.append({
                                "name": fullname,
                                "email": email_contact,
                                "phone": phone,
                                "cat": category,
                                "notes": notes
                            })
                            st.toast("🎴 Contact sauvegardé !", icon="✅")
                            st.rerun()
                        else:
                            st.warning("Veuillez renseigner au moins le nom du contact.")
                for ct in st.session_state.saved_contacts:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{ct["name"]} <span class="zapio-badge" style="font-size:0.7rem;">{ct["cat"]}</span></h3><p style="color:{desc_color};">📧 {ct["email"]} | 📞 {ct["phone"]}</p><p style="color:{desc_color}; font-size:0.85rem;">{ct["notes"]}</p></div>', unsafe_allow_html=True)

            elif sub_tab == "📧 Modèles d'Emails & Scripts":
                st.markdown(f'''
                    <div class="sub-section-header">
                        <span class="zapio-badge">COMMUNICATION & TEMPLATES</span>
                        <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">📧 Modèles d'Emails & Scripts</h1>
                    </div>
                ''', unsafe_allow_html=True)
                with st.form("form_email_tpl", clear_on_submit=True):
                    title = st.text_input("Titre du modèle (ex: Relance devis DJ, Prospection)")
                    subject = st.text_input("Objet du mail")
                    body = st.text_area("Corps du message / Script")
                    if st.form_submit_button("Sauvegarder le modèle"):
                        if title and body:
                            st.session_state.saved_email_templates.append({
                                "title": title,
                                "subject": subject,
                                "body": body
                            })
                            st.toast("📧 Modèle d'email sauvegardé !", icon="✅")
                            st.rerun()
                        else:
                            st.warning("Veuillez renseigner le titre et le corps du message.")
                for et in st.session_state.saved_email_templates:
                    st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{et["title"]}</h3><p style="color:{desc_color};"><b>Objet:</b> {et["subject"]}</p>', unsafe_allow_html=True)
                    st.code(et['body'], language='markdown')
                    st.markdown('</div>', unsafe_allow_html=True)
