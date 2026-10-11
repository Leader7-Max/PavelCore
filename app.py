# ROUTAGE DES VUES PRINCIPALES DEPUIS LE TABLEAU DE BORD
    if st.session_state.current_view == "home":
        render_home_view()
        
        # Appel de la vue de sauvegarde modulaire propre
        render_backup_view(sub_title_color)

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
            
        elif current == "Sauvegarde":
            render_backup_view(sub_title_color)
