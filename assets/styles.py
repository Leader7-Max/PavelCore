import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

        /* 1. FOND DE PAGE PRO (Anthracite très sombre, zéro reflet parasite) */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
            background-color: #0F1117 !important;
            color: #F0F2F6 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        /* Masquage Sidebar */
        [data-testid="stSidebarCollapseButton"], 
        [data-testid="collapsedControl"],
        [data-testid="stSidebar"] {
            display: none !important;
        }

        /* Titres et labels bien lisibles */
        h1, h2, h3, h4, label, label p {
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }

        /* 2. CHAMPS DE SAISIE (Inputs & Textareas) */
        div[data-baseweb="input"], 
        div[data-baseweb="textarea"] {
            background-color: #1A1D27 !important;
            border: 1px solid #2E3345 !important;
            border-radius: 10px !important;
        }

        input, textarea {
            color: #FFFFFF !important;
            font-size: 0.95rem !important;
            background-color: transparent !important;
        }

        input::placeholder, textarea::placeholder {
            color: #8C94A8 !important;
        }

        /* Focus sur champ actif */
        div[data-baseweb="input"]:focus-within, 
        div[data-baseweb="textarea"]:focus-within {
            border-color: #FF3B30 !important;
            box-shadow: 0 0 0 2px rgba(255, 59, 48, 0.2) !important;
        }

        /* 3. MENUS DÉROULANTS (SELECTBOX & LISTES) — CORRECTION TOTALE */
        div[data-baseweb="select"] > div {
            background-color: #1A1D27 !important;
            border: 1px solid #2E3345 !important;
            border-radius: 10px !important;
            color: #FFFFFF !important;
        }

        /* Conteneur de la liste déroulante (Pop-over) */
        div[data-baseweb="popover"], 
        div[role="listbox"], 
        ul[role="listbox"] {
            background-color: #1A1D27 !important;
            border: 1px solid #3A3F54 !important;
            border-radius: 10px !important;
        }

        /* Éléments individuels de la liste */
        li[role="option"], 
        div[role="option"] {
            background-color: #1A1D27 !important;
            color: #FFFFFF !important;
            font-size: 0.95rem !important;
            padding: 10px 14px !important;
        }

        /* Élément survolé ou sélectionné dans la liste */
        li[role="option"]:hover, 
        div[role="option"]:hover,
        li[aria-selected="true"] {
            background-color: #FF3B30 !important;
            color: #FFFFFF !important;
        }

        /* Texte du composant Select */
        div[data-baseweb="select"] span {
            color: #FFFFFF !important;
        }

        [data-testid="InputInstructions"] {
            display: none !important;
        }

        /* 4. BOUTONS ACTION ROUGE PRO */
        .stButton > button {
            background-color: #FF3B30 !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
        }

        .stButton > button:hover {
            background-color: #E03228 !important;
            box-shadow: 0 4px 12px rgba(255, 59, 48, 0.3) !important;
        }

        /* 5. NAVIGATION HORIZONTALE (RADIO BUTTONS) */
        div[data-testid="stRadio"] > div {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        div[data-testid="stRadio"] label {
            background-color: #1A1D27 !important;
            border: 1px solid #2E3345 !important;
            border-radius: 20px !important;
            padding: 8px 16px !important;
            cursor: pointer !important;
        }

        div[data-testid="stRadio"] label:has(input:checked) {
            background-color: #FF3B30 !important;
            border-color: #FF3B30 !important;
        }

        div[data-testid="stRadio"] label span {
            color: #FFFFFF !important;
            font-weight: 500 !important;
            font-size: 0.85rem !important;
        }

        /* 6. CARTES ET ENCADRÉS */
        .zapio-card {
            background-color: #181B24 !important;
            border: 1px solid #2A2E3D !important;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
        }

        .zapio-badge {
            display: inline-flex;
            align-items: center;
            background: rgba(255, 59, 48, 0.15);
            color: #FF5247;
            border: 1px solid rgba(255, 59, 48, 0.3);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .zapio-badge-green {
            display: inline-flex;
            align-items: center;
            background: rgba(48, 209, 88, 0.15);
            color: #30D158;
            border: 1px solid rgba(48, 209, 88, 0.3);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        /* ONGLETS (TABS) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background-color: #1A1D27 !important;
            padding: 4px;
            border-radius: 10px;
            border: 1px solid #2E3345;
        }

        .stTabs [aria-selected="true"] {
            background-color: #FF3B30 !important;
            color: #FFFFFF !important;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)
