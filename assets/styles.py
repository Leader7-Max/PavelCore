import streamlit as st

def inject_custom_design():
    st.markdown("""
        <style>
        .stApp {
            background-color: #0E031C !important;
            color: #F8FAFC !important;
        }
        .pavel-hero-banner {
            background: linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
            border: 1px solid rgba(236, 72, 153, 0.25);
            border-radius: 18px;
            padding: 30px 20px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        .sub-section-header {
            background: linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
            border-left: 5px solid #EC4899;
            padding: 15px 20px;
            border-radius: 0 12px 12px 0;
            margin-bottom: 25px;
            margin-top: 10px;
        }
        .pavel-card-grid {
            background: linear-gradient(135deg, #1A0B36 0%, #120524 100%);
            border: 1px solid #2B1552;
            border-radius: 14px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
            margin-bottom: 15px;
        }
        .pavel-card-grid:hover {
            transform: translateY(-4px);
            border-color: #EC4899;
            box-shadow: 0 10px 35px rgba(236, 72, 153, 0.18);
        }
        .zapio-badge {
            background: rgba(236, 72, 153, 0.1);
            color: #DB2777;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid rgba(236, 72, 153, 0.2);
        }
        .zapio-badge-green {
            background: rgba(16, 185, 129, 0.1);
            color: #059669;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }
        .zapio-card {
            background: #170A2E;
            border: 1px solid #2B1552;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.03);
        }
        .calendar-header-box {
            background: #1E0A3C;
            color: #A78BFA;
            text-align: center;
            padding: 8px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.85rem;
            border: 1px solid #2B1552;
        }
        .calendar-day-box {
            min-height: 90px;
            border-radius: 8px;
            padding: 6px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        div[data-testid="stPills"] button {
            background-color: #170A2E !important;
            border: 1px solid #2B1552 !important;
            color: #F8FAFC !important;
            border-radius: 8px !important;
            font-weight: 500;
        }
        div[data-testid="stPills"] button[aria-selected="true"] {
            background-color: #EC4899 !important;
            border-color: #EC4899 !important;
            color: #FFF !important;
        }
        </style>
    """, unsafe_allow_html=True)
