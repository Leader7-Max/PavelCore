import streamlit as st

def inject_custom_design():
    """Injecte un Design System SaaS pur-sang, s'affranchissant des contraintes natives de Streamlit."""
    st.markdown("""
        <style>
            /* --- 1. RESET & SURCHARGE GLOBALE STREAMLIT --- */
            .stApp {
                background-color: #090612 !important;
                color: #F8FAFC !important;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            }

            /* Suppression des marges et paddings excessifs de Streamlit */
            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 3rem !important;
                max-width: 100% !important;
            }

            /* Masquer les éléments superflus de Streamlit (Header natif, footer "Made with Streamlit") */
            header[data-testid="stHeader"] {
                background: transparent !important;
            }
            footer {visibility: hidden !important;}
            #MainMenu {visibility: hidden !important;}

            /* --- 2. COMPOSANTS GLASSMORPHISM & CARTES --- */
            .pavel-hero-banner {
                background: linear-gradient(135deg, rgba(30, 10, 60, 0.75) 0%, rgba(23, 10, 46, 0.85) 100%);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(139, 92, 246, 0.2);
                padding: 40px;
                border-radius: 16px;
                margin-bottom: 30px;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(236, 72, 153, 0.15);
            }
            
            .pavel-card-grid {
                background: rgba(23, 10, 46, 0.65);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(139, 92, 246, 0.15);
                padding: 24px;
                border-radius: 14px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            }

            .pavel-card-grid:hover {
                border-color: rgba(236, 72, 153, 0.5);
                transform: translateY(-4px);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6), 0 0 25px rgba(236, 72, 153, 0.25);
            }

            /* --- 3. SYSTÈME DE BOUTONS (PHYSIQUE DE RESSORT) --- */
            .stButton > button {
                background: linear-gradient(135deg, #170A2E 0%, #1E0A3C 100%) !important;
                border: 1px solid rgba(139, 92, 246, 0.3) !important;
                color: #F8FAFC !important;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
                border-radius: 10px !important;
                font-weight: 600 !important;
                letter-spacing: 0.4px !important;
                padding: 0.6rem 1.2rem !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
            }
            
            .stButton > button:hover {
                background: linear-gradient(135deg, rgba(236, 72, 153, 0.2) 0%, rgba(139, 92, 246, 0.2) !important;
                border-color: #EC4899 !important;
                transform: translateY(-2px) scale(1.01) !important;
                box-shadow: 0 10px 25px rgba(236, 72, 153, 0.35), 0 0 15px rgba(139, 92, 246, 0.3) !important;
            }
            
            .stButton > button:active {
                transform: translateY(1px) scale(0.99) !important;
                box-shadow: 0 2px 8px rgba(236, 72, 153, 0.2) !important;
            }

            /* Boutons primaires Streamlit forcés au design PavelCore */
            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                border: none !important;
                color: #FFFFFF !important;
            }

            /* --- 4. FORMULAIRES & CHAMPS DE SAISIE --- */
            .stTextInput input, .stPasswordInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
                background-color: rgba(12, 5, 24, 0.85) !important;
                border: 1px solid rgba(139, 92, 246, 0.25) !important;
                border-radius: 10px !important;
                color: #F8FAFC !important;
                transition: all 0.3s ease !important;
            }

            .stTextInput input:focus, .stPasswordInput input:focus, .stTextArea textarea:focus {
                border-color: #EC4899 !important;
                box-shadow: 0 0 20px rgba(236, 72, 153, 0.3) !important;
            }

            /* --- 5. ONGLETS (TABS) MODERNES --- */
            .stTabs [data-baseweb="tab-list"] {
                gap: 10px;
                background-color: transparent;
                border-bottom: 1px solid rgba(139, 92, 246, 0.15);
                padding-bottom: 10px;
            }

            .stTabs [data-baseweb="tab"] {
                background-color: rgba(23, 10, 46, 0.5);
                border: 1px solid rgba(139, 92, 246, 0.15);
                border-radius: 8px;
                color: #CBD5E1;
                padding: 8px 16px;
                font-weight: 600;
                transition: all 0.3s ease;
            }

            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, rgba(236, 72, 153, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%) !important;
                border-color: #EC4899 !important;
                color: #FFFFFF !important;
                box-shadow: 0 0 15px rgba(236, 72, 153, 0.25);
            }

            /* --- 6. BADGES DE STATUT --- */
            .zapio-badge {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%);
                color: white;
                padding: 5px 12px;
                border-radius: 8px;
                font-size: 0.75rem;
                font-weight: 600;
                letter-spacing: 0.5px;
                box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3);
            }

            .zapio-badge-green {
                background: linear-gradient(135deg, #059669 0%, #10B981 100%);
                color: white;
                padding: 3px 10px;
                border-radius: 8px;
                font-size: 0.7rem;
                font-weight: 600;
                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
            }
        </style>
    """, unsafe_allow_html=True)
