import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* 1. FOND DE PAGE BLANC PUR */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            color: #0F172A !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        /* Masquage Sidebar */
        [data-testid="stSidebarCollapseButton"], 
        [data-testid="collapsedControl"],
        [data-testid="stSidebar"] {
            display: none !important;
        }

        /* Titres et labels en Noir Anthracite très foncé */
        h1, h2, h3, h4, label, label p {
            color: #0F172A !important;
            font-weight: 700 !important;
        }

        /* 2. ONGLET / TABS (AJOUTER UN ÉVÉNEMENT / VUE CALENDRIER) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px !important;
            background-color: #F1F5F9 !important;
            padding: 6px !important;
            border-radius: 12px !important;
            border: 1px solid #E2E8F0 !important;
        }

        /* Onglet Inactif (Bien visible avec texte sombre) */
        .stTabs [data-baseweb="tab"] {
            height: auto !important;
            padding: 10px 18px !important;
            border-radius: 8px !important;
            background-color: transparent !important;
            border: none !important;
            transition: all 0.2s ease !important;
        }

        .stTabs [data-baseweb="tab"] p, 
        .stTabs [data-baseweb="tab"] div,
        .stTabs [data-baseweb="tab"] span {
            color: #334155 !important; /* Gris foncé très lisible */
            font-weight: 600 !important;
            font-size: 0.9rem !important;
        }

        /* Survol onglet inactif */
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #E2E8F0 !important;
        }

        /* Onglet Sélectionné / Actif (Rouge) */
        .stTabs [aria-selected="true"] {
            background-color: #FF3B30 !important;
            box-shadow: 0 4px 12px rgba(255, 59, 48, 0.25) !important;
        }

        .stTabs [aria-selected="true"] p, 
        .stTabs [aria-selected="true"] div,
        .stTabs [aria-selected="true"] span {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        .stTabs [data-baseweb="tab-highlight-title"] {
            display: none !important;
        }

        /* 3. CHAMPS DE SAISIE (INPUTS & TEXTAREAS BLANCS) */
        div[data-baseweb="input"], 
        div[data-baseweb="textarea"] {
            background-color: #F8FAFC !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 10px !important;
        }

        input, textarea {
            color: #0F172A !important;
            font-size: 0.95rem !important;
            background-color: transparent !important;
        }

        input::placeholder, textarea::placeholder {
            color: #64748B !important;
        }

        /* Focus sur champ actif */
        div[data-baseweb="input"]:focus-within, 
        div[data-baseweb="textarea"]:focus-within {
            border-color: #FF3B30 !important;
            background-color: #FFFFFF !important;
            box-shadow: 0 0 0 3px rgba(255, 59, 48, 0.15) !important;
        }

        /* 4. MENUS DÉROULANTS (SELECTBOX & LISTES) */
        div[data-baseweb="select"] > div {
            background-color: #F8FAFC !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 10px !important;
            color: #0F172A !important;
        }

        div[data-baseweb="popover"], 
        div[role="listbox"], 
        ul[role="listbox"] {
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 10px !important;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1) !important;
        }

        li[role="option"], 
        div[role="option"] {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
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
            color: #0F172A !important;
        }

        [data-testid="InputInstructions"] {
            display: none !important;
        }

        /* 5. BOUTONS ROUGE ACTION */
        .stButton > button {
            background-color: #FF3B30 !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 14px rgba(255, 59, 48, 0.25) !important;
            width: 100% !important;
        }

        .stButton > button:hover {
            background-color: #E03228 !important;
            box-shadow: 0 6px 18px rgba(255, 59, 48, 0.35) !important;
        }

        /* 6. NAVIGATION HORIZONTALE (RADIO BUTTONS) */
        div[data-testid="stRadio"] > div {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        div[data-testid="stRadio"] label {
            background-color: #F1F5F9 !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 20px !important;
            padding: 8px 16px !important;
            cursor: pointer !important;
        }

        div[data-testid="stRadio"] label:has(input:checked) {
            background-color: #FF3B30 !important;
            border-color: #FF3B30 !important;
        }

        div[data-testid="stRadio"] label span {
            color: #334155 !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
        }

        div[data-testid="stRadio"] label:has(input:checked) span {
            color: #FFFFFF !important;
        }

        /* 7. CARTES ET ENCADRÉS EN BLANC RELIEF */
        .zapio-card {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        .zapio-badge {
            display: inline-flex;
            align-items: center;
            background: #FEF2F2;
            color: #DC2626;
            border: 1px solid #FECACA;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .zapio-badge-green {
            display: inline-flex;
            align-items: center;
            background: #F0FDF4;
            color: #16A34A;
            border: 1px solid #BBF7D0;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)
