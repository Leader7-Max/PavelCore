import streamlit as st
import time
import random

def render_home_view():
    """Affiche le Tableau de Bord principal de PavelCore avec des notifications rotatives internationales en direct."""
    
    # CSS pour le style des cartes et l'animation de la notification flottante
    st.markdown("""
        <style>
            /* Badges de compteurs néon */
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

            /* Animation de la notification popup style toast */
            @keyframes slideInNotification {
                0% { opacity: 0; transform: translateY(-20px) scale(0.95); }
                100% { opacity: 1; transform: translateY(0) scale(1); }
            }

            .pavel-live-notification {
                background: linear-gradient(135deg, rgba(30, 10, 60, 0.95) 0%, rgba(20, 8, 40, 0.98) 100%) !important;
                border: 1px solid rgba(236, 72, 153, 0.5) !important;
                border-radius: 16px !important;
                padding: 14px 18px !important;
                margin-top: 20px !important;
                margin-bottom: 20px !important;
                box-shadow: 0 8px 30px rgba(236, 72, 153, 0.25), 0 2px 10px rgba(0, 0, 0, 0.5) !important;
                display: flex;
                align-items: center;
                gap: 15px;
                animation: slideInNotification 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
                position: relative;
                overflow: hidden;
            }

            .pavel-live-notification::before {
                content: '';
                position: absolute;
                top: 0; left: 0; width: 4px; height: 100%;
                background: linear-gradient(180deg, #EC4899 0%, #8B5CF6 100%);
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
                <span class="pavel-counter-badge">🚀 Workspace Actif (200+ Membres)</span>
                <h1 style="color: #FFFFFF; margin-top: 10px; font-size: 2.2rem; font-weight: 800;">Tableau de Bord</h1>
                <p style="color: #CBD5E1; font-size: 1.05rem; margin-bottom: 0;">
                    Bienvenue dans votre espace sécurisé, <strong style="color: #F472B6;">{user_email}</strong>. 
                    Pilotez vos agendas, votre coffre-fort et vos projets en toute fluidité.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- LISTE ÉTENDUE DES TÉMOIGNAGES INTERNATIONAUX ---
    international_testimonials = [
        {
            "name": "Yannick M.",
            "role": "Cameroun 🇨🇲",
            "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
            "comment": "J'adore cette application ! L'agenda et la gestion des events sont parfaits depuis Douala.",
            "time": "En direct"
        },
        {
            "name": "Aïssatou B.",
            "role": "France 🇫🇷",
            "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
            "comment": "Une fluidité remarquable, bravo à l'équipe pour ce bijou technologique depuis Grenoble !",
            "time": "En direct"
        },
        {
            "name": "Koffi K.",
            "role": "Côte d'Ivoire 🇨🇮",
            "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
            "comment": "Franchement propre ! Le coffre-fort et les outils IA me font gagner un temps fou à Abidjan.",
            "time": "En direct"
        },
        {
            "name": "Fatoumata D.",
            "role": "Guinée 🇬🇳",
            "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80",
            "comment": "J'adore l'interface et la recherche universelle, c'est ultra intuitif à Conakry.",
            "time": "En direct"
        },
        {
            "name": "John S.",
            "role": "USA 🇺🇸",
            "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80",
            "comment": "Amazing workspace! The performance and security standards are top notch.",
            "time": "En direct"
        },
        {
            "name": "Emre K.",
            "role": "Turquie 🇹🇷",
            "avatar": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&auto=format&fit=crop&q=80",
            "comment": "Harika bir uygulama! Design and speed are incredible. Greetings from Istanbul!",
            "time": "En direct"
        }
    ]

    # Gestion de l'index rotatif dans l'état de session
    if "notif_idx" not in st.session_state:
        st.session_state.notif_idx = 0

    curr_notif = international_testimonials[st.session_state.notif_idx]

    # Affichage du conteneur de notification en temps réel
    st.markdown(f"""
        <div class="pavel-live-notification">
            <img src="{curr_notif['avatar']}" style="width: 48px; height: 48px; border-radius: 50%; object-fit: cover; border: 2px solid #EC4899; box-shadow: 0 0 10px rgba(236,72,153,0.5);" alt="Avatar">
            <div style="flex-grow: 1; min-width: 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                    <div>
                        <strong style="color: #FFFFFF; font-size: 0.95rem;">{curr_notif['name']}</strong>
                        <span style="color: #A78BFA; font-size: 0.75rem; margin-left: 6px;">({curr_notif['role']})</span>
                    </div>
                    <span style="font-size: 0.7rem; color: #34C759; font-weight: 700;">● {curr_notif['time']}</span>
                </div>
                <p style="color: #CBD5E1; font-size: 0.88rem; margin: 0; font-style: italic; line-height: 1.3;">"{curr_notif['comment']}"</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Passage automatique au témoignage suivant et actualisation toutes les 5 secondes
    st.session_state.notif_idx = (st.session_state.notif_idx + 1) % len(international_testimonials)
    time.sleep(5)
    st.rerun()
    # -------------------------------------------------------------------------

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
