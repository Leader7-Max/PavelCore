import streamlit as st

def render_projets_view(sub_title_color="#FFF", desc_color="#CBD5E1"):
    """Gère l'affichage des projets en cours, futurs et de la boîte à idées avec des cartes ouvrables."""
    
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
            
            if st.form_submit_button("Enregistrer", use_container_width=True):
                if name:
                    st.session_state.saved_current_projects.append({
                        "name": name, 
                        "client": client, 
                        "priority": priority, 
                        "next": next_step, 
                        "deadline": str(deadline), 
                        "desc": project_desc
                    })
                    st.toast("🚀 Projet en cours enregistré avec succès !", icon="✅")
                    st.rerun()
                else:
                    st.warning("Veuillez renseigner le nom du projet.")
                    
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📂 Projets Enregistrés (Cliquez pour ouvrir)")
        
        if not st.session_state.saved_current_projects:
            st.info("Aucun projet en cours pour le moment.")
        
        for cp in st.session_state.saved_current_projects:
            with st.expander(f"🚀 {cp['name']} — 👤 Client: {cp['client']} (Échéance: {cp['deadline']})"):
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.markdown(f"**Priorité :** {cp['priority']}")
                    st.markdown(f"**Prochaine étape :** {cp['next']}")
                with col_info2:
                    st.markdown(f"**Date limite :** {cp['deadline']}")
                
                st.markdown("---")
                st.markdown("**Description du projet :**")
                st.info(cp['desc'] if cp['desc'] else "Aucune description renseignée pour ce projet.")

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
            
            if st.form_submit_button("Ajouter", use_container_width=True):
                if name:
                    st.session_state.saved_future_projects.append({
                        "name": name, 
                        "horizon": horizon, 
                        "resources": resources, 
                        "goal": goal
                    })
                    st.toast("🔮 Projet futur ajouté avec succès !", icon="✨")
                    st.rerun()
                else:
                    st.warning("Veuillez renseigner le nom du projet futur.")
                    
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📂 Roadmaps Enregistrées (Cliquez pour ouvrir)")
        
        if not st.session_state.saved_future_projects:
            st.info("Aucun projet futur enregistré.")
        
        for fp in st.session_state.saved_future_projects:
            with st.expander(f"🔮 {fp['name']} ({fp['horizon']})"):
                st.markdown(f"**Objectif :** {fp['goal']}")
                st.markdown(f"**Ressources requises :**")
                st.info(fp['resources'] if fp['resources'] else "Aucune ressource spécifiée.")

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
            
            if st.form_submit_button("Sauvegarder", use_container_width=True):
                if title:
                    st.session_state.saved_ideas.append({
                        "title": title, 
                        "cat": category, 
                        "desc": description, 
                        "impact": impact
                    })
                    st.toast("💡 Idée sauvegardée avec succès !", icon="💡")
                    st.rerun()
                else:
                    st.warning("Veuillez renseigner un titre.")
                    
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📂 Idées Enregistrées (Cliquez pour ouvrir)")
        
        if not st.session_state.saved_ideas:
            st.info("Aucune idée enregistrée pour le moment.")
        
        for id_item in st.session_state.saved_ideas:
            with st.expander(f"💡 {id_item['title']} [{id_item['cat']}] (Impact: {id_item['impact']})"):
                st.markdown(f"**Description détaillée :**")
                st.info(id_item['desc'] if id_item['desc'] else "Aucune description fournie.")
