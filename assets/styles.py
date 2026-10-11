import streamlit as st

def inject_custom_design():
    """Injecte le design et force l'affichage permanent du bouton de téléchargement."""
    
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
               3. CHAMPS DE SAISIE (INPUTS / TEXTAREAS)
               ========================================================= */
            div[data-baseweb="input"] > div, 
            div[data-baseweb="textarea"] > div,
            div[data-baseweb="select"] > div {
                background-color: #230E3D !important;
                border: 1px solid rgba(236, 72, 153, 0.4) !important;
                border-radius: 10px !important;
                color: #FFFFFF !important;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4) !important;
            }

            div[data-baseweb="input"]:focus-within > div, 
            div[data-baseweb="textarea"]:focus-within > div,
            div[data-baseweb="select"]:focus-within > div {
                border-color: #EC4899 !important;
                box-shadow: 0 0 12px rgba(236, 72, 153, 0.5) !important;
                background-color: #2A104D !important;
            }

            input, textarea {
                color: #FFFFFF !important;
                font-weight: 500 !important;
                caret-color: #EC4899 !important;
            }

            input::placeholder, textarea::placeholder {
                color: #94A3B8 !important;
            }

            div[data-baseweb="select"] span {
                color: #FFFFFF !important;
            }

            /* =========================================================
               4. BOUTONS NÉON VIP & CORRECTION CIBLÉE DU DOWNLOAD BUTTON
               ========================================================= */
            div[data-testid="stButton"] > button,
            div[data-testid="stFormSubmitButton"] > button {
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
                width: 100% !important;
            }

            /* Règle spécifique implacable pour le bouton de téléchargement */
            div[data-testid="stDownloadButton"] button,
            .stDownloadButton button {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                background-color: #EC4899 !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
                font-size: 0.95rem !important;
                border-radius: 50px !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                padding: 10px 24px !important;
                box-shadow: 0 4px 18px rgba(236, 72, 153, 0.45) !important;
                width: 100% !important;
                opacity: 1 !important;
            }

            div[data-testid="stDownloadButton"] button * {
                color: #FFFFFF !important;
            }

            div[data-testid="stButton"] > button:hover,
            div[data-testid="stFormSubmitButton"] > button:hover,
            div[data-testid="stDownloadButton"] button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 8px 28px rgba(236, 72, 153, 0.75) !important;
                border-color: #FFFFFF !important;
            }

            /* =========================================================
               5. CORRECTION RADICALE DU CONTENEUR BLANC DE L'UPLOADER
               ========================================================= */
            div[data-testid="stFileUploader"],
            section[data-testid="stFileUploaderDropzone"],
            div[data-baseweb="file-uploader"] {
                background-color: #230E3D !important;
                border: 2px dashed #EC4899 !important;
                border-radius: 12px !important;
                padding: 20px !important;
            }

            div[data-testid="stFileUploader"] * {
                color: #FFFFFF !important;
            }

            div[data-testid="stFileUploader"] small {
                color: #CBD5E1 !important;
            }

            div[data-testid="stFileUploader"] button {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
                border-radius: 8px !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                box-shadow: 0 4px 12px rgba(236, 72, 153, 0.4) !important;
            }

            /* =========================================================
               6. EXPANDERS & CARTES
               ========================================================= */
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
