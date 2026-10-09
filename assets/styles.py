import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* Background Violet Deep (Thème Design Calendar) */
        html, body, [data-testid="stAppViewContainer"], .stApp {
            background: linear-gradient(135deg, #1A0B2E 0%, #110520 100%) !important;
            color: #F3F4F6 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        [data-testid="stHeader"] {
            background-color: transparent !important;
        }

        h1, h2, h3, h4, h5, h6, label, label p, .stMarkdown {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* Champs de Saisie Lisibles */
        div[data-baseweb="input"] input, 
        div[data-baseweb="textarea"] textarea,
        .stTextInput input, 
        .stTextArea textarea {
            color: #1A0B2E !important;
            background-color: #FFFFFF !important;
            border: 2px solid #D8B4FE !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }

        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #1A0B2E !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
        }

        div[data-baseweb="popover"] ul, div[role="listbox"] {
            background-color: #FFFFFF !important;
            color: #1A0B2E !important;
        }
        li[role="option"] {
            color: #1A0B2E !important;
            font-weight: 600 !important;
        }

        /* FIX CRITIQUE : ONGLET INACTIF ULTRA VISIBLE & LISIBLE SUR MOBILE */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px !important;
            background-color: #261245 !important;
            padding: 8px !important;
            border-radius: 16px !important;
            border: 1px solid #5B21B6 !important;
            overflow-x: auto !important;
            white-space: nowrap !important;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: #3B1578 !important;
            border-radius: 12px !important;
            padding: 10px 16px !important;
            border: 1px solid #7C3AED !important;
        }

        /* Texte BLANC Néon forcé sur TOUS les onglets */
        .stTabs [data-baseweb="tab"] p, 
        .stTabs [data-baseweb="tab"] span, 
        .stTabs [data-baseweb="tab"] div {
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 0.9rem !important;
        }

        /* Onglet Actif Violet/Rose Vif */
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
            border-color: #F472B6 !important;
            box-shadow: 0 4px 15px rgba(236, 72, 153, 0.5) !important;
        }

        /* Boutons de Formulaire 3D */
        .stButton > button, 
        div[data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(135deg, #EC4899 0%, #A855F7 100%) !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 1rem !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 14px 24px !important;
            width: 100% !important;
            box-shadow: 0 6px 20px rgba(236, 72, 153, 0.4) !important;
        }

        /* Cartes du Workspace Style Purple Glass */
        .zapio-card {
            background: linear-gradient(135deg, rgba(46, 16, 80, 0.8) 0%, rgba(27, 9, 48, 0.9) 100%) !important;
            border: 1px solid #6D28D9 !important;
            border-radius: 18px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        /* CARTE AGENDA : BLOC LISTE SOUS LE CALENDRIER */
        .calendar-event-card {
            background: linear-gradient(135deg, #2D1254 0%, #1E0A3C 100%);
            border: 1px solid #A855F7;
            border-radius: 20px;
            padding: 18px;
            margin-bottom: 16px;
            display: flex;
            gap: 16px;
            align-items: center;
            box-shadow: 0 8px 25px rgba(168, 85, 247, 0.25);
        }

        .calendar-date-box {
            background: linear-gradient(135deg, #F43F5E 0%, #EC4899 100%);
            color: #FFFFFF;
            min-width: 85px;
            height: 85px;
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            box-shadow: 0 4px 14px rgba(244, 63, 94, 0.4);
        }

        /* Badges */
        .zapio-badge {
            background-color: #4C1D95;
            color: #F472B6;
            padding: 5px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 700;
            border: 1px solid #7C3AED;
        }

        .zapio-badge-green {
            background-color: rgba(52, 199, 89, 0.15);
            color: #34C759;
            padding: 5px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)
