import streamlit as st

def inject_custom_design():
    """Gère les couleurs dynamiques et injecte le design CSS global de PavelCore."""
    
    theme_mode = st.session_state.get("theme_mode", "Sombre Nuit")

    if theme_mode == "Blanc Épuré":
        bg_app = "#F8FAFC"
        text_color = "#0F172A"
        card_bg = "#FFFFFF"
        card_border = "#E2E8F0"
        card_gradient = "linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%)"
        header_box_bg = "#F1F5F9"
        header_box_text = "#475569"
        desc_color = "#475569"
        sub_title_color = "#0F172A"
        hero_bg = "linear-gradient(135deg, rgba(236, 72, 153, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%)"
    else:
        bg_app = "#0E031C"
        text_color = "#F8FAFC"
        card_bg = "#170A2E"
        card_border = "#2B1552"
        card_gradient = "linear-gradient(135deg, #1A0B36 0%, #120524 100%)"
        header_box_bg = "#1E0A3C"
        header_box_text = "#A78BFA"
        desc_color = "#CBD5E1"
        sub_title_color = "#FFF"
        hero_bg = "linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%)"

    st.markdown(f"""
        <style>
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(8px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .stApp {{
            background-color: {bg_app} !important;
            color: {text_color} !important;
            animation: fadeIn 0.4s ease-in-out;
        }}
        .pavel-hero-banner {{
            background: {hero_bg};
            border: 1px solid rgba(236, 72, 153, 0.25);
            border-radius: 18px;
            padding: 30px 20px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        }}
        .sub-section-header {{
            background: {hero_bg};
            border-left: 5px solid #EC4899;
            padding: 15px 20px;
            border-radius: 0 12px 12px 0;
            margin-bottom: 25px;
            margin-top: 10px;
        }}
        .pavel-card-grid {{
            background: {card_gradient};
            border: 1px solid {card_border};
            border-radius: 14px;
            padding: 25px;
            text-align: center;
            margin-bottom: 15px;
        }}
        .zapio-badge {{
            background: rgba(236, 72, 153, 0.1);
            color: #DB2777;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid rgba(236, 72, 153, 0.2);
        }}
        .zapio-badge-green {{
            background: rgba(16, 185, 129, 0.1);
            color: #059669;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }}
        .zapio-card {{
            background: {card_bg};
            border: 1px solid {card_border};
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        }}

        /* --- STYLING DES BOUTONS EN ROUGE --- */
        div.stButton > button, 
        button[kind="primary"], 
        button[kind="secondary"],
        button {{
            background-color: #EF4444 !important;
            background: #EF4444 !important;
            color: #FFFFFF !important;
            border: 1px solid #DC2626 !important;
            font-weight: 700 !important;
            border-radius: 8px !important;
        }}
        
        div.stButton > button:hover, 
        button[kind="primary"]:hover, 
        button[kind="secondary"]:hover,
        button:hover {{
            background-color: #DC2626 !important;
            background: #DC2626 !important;
            color: #FFFFFF !important;
            border-color: #B91C1C !important;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4) !important;
        }}
        
        div.stButton > button p, button p, span {{
            color: #FFFFFF !important;
        }}

        /* --- FORÇAGE DU TEXTE EN NOIR FONCÉ POUR TOUS LES CHAMPS DE SAISIE ET TEXT AREAS --- */
        input, textarea, div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {{
            color: #0F172A !important;
            font-weight: 700 !important;
            opacity: 1 !important;
            -webkit-text-fill-color: #0F172A !important;
        }}

        div[data-baseweb="select"] span, div[data-baseweb="select"] div {{
            color: #0F172A !important;
            font-weight: 700 !important;
            -webkit-text-fill-color: #0F172A !important;
        }}

        div[data-testid="stPills"] button {{
            background-color: {card_bg} !important;
            border: 1px solid {card_border} !important;
            color: {text_color} !important;
            border-radius: 8px !important;
            font-weight: 500;
        }}
        div[data-testid="stPills"] button[aria-selected="true"] {{
            background-color: #EC4899 !important;
            border-color: #EC4899 !important;
            color: #FFF !important;
        }}
        </style>
    """, unsafe_allow_html=True)
