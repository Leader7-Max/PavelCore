import streamlit as st

def render_projets_module():
    sub_tab = st.pills(
        "Navigation Projets",
        options=["🚀 Projets en cours", "🔮 Projets futurs", "💡 Idées"],
        default="🚀 Projets en cours",
        label_visibility="collapsed"
    )
    
    if sub_tab == "🚀 Projets en cours":
        st.markdown('''
            <div class="sub-section-header">
                <span class="zapio-badge">SUIVI OPÉRATIONNEL</span>
                <h1 style="color: #FFF; font-size: 1.8rem; margin: 5px 0 0 0;">🚀 Projets en cours</h1>
            </div>
        ''', unsafe_allow_html=True)
        with st.form("form_curr_proj"):
            name = st.text_input("Nom du projet")
            client = st.text_input("Client / Marque")
            deadline = st.date_input("Date limite")
            if st.form_submit_button("Enregistrer"):
                if name:
                    st.session_state.saved_current_projects.append({"name": name, "client": client, "deadline": str(deadline)})
                    st.toast("🚀 Projet en cours enregistré !", icon="✅")
                    st.rerun()
        for cp in st.session_state.saved_current_projects:
            st.markdown(f'<div class="zapio-card"><h3 style="color:#FFF;">{cp["name"]}</h3><p style="color:#CBD5E1;">Client: {cp["client"]} | Échéance: {cp["deadline"]}</p></div>', unsafe_allow_html=True)

    elif sub_tab == "🔮 Projets futurs":
        st.markdown('''
            <div class="sub-section-header">
                <span class="zapio-badge">VISION & ROADMAP</span>
                <h1 style="color: #FFF; font-size: 1.8rem; margin: 5px 0 0 0;">🔮 Projets futurs</h1>
            </div>
        ''', unsafe_allow_html=True)
        with st.form("form_fut_proj"):
            name = st.text_input("Nom du projet futur")
            goal = st.text_input("Objectif")
            if st.form_submit_button("Ajouter"):
                if name:
                    st.session_state.saved_future_projects.append({"name": name, "goal": goal})
                    st.toast("🔮 Projet futur ajouté !", icon="✨")
                    st.rerun()
        for fp in st.session_state.saved_future_projects:
            st.markdown(f'<div class="zapio-card"><h3 style="color:#FFF;">{fp["name"]}</h3><p style="color:#CBD5E1;">Objectif: {fp["goal"]}</p></div>', unsafe_allow_html=True)

    elif sub_tab == "💡 Idées":
        st.markdown('''
            <div class="sub-section-header">
                <span class="zapio-badge">INSPIRATION & CONCEPTS</span>
                <h1 style="color: #FFF; font-size: 1.8rem; margin: 5px 0 0 0;">💡 Boîte à Idées</h1>
            </div>
        ''', unsafe_allow_html=True)
        with st.form("form_ideas"):
            title = st.text_input("Titre de l'idée")
            description = st.text_area("Description")
            if st.form_submit_button("Sauvegarder"):
                if title:
                    st.session_state.saved_ideas.append({"title": title, "desc": description})
                    st.toast("💡 Idée sauvegardée !", icon="💡")
                    st.rerun()
        for id_item in st.session_state.saved_ideas:
            st.markdown(f'<div class="zapio-card"><h3 style="color:#FFF;">{id_item["title"]}</h3><p style="color:#CBD5E1;">{id_item["desc"]}</p></div>', unsafe_allow_html=True)
