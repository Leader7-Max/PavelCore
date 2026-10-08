import sys
import os
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Configuration de la page
st.set_page_config(
    page_title="PavelCore — Dark Red Edition",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

from assets.styles import inject_custom_design
inject_custom_design()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ----------------------------------------------------
# 1. AUTHENTIFICATION STYLE ZAPIO
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
                <h2 style="font-size: 2rem; margin-top: 20px; font-weight: 800;">
                    Toutes vos ressources, <span style="color: #FF3B30;">sur un seul écran.</span>
                </h2>
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
    with st.sidebar:
        st.markdown("""
            <h2 style="font-size: 1.8rem;">
                <span style="color: #FFF;">pavel</span><span style="background: #FF3B30; color: #FFF; padding: 2px 8px; border-radius: 6px; font-size: 1.2rem;">CORE</span>
            </h2>
        """, unsafe_allow_html=True)
        st.markdown('<span class="zapio-badge-green">● Connecté</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        menu = st.radio(
            "Navigation",
            ["Dashboard", "Mes Prompts & Code", "Projets & Agenda", "Boîte à Idées", "Coffre-Fort Docs"],
            index=0
        )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Déconnexion"):
            st.session_state.authenticated = False
            st.rerun()

    # --- DASHBOARD ---
    if menu == "Dashboard":
        st.markdown("""
            <div style="margin-bottom: 25px;">
                <span class="zapio-badge">🔴 PavelCore Hub</span>
                <h1 style="margin-top: 10px;">Tableau de Bord</h1>
            </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
                <div class="zapio-card">
                    <span style="color: #8E8E93; font-size: 0.9rem;">Projets Actifs</span>
                    <h1 style="color: #FF3B30; margin: 8px 0; font-size: 2.5rem;">08</h1>
                    <span class="zapio-badge">En cours</span>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
                <div class="zapio-card">
                    <span style="color: #8E8E93; font-size: 0.9rem;">Snippets & Prompts</span>
                    <h1 style="color: #FFFFFF; margin: 8px 0; font-size: 2.5rem;">142</h1>
                    <span class="zapio-badge-green">Prêts à copier</span>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
                <div class="zapio-card">
                    <span style="color: #8E8E93; font-size: 0.9rem;">Échéances Proches</span>
                    <h1 style="color: #FF9500; margin: 8px 0; font-size: 2.5rem;">03</h1>
                    <span style="color: #FF9500; font-size: 0.85rem; font-weight: 600;">Cette semaine</span>
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
            st.error("⚠️ Fichier `snippets_component.html` introuvable dans `assets/`.")

    # --- PROJETS & AGENDA ---
    elif menu == "Projets & Agenda":
        st.markdown("## 📅 Projets & Agenda")
        if "projects" not in st.session_state:
            st.session_state.projects = [
                {"name": "PavelCore App", "status": "En cours", "deadline": "2026-10-25", "priority": "Haute", "desc": "Développement du coffre-fort"},
                {"name": "Reborn Beauty Platform", "status": "En cours", "deadline": "2026-11-15", "priority": "Moyenne", "desc": "Marketplace e-commerce"}
            ]

        tab1, tab2 = st.tabs(["🚀 Suivi de Projets", "📆 Vue Agenda"])

        with tab1:
            with st.expander("➕ Ajouter un Projet"):
                with st.form("new_project_form"):
                    p_name = st.text_input("Nom du Projet")
                    p_status = st.selectbox("Statut", ["Idée", "Planifié", "En cours", "Terminé"])
                    p_priority = st.selectbox("Priorité", ["Basse", "Moyenne", "Haute", "Urgente"])
                    p_deadline = st.date_input("Échéance")
                    p_desc = st.text_area("Description")
                    if st.form_submit_button("Créer le projet"):
                        if p_name:
                            st.session_state.projects.append({
                                "name": p_name, "status": p_status, "deadline": str(p_deadline),
                                "priority": p_priority, "desc": p_desc
                            })
                            st.rerun()

            for p in st.session_state.projects:
                st.markdown(f"""
                    <div class="zapio-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h3 style="margin:0; color:#FF3B30;">{p['name']}</h3>
                            <span class="zapio-badge">{p['priority']}</span>
                        </div>
                        <p style="color:#A0A0AB; margin:10px 0;">{p['desc']}</p>
                        <div style="font-size:0.85rem; color:#FFF;">
                            📌 Statut : <b>{p['status']}</b> | ⏱️ Échéance : <b>{p['deadline']}</b>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        with tab2:
            df = pd.DataFrame(st.session_state.projects)
            if not df.empty:
                st.dataframe(df, use_container_width=True)

    # --- BOÎTE À IDÉES ---
    elif menu == "Boîte à Idées":
        st.markdown("## 💡 Boîte à Idées")
        if "ideas" not in st.session_state:
            st.session_state.ideas = [
                {"title": "Application Web Flet & Python", "category": "Tech", "note": "Créer une app desktop locale ultra rapide."},
                {"title": "Concept Marketing Musical", "category": "Événementiel", "note": "Organiser une soirée à thème Afrobeat & Zouglou."}
            ]

        with st.form("add_idea"):
            title = st.text_input("Titre de l'idée")
            category = st.selectbox("Domaine", ["Tech & Dev", "Musique & Event", "Business", "Personnel"])
            note = st.text_area("Détail / Notes")
            if st.form_submit_button("Sauvegarder l'Idée"):
                if title:
                    st.session_state.ideas.append({"title": title, "category": category, "note": note})
                    st.rerun()

        for i in st.session_state.ideas:
            st.markdown(f"""
                <div class="zapio-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h4 style="margin:0; color:#FFF;">{i['title']}</h4>
                        <span class="zapio-badge">{i['category']}</span>
                    </div>
                    <p style="color:#A0A0AB; margin-top:10px;">{i['note']}</p>
                </div>
            """, unsafe_allow_html=True)

    # --- COFFRE-FORT DOCS ---
    elif menu == "Coffre-Fort Docs":
        st.markdown("## 🔐 Coffre-Fort Documents")
        if "vault_items" not in st.session_state:
            st.session_state.vault_items = []

        with st.form("add_vault_item"):
            item_name = st.text_input("Intitulé")
            item_secret = st.text_area("Contenu confidentiel")
            if st.form_submit_button("Ajouter au Coffre Fort"):
                if item_name and item_secret:
                    st.session_state.vault_items.append({"title": item_name, "content": item_secret})
                    st.rerun()

        for item in st.session_state.vault_items:
            with st.expander(f"🔒 {item['title']}"):
                st.code(item['content'], language="text")
