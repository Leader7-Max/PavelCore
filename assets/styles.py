import streamlit as st

def inject_custom_design(theme="dark"):
    if theme == "light":
        # ==================== THÈME CLAIR / BLANC PUR ====================
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

            html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
                background-color: #FFFFFF !important;
                background: #FFFFFF !important;
                color: #0F172A !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
            }

            [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"], [data-testid="stSidebar"] {
                display: none !important;
            }

            h1, h2, h3, h4, label, label p {
                color: #0F172A !important;
                font-weight: 700 !important;
            }

            /* TABS CLAIR */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px !important;
                background-color: #F1F5F9 !important;
                padding: 6px !important;
                border-radius: 12px !important;
                border: 1px solid #E2E8F0 !important;
            }

            .stTabs [data-baseweb="tab"] {
                padding: 10px 18px !important;
                border-radius: 8px !important;
                background-color: transparent !important;
                border: none !important;
            }

            .stTabs [data-baseweb="tab"] p, .stTabs [data-baseweb="tab"] div, .stTabs [data-baseweb="tab"] span {
                color: #334155 !important;
                font-weight: 600 !important;
            }

            .stTabs [aria-selected="true"] {
                background-color: #FF3B30 !important;
                box-shadow: 0 4px 12px rgba(255, 59, 48, 0.25) !important;
            }

            .stTabs [aria-selected="true"] p, .stTabs [aria-selected="true"] div, .stTabs [aria-selected="true"] span {
                color: #FFFFFF !important;
                font-weight: 700 !important;
            }

            /* INPUTS CLAIR */
            div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"] > div {
                background-color: #F8FAFC !important;
                border: 1px solid #CBD5E1 !important;
                border-radius: 10px !important;
                color: #0F172A !important;
            }

            input, textarea, div[data-baseweb="select"] span {
                color: #0F172A !important;
            }

            div[data-baseweb="popover"], div[role="listbox"], ul[role="listbox"] {
                background-color: #FFFFFF !important;
                border: 1px solid #CBD5E1 !important;
            }

            li[role="option"], div[role="option"] {
                background-color: #FFFFFF !important;
                color: #0F172A !important;
            }

            li[role="option"]:hover, div[role="option"]:hover, li[aria-selected="true"] {
                background-color: #FF3B30 !important;
                color: #FFFFFF !important;
            }

            .stButton > button {
                background-color: #FF3B30 !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 10px 20px !important;
                width: 100% !important;
            }

            .zapio-card {
                background-color: #FFFFFF !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 14px;
                padding: 22px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            }
            </style>
        """, unsafe_allow_html=True)

    else:
        # ==================== THÈME SOMBRE PRO ====================
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

            html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
                background-color: #0F1117 !important;
                background: #0F1117 !important;
                color: #F0F2F6 !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
            }

            [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"], [data-testid="stSidebar"] {
                display: none !important;
            }

            h1, h2, h3, h4, label, label p {
                color: #FFFFFF !important;
                font-weight: 700 !important;
            }

            /* TABS SOMBRE (Correction visibilité) */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px !important;
                background-color: #1A1D27 !important;
                padding: 6px !important;
                border-radius: 12px !important;
                border: 1px solid #2E3345 !important;
            }

            .stTabs [data-baseweb="tab"] {
                padding: 10px 18px !important;
                border-radius: 8px !important;
                background-color: transparent !important;
                border: none !important;
            }

            .stTabs [data-baseweb="tab"] p, .stTabs [data-baseweb="tab"] div, .stTabs [data-baseweb="tab"] span {
                color: #E2E8F0 !important;
                font-weight: 600 !important;
            }

            .stTabs [aria-selected="true"] {
                background-color: #FF3B30 !important;
                box-shadow: 0 4px 12px rgba(255, 59, 48, 0.35) !important;
            }

            .stTabs [aria-selected="true"] p, .stTabs [aria-selected="true"] div, .stTabs [aria-selected="true"] span {
                color: #FFFFFF !important;
                font-weight: 700 !important;
            }

            /* INPUTS SOMBRE */
            div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"] > div {
                background-color: #1A1D27 !important;
                border: 1px solid #2E3345 !important;
                border-radius: 10px !important;
                color: #FFFFFF !important;
            }

            input, textarea, div[data-baseweb="select"] span {
                color: #FFFFFF !important;
            }

            div[data-baseweb="popover"], div[role="listbox"], ul[role="listbox"] {
                background-color: #1A1D27 !important;
                border: 1px solid #3A3F54 !important;
            }

            li[role="option"], div[role="option"] {
                background-color: #1A1D27 !important;
                color: #FFFFFF !important;
            }

            li[role="option"]:hover, div[role="option"]:hover, li[aria-selected="true"] {
                background-color: #FF3B30 !important;
                color: #FFFFFF !important;
            }

            .stButton > button {
                background-color: #FF3B30 !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 10px 20px !important;
                width: 100% !important;
            }

            .zapio-card {
                background-color: #181B24 !important;
                border: 1px solid #2A2E3D !important;
                border-radius: 14px;
                padding: 22px;
            }
            </style>
        """, unsafe_allow_html=True)
