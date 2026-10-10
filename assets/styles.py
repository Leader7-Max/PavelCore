import streamlit as st

def inject_custom_design():
    """Injecte le design global, la charte graphique et les effets interactifs de PavelCore."""
    st.markdown("""
        <style>
            /* --- CHARTE GRAPHIQUE & BANNIÈRES --- */
            .pavel-hero-banner {
                background: linear-gradient(135deg, #1E0A3C 0%, #170A2E 100%);
                border: 1px solid #2B1552;
                padding: 30px;
                border-radius: 12px;
                margin-bottom: 25px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            
            .pavel-card-grid {
                background-color: #170A2E;
                border: 1px solid #2B1552;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }

            .zapio-badge {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%);
                color: white;
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 0.75rem;
                font-weight: 600;
            }

            .zapio-badge-green {
                background: #10B981;
                color: white;
                padding: 2px 8px;
                border-radius: 6px;
                font-size: 0.7rem;
                font-weight: 600;
            }

            /* --- EFFETS FLUIDES SUR TOUS LES BOUTONS --- */
            .stButton > button {
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                letter-spacing: 0.3px !important;
            }
            
            /* Effet au survol (Hover) : Légère élévation + Ombre lumineuse */
            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 25px rgba(236, 72, 153, 0.35) !important;
                border-color: #EC4899 !important;
            }
            
            /* Effet au clic (Active) : Sensation de pression vers le bas */
            .stButton > button:active {
                transform: translateY(1px) !important;
                box-shadow: 0 3px 10px rgba(236, 72, 153, 0.2) !important;
            }
        </style>
    """, unsafe_allow_html=True)
