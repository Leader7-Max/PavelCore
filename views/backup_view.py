import streamlit as st
import json
from datetime import datetime, date, time

def render_backup_view(sub_title_color="#FFF"):
    """Gère la vue de sauvegarde et de restauration globale du workspace."""
    
    st.markdown(f'''
        <div class="sub-section-header">
            <span class="zapio-badge">SÉCURITÉ & DONNÉES</span>
            <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">⚙️ Gestion & Sauvegarde Globale</h1>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("📦 Panneau de Sauvegarde & Restauration (Backup JSON)", expanded=True):
        st.markdown("""
            <p style='color: #CBD5E1; font-size: 0.95rem; line-height: 1.5; margin-bottom: 20px;'>
                Cette section vous permet de sécuriser vos données. Vous pouvez télécharger une copie de secours 
                de tout votre espace de travail ou restaurer vos informations à partir d'un fichier de sauvegarde précédent.
            </p>
        """, unsafe_allow_html=True)
        
        col_exp, col_imp = st.columns(2, gap="large")
        
        # --- EXPORTATION ---
        with col_exp:
            st.markdown("### 📤 Exporter vos données")
            st.markdown("<p style='color: #94A3B8; font-size: 0.85rem;'>Téléchargez une copie de secours de tout votre espace de travail sur votre appareil.</p>", unsafe_allow_html=True)
            
            # Sérialisation propre des événements agenda (conversion des dates/heures en string pour le JSON)
            agenda_serializable = []
            for e in st.session_state.get("agenda_events", []):
                agenda_serializable.append({
                    "title": e.get("title", ""),
                    "date": e["date"].strftime("%Y-%m-%d") if isinstance(e.get("date"), (date, datetime)) else str(e.get("date", "")),
                    "time": e["time"].strftime("%H:%M") if isinstance(e.get("time"), time) else str(e.get("time", "")),
                    "category": e.get("category", ""),
                    "desc": e.get("desc", ""),
                    "ringtone": e.get("ringtone", "")
                })

            workspace_data = {
                "agenda_events": agenda_serializable,
                "saved_prompts_library": st.session_state.get("saved_prompts_library", []),
                "saved_code_snippets": st.session_state.get("saved_code_snippets", []),
                "saved_ideas": st.session_state.get("saved_ideas", []),
                "saved_current_projects": st.session_state.get("saved_current_projects", []),
                "saved_future_projects": st.session_state.get("saved_future_projects", []),
                "saved_links": st.session_state.get("saved_links", []),
                "saved_media_files": st.session_state.get("saved_media_files", []),
                "saved_api_keys": st.session_state.get("saved_api_keys", []),
                "saved_user_credentials": st.session_state.get("saved_user_credentials", []),
                "saved_contacts": st.session_state.get("saved_contacts", []),
                "saved_email_templates": st.session_state.get("saved_email_templates", [])
            }
            
            json_str = json.dumps(workspace_data, indent=4, ensure_ascii=False)
            
            st.download_button(
                label="📥 Télécharger le Backup (.json)",
                data=json_str,
                file_name=f"pavelcore_backup_{date.today().strftime('%Y-%m-%d')}.json",
                mime="application/json",
                key="btn_download_backup",
                use_container_width=True,
                help="Cliquez pour sauvegarder l'intégralité de vos données."
            )

        # --- RESTAURATION ---
        with col_imp:
            st.markdown("### 📥 Restaurer une sauvegarde (.json)")
            st.info("💡 **Instructions :** Utilisez le champ ci-dessous pour importer votre fichier de sauvegarde `.json` et récupérer vos données.")

            uploaded_file = st.file_uploader(
                label="👉 **Sélectionnez votre fichier de sauvegarde (.json) :**",
                type=["json"],
                key="backup_uploader",
                help="Choisissez votre fichier de backup JSON."
            )

            if uploaded_file is not None:
                try:
                    imported_data = json.load(uploaded_file)
                    st.success("✅ Fichier détecté et analysé avec succès !")
                    
                    if st.button("🚀 Valider et Restaurer le Workspace", key="btn_confirm_restore", use_container_width=True):
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
                                "title": ev.get("title", ""),
                                "date": datetime.strptime(ev["date"], "%Y-%m-%d").date() if "date" in ev else date.today(),
                                "time": datetime.strptime(ev["time"], "%H:%M").time() if "time" in ev else time(8, 0),
                                "category": ev.get("category", ""),
                                "desc": ev.get("desc", ""),
                                "ringtone": ev.get("ringtone", "")
                            })
                        st.session_state.agenda_events = restored_events
                        
                        st.toast("🎉 Workspace restauré avec succès !", icon="✅")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Erreur lors de la lecture du fichier JSON : {e}")
