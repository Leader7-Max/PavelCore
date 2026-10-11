# ROUTAGE DES VUES PRINCIPALES DEPUIS LE TABLEAU DE BORD
    if st.session_state.current_view == "home":
        render_home_view()
        
        # Section de Gestion & Sauvegarde Globale du Workspace sous le dashboard
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
        
        # Bouton de retour universel stylisé en haut de chaque module
        if st.button("← Retour au Tableau de Bord", key="back_to_home_universal", type="secondary"):
            st.session_state.current_view = "home"
            st.rerun()
            
        st.markdown(f"<h2 style='color: #EC4899; margin-top: 15px;'>Espace : {current}</h2>", unsafe_allow_html=True)

        # Aiguillage des vues selon la valeur exacte stockée dans current_view
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
