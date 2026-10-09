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

        /* En-tête Streamlit visible */
        [data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Correctif Titres et Labels */
        h1, h2, h3, h4, h5, h6, label, label p, .stMarkdown {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* FIX CRITIQUE : Champs de saisie (Inputs & Textarea) */
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

        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border-radius: 8px !important;
        }

        /* Cartes Workspace */
        .zapio-card {
            background-color: #181B24 !important;
            border: 1px solid #2A2E3D !important;
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 15px;
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

        /* Buttons */
        .stButton > button {
            background-color: #FF3B30 !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            width: 100% !important;
        }
        </style>
    """, unsafe_allow_html=True)
