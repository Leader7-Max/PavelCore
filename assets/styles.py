import streamlit as st

def inject_custom_design():
    """Injecte le système de design Silicon Valley premium avec effets néon et animations sur TOUS les boutons."""
    
    st.markdown("""
        <style>
            /* =========================================================
               1. FOND DE PAGE & FONT GLOBALE
               ========================================================= */
            .stApp {
                background-color: #1A0B2E !important;
                background-image: 
                    radial-gradient(at 0% 0%, rgba(124, 58, 237, 0.15) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.15) 0px, transparent 50%) !important;
                color: #F8FAFC !important;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            }

            /* =========================================================
               2. EFFET GLOBAL SUR ABSOLUMENT TOUS LES BOUTONS
               ========================================================= */
            /* Style de base pour TOUS les boutons principaux (st.button, form_submit_button, download_button) */
            div[data-testid="stButton"] > button,
            div[data-testid="stFormSubmitButton"] > button,
            div[data-testid="stDownloadButton"] > button {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
                font-size: 0.95rem !important;
                border-radius: 50px !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                padding: 10px 24px !important;
                box-shadow: 0 4px 18px rgba(236, 72, 153, 0.45), 0 0 12px rgba(139, 92, 246, 0.3) !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                cursor: pointer !important;
            }

            /* Effet au survol (Hover / Zoom / Halo Néon) sur TOUS les boutons */
            div[data-testid="stButton"] > button:hover,
            div[data-testid="stFormSubmitButton"] > button:hover,
            div[data-testid="stDownloadButton"] > button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 8px 28px rgba(236, 72, 153, 0.75), 0 0 20px rgba(139, 92, 246, 0.6) !important;
                border-color: #FFFFFF !important;
            }

            /* Effet au clic (Active) */
            div[data-testid="stButton"] > button:active,
            div[data-testid="stFormSubmitButton"] > button:active,
            div[data-testid="stDownloadButton"] > button:active {
                transform: translateY(1px) scale(0.98) !important;
                box-shadow: 0 2px 10px rgba(236, 72, 153, 0.5) !important;
            }

            /* =========================================================
               3. PERSONNALISATION COULEURS PAR TYPE / CLÉ
               ========================================================= */

            /* Boutons Secondaires (Variant Secondary) -> Violet Émeraude Néon */
            div[data-testid="stButton"] > button[kind="secondary"] {
                background: linear-gradient(135deg, #7C3AED 0%, #4C1D95 100%) !important;
                box-shadow: 0 4px 18px rgba(124, 58, 237, 0.45) !important;
            }
            div[data-testid="stButton"] > button[kind="secondary"]:hover {
                box-shadow: 0 8px 28px rgba(124, 58, 237, 0.8) !important;
            }

            /* Boutons de Formulaires (Enregistrer, Ajouter, Validations) -> Vert Émeraude Néon */
            div[data-testid="stFormSubmitButton"] > button {
                background: linear-gradient(135deg, #10B981 0%, #047857 100%) !important;
                box-shadow: 0 4px 18px rgba(16, 185, 129, 0.45) !important;
            }
            div[data-testid="stFormSubmitButton"] > button:hover {
                box-shadow: 0 8px 28px rgba(16, 185, 129, 0.8) !important;
            }

            /* Boutons d'Action Spécifiques Dashboard (Agenda - Cyan) */
            div[data-testid="stElementContainer"]:has(button[key="btn_agenda"]) button {
                background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%) !important;
                box-shadow: 0 4px 18px rgba(14, 165, 233, 0.45) !important;
            }
            div[data-testid="stElementContainer"]:has(button[key="btn_agenda"]) button:hover {
                box-shadow: 0 8px 28px rgba(14, 165, 233, 0.8) !important;
            }

            /* Boutons Dashboard (Coffre-Fort - Violet Flash) */
            div[data-testid="stElementContainer"]:has(button[key="btn_vault"]) button {
                background: linear-gradient(135deg, #A855F7 0%, #7E22CE 100%) !important;
                box-shadow: 0 4px 18px rgba(168, 85, 247, 0.45) !important;
            }
            div[data-testid="stElementContainer"]:has(button[key="btn_vault"]) button:hover {
                box-shadow: 0 8px 28px rgba(168, 85, 247, 0.8) !important;
            }

            /* Boutons Dashboard (Prompts - Vert) */
            div[data-testid="stElementContainer"]:has(button[key="btn_prompts"]) button {
                background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
                box-shadow: 0 4px 18px rgba(16, 185, 129, 0.45) !important;
            }
            div[data-testid="stElementContainer"]:has(button[key="btn_prompts"]) button:hover {
                box-shadow: 0 8px 28px rgba(16, 185, 129, 0.8) !important;
            }

            /* Boutons Dashboard (Projets - Magenta/Pink) */
            div[data-testid="stElementContainer"]:has(button[key="btn_projects"]) button {
                background: linear-gradient(135deg, #EC4899 0%, #BE185D 100%) !important;
                box-shadow: 0 4px 18px rgba(236, 72, 153, 0.45) !important;
            }
            div[data-testid="stElementContainer"]:has(button[key="btn_projects"]) button:hover {
                box-shadow: 0 8px 28px rgba(236, 72, 153, 0.8) !important;
            }

            /* Boutons Dashboard (Médias - Orange Gold) */
            div[data-testid="stElementContainer"]:has(button[key="btn_media"]) button {
                background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%) !important;
                box-shadow: 0 4px 18px rgba(245, 158, 11, 0.45) !important;
            }
            div[data-testid="stElementContainer"]:has(button[key="btn_media"]) button:hover {
                box-shadow: 0 8px 28px rgba(245, 158, 11, 0.8) !important;
            }

            /* Boutons Dashboard (Contacts - Indigo) */
            div[data-testid="stElementContainer"]:has(button[key="btn_contacts"]) button {
                background: linear-gradient(135deg, #6366F1 0%, #4338CA 100%) !important;
                box-shadow: 0 4px 18px rgba(99, 102, 241, 0.45) !important;
            }
            div[data-testid="stElementContainer"]:has(button[key="btn_contacts"]) button:hover {
                box-shadow: 0 8px 28px rgba(99, 102, 241, 0.8) !important;
            }

            /* =========================================================
               4. CARTES & BADGES
               ========================================================= */
            .pavel-card-grid, .zapio-card {
                background: rgba(23, 10, 46, 0.7) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 16px !important;
                padding: 18px !important;
                backdrop-filter: blur(10px) !important;
                transition: transform 0.2s ease, border-color 0.2s ease !important;
            }
            .pavel-card-grid:hover, .zapio-card:hover {
                border-color: rgba(236, 72, 153, 0.5) !important;
                transform: translateY(-2px) !important;
            }
            
            .zapio-badge {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                color: #FFFFFF !important;
                padding: 4px 12px !important;
                border-radius: 20px !important;
                font-size: 0.75rem !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
            }
            
            .pavel-hero-banner {
                background: linear-gradient(135deg, rgba(124, 58, 237, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%) !important;
                border: 1px solid rgba(255, 255, 255, 0.15) !important;
                border-radius: 20px !important;
                padding: 28px !important;
                margin-bottom: 25px !important;
                backdrop-filter: blur(12px) !important;
            }
        </style>
    """, unsafe_allow_html=True)
