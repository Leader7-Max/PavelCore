import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* Background Violet Deep */
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

        /* ====================================================
           🔥 STYLES DES BOUTONS DE NAVIGATION EN PILULES 3D
           ==================================================== */

        button[kind="primary"] {
            background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 0.95rem !important;
            border: 2px solid #F472B6 !important;
            border-radius: 50px !important;
            padding: 12px 24px !important;
            box-shadow: 0 0 20px rgba(236, 72, 153, 0.7), 0 6px 15px rgba(0,0,0,0.4) !important;
            transition: all 0.3s ease !important;
        }

        button[kind="secondary"] {
            background: linear-gradient(135deg, #2D1452 0%, #1E0A3C 100%) !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 0.95rem !important;
            border: 2px solid #5B21B6 !important;
            border-radius: 50px !important;
            padding: 12px 24px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s ease !important;
        }

        button[kind="primary"] p, button[kind="secondary"] p,
        button[kind="primary"] span, button[kind="secondary"] span {
            color: #FFFFFF !important;
            font-weight: 800 !important;
            -webkit-text-fill-color: #FFFFFF !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.5) !important;
        }

        button[kind="secondary"]:hover {
            background: linear-gradient(135deg, #4C1D95 0%, #31105E 100%) !important;
            border-color: #EC4899 !important;
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 8px 22px rgba(236, 72, 153, 0.45) !important;
        }

        button[kind="primary"]:hover {
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 0 25px rgba(236, 72, 153, 0.9) !important;
        }

        div[data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(135deg, #EC4899 0%, #A855F7 100%) !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 1rem !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 14px 24px !important;
            width: 100% !important;
            box-shadow: 0 6px 20px rgba(236, 72, 153, 0.4) !important;
            transition: all 0.3s ease !important;
        }

        div[data-testid="stFormSubmitButton"] > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(236, 72, 153, 0.6) !important;
        }

        .zapio-card {
            background: linear-gradient(135deg, rgba(46, 16, 80, 0.8) 0%, rgba(27, 9, 48, 0.9) 100%) !important;
            border: 1px solid #6D28D9 !important;
            border-radius: 18px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

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
