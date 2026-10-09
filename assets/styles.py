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

        /* En-tête Streamlit */
        [data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Titres & Labels */
        h1, h2, h3, h4, h5, h6, label, label p, .stMarkdown {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* Champs de saisie texte (Input & Textarea) */
        div[data-baseweb="input"] input, 
        div[data-baseweb="textarea"] textarea,
        .stTextInput input, 
        .stTextArea textarea {
            color: #0F172A !important;
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
        }

        /* Menus déroulants (Selectbox) */
        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border-radius: 8px !important;
        }

        li[role="option"], div[role="option"] {
            color: #0F172A !important;
            background-color: #FFFFFF !important;
        }

        /* FIX BOUTONS (Soumettre / Connexion / Enregistrer) */
        .stButton > button, div[data-testid="stFormSubmitButton"] > button {
            background-color: #FF3B30 !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 20px !important;
            width: 100% !important;
            box-shadow: 0 4px 12px rgba(255, 59, 48, 0.3) !important;
        }

        /* FIX ONGLETS (Vue Calendrier & Liste, etc.) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px !important;
            background-color: #1A1D27 !important;
            padding: 6px !important;
            border-radius: 10px !important;
            border: 1px solid #2A2E3D !important;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 6px !important;
            padding: 8px 16px !important;
            background-color: transparent !important;
        }

        .stTabs [data-baseweb="tab"] p, .stTabs [data-baseweb="tab"] span {
            color: #E2E8F0 !important;
            font-weight: 600 !important;
        }

        .stTabs [aria-selected="true"] {
            background-color: #FF3B30 !important;
        }

        .stTabs [aria-selected="true"] p, .stTabs [aria-selected="true"] span {
            color: #FFFFFF !important;
            font-weight: 800 !important;
        }

        /* Cartes & Badges */
        .zapio-card {
            background-color: #181B24 !important;
            border: 1px solid #2A2E3D !important;
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 15px;
        }

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
