# assets/styles.py

import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        /* Importation d'une police moderne */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Arrière-plan global avec dégradé subtil */
        .stApp {
            background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, #0d0e15 80%);
        }

        /* Cartes en Glassmorphism (Effet Verre Dépoli) */
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            transition: all 0.3s ease-in-out;
            margin-bottom: 20px;
        }

        .glass-card:hover {
            border: 1px solid rgba(0, 242, 254, 0.4);
            transform: translateY(-2px);
            box-shadow: 0 12px 40px 0 rgba(0, 242, 254, 0.15);
        }

        /* Personnalisation des champs de saisie (Inputs) */
        .stTextInput input, .stTextArea textarea, .stSelectbox > div {
            background-color: rgba(24, 26, 38, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            color: #E0E6ED !important;
            padding: 12px 16px !important;
            transition: all 0.3s ease !important;
        }

        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #00F2FE !important;
            box-shadow: 0 0 12px rgba(0, 242, 254, 0.3) !important;
        }

        /* Personnalisation de la barre latérale (Sidebar) */
        [data-testid="stSidebar"] {
            background-color: rgba(13, 14, 21, 0.9) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Boutons ultra-modernes avec effet néon */
        .stButton > button {
            background: linear-gradient(135deg, #4F46E5 0%, #00F2FE 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 28px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 242, 254, 0.2) !important;
        }

        .stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(0, 242, 254, 0.4) !important;
        }

        /* Badges & Tags */
        .badge {
            background: rgba(0, 242, 254, 0.1);
            color: #00F2FE;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            border: 1px solid rgba(0, 242, 254, 0.3);
            display: inline-block;
        }
        </style>
    """, unsafe_allow_html=True)
