import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        /* 1. FOND GLOBAL : GRIS SLATE / ANTHRACITE CLAIR */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
            background-color: #2A2E3D !important;
            background: #2A2E3D !important;
            color: #FFFFFF !important;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Masquage de la Sidebar */
        [data-testid="stSidebarCollapseButton"], 
        [data-testid="collapsedControl"],
        [data-testid="stSidebar"] {
            display: none !important;
        }

        h1, h2, h3, h4, label, label p, span {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* 2. CHAMPS DE SAISIE & INPUTS (FOND CLAIR LISIBLE #3F4457) */
        div[data-baseweb="input"], 
        div[data-baseweb="textarea"], 
        div[data-baseweb="select"] > div,
        input, textarea, select {
            background-color: #3F4457 !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 10px !important;
            color: #FFFFFF !important;
        }

        /* Placeholder / Texte indicatif bien lisible */
        input::placeholder, textarea::placeholder {
            color: #B0B7C6 !important;
            opacity: 1 !important;
        }

        /* Focus sur champ actif */
        div[data-baseweb="input"]:focus-within, 
        div[data-baseweb="textarea"]:focus-within {
            border-color: #FF3B30 !important;
            background-color: #484E63 !important;
            box-shadow: 0 0 10px rgba(255, 59, 48, 0.4) !important;
        }

        div[data-baseweb="input"] input, 
        div[data-baseweb="textarea"] textarea {
            color: #FFFFFF !important;
            font-size: 0.95rem !important;
            background-color: transparent !important;
        }

        /* Harmonisation spécifique des Pickers Date & Heure */
        div[data-baseweb="calendar"], 
        div[role="listbox"] {
            background-color: #3F4457 !important;
            color: #FFFFFF !important;
        }

        [data-testid="InputInstructions"] {
            display: none !important;
        }

        /* 3. BOUTONS ROUGE NÉON ACCENTUÉS */
        .stButton > button {
            background: linear-gradient(135deg, #FF3B30 0%, #D7261C 100%) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            box-shadow: 0 4px 15px rgba(255, 59, 48, 0.4) !important;
            transition: all 0.2s ease-in-out !important;
            width: 100% !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 59, 48, 0.6) !important;
        }

        /* 4. NAVIGATION HORIZONTALE (BOUTONS RADIO) */
        div[data-testid="stRadio"] > div {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        div[data-testid="stRadio"] label {
            background-color: #3F4457 !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 25px !important;
            padding: 8px 16px !important;
            margin: 0 !important;
            cursor: pointer !important;
        }

        div[data-testid="stRadio"] label:has(input:checked) {
            background-color: #FF3B30 !important;
            border-color: #FF3B30 !important;
            box-shadow: 0 4px 12px rgba(255, 59, 48, 0.4) !important;
        }

        div[data-testid="stRadio"] label span {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
        }

        /* 5. CARTES ET ENCADRÉS */
        .zapio-card {
            background: #353A4B !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }

        .zapio-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255, 59, 48, 0.25);
            color: #FF6B63;
            border: 1px solid rgba(255, 59, 48, 0.4);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .zapio-badge-green {
            background: rgba(48, 209, 88, 0.25);
            color: #34C759;
            border: 1px solid rgba(48, 209, 88, 0.4);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        /* ONGLET (TABS) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #353A4B !important;
            padding: 6px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .stTabs [aria-selected="true"] {
            background-color: #FF3B30 !important;
            color: #FFFFFF !important;
        }
        </style>
    """, unsafe_allow_html=True)
