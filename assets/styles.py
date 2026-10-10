import streamlit as st

def inject_custom_design():
    """Gère les couleurs dynamiques et injecte le design CSS global de PavelCore."""
    
    # Récupération du mode de thème depuis la session
    theme_mode = st.session_state.get("theme_mode", "Sombre Nuit")

    # Couleurs dynamiques
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

    # Styles CSS globaux avec effets d'animation et de survol
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
            transition: all 0.3s ease-in-out;
        }}
        .pavel-hero-banner:hover {{
            box-shadow: 0 12px 35px rgba(236, 72, 153, 0.25);
        }}
        .sub-section-header {{
            background: {hero_bg};
            border-left: 5px solid #EC4899;
            padding: 15px 20px;
            border-radius: 0 12px 12px 0;
            margin-bottom: 25px;
            margin-top: 10px;
            animation: fadeIn 0.3s ease-in-out;
        }}
        .pavel-card-grid {{
            background: {card_gradient};
            border: 1px solid {card_border};
            border-radius: 14px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
            margin-bottom: 15px;
        }}
        .pavel-card-grid:hover {{
            transform: translateY(-6px) scale(1.01);
            border-color: #EC4899;
            box-shadow: 0 12px 35px rgba(236, 72, 153, 0.25);
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
            box-shadow: 0 2px 12px rgba(0,0,0,0.03);
            transition: all 0.25s ease-in-out;
        }}
        .zapio-card:hover {{
            border-color: #8B5CF6;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(139, 92, 246, 0.15);
        }}
        div[data-testid="stPills"] button {{
            background-color: {card_bg} !important;
            border: 1px solid {card_border} !important;
            color: {text_color} !important;
            border-radius: 8px !important;
            font-weight: 500;
            transition: all 0.2s ease-in-out !important;
        }}
        div[data-testid="stPills"] button:hover {{
            border-color: #EC4899 !important;
            transform: translateY(-1px);
        }}
        div[data-testid="stPills"] button[aria-selected="true"] {{
            background-color: #EC4899 !important;
            border-color: #EC4899 !important;
            color: #FFF !important;
            box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3);
        }}
        </style>
    """, unsafe_allow_html=True)
