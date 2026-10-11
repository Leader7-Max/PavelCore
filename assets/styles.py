import streamlit as st

def inject_custom_design():
    """Injecte le système de design Silicon Valley premium avec contraste parfait pour les formulaires."""
    
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
            /* Force tous les titres de champs (Priorité, Date limite, Description, etc.) en blanc éclatant */
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
            /* Inputs texte, zones de texte, selectbox, datepicker */
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

            /* Effet au survol et focus des champs */
            div[data-baseweb="input"]:focus-within > div, 
            div[data-baseweb="textarea"]:focus-within > div,
            div[data-baseweb="select"]:focus-within > div {
                border-color: #EC4899 !important;
                box-shadow: 0 0 12px rgba(236, 72, 153, 0.5) !important;
                background-color: rgba(30, 12, 60, 0.95) !important;
            }

            /* Couleur du texte tape a l'interieur du champ */
            input, textarea, div[data-baseweb="select"] * {
                color: #FFFFFF !important;
                font-weight: 500 !important;
            }

            /* Placeholders (Texte d'aide indicatif) */
            input::placeholder, textarea::placeholder {
                color: #94A3B8 !important;
            }

            /* =========================================================
               4. BOUTONS NÉON VIP
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
                box-shadow: 0 4px 18px rgba(236, 72, 153, 0.45) !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }

            div[data-testid="stButton"] > button:hover,
            div[data-testid="stFormSubmitButton"] > button:hover,
            div[data-testid="stDownloadButton"] > button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 8px 28px rgba(236, 72, 153, 0.75) !important;
            }

            /* =========================================================
               5. CARTES ET PANNEAUX EXPANDERS (PROJETS)
               ========================================================= */
            div[data-testid="stExpander"] {
                background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
                border-radius: 12px !important;
                border: 1px solid rgba(255, 255, 255, 0.25) !important;
                margin-bottom: 12px !important;
            }
            .streamlit-expanderHeader p, .streamlit-expanderHeader span, div[data-testid="stExpander"] summary {
                color: #FFFFFF !important;
                font-weight: 700 !important;
            }
            div[data-testid="stExpanderDetails"] {
                background-color: rgba(0, 0, 0, 0.25) !important;
                color: #FFFFFF !important;
            }
        </style>
    """, unsafe_allow_html=True)
