import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Arrière-plan global */
        .stApp {
            background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, #0d0e15 80%);
        }

        /* Correctif de la Sidebar (Mode Sombre) */
        [data-testid="stSidebar"] {
            background-color: #0D0E15 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        [data-testid="stSidebar"] * {
            color: #E0E6ED !important;
        }

        /* Titres et labels de formulaires */
        .stForm h3, .stMarkdown h3, label[data-testid="stWidgetLabel"] p {
            color: #E0E6ED !important;
            font-weight: 600 !important;
        }

        /* Correctif des Champs de saisie (Inputs) */
        div[data-baseweb="input"] {
            background-color: #181A26 !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            padding-right: 8px !important;
        }

        div[data-baseweb="input"]:focus-within {
            border-color: #00F2FE !important;
            box-shadow: 0 0 12px rgba(0, 242, 254, 0.3) !important;
        }

        div[data-baseweb="input"] input {
            background-color: transparent !important;
            color: #00F2FE !important;
            font-size: 1.05rem !important;
            padding: 12px !important;
        }

        div[data-baseweb="input"] input::placeholder {
            color: #64748B !important;
        }

        div[data-baseweb="input"] button {
            background-color: transparent !important;
            border: none !important;
            color: #8E9BAE !important;
        }

        div[data-baseweb="input"] button:hover {
            color: #00F2FE !important;
        }

        /* Textarea */
        .stTextArea textarea {
            background-color: #181A26 !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            color: #E0E6ED !important;
        }

        /* Masquer le texte "Press Enter to submit" */
        [data-testid="InputInstructions"] {
            display: none !important;
        }

        /* Cartes Glassmorphism */
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            margin-bottom: 20px;
        }

        /* Boutons Néon */
        .stButton > button {
            background: linear-gradient(135deg, #4F46E5 0%, #00F2FE 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 28px !important;
            box-shadow: 0 4px 15px rgba(0, 242, 254, 0.2) !important;
        }

        /* Badges */
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
