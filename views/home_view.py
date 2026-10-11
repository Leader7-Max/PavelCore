import streamlit as st

def render_home_view():
    """Affiche le Tableau de Bord principal de PavelCore avec compteurs dynamiques et boutons colorés à effets."""
    
    # CSS pour personnaliser la couleur et les effets de CHAQUE bouton du Dashboard
    st.markdown("""
        <style>
            /* Style de base pour tous les boutons du dashboard */
            div[data-testid="stButton"] > button {
                border-radius: 50px !important;
                font-weight: 700 !important;
                letter-spacing: 0.5px !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                color: #FFFFFF !important;
            }

            /* 1. Bouton Agenda (Bleu Cyan Néon) */
            div[data-testid="stElementContainer"]:has(button[key="btn_agenda"]) button {
                background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%) !important;
                box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4) !important;
            }
            div[data-testid="stElementContainer"]:has(button[key="btn_agenda"]) button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 8px 25px rgba(14, 165, 233, 0.7) !important;
            }

            /* 2. Bouton Coffre-Fort (Violet / Rose Néon) */
            div[data-testid="stElementContainer"]:has(button[key="btn_vault"]) button {
                background: linear-gradient(135deg, #A855F7 0%, #7E22CE 100%) !important;
                box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4) !important;
            }
            div[data-testid="stElementContainer"]:has(button[key="btn_vault"]) button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 8px 25px rgba(168, 85, 247, 0.7) !important;
            }

            /* 3. Bouton Prompts & IA (Vert Émeraude Néon) */
            div[data-testid="stElementContainer"]:has(button[key="btn_prompts"]) button {
                background: linear-gradient(135deg, #10B981 0%, #047857 100%) !important;
                box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4) !important;
            }
            div[data-testid="stElementContainer"]:has(button[key="btn_prompts"]) button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 8px 25px rgba(16, 185, 129, 0.7) !important;
            }

            /* 4. Bouton Projets (Rose Flash / Magenta Néon) */
            div[data-testid="stElementContainer"]:has(button[key="btn_projects"]) button {
                background: linear-gradient(135deg, #EC4899 0%, #BE185D 100%) !important;
                box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4) !important;
            }
            div[data-testid="stElementContainer"]:has(button[key="btn_projects"]) button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 8px 25px rgba(236, 72, 153, 0.7) !important;
            }

            /* 5. Bouton Médias (Orange Ambré Néon) */
            div[data-testid="stElementContainer"]:has(button[key="btn_media"]) button {
                background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%) !important;
                box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4) !important;
            }
            div[data-testid="stElementContainer"]:has(button[key="btn_media"]) button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 8px 25px rgba(245, 158, 11, 0.7) !important;
            }

            /* 6. Bouton Contacts & Emails (Bleu Indigo Néon) */
            div[data-testid="stElementContainer"]:has(button[key="btn_contacts"]) button {
                background: linear-gradient(135deg, #6366F1 0%, #4338CA 100%) !important;
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
            }
            div[data-testid="stElementContainer"]:has(button[key="btn_contacts"]) button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 8px 25px rgba(99, 102, 241, 0.7) !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    user_email = st.session_state.user_info.get("email", "Utilisateur") if st.session_state.get("user_info") else "Mode Invité"
    
    # Compteurs en temps réel
    count_agenda = len(st.session_state.get("agenda_events", []))
    count_prompts = len(st.session_state.get("saved_prompts_library", []))
    count_media = len(st.session_state.get("saved_media_files", []))
    count_projects = len(st.session_state.get("saved_current_projects", [])) + len(st.session_state.get("saved_future_projects", []))
    count_vault = len(st.session_state.get("saved_api_keys", [])) + len(st.session_state.get("saved_user_credentials", []))
    count_contacts = len(st.session_state.get("saved_contacts", []))
    
    # En-tête / Bannière
    st.markdown(f"""
        <div class="pavel-hero-banner" style="position: relative; overflow: hidden;">
            <div style="position: relative; z-index: 2;">
                <span class="zapio-badge">🚀 Workspace Actif</span>
                <h1 style="color: #FFFFFF; margin-top: 10px; font-size: 2.2rem; font-weight: 800;">Tableau de Bord</h1>
                <p style="color: #CBD5E1; font-size: 1.05rem; margin-bottom: 0;">
                    Bienvenue dans votre espace sécurisé, <strong style="color: #F472B6;">{user_email}</strong>. 
                    Pilotez vos agendas, votre coffre-fort et vos projets en toute fluidité.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Métriques Globale
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="pavel-card-grid">
                <div style="font-size: 0.85rem; color: #A78BFA; font-weight: 700; text-transform: uppercase;">📅 Agenda</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #FFFFFF; margin: 6px 0;">{count_agenda} Événement(s)</div>
                <div style="font-size: 0.8rem; color: #34C759; font-weight: 600;">● Module actif</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="pavel-card-grid">
                <div style="font-size: 0.85rem; color: #A78BFA; font-weight: 700; text-transform: uppercase;">🔐 Coffre-Fort</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #FFFFFF; margin: 6px 0;">{count_vault} Élément(s)</div>
                <div style="font-size: 0.8rem; color: #F472B6; font-weight: 600;">● Cloisonné</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="pavel-card-grid">
                <div style="font-size: 0.85rem; color: #A78BFA; font-weight: 700; text-transform: uppercase;">⚡ Performance</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #FFFFFF; margin: 6px 0;">Ultra-Fluide</div>
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
                    <span class="zapio-badge">{count_agenda}</span>
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
                    <span class="zapio-badge">{count_vault}</span>
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
                    <span class="zapio-badge">{count_prompts}</span>
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
                    <span class="zapio-badge">{count_projects}</span>
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
                    <span class="zapio-badge">{count_media}</span>
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
                    <span class="zapio-badge">{count_contacts}</span>
                </div>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 0;">Répertoire et templates de communication.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Ouvrir Contacts & Emails", key="btn_contacts", use_container_width=True):
            st.session_state.current_view = "Contacts & Emails"
            st.rerun()
