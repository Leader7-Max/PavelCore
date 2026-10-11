import streamlit as st

def render_home_view():
    """Affiche le Tableau de Bord principal de PavelCore avec un design ultra-premium."""
    
    # Récupération de l'utilisateur connecté
    user_email = st.session_state.user_info.get("email", "Utilisateur") if st.session_state.get("user_info") else "Mode Invité"
    
    # En-tête / Bannière Héroïque
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

    # Grille de Métriques / Statistiques Rapides
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="pavel-card-grid">
                <div style="font-size: 0.85rem; color: #A78BFA; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">📅 Agenda & Planning</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #FFFFFF; margin: 8px 0;">Synchronisé</div>
                <div style="font-size: 0.8rem; color: #34C759; font-weight: 600;">● Module actif et sécurisé</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="pavel-card-grid">
                <div style="font-size: 0.85rem; color: #A78BFA; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">🔐 Coffre-Fort</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #FFFFFF; margin: 8px 0;">Chiffré</div>
                <div style="font-size: 0.8rem; color: #F472B6; font-weight: 600;">● Protection cloisonnée</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="pavel-card-grid">
                <div style="font-size: 0.85rem; color: #A78BFA; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">⚡ Performance</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #FFFFFF; margin: 8px 0;">Ultra-Fluide</div>
                <div style="font-size: 0.8rem; color: #34C759; font-weight: 600;">● Design System Actif</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Section Actions Rapides & Aperçu
    st.markdown("### ⚡ Accès Rapide aux Modules")
    
    q_col1, q_col2 = st.columns(2)
    
    with q_col1:
        st.markdown("""
            <div class="pavel-card-grid">
                <h3 style="color: #FFFFFF; margin-top: 0; font-size: 1.2rem;">🗓️ Gérer l'Agenda</h3>
                <p style="color: #94A3B8; font-size: 0.9rem;">Consultez votre calendrier, planifiez vos événements et suivez vos échéances.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Ouvrir l'Agenda", key="goto_agenda", type="primary"):
            st.session_state.active_tab = "Agenda"
            st.rerun()

    with q_col2:
        st.markdown("""
            <div class="pavel-card-grid">
                <h3 style="color: #FFFFFF; margin-top: 0; font-size: 1.2rem;">🔑 Sécuriser vos Données</h3>
                <p style="color: #94A3B8; font-size: 0.9rem;">Accédez à votre coffre-fort pour stocker vos clés API et identifiants en toute sécurité.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Ouvrir le Coffre-Fort", key="goto_vault", type="secondary"):
            st.session_state.active_tab = "Coffre-Fort"
            st.rerun()
