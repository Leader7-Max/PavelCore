st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📂 Projets Enregistrés (Cliquez pour ouvrir)")
        
        for cp in st.session_state.saved_current_projects:
            # Utilisation d'un expander interactif pour ouvrir/fermer le projet et voir les détails
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
