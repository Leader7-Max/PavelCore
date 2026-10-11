import streamlit as st
import json

def render_backup_view(sub_title_color="#FFF"):
    """Gère la vue de sauvegarde et de restauration globale du workspace avec des explications claires et un design Silicon Valley."""
    
    # En-tête de la section
    st.markdown(f'''
        <div class="sub-section-header">
            <span class="zapio-badge">SÉCURITÉ & DONNÉES</span>
            <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">⚙️ Gestion & Sauvegarde Globale</h1>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Utilisation d'un expander stylisé et 100% lisible
    with st.expander("📦 Panneau de Sauvegarde & Restauration (Backup JSON)", expanded=True):
        st.markdown("""
            <p style='color: #CBD5E1; font-size: 0.95rem; line-height: 1.5; margin-bottom: 20px;'>
                Cette section vous permet de sécuriser vos données. Vous pouvez télécharger une copie de secours 
                de tout votre espace de travail ou restaurer vos informations à partir d'un fichier de sauvegarde précédent.
            </p>
        """, unsafe_allow_html=True)
        
        col_exp, col_imp = st.columns(2, gap="large")
        
        # --- COLONNE EXPORTATION ---
        with col_exp:
            st.markdown("### 📤 Exporter vos données")
            st.markdown("<p style='color: #94A3B8; font-size: 0.85rem;'>Téléchargez une copie de secours de tout votre espace de travail (Projets, Agenda, Coffre-fort, etc.) sur votre appareil.</p>", unsafe_allow_html=True)
            
            # Préparation des données pour l'export JSON global de PavelCore
            workspace_data = {
                "current_projects": st.session_state.get("saved_current_projects", []),
                "future_projects": st.session_state.get("saved_future_projects", []),
                "ideas": st.session_state.get("saved_ideas", []),
                "agenda_events": st.session_state.get("agenda_events", []),
                "api_keys": st.session_state.get("saved_api_keys", []),
                "credentials": st.session_state.get("saved_user_credentials", []),
                "prompts": st.session_state.get("saved_prompts_library", []),
                "media_files": st.session_state.get("saved_media_files", []),
                "contacts": st.session_state.get("saved_contacts", [])
            }
            
            json_str = json.dumps(workspace_data, indent=4, ensure_ascii=False)
            
            st.download_button(
                label="📥 Télécharger le Backup (.json)",
                data=json_str,
                file_name="pavelcore_workspace_backup.json",
                mime="application/json",
                key="btn_download_backup",
                use_container_width=True,
                help="Cliquez pour sauvegarder l'intégralité de vos données sur votre ordinateur ou téléphone."
            )

        # --- COLONNE RESTAURATION ---
        with col_imp:
            st.markdown("### 📥 Restaurer une sauvegarde (.json)")
            st.info("💡 **Instructions :** Utilisez le cadre ci-dessous pour importer votre ancien fichier de sauvegarde `.json` afin de récupérer vos données.")

            uploaded_file = st.file_uploader(
                label="👉 **Sélectionnez votre fichier de sauvegarde (.json) :**",
                type=["json"],
                help="Cliquez sur le bouton pour parcourir vos fichiers et sélectionner votre backup."
            )

            if uploaded_file is not None:
                try:
                    imported_data = json.load(uploaded_file)
                    st.success("✅ Fichier détecté et analysé avec succès ! Prêt pour la restauration.")
                    
                    if st.button("🚀 Valider et Restaurer le Workspace", key="btn_confirm_restore", use_container_width=True):
                        # Restauration dans le session_state
                        st.session_state.saved_current_projects = imported_data.get("current_projects", [])
                        st.session_state.saved_future_projects = imported_data.get("future_projects", [])
                        st.session_state.saved_ideas = imported_data.get("ideas", [])
                        st.session_state.agenda_events = imported_data.get("agenda_events", [])
                        st.session_state.saved_api_keys = imported_data.get("api_keys", [])
                        st.session_state.saved_user_credentials = imported_data.get("credentials", [])
                        st.session_state.saved_prompts_library = imported_data.get("prompts", [])
                        st.session_state.saved_media_files = imported_data.get("media_files", [])
                        st.session_state.saved_contacts = imported_data.get("contacts", [])
                        
                        st.toast("🎉 Workspace restauré avec succès !", icon="✅")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Erreur lors de la lecture du fichier JSON : {e}")
