import streamlit as st

def inject_custom_design():
    """Injecte le système de design Silicon Valley premium avec contraste parfait, boutons néon et lisibilité totale."""
    
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
               2. CORRECTION CRITIQUE : LABELS DE FORMULAIRES ULTRA-LISIBLES
               ========================================================= */
            div[data-testid="stWidgetLabel"] label, 
            div[data-testid="stWidgetLabel"] p,
            label[data-testid="stMetricLabel"],
            .stTextInput label, .stTextArea label, .stSelectbox label, .stDateInput label {
                color: #FFFFFF !important;
                font-weight: 700 !important;
                font-size: 0.95rem !important;
                letter-spacing: 0.3px !important;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6) !important;
                margin-bottom: 6px !important;
            }

            /* =========================================================
               3. CHAMPS DE SAISIE DESIGN GLASSMORPHISM PREMIUM
               ========================================================= */
            div[data-baseweb="input"] > div, 
            div[data-baseweb="textarea"] > div,
            div[data-baseweb="select"] > div {
                background-color: rgba(23, 10, 46, 0.85) !important;
                border: 1px solid rgba(236, 72, 153, 0.4) !important;
                border-radius: 10px !important;
                color: #FFFFFF !important;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
                transition: all 0.25s ease !important;
            }

            div[data-baseweb="input"]:focus-within > div, 
            div[data-baseweb="textarea"]:focus-within > div,
            div[data-baseweb="select"]:focus-within > div {
                border-color: #EC4899 !important;
                box-shadow: 0 0 12px rgba(236, 72, 153, 0.5) !important;
                background-color: rgba(30, 12, 60, 0.95) !important;
            }

            input, textarea, div[data-baseweb="select"] * {
                color: #FFFFFF !important;
                font-weight: 500 !important;
            }

            input::placeholder, textarea::placeholder {
                color: #94A3B8 !important;
            }

            /* =========================================================
               4. BOUTONS NÉON VIP (EFFET HOVER & GLOW)
               ========================================================= */
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

            div[data-testid="stButton"] > button:hover,
            div[data-testid="stFormSubmitButton"] > button:hover,
            div[data-testid="stDownloadButton"] > button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 8px 28px rgba(236, 72, 153, 0.75), 0 0 20px rgba(139, 92, 246, 0.6) !important;
                border-color: #FFFFFF !important;
            }

            div[data-testid="stButton"] > button:active,
            div[data-testid="stFormSubmitButton"] > button:active,
            div[data-testid="stDownloadButton"] > button:active {
                transform: translateY(1px) scale(0.98) !important;
            }

            /* =========================================================
               5. CARTES, BADGES & EXPANDERS
               ========================================================= */
            .pavel-card-grid, .zapio-card {
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
                transform: translateY(-2px) !important;
            }
            
            .zapio-badge, .pavel-counter-badge {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                color: #FFFFFF !important;
                padding: 4px 12px !important;
                border-radius: 20px !important;
                font-size: 0.75rem !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
                box-shadow: 0 0 12px rgba(236, 72, 153, 0.6) !important;
            }
            
            .pavel-hero-banner {
                background: linear-gradient(135deg, rgba(124, 58, 237, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%) !important;
                border: 1px solid rgba(255, 255, 255, 0.15) !important;
                border-radius: 20px !important;
                padding: 28px !important;
                margin-bottom: 25px !important;
                backdrop-filter: blur(12px) !important;
            }

            /* =========================================================
               6. CORRECTION EXPANDERS & FILE UPLOADER (SAUVEGARDE)
               ========================================================= */
            div[data-testid="stExpander"] {
                background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
                border-radius: 12px !important;
                border: 1px solid rgba(255, 255, 255, 0.25) !important;
                margin-bottom: 12px !important;
                box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25) !important;
            }

            .streamlit-expanderHeader p, 
            .streamlit-expanderHeader span, 
            div[data-testid="stExpander"] summary, 
            div[data-testid="stExpander"] summary p {
                color: #FFFFFF !important;
                font-weight: 700 !important;
            }

            div[data-testid="stExpanderDetails"] {
                background-color: rgba(0, 0, 0, 0.25) !important;
                border-bottom-left-radius: 12px !important;
                border-bottom-right-radius: 12px !important;
                padding: 15px !important;
                color: #FFFFFF !important;
            }

            /* Correction spécifique File Uploader (Restauration Backup JSON) */
            div[data-testid="stFileUploader"] label,
            div[data-testid="stFileUploader"] span,
            div[data-testid="stFileUploader"] div {
                color: #FFFFFF !important;
                font-weight: 600 !important;
            }
            
            div[data-testid="stFileUploader"] small {
                color: #CBD5E1 !important;
            }
        </style>
    """, unsafe_allow_html=True)
