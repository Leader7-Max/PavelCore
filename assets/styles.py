import streamlit as st

def inject_custom_design():
    """Injecte le Design System 'Ultra-Premium' de PavelCore (inspiration Linear / Vercel)."""
    st.markdown("""
        <style>
            /* --- DESIGN TOKENS & VARIABLES --- */
            :root {
                --bg-obsidian: #090612;
                --card-surface: rgba(23, 10, 46, 0.75);
                --card-border: rgba(139, 92, 246, 0.2);
                --card-border-hover: rgba(236, 72, 153, 0.5);
                --accent-gradient: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%);
                --shadow-elevation: 0 12px 40px -10px rgba(0, 0, 0, 0.5);
                --shadow-glow: 0 0 25px rgba(236, 72, 153, 0.25);
            }

            /* --- FOND GLOBAL --- */
            .stApp {
                background-color: var(--bg-obsidian);
            }

            /* --- HERO BANNER & COMPOSANTS (Glassmorphism) --- */
            .pavel-hero-banner {
                background: linear-gradient(135deg, rgba(30, 10, 60, 0.85) 0%, rgba(23, 10, 46, 0.95) 100%);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid var(--card-border);
                padding: 35px;
                border-radius: 16px;
                margin-bottom: 25px;
                box-shadow: var(--shadow-elevation), var(--shadow-glow);
            }
            
            .pavel-card-grid {
                background-color: var(--card-surface);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid var(--card-border);
                padding: 24px;
                border-radius: 14px;
                box-shadow: var(--shadow-elevation);
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            }

            .pavel-card-grid:hover {
                border-color: var(--card-border-hover);
                transform: translateY(-3px);
                box-shadow: var(--shadow-elevation), 0 0 30px rgba(139, 92, 246, 0.25);
            }

            /* --- BADGES HAUT DE GAMME --- */
            .zapio-badge {
                background: var(--accent-gradient);
                color: white;
                padding: 5px 12px;
                border-radius: 8px;
                font-size: 0.75rem;
                font-weight: 600;
                letter-spacing: 0.5px;
                box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3);
            }

            .zapio-badge-green {
                background: linear-gradient(135deg, #059669 0%, #10B981 100%);
                color: white;
                padding: 3px 10px;
                border-radius: 8px;
                font-size: 0.7rem;
                font-weight: 600;
                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
            }

            /* --- BOUTONS : MICRO-INTERACTIONS & PHYSIQUE DE RESSORT --- */
            .stButton > button {
                background: var(--card-surface) !important;
                border: 1px solid var(--card-border) !important;
                color: #F8FAFC !important;
                transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
                border-radius: 10px !important;
                font-weight: 600 !important;
                letter-spacing: 0.4px !important;
                padding: 0.5rem 1rem !important;
            }
            
            /* Effet au survol (Hover) : lévitation + lueur néon */
            .stButton > button:hover {
                background: linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%) !important;
                border-color: #EC4899 !important;
                transform: translateY(-2px) scale(1.01) !important;
                box-shadow: 0 10px 30px rgba(236, 72, 153, 0.4), 0 0 20px rgba(139, 92, 246, 0.3) !important;
            }
            
            /* Effet au clic (Active) : effet de pression mécanique */
            .stButton > button:active {
                transform: translateY(1px) scale(0.99) !important;
                box-shadow: 0 4px 15px rgba(236, 72, 153, 0.2) !important;
            }

            /* --- CHAMPS DE SAISIE (INPUTS / FORMS) --- */
            .stTextInput input, .stPasswordInput input, .stTextArea textarea {
                background-color: rgba(15, 6, 28, 0.9) !important;
                border: 1px solid var(--card-border) !important;
                border-radius: 10px !important;
                color: #FFF !important;
                transition: all 0.3s ease !important;
            }

            .stTextInput input:focus, .stPasswordInput input:focus, .stTextArea textarea:focus {
                border-color: #EC4899 !important;
                box-shadow: 0 0 20px rgba(236, 72, 153, 0.3) !important;
            }
        </style>
    """, unsafe_allow_html=True)
