import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        /* Importation de la police moderne */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Arrière-plan global */
        .stApp {
            background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, #0d0e15 80%);
        }

        /* ---------------------------------------------------- */
        /* CORRECTION LISIBILITÉ TITRES & INPUTS AUTHENTIFICATION */
        /* ---------------------------------------------------- */

        /* 1. Titre 'Authentification' et libellés clairs */
        .stForm h3, .stMarkdown h3, label[data-testid="stWidgetLabel"] p {
            color: #E0E6ED !important;
            font-weight: 600 !important;
        }

        /* 2. Conteneur principal des champs (Fond sombre et bordure néon) */
        div[data-baseweb="input"] {
            background-color: #181A26 !important; /* Fond sombre au lieu du blanc */
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            padding-right: 8px !important;
        }

        div[data-baseweb="input"]:focus-within {
            border-color: #00F2FE !important;
            box-shadow: 0 0 12px rgba(0, 242, 254, 0.3) !important;
        }

        /* 3. Texte/Masque saisi (points/étoiles en clair très lisible) */
        div[data-baseweb="input"] input {
            background-color: transparent !important;
            color: #00F2FE !important; /* Points/Étoiles en Cyan clair */
            font-size: 1.1rem !important;
            padding: 12px !important;
        }

        /* Placeholder (Texte d'indication quand vide) */
        div[data-baseweb="input"] input::placeholder {
            color: #64748B !important;
        }

        /* 4. Bouton Œil (Afficher/Masquer) */
        div[data-baseweb="input"] button {
            background-color: transparent !important;
            border: none !important;
            color: #8E9BAE !important;
        }

        div[data-baseweb="input"] button:hover {
            color: #00F2FE !important;
        }

        /* 5. Masquer les instructions inutiles Streamlit */
        [data-testid="InputInstructions"] {
            display: none !important;
        }

        /* ---------------------------------------------------- */
        /* CARTES EN VERRE & BOUTONS                            */
        /* ---------------------------------------------------- */

        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            margin-bottom: 20px;
        }

        .stButton > button {
            background: linear-gradient(135deg, #4F46E5 0%, #00F2FE 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 28px !important;
            box-shadow: 0 4px 15px rgba(0, 242, 254, 0.2) !important;
        }
        </style>
    """, unsafe_allow_html=True)
