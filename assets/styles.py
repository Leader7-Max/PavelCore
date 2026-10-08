import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        /* Importation de la police moderne */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Arrière-plan global avec dégradé subtil */
        .stApp {
            background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, #0d0e15 80%);
        }

        /* ---------------------------------------------------- */
        /* CORRECTIFS DES CHAMPS DE SAISIE (INPUTS & MOBILES)   */
        /* ---------------------------------------------------- */

        /* 1. Masquer les instructions automatiques Streamlit ('Press Enter to submit') */
        [data-testid="InputInstructions"] {
            display: none !important;
        }

        /* 2. Conteneur principal du champ (Bordure, fond et alignement) */
        div[data-baseweb="input"] {
            background-color: rgba(24, 26, 38, 0.9) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 12px !important;
            padding-right: 10px !important;
            transition: all 0.3s ease !important;
        }

        /* Effet au survol et au focus */
        div[data-baseweb="input"]:focus-within {
            border-color: #00F2FE !important;
            box-shadow: 0 0 12px rgba(0, 242, 254, 0.25) !important;
        }

        /* 3. Texte saisi à l'intérieur du champ */
        div[data-baseweb="input"] input {
            background-color: transparent !important;
            border: none !important;
            color: #E0E6ED !important;
            padding: 12px 14px !important;
            font-size: 0.95rem !important;
        }

        /* Couleur du placeholder (texte indicatif quand c'est vide) */
        div[data-baseweb="input"] input::placeholder {
            color: #64748B !important;
            opacity: 0.7 !important;
        }

        /* 4. Bouton de l'œil (Afficher/Masquer le texte) */
        div[data-baseweb="input"] button {
            background: transparent !important;
            border: none !important;
            color: #8E9BAE !important;
            padding: 0 8px !important;
            margin: 0 !important;
        }

        div[data-baseweb="input"] button:hover {
            color: #00F2FE !important;
            background: transparent !important;
        }

        /* Correctif pour les zones de texte (Textarea) */
        .stTextArea textarea {
            background-color: rgba(24, 26, 38, 0.9) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 12px !important;
            color: #E0E6ED !important;
            padding: 12px 14px !important;
        }

        .stTextArea textarea:focus {
            border-color: #00F2FE !important;
            box-shadow: 0 0 12px rgba(0, 242, 254, 0.25) !important;
        }

        /* ---------------------------------------------------- */
        /* UI GLASSMORPHISM & BOUTONS ULTRA-PREMIUM             */
        /* ---------------------------------------------------- */

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

        /* Boutons avec dégradé Néon */
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

        /* Personnalisation de la barre latérale (Sidebar) */
        [data-testid="stSidebar"] {
            background-color: rgba(13, 14, 21, 0.95) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
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
