import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* Structure Globale Dark Premium */
        html, body, [data-testid="stAppViewContainer"], .stApp {
            background-color: #0B0D12 !important;
            color: #F3F4F6 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        [data-testid="stHeader"] {
            background-color: transparent !important;
        }

        h1, h2, h3, h4, h5, h6, label, label p, .stMarkdown {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* Champs de Saisie Ultra Lisibles */
        div[data-baseweb="input"] input, 
        div[data-baseweb="textarea"] textarea,
        .stTextInput input, 
        .stTextArea textarea {
            color: #0F172A !important;
            background-color: #FFFFFF !important;
            border: 2px solid #E2E8F0 !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }

        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }

        div[data-baseweb="popover"] ul, div[role="listbox"] {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
        }
        li[role="option"] {
            color: #0F172A !important;
            font-weight: 600 !important;
        }

        /* ONGLETS STREAMLIT (Tabs Agenda) - Haute Visibilité */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px !important;
            background-color: #141721 !important;
            padding: 8px !important;
            border-radius: 16px !important;
            border: 1px solid #232838 !important;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: #1E2333 !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            border: 1px solid #2D3448 !important;
        }

        .stTabs [data-baseweb="tab"] p, 
        .stTabs [data-baseweb="tab"] span, 
        .stTabs [data-baseweb="tab"] div {
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 1rem !important;
        }

        .stTabs [aria-selected="true"] {
            background-color: #FF3B30 !important;
            border-color: #FF3B30 !important;
            box-shadow: 0 4px 14px rgba(255, 59, 48, 0.4) !important;
        }

        /* Boutons de Formulaire */
        .stButton > button, 
        div[data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(135deg, #FF3B30 0%, #D7261C 100%) !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 1rem !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 14px 24px !important;
            width: 100% !important;
            box-shadow: 0 6px 18px rgba(255, 59, 48, 0.35) !important;
        }

        /* Cartes du Workspace */
        .zapio-card {
            background-color: #141721 !important;
            border: 1px solid #232838 !important;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
        }

        /* NOUVEAU DESIGN : Bloc Agenda Style Event Card */
        .timeline-container {
            display: flex;
            gap: 16px;
            background: #141721;
            border: 1px solid #232838;
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 16px;
            position: relative;
            overflow: hidden;
        }

        .timeline-badge-time {
            background: linear-gradient(135deg, #FF3B30 0%, #C0261D 100%);
            color: #FFFFFF;
            min-width: 90px;
            height: 90px;
            border-radius: 14px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            box-shadow: 0 4px 14px rgba(255, 59, 48, 0.3);
        }

        .timeline-content {
            flex-grow: 1;
        }

        .zapio-badge {
            background-color: #232838;
            color: #FF3B30;
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 700;
        }

        .zapio-badge-green {
            background-color: rgba(52, 199, 89, 0.15);
            color: #34C759;
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)
