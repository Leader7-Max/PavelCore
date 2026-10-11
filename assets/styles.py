import streamlit as st

def inject_custom_design():
    """Injecte le système de design Silicon Valley avec correction complète du bouton d'upload."""
    
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
               2. LABELS DE FORMULAIRES ULTRA-LISIBLES
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
               3. CHAMPS DE SAISIE DESIGN GLASSMORPHISM
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
                cursor: pointer !important;
            }

            div[data-testid="stButton"] > button:hover,
            div[data-testid="stFormSubmitButton"] > button:hover,
            div[data-testid="stDownloadButton"] > button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 8px 28px rgba(236, 72, 153, 0.75) !important;
                border-color: #FFFFFF !important;
            }

            /* =========================================================
               5. FIX TOTAL BOUTON FILE UPLOADER ET ACCESSIBILITÉ
               ========================================================= */
            
            /* Fond du conteneur de dépôt de fichier */
            div[data-testid="stFileUploader"] {
                background-color: rgba(35, 14, 61, 0.9) !important;
                border: 2px dashed #EC4899 !important;
                border-radius: 14px !important;
                padding: 15px !important;
            }

            /* Bouton "Browse files" / "Parcourir" interne au file uploader */
            div[data-testid="stFileUploader"] button {
                background: linear-gradient(135deg, #F43F5E 0%, #E11D48 100%) !important;
                color: #FFFFFF !important;
                font-weight: 800 !important;
                border-radius: 8px !important;
                border: none !important;
                padding: 8px 18px !important;
                box-shadow: 0 4px 12px rgba(225, 29, 72, 0.4) !important;
            }

            div[data-testid="stFileUploader"] button:hover {
                background: linear-gradient(135deg, #FB7185 0%, #F43F5E 100%) !important;
                box-shadow: 0 6px 18px rgba(225, 29, 72, 0.7) !important;
            }

            /* Forcer le texte explicatif de l'uploader en blanc et gris clair */
            div[data-testid="stFileUploader"] section * {
                color: #FFFFFF !important;
            }

            div[data-testid="stFileUploader"] small {
                color: #CBD5E1 !important;
                font-size: 0.85rem !important;
            }

            /* Expanders */
            div[data-testid="stExpander"], details {
                background: #230E3D !important;
                border: 1px solid rgba(236, 72, 153, 0.3) !important;
                border-radius: 12px !important;
            }

            div[data-testid="stExpander"] summary, details summary {
                background-color: #230E3D !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
            }

            div[data-testid="stExpanderDetails"], details > div {
                background-color: rgba(15, 5, 29, 0.6) !important;
                color: #FFFFFF !important;
            }

            /* Cartes & Badges */
            .pavel-card-grid, .zapio-card {
                background: rgba(23, 10, 46, 0.75) !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                border-radius: 16px !important;
                padding: 18px !important;
            }
            
            .zapio-badge, .pavel-counter-badge {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                color: #FFFFFF !important;
                padding: 4px 12px !important;
                border-radius: 20px !important;
                font-size: 0.75rem !important;
                font-weight: 700 !important;
            }
        </style>
    """, unsafe_allow_html=True)
