import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #0B0B0E !important;
            color: #FFFFFF !important;
        }

        .stApp {
            background-color: #0B0B0E !important;
        }

        /* Masquage de la Sidebar et des flèches */
        [data-testid="stSidebarCollapseButton"], 
        [data-testid="collapsedControl"],
        [data-testid="stSidebar"] {
            display: none !important;
        }

        h1, h2, h3, h4, label p {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* CORRECTION FOND DES INPUTS ET ZONES DE TEXTE (SOMBRE ET LISIBLE) */
        div[data-baseweb="input"], 
        div[data-baseweb="textarea"], 
        div[data-baseweb="select"] > div,
        input, textarea {
            background-color: #16161E !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 12px !important;
            color: #FFFFFF !important;
        }

        div[data-baseweb="input"]:focus-within, 
        div[data-baseweb="textarea"]:focus-within {
            border-color: #FF3B30 !important;
            box-shadow: 0 0 12px rgba(255, 59, 48, 0.3) !important;
        }

        div[data-baseweb="input"] input, 
        div[data-baseweb="textarea"] textarea {
            color: #FFFFFF !important;
            font-size: 0.95rem !important;
            background-color: transparent !important;
        }

        [data-testid="InputInstructions"] {
            display: none !important;
        }

        /* Boutons Rouge Néon */
        .stButton > button {
            background: linear-gradient(135deg, #FF3B30 0%, #E02B20 100%) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 10px 20px !important;
            box-shadow: 0 6px 20px rgba(255, 59, 48, 0.35) !important;
            transition: all 0.2s ease-in-out !important;
            width: 100% !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 59, 48, 0.5) !important;
        }

        /* Navigation Horizontale Tactile */
        div[data-testid="stRadio"] > div {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        div[data-testid="stRadio"] label {
            background-color: #16161E !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 30px !important;
            padding: 8px 16px !important;
            margin: 0 !important;
            cursor: pointer !important;
        }

        div[data-testid="stRadio"] label:has(input:checked) {
            background-color: #FF3B30 !important;
            border-color: #FF3B30 !important;
            box-shadow: 0 4px 15px rgba(255, 59, 48, 0.4) !important;
        }

        div[data-testid="stRadio"] label span {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
        }

        /* Cartes & Badges */
        .zapio-card {
            background: #16161E;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
        }

        .zapio-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255, 59, 48, 0.12);
            color: #FF3B30;
            border: 1px solid rgba(255, 59, 48, 0.25);
            padding: 4px 12px;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .zapio-badge-green {
            background: rgba(48, 209, 88, 0.12);
            color: #30D158;
            border: 1px solid rgba(48, 209, 88, 0.25);
            padding: 4px 12px;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #121217;
            padding: 6px;
            border-radius: 12px;
        }

        .stTabs [aria-selected="true"] {
            background-color: #FF3B30 !important;
            color: #FFFFFF !important;
        }
        </style>
    """, unsafe_allow_html=True)
