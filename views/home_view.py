import streamlit as st
import random

def render_home_view():
    """Affiche le Tableau de Bord principal de PavelCore avec un widget de témoignages mondiaux en bas à droite (dynamique au clic/action, 0 latence)."""
    
    # CSS pour positionner le widget fixe en bas à droite, propre et sans fioritures
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

            /* Halo lumineux au survol des cartes de modules */
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

            /* Widget de notification fixe en bas à droite */
            .pavel-bottom-right-toast {
                position: fixed;
                bottom: 25px;
                right: 25px;
                z-index: 99999;
                background: rgba(23, 10, 46, 0.95) !important;
                border: 1px solid rgba(236, 72, 153, 0.4) !important;
                border-radius: 14px !important;
                padding: 14px 16px !important;
                width: 350px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7) !important;
                display: flex;
                align-items: center;
                gap: 12px;
                backdrop-filter: blur(10px);
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
                <span class="pavel-counter-badge">🚀 Workspace Actif (300+ Membres Mondiaux)</span>
                <h1 style="color: #FFFFFF; margin-top: 10px; font-size: 2.2rem; font-weight: 800;">Tableau de Bord</h1>
                <p style="color: #CBD5E1; font-size: 1.05rem; margin-bottom: 0;">
                    Bienvenue dans votre espace sécurisé, <strong style="color: #F472B6;">{user_email}</strong>. 
                    Pilotez vos agendas, votre coffre-fort et vos projets en toute fluidité.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- BASE DE DONNÉES MONDIALE DES TÉMOIGNAGES (TOUS LES PAYS AVEC DRAPEAUX) ---
    world_testimonials = [
        # Afrique
        {"name": "Yannick M.", "country": "🇨🇲 Cameroun", "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150&auto=format&fit=crop&q=80", "comment": "J'adore cette application ! L'agenda est parfait depuis Douala."},
        {"name": "Koffi K.", "country": "🇨🇮 Côte d'Ivoire", "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80", "comment": "Le coffre-fort et les outils IA me font gagner un temps fou à Abidjan."},
        {"name": "Aïssatou D.", "country": "🇬🇳 Guinée", "avatar": "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=150&auto=format&fit=crop&q=80", "comment": "L'interface et la recherche universelle sont ultra intuitives à Conakry."},
        {"name": "Mamadou S.", "country": "🇸🇳 Sénégal", "avatar": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150&auto=format&fit=crop&q=80", "comment": "Le top du top pour gérer mes plannings et projets depuis Dakar. J'valide !"},
        {"name": "Amine B.", "country": "🇲🇦 Maroc", "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80", "comment": "Application magnifique et extrêmement rapide depuis Casablanca."},
        {"name": "Mehdi T.", "country": "🇹🇳 Tunisie", "avatar": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=150&auto=format&fit=crop&q=80", "comment": "Un outil de travail exceptionnel. Salutations depuis Tunis !"},
        {"name": "Ibrahim K.", "country": "🇲🇱 Mali", "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80", "comment": "Une fluidité exemplaire, bravo pour PavelCore depuis Bamako."},

        # Europe
        {"name": "Éléonore V.", "country": "🇫🇷 France", "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&auto=format&fit=crop&q=80", "comment": "Une fluidité remarquable, bravo pour ce bijou technologique depuis Grenoble !"},
        {"name": "Emre K.", "country": "🇹🇷 Turquie", "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80", "comment": "Harika bir uygulama! Design and speed are incredible from Istanbul."},
        {"name": "Hans W.", "country": "🇩🇪 Allemagne", "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150&auto=format&fit=crop&q=80", "comment": "Ausgezeichnet! Incredible speed and clean architecture from Berlin."},
        {"name": "Matteo R.", "country": "🇮🇹 Italie", "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80", "comment": "Fantastico! Un workspace davvero potente ed elegante da Milano."},
        {"name": "Carmen G.", "country": "🇪🇸 Espagne", "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80", "comment": "Me encanta esta aplicación, muy fluida y profesional desde Madrid."},
        {"name": "Lucas D.", "country": "🇧🇪 Belgique", "avatar": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=150&auto=format&fit=crop&q=80", "comment": "Super boulot, c'est devenu mon outil quotidien à Bruxelles."},
        {"name": "Noah S.", "country": "🇨🇭 Suisse", "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150&auto=format&fit=crop&q=80", "comment": "Précis, sécurisé et ultra rapide. Salutations depuis Genève !"},

        # Amérique & Asie
        {"name": "Michael S.", "country": "🇺🇸 USA", "avatar": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=150&auto=format&fit=crop&q=80", "comment": "Amazing workspace! The performance and security standards are top notch."},
        {"name": "Sophie L.", "country": "🇨🇦 Canada", "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80", "comment": "Super clean interface, very fast and secure from Montreal."},
        {"name": "Kenji T.", "country": "🇯🇵 Japon", "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80", "comment": "Subarashii! The design and reactivity are futuristic from Tokyo."},
        {"name": "Beatriz S.", "country": "🇧🇷 Brésil", "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80", "comment": "Maravilhoso! Estou amando usar o PavelCore no Rio de Janeiro."}
    ]

    # Rotation propre et instantanée à chaque interaction de l'utilisateur (0 latence)
    if "notif_idx" not in st.session_state:
        st.session_state.notif_idx = 0
    else:
        st.session_state.notif_idx = (st.session_state.notif_idx + 1) % len(world_testimonials)

    curr_notif = world_testimonials[st.session_state.notif_idx]

    # Affichage du widget fixe en bas à droite
    st.markdown(f"""
        <div class="pavel-bottom-right-toast">
            <img src="{curr_notif['avatar']}" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover; border: 2px solid #EC4899;" alt="Avatar">
            <div style="flex-grow: 1; min-width: 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                    <strong style="color: #FFFFFF; font-size: 0.88rem;">{curr_notif['name']}</strong>
                    <span style="font-size: 0.78rem; color: #A78BFA; font-weight: 700;">{curr_notif['country']}</span>
                </div>
                <p style="color: #CBD5E1; font-size: 0.82rem; margin: 0; font-style: italic; line-height: 1.25;">"{curr_notif['comment']}"</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    # -----------------------------------------------------------------------------------

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
