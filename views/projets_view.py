import streamlit as st

def render_projets_view(sub_title_color="#FFF", desc_color="#CBD5E1"):
    """Gère l'affichage et la gestion des projets actuels et futurs dans PavelCore."""
    
    st.markdown(f'''
        <div class="sub-section-header">
            <span class="zapio-badge">WORKSPACE</span>
            <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🚀 Gestion des Projets</h1>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Initialisation des listes dans le session_state si elles n'existent pas
    if "saved_current_projects" not in st.session_state:
        st.session_state.saved_current_projects = []
    if "saved_future_projects" not in st.session_state:
        st.session_state.saved_future_projects = []

    tab_current, tab_future, tab_add = st.tabs(["🟢 Projets en Cours", "🔮 Projets Futurs", "➕ Ajouter un Projet"])

    with tab_current:
        st.markdown(f"<p style='color: {desc_color};'>Suivi de vos projets actifs et en cours de développement.</p>", unsafe_allow_html=True)
        
        if not st.session_state.saved_current_projects:
            st.info("Aucun projet en cours pour le moment. Utilisez l'onglet 'Ajouter un Projet' pour en créer un.")
        else:
            for idx, proj in enumerate(st.session_state.saved_current_projects):
                st.markdown(f'''
                    <div class="zapio-card" style="margin-bottom: 15px;">
                        <span class="zapio-badge">ACTIF</span>
                        <h3 style="color: {sub_title_color}; margin-top: 8px;">{proj.get("name", "Sans nom")}</h3>
                        <p style="color: {desc_color};">{proj.get("desc", "Aucune description")}</p>
                        <p style="font-size: 0.85rem; color: #94A3B8;">Client / Contexte : <strong>{proj.get("client", "N/A")}</strong></p>
                    </div>
                ''', unsafe_allow_html=True)

    with tab_future:
        st.markdown(f"<p style='color: {desc_color};'>Idées et projets planifiés pour le futur.</p>", unsafe_allow_html=True)
        
        if not st.session_state.saved_future_projects:
            st.info("Aucun projet futur enregistré.")
        else:
            for idx, proj in enumerate(st.session_state.saved_future_projects):
                st.markdown(f'''
                    <div class="zapio-card" style="margin-bottom: 15px;">
                        <span class="zapio-badge" style="background: #8B5CF6 !important;">FUTUR</span>
                        <h3 style="color: {sub_title_color}; margin-top: 8px;">{proj.get("name", "Sans nom")}</h3>
                        <p style="color: {desc_color};">{proj.get("desc", "Aucune description")}</p>
                    </div>
                ''', unsafe_allow_html=True)

    with tab_add:
        st.markdown("### ➕ Créer un nouveau projet")
        
        with st.form("form_add_project"):
            p_name = st.text_input("Nom du Projet", placeholder="ex: Application PavelConnect")
            p_desc = st.text_area("Description & Objectifs", placeholder="Détails du projet...")
            p_client = st.text_input("Client ou Cible", placeholder="ex: Interne / Nom du client")
            p_type = st.selectbox("Type de projet", ["Projet en Cours", "Projet Futur"])
            
            submit_proj = st.form_submit_button("Enregistrer le projet", use_container_width=True)
            
            if submit_proj:
                if p_name.strip():
                    new_item = {
                        "name": p_name.strip(),
                        "desc": p_desc.strip(),
                        "client": p_client.strip()
                    }
                    if p_type == "Projet en Cours":
                        st.session_state.saved_current_projects.append(new_item)
                    else:
                        st.session_state.saved_future_projects.append(new_item)
                    
                    st.toast("✅ Projet ajouté avec succès !", icon="🚀")
                    st.rerun()
                else:
                    st.error("Le nom du projet est obligatoire.")
