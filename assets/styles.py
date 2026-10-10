import streamlit as st

def inject_custom_design():
    """Injecte un arrière-plan éclairci, lumineux et plus contrasté pour PavelCore."""
    st.markdown("""
        <style>
            /* --- 1. ARRIÈRE-PLAN GLOBAL ÉCLAIRCI & LUMINEUX --- */
            .stApp {
                background: radial-gradient(circle at 50% 10%, #1D0F38 0%, #120B24 60%, #0D071B 100%) !important;
                color: #F8FAFC !important;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            }

            /* --- 2. CARTES & BLOCS CONTRASTÉS --- */
            .pavel-card-grid {
                background-color: rgba(30, 16, 53, 0.85) !important;
                border: 1px solid rgba(168, 85, 247, 0.3) !important;
                border-radius: 16px !important;
                padding: 24px !important;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
                transition: all 0.3s ease !important;
            }

            .pavel-card-grid:hover {
                border-color: #EC4899 !important;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5), 0 0 25px rgba(236, 72, 153, 0.35) !important;
            }

            .pavel-hero-banner {
                background: linear-gradient(135deg, rgba(45, 21, 80, 0.9) 0%, rgba(29, 14, 54, 0.95) 100%) !important;
                border: 1px solid rgba(168, 85, 247, 0.35) !important;
                border-radius: 16px !important;
                padding: 30px !important;
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5) !important;
                margin-bottom: 25px !important;
            }

            /* --- 3. CHAMPS DE SAISIE (INPUTS BLANCS LUMINEUX) --- */
            .stTextInput input, .stPasswordInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
                background-color: #FFFFFF !important;
                border: 1px solid rgba(168, 85, 247, 0.5) !important;
                border-radius: 12px !important;
                color: #0F172A !important;
                font-weight: 500 !important;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
            }

            .stTextInput input:focus, .stPasswordInput input:focus, .stTextArea textarea:focus {
                border-color: #EC4899 !important;
                box-shadow: 0 0 20px rgba(236, 72, 153, 0.4) !important;
            }

            /* Fix couleur des placeholders et textes dans inputs */
            .stTextInput input::placeholder, .stTextArea textarea::placeholder {
                color: #64748B !important;
            }

            /* --- 4. CORRECTION DES ALERTES (ex: "Aucune clé API") --- */
            .stAlert {
                background-color: rgba(30, 16, 53, 0.9) !important;
                border: 1px solid rgba(168, 85, 247, 0.4) !important;
                color: #E2E8F0 !important;
                border-radius: 12px !important;
            }

            /* --- 5. BOUTONS (DÉGRADÉ MAGENTA/VIOLET & EFFET GLOW) --- */
            .stButton > button {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                border: none !important;
                color: #FFFFFF !important;
                border-radius: 12px !important;
                font-weight: 600 !important;
                letter-spacing: 0.4px !important;
                padding: 0.6rem 1.2rem !important;
                box-shadow: 0 6px 20px rgba(236, 72, 153, 0.4) !important;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
            }

            .stButton > button:hover {
                transform: translateY(-2px) scale(1.01) !important;
                box-shadow: 0 10px 30px rgba(236, 72, 153, 0.6), 0 0 25px rgba(168, 85, 247, 0.5) !important;
            }

            .stButton > button:active {
                transform: translateY(1px) scale(0.99) !important;
                box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3) !important;
            }

            /* --- 6. ONGLETS (TABS) BIEN VISIBLES --- */
            .stTabs [data-baseweb="tab-list"] {
                gap: 10px;
                background-color: transparent;
                border-bottom: 1px solid rgba(168, 85, 247, 0.25);
                padding-bottom: 10px;
            }

            .stTabs [data-baseweb="tab"] {
                background-color: rgba(30, 16, 53, 0.7);
                border: 1px solid rgba(168, 85, 247, 0.3);
                border-radius: 10px;
                color: #CBD5E1;
                padding: 8px 16px;
                font-weight: 600;
            }

            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                border: none !important;
                color: #FFFFFF !important;
                box-shadow: 0 0 20px rgba(236, 72, 153, 0.4);
            }

            /* --- 7. BADGES --- */
            .zapio-badge {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%);
                color: white;
                padding: 5px 12px;
                border-radius: 8px;
                font-size: 0.75rem;
                font-weight: 600;
                box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3);
            }
        </style>
    """, unsafe_allow_html=True)
