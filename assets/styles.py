import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        /* FORCE LE FOND GLOBAL ANTHRACITE CLAIR (FINI LE NOIR PROPRiÉTAIRE STREAMLIT) */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
            background-color: #1E202C !important;
            background: #1E202C !important;
            color: #FFFFFF !important;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Masquage complet de la Sidebar et contrôles */
        [data-testid="stSidebarCollapseButton"], 
        [data-testid="collapsedControl"],
        [data-testid="stSidebar"] {
            display: none !important;
        }

        h1, h2, h3, h4, label p, span {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* CHAMPS DE SAISIE ET ZONES DE TEXTE (FOND GRIS CLAIR BIEN VISIBLE) */
        div[data-baseweb="input"], 
        div[data-baseweb="textarea"], 
        div[data-baseweb="select"] > div,
        input, textarea, [data-baseweb="base-input"] {
            background-color: #32364A !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            color: #FFFFFF !important;
        }

        /* Effet au survol / focus des champs de texte */
        div[data-baseweb="input"]:focus-within, 
        div[data-baseweb="textarea"]:focus-within {
            border-color: #FF3B30 !important;
            background-color: #3B3F56 !important;
            box-shadow: 0 0 12px rgba(255, 59, 48, 0.4) !important;
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

        /* BOUTONS ROUGE NÉON */
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

        /* NAVIGATION HORIZONTALE TACTILE (BOUTONS / RADIOS) */
        div[data-testid="stRadio"] > div {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        div[data-testid="stRadio"] label {
            background-color: #2A2D3D !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
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

        /* CARTES ET BLOCS DE CONTENU EN RELIEF */
        .zapio-card {
            background: #2A2D3D !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 16px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
        }

        .zapio-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255, 59, 48, 0.2);
            color: #FF5247;
            border: 1px solid rgba(255, 59, 48, 0.4);
            padding: 4px 12px;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .zapio-badge-green {
            background: rgba(48, 209, 88, 0.2);
            color: #34C759;
            border: 1px solid rgba(48, 209, 88, 0.4);
            padding: 4px 12px;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        /* ONGLETS (TABS) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #2A2D3D !important;
            padding: 6px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .stTabs [aria-selected="true"] {
            background-color: #FF3B30 !important;
            color: #FFFFFF !important;
        }
        </style>
    """, unsafe_allow_html=True)
