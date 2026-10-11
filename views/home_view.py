import streamlit as st

def render_home_view():
    """Affiche le Tableau de Bord principal de PavelCore avec des compteurs dynamiques au design néon/glow ultra-premium."""
    
    # CSS dédié au stylage haut de gamme des compteurs et badges du dashboard
    st.markdown("""
        <style>
            /* Badges de compteurs néon en haut à droite des cartes */
            .pavel-counter-badge {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                color: #FFFFFF !important;
                font-weight: 800 !important;
                font-size: 0.85rem !important;
                padding: 4px 12px !important;
                border-radius: 20px !important;
                box-shadow: 0 0 12px rgba(236, 72, 153, 0.6), 0 2px 6px rgba(0, 0, 0, 0.4) !important;
                border: 1px solid rgba(255, 255, 255, 0.4) !important;
                letter-spacing: 0.5px !important;
            }

            /* Valeurs chiffrées des cartes de métriques du haut */
            .pavel-metric-value {
                font-size: 1.6rem !important;
                font-weight: 800 !important;
                background: linear-gradient(135deg, #FFFFFF 0%, #F472B6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                filter: drop-shadow(0 2px 8px rgba(236, 72, 153, 0.4));
                margin: 6px 0 !important;
            }

            /* Halo lumineux au survol des cartes */
            .pavel-card-grid {
                background: rgba(23, 10, 46, 0.75) !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                border-radius: 16px !important;
                padding: 18px !important;
                backdrop-filter: blur(12px) !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }

            .pavel-card-grid:hover {
                border-color: rgba(236, 72, 153, 0.6) !important;
                box-shadow: 0 8px 25px rgba(139, 92, 246, 0.25) !important;
                transform: translateY(-3px) !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    user_email = st.session_state.user_info.get("email", "Utilisateur") if st.session_state.get("user_info") else "Mode Invité"
    
    # Récupération des compteurs en temps réel
    count_agenda = len(st.session_state.get("agenda_events", []))
    count_prompts = len(st.session_state.get("saved_prompts_library", []))
    count_media = len(st.session_state.get("saved_media_files", []))
    count_projects = len(st.session_state.get("saved_current_projects", [])) + len(st.session_state.get("saved_future_projects", []))
    count_vault = len(st.session_state.get("saved_api_keys", [])) + len(st.session_state.get("saved_user_credentials", []))
    count_contacts = len(st.session_state.get("saved_contacts", []))
    
    # En-tête / Bannière Héroïque
    st.markdown(f"""
        <div class="pavel-hero-banner" style="position: relative; overflow: hidden;">
            <div style="position: relative; z-index: 2;">
                <span class="pavel-counter-badge">🚀 Workspace Actif</span>
                <h1 style="color: #FFFFFF; margin-top: 10px; font-size: 2.2rem; font-weight: 800;">Tableau de Bord</h1>
                <p style="color: #CBD5E1; font-size: 1.05rem; margin-bottom: 0;">
                    Bienvenue dans votre espace sécurisé, <strong style="color: #F472B6;">{user_email}</strong>. 
                    Pilotez vos agendas, votre coffre-fort et vos projets en toute fluidité.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Grille de Métriques Globales du Haut
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="pavel-card-grid">
                <div style="font-size: 0.85rem; color: #A78BFA; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">📅 Agenda</div>
                <div class="pavel-metric-value">{count_agenda} Événement(s)</div>
                <div style="font-size: 0.8rem; color: #34C759; font-weight: 600;">● Module actif</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="pavel-card-grid">
                <div style="font-size: 0.85rem; color: #A78BFA; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">🔐 Coffre-Fort</div>
                <div class="pavel-metric-value">{count_vault} Élément(s)</div>
                <div style="font-size: 0.8rem; color: #F472B6; font-weight: 600;">● Cloisonné</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="pavel-card-grid">
                <div style="font-size: 0.85rem; color: #A78BFA; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">⚡ Performance</div>
                <div class="pavel-metric-value">Ultra-Fluide</div>
                <div style="font-size: 0.8rem; color: #34C759; font-weight: 600;">● Design Actif</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ⚡ Accès Rapide aux Modules")
    
    # Ligne 1
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.markdown(f"""
            <div class="pavel-card-grid" style="min-height: 125px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="color: #FFFFFF; margin-top: 0; font-size: 1.1rem;">🗓️ Gérer l'Agenda</h3>
                    <span class="pavel-counter-badge">{count_agenda}</span>
                </div>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 0;">Consultez votre calendrier et planifiez vos événements.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Ouvrir l'Agenda", key="btn_agenda", use_container_width=True):
            st.session_state.current_view = "Agenda"
            st.rerun()

    with r_col2:
        st.markdown(f"""
            <div class="pavel-card-grid" style="min-height: 125px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="color: #FFFFFF; margin-top: 0; font-size: 1.1rem;">🔐 Coffre-Fort Sécurisé</h3>
                    <span class="pavel-counter-badge">{count_vault}</span>
                </div>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 0;">Stockez vos clés API et mots de passe en toute sécurité.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Ouvrir le Coffre-Fort", key="btn_vault", use_container_width=True):
            st.session_state.current_view = "Coffre-Fort"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Ligne 2
    r_col3, r_col4 = st.columns(2)
    with r_col3:
        st.markdown(f"""
            <div class="pavel-card-grid" style="min-height: 125px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="color: #FFFFFF; margin-top: 0; font-size: 1.1rem;">🤖 Prompts & IA</h3>
                    <span class="pavel-counter-badge">{count_prompts}</span>
                </div>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 0;">Bibliothèque complète de prompts et scripts.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Ouvrir Prompts & IA", key="btn_prompts", use_container_width=True):
            st.session_state.current_view = "Prompts & IA"
            st.rerun()

    with r_col4:
        st.markdown(f"""
            <div class="pavel-card-grid" style="min-height: 125px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="color: #FFFFFF; margin-top: 0; font-size: 1.1rem;">🚀 Projets & Idées</h3>
                    <span class="pavel-counter-badge">{count_projects}</span>
                </div>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 0;">Suivi de vos projets actifs et futurs.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Ouvrir Projets", key="btn_projects", use_container_width=True):
            st.session_state.current_view = "Projets"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Ligne 3
    r_col5, r_col6 = st.columns(2)
    with r_col5:
        st.markdown(f"""
            <div class="pavel-card-grid" style="min-height: 125px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="color: #FFFFFF; margin-top: 0; font-size: 1.1rem;">📁 Médias & Fichiers</h3>
                    <span class="pavel-counter-badge">{count_media}</span>
                </div>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 0;">Gestion des images, documents et fichiers.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Ouvrir Médias & Fichiers", key="btn_media", use_container_width=True):
            st.session_state.current_view = "Médias & Fichiers"
            st.rerun()

    with r_col6:
        st.markdown(f"""
            <div class="pavel-card-grid" style="min-height: 125px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="color: #FFFFFF; margin-top: 0; font-size: 1.1rem;">🎴 Contacts & Emails</h3>
                    <span class="pavel-counter-badge">{count_contacts}</span>
                </div>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 0;">Répertoire et templates de communication.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Ouvrir Contacts & Emails", key="btn_contacts", use_container_width=True):
            st.session_state.current_view = "Contacts & Emails"
            st.rerun()
