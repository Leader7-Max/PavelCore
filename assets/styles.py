import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* Structure générale */
        html, body, [data-testid="stAppViewContainer"], .stApp {
            background-color: #0F1117 !important;
            color: #F0F2F6 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        [data-testid="stHeader"] {
            background-color: transparent !important;
        }

        h1, h2, h3, h4, h5, h6, label, label p, .stMarkdown {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* Champs de saisie */
        div[data-baseweb="input"] input, 
        div[data-baseweb="textarea"] textarea,
        .stTextInput input, 
        .stTextArea textarea {
            color: #0F172A !important;
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }

        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }

        /* Dropdown Options */
        div[data-baseweb="popover"] ul, div[role="listbox"] {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
        }
        li[role="option"] {
            color: #0F172A !important;
            font-weight: 600 !important;
        }

        /* FIX CRITIQUE : ONGLETS STREAMLIT (Tabs Agenda) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px !important;
            background-color: #161922 !important;
            padding: 8px !important;
            border-radius: 14px !important;
            border: 1px solid #2A2E3D !important;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: #222736 !important;
            border-radius: 10px !important;
            padding: 10px 18px !important;
            border: 1px solid #32384A !important;
        }

        /* Forcer la couleur blanche sur le texte de l'onglet inactif */
        .stTabs [data-baseweb="tab"] p, 
        .stTabs [data-baseweb="tab"] span, 
        .stTabs [data-baseweb="tab"] div {
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 0.95rem !important;
        }

        /* Onglet actif (sélectionné) */
        .stTabs [aria-selected="true"] {
            background-color: #FF3B30 !important;
            border-color: #FF3B30 !important;
        }

        .stTabs [aria-selected="true"] p, 
        .stTabs [aria-selected="true"] span {
            color: #FFFFFF !important;
        }

        /* Boutons de formulaire */
        .stButton > button, 
        div[data-testid="stFormSubmitButton"] > button {
            background-color: #FF3B30 !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 0.95rem !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 20px !important;
            width: 100% !important;
            box-shadow: 0 4px 12px rgba(255, 59, 48, 0.4) !important;
        }

        /* Cartes Workspace */
        .zapio-card {
            background-color: #181B24 !important;
            border: 1px solid #2A2E3D !important;
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 15px;
        }

        /* Carte Style Agenda Pro */
        .agenda-card {
            background: linear-gradient(135deg, #1A1E2B 0%, #12141D 100%);
            border-left: 5px solid #FF3B30;
            border-top: 1px solid #2A2E3D;
            border-right: 1px solid #2A2E3D;
            border-bottom: 1px solid #2A2E3D;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }

        /* Badges */
        .zapio-badge {
            background-color: #2E3345;
            color: #FF3B30;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 700;
        }

        .zapio-badge-green {
            background-color: rgba(52, 199, 89, 0.15);
            color: #34C759;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)
