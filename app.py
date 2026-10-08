import sys
import os
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Configuration de la page
st.set_page_config(
    page_title="PavelCore — Coffre-Fort & Workspace",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injection du design CSS
from assets.styles import inject_custom_design
inject_custom_design()

# État de la session
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ----------------------------------------------------
# 1. ÉCRAN DE CONNEXION / AUTHENTIFICATION
# ----------------------------------------------------
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <h1 style="background: linear-gradient(90deg, #00F2FE, #4F46E5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0;">PavelCore</h1>
                <p style="color: #8E9BAE; font-size: 0.95rem;">Espace Ultra-Sécurisé & Second Brain</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            st.subheader("Authentification")
            email = st.text_input("Adresse Email", placeholder="exemple@domaine.com")
            master_key = st.text_input("Clé Maîtresse / PIN", type="password", placeholder="••••••••")
            submit = st.form_submit_button("Déverrouiller le Coffre", use_container_width=True)

            if submit:
                if master_key != "":
                    st.session_state.authenticated = True
                    st.success("Accès accordé.")
                    st.rerun()
                else:
                    st.error("Saisis ta clé d'accès.")

# ----------------------------------------------------
# 2. APPLICATION PRINCIPALE & MODULES
# ----------------------------------------------------
else:
    with st.sidebar:
        st.markdown("<h2 style='color: #00F2FE;'>PavelCore</h2>", unsafe_allow_html=True)
        st.markdown('<span class="badge">Session Sécurisée</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        menu = st.radio(
            "Navigation",
            ["Dashboard", "Mes Prompts & Code", "Projets & Agenda", "Boîte à Idées", "Coffre-Fort Docs"],
            index=0
        )
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.button("Verrouiller la session", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # --- DASHBOARD ---
    if menu == "Dashboard":
        st.markdown("## 🚀 Dashboard")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
                <div class="glass-card">
                    <h4 style="color: #8E9BAE; margin:0;">Projets Actifs</h4>
                    <h1 style="color: #00F2FE; margin:10px 0;">08</h1>
                    <span class="badge">En progression</span>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
                <div class="glass-card">
                    <h4 style="color: #8E9BAE; margin:0;">Prompts & Snippets</h4>
                    <h1 style="color: #4F46E5; margin:10px 0;">142</h1>
                    <span class="badge">Sauvegardés</span>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
                <div class="glass-card">
                    <h4 style="color: #8E9BAE; margin:0;">Échéances Proches</h4>
                    <h1 style="color: #FF007A; margin:10px 0;">03</h1>
                    <span class="badge" style="color:#FF007A; border-color:#FF007A;">Aujourd'hui</span>
                </div>
            """, unsafe_allow_html=True)

    # --- MES PROMPTS & CODE ---
    elif menu == "Mes Prompts & Code":
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "assets", "snippets_component.html"),
            os.path.join(os.path.dirname(__file__), "snippets_component.html"),
            os.path.join(os.getcwd(), "assets", "snippets_component.html"),
            os.path.join(os.getcwd(), "snippets_component.html"),
        ]
        html_code = None
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    html_code = f.read()
                break

        if html_code:
            components.html(html_code, height=950, scrolling=True)
        else:
            st.error("⚠️ Le fichier `snippets_component.html` est introuvable dans le dossier `assets/`.")

    # --- PROJETS & AGENDA ---
    elif menu == "Projets & Agenda":
        st.markdown("""
            <div style="margin-bottom: 20px;">
                <h2 style="color: #00F2FE; margin:0;">📅 Projets & Agenda Ultra-Moderne</h2>
                <p style="color: #8E9BAE;">Planification, suivi de projets et rappels d'échéances.</p>
            </div>
        """, unsafe_allow_html=True)

        if "projects" not in st.session_state:
            st.session_state.projects = [
                {"name": "PavelCore App", "status": "En cours", "deadline": "2026-10-25", "priority": "Haute", "desc": "Développement du coffre-fort"},
                {"name": "Reborn Beauty Platform", "status": "En cours", "deadline": "2026-11-15", "priority": "Moyenne", "desc": "Marketplace e-commerce"}
            ]

        tab1, tab2 = st.tabs(["🚀 Suivi de Projets", "📆 Agenda & Échéances"])

        with tab1:
            with st.expander("➕ Créer un nouveau Projet"):
                with st.form("new_project_form"):
                    p_name = st.text_input("Nom du Projet")
                    p_status = st.selectbox("Statut", ["Idée", "Planifié", "En cours", "Terminé"])
                    p_priority = st.selectbox("Priorité", ["Basse", "Moyenne", "Haute", "Urgente"])
                    p_deadline = st.date_input("Échéance ciblée")
                    p_desc = st.text_area("Description / Jalons")
                    
                    if st.form_submit_button("Enregistrer le projet"):
                        if p_name:
                            st.session_state.projects.append({
                                "name": p_name, "status": p_status, "deadline": str(p_deadline),
                                "priority": p_priority, "desc": p_desc
                            })
                            st.toast("Projet créé avec succès !", icon="🚀")
                            st.rerun()

            st.markdown("### Mes Projets Actifs")
            for p in st.session_state.projects:
                color = "#00F2FE" if p["status"] == "En cours" else "#10B981"
                st.markdown(f"""
                    <div class="glass-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h3 style="color:{color}; margin:0;">{p['name']}</h3>
                            <span class="badge">{p['priority']}</span>
                        </div>
                        <p style="color:#8E9BAE; margin:10px 0;">{p['desc']}</p>
                        <div style="display:flex; gap:15px; font-size:0.85rem; color:#E0E6ED;">
                            <span>📌 Statut : <b>{p['status']}</b></span>
                            <span>⏱️ Échéance : <b>{p['deadline']}</b></span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        with tab2:
            st.markdown("### Vue Calendrier des Échéances")
            df = pd.DataFrame(st.session_state.projects)
            if not df.empty:
                st.dataframe(df[["name", "deadline", "priority", "status"]], use_container_width=True)

    # --- BOÎTE À IDÉES ---
    elif menu == "Boîte à Idées":
        st.markdown("""
            <div style="margin-bottom: 20px;">
                <h2 style="color: #00F2FE; margin:0;">💡 Boîte à Idées & Concepts</h2>
                <p style="color: #8E9BAE;">Capturez vos réflexions, opportunités et visions futures.</p>
            </div>
        """, unsafe_allow_html=True)

        if "ideas" not in st.session_state:
            st.session_state.ideas = [
                {"title": "Application Web Flet & Python", "category": "Tech", "note": "Créer une app desktop locale ultra rapide."},
                {"title": "Concept Marketing Musical", "category": "Événementiel", "note": "Organiser une soirée à thème Afrobeat & Zouglou."}
            ]

        with st.form("add_idea"):
            title = st.text_input("Titre de l'idée")
            category = st.selectbox("Domaine", ["Tech & Dev", "Musique & Event", "Business", "Personnel"])
            note = st.text_area("Détail / Notes de réflexion")
            if st.form_submit_button("Sauvegarder l'Idée"):
                if title:
                    st.session_state.ideas.append({"title": title, "category": category, "note": note})
                    st.toast("Idée enregistrée !", icon="💡")
                    st.rerun()

        st.markdown("---")
        st.markdown("### Mes Idées Sauvegardées")
        for i in st.session_state.ideas:
            st.markdown(f"""
                <div class="glass-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h4 style="color:#00F2FE; margin:0;">{i['title']}</h4>
                        <span class="badge">{i['category']}</span>
                    </div>
                    <p style="color:#E0E6ED; margin-top:10px;">{i['note']}</p>
                </div>
            """, unsafe_allow_html=True)

    # --- COFFRE-FORT DOCS ---
    elif menu == "Coffre-Fort Docs":
        st.markdown("""
            <div style="margin-bottom: 20px;">
                <h2 style="color: #00F2FE; margin:0;">🔐 Coffre-Fort, Mails & Contacts</h2>
                <p style="color: #8E9BAE;">Espace sécurisé pour documents importants, identifiants et carnet d'adresses.</p>
            </div>
        """, unsafe_allow_html=True)

        if "vault_items" not in st.session_state:
            st.session_state.vault_items = []

        tab1, tab2 = st.tabs(["📄 Documents & Notes Secrètes", "🎇 Contacts Privés"])

        with tab1:
            with st.form("add_vault_item"):
                item_name = st.text_input("Intitulé du document / Note")
                item_secret = st.text_area("Contenu sensible / Code d'accès")
                if st.form_submit_button("Ajouter au Coffre Fort"):
                    if item_name and item_secret:
                        st.session_state.vault_items.append({"title": item_name, "content": item_secret})
                        st.toast("Élément sécurisé ajouté !", icon="🔐")
                        st.rerun()

            st.markdown("### Vos Éléments Sécurisés")
            for item in st.session_state.vault_items:
                with st.expander(f"🔒 {item['title']}"):
                    st.code(item['content'], language="text")

        with tab2:
            st.info("Section Annuaire de contacts d'urgence & VIP.")
