import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

        /* 1. FOND DE PAGE PRO */
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

        /* Titres et labels */
        h1, h2, h3, h4, label, label p {
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }

        /* 2. CORRECTION CRITIQUE : ONGLET / TABS (VOIR CALENDRIER & LISTE) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px !important;
            background-color: #1A1D27 !important;
            padding: 6px !important;
            border-radius: 12px !important;
            border: 1px solid #2E3345 !important;
        }

        /* Onglet individuel (Inactif par défaut) : Texte BLANC / GRIS CLAIR BIEN VISIBLE */
        .stTabs [data-baseweb="tab"] {
            height: auto !important;
            padding: 10px 18px !important;
            border-radius: 8px !important;
            background-color: transparent !important;
            border: none !important;
            transition: all 0.2s ease !important;
        }

        /* Style du texte à l'intérieur de l'onglet INACTIF */
        .stTabs [data-baseweb="tab"] p, 
        .stTabs [data-baseweb="tab"] div,
        .stTabs [data-baseweb="tab"] span {
            color: #E2E8F0 !important; /* Blanc cassé / Gris très clair */
            font-weight: 600 !important;
            font-size: 0.9rem !important;
        }

        /* Survol de l'onglet inactif */
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #2E3345 !important;
        }

        .stTabs [data-baseweb="tab"]:hover p,
        .stTabs [data-baseweb="tab"]:hover div,
        .stTabs [data-baseweb="tab"]:hover span {
            color: #FFFFFF !important;
        }

        /* Onglet SÉLECTIONNÉ / ACTIF (Rouge Néon) */
        .stTabs [aria-selected="true"] {
            background-color: #FF3B30 !important;
            box-shadow: 0 4px 12px rgba(255, 59, 48, 0.35) !important;
        }

        .stTabs [aria-selected="true"] p, 
        .stTabs [aria-selected="true"] div,
        .stTabs [aria-selected="true"] span {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* Supprimer la barre rouge inférieure par défaut de Streamlit sous les tabs */
        .stTabs [data-baseweb="tab-highlight-title"] {
            display: none !important;
        }

        /* 3. CHAMPS DE SAISIE (INPUTS & TEXTAREAS) */
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

        div[data-baseweb="input"]:focus-within, 
        div[data-baseweb="textarea"]:focus-within {
            border-color: #FF3B30 !important;
            box-shadow: 0 0 0 2px rgba(255, 59, 48, 0.2) !important;
        }

        /* 4. MENUS DÉROULANTS (SELECTBOX & LISTES) */
        div[data-baseweb="select"] > div {
            background-color: #1A1D27 !important;
            border: 1px solid #2E3345 !important;
            border-radius: 10px !important;
            color: #FFFFFF !important;
        }

        div[data-baseweb="popover"], 
        div[role="listbox"], 
        ul[role="listbox"] {
            background-color: #1A1D27 !important;
            border: 1px solid #3A3F54 !important;
            border-radius: 10px !important;
        }

        li[role="option"], 
        div[role="option"] {
            background-color: #1A1D27 !important;
            color: #FFFFFF !important;
            font-size: 0.95rem !important;
            padding: 10px 14px !important;
        }

        li[role="option"]:hover, 
        div[role="option"]:hover,
        li[aria-selected="true"] {
            background-color: #FF3B30 !important;
            color: #FFFFFF !important;
        }

        div[data-baseweb="select"] span {
            color: #FFFFFF !important;
        }

        [data-testid="InputInstructions"] {
            display: none !important;
        }

        /* 5. BOUTONS ACTION ROUGE */
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

        /* 6. NAVIGATION HORIZONTALE (RADIO BUTTONS) */
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

        /* 7. CARTES ET ENCADRÉS */
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
        </style>
    """, unsafe_allow_html=True)
