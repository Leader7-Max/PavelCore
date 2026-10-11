import streamlit as st

def inject_custom_design():
    """Injecte le système de design Silicon Valley et assure la visibilité permanente de tous les boutons et uploaders."""
    
    st.markdown("""
        <style>
            /* =========================================================
               1. FOND DE PAGE & FONT GLOBALE
               ========================================================= */
            .stApp {
                background-color: #1A0B2E !important;
                background-image: 
                    radial-gradient(at 0% 0%, rgba(124, 58, 237, 0.15) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.15) 0px, transparent 50%) !important;
                color: #F8FAFC !important;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            }

            /* =========================================================
               2. LABELS DE FORMULAIRES ULTRA-LISIBLES
               ========================================================= */
            div[data-testid="stWidgetLabel"] label, 
            div[data-testid="stWidgetLabel"] p,
            label[data-testid="stMetricLabel"],
            .stTextInput label, .stTextArea label, .stSelectbox label, .stDateInput label {
                color: #FFFFFF !important;
                font-weight: 700 !important;
                font-size: 0.95rem !important;
                letter-spacing: 0.3px !important;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6) !important;
                margin-bottom: 6px !important;
            }

            /* =========================================================
               3. CHAMPS DE SAISIE — fond sombre + texte blanc lisible
                  (toutes les couches, quelle que soit la version de Streamlit)
               ========================================================= */
            div[data-baseweb="input"],
            div[data-baseweb="base-input"],
            div[data-baseweb="textarea"],
            div[data-baseweb="select"] > div,
            [data-testid="stTextInputRootElement"],
            [data-testid="stTextAreaRootElement"],
            [data-testid="stNumberInputContainer"],
            div[data-baseweb="input"] input,
            div[data-baseweb="base-input"] input,
            textarea,
            input[type="text"], input[type="password"], input[type="email"],
            input[type="number"], input[type="search"], input[type="date"], input[type="time"] {
                background-color: #230E3D !important;
                color: #FFFFFF !important;
                -webkit-text-fill-color: #FFFFFF !important;
            }

            /* Bordure + coins arrondis (une seule couche pour éviter le double cadre) */
            div[data-baseweb="base-input"],
            div[data-baseweb="textarea"],
            div[data-baseweb="select"] > div {
                border: 1px solid rgba(236, 72, 153, 0.4) !important;
                border-radius: 10px !important;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4) !important;
            }
            div[data-baseweb="input"] {
                border: none !important;
                border-radius: 10px !important;
                box-shadow: none !important;
            }
            [data-testid="stTextInputRootElement"],
            [data-testid="stTextAreaRootElement"] {
                border-radius: 10px !important;
            }
            /* Si Streamlit n'utilise plus BaseWeb : bordure sur le conteneur */
            [data-testid="stTextInputRootElement"]:not(:has([data-baseweb])),
            [data-testid="stTextAreaRootElement"]:not(:has([data-baseweb])) {
                border: 1px solid rgba(236, 72, 153, 0.4) !important;
            }

            /* Focus */
            div[data-baseweb="input"]:focus-within,
            div[data-baseweb="base-input"]:focus-within,
            div[data-baseweb="textarea"]:focus-within,
            div[data-baseweb="select"]:focus-within > div,
            [data-testid="stTextInputRootElement"]:focus-within,
            [data-testid="stTextAreaRootElement"]:focus-within,
            div[data-baseweb="input"]:focus-within input,
            div[data-baseweb="base-input"]:focus-within input,
            div[data-baseweb="textarea"]:focus-within textarea {
                background-color: #2A104D !important;
            }
            div[data-baseweb="base-input"]:focus-within,
            div[data-baseweb="textarea"]:focus-within,
            div[data-baseweb="select"]:focus-within > div,
            [data-testid="stTextInputRootElement"]:not(:has([data-baseweb])):focus-within,
            [data-testid="stTextAreaRootElement"]:not(:has([data-baseweb])):focus-within {
                border-color: #EC4899 !important;
                box-shadow: 0 0 12px rgba(236, 72, 153, 0.5) !important;
            }

            input, textarea {
                font-weight: 600 !important;
                caret-color: #EC4899 !important;
            }

            input::placeholder, textarea::placeholder {
                color: #94A3B8 !important;
                -webkit-text-fill-color: #94A3B8 !important;
            }

            /* Remplissage automatique du navigateur (évite le fond clair) */
            input:-webkit-autofill,
            input:-webkit-autofill:hover,
            input:-webkit-autofill:focus {
                -webkit-box-shadow: 0 0 0 1000px #230E3D inset !important;
                -webkit-text-fill-color: #FFFFFF !important;
                caret-color: #EC4899 !important;
            }

            div[data-baseweb="select"] span {
                color: #FFFFFF !important;
            }

            /* =========================================================
               4. BOUTONS NÉON VIP & CORRECTION CIBLÉE DU DOWNLOAD BUTTON
               ========================================================= */
            div[data-testid="stButton"] > button,
            div[data-testid="stFormSubmitButton"] > button {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
                font-size: 0.95rem !important;
                border-radius: 50px !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                padding: 10px 24px !important;
                box-shadow: 0 4px 18px rgba(236, 72, 153, 0.45) !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                cursor: pointer !important;
                width: 100% !important;
            }

            div[data-testid="stDownloadButton"] button,
            .stDownloadButton button {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                background-color: #EC4899 !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
                font-size: 0.95rem !important;
                border-radius: 50px !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                padding: 10px 24px !important;
                box-shadow: 0 4px 18px rgba(236, 72, 153, 0.45) !important;
                width: 100% !important;
                opacity: 1 !important;
            }

            div[data-testid="stDownloadButton"] button * {
                color: #FFFFFF !important;
            }

            div[data-testid="stButton"] > button:hover,
            div[data-testid="stFormSubmitButton"] > button:hover,
            div[data-testid="stDownloadButton"] button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 8px 28px rgba(236, 72, 153, 0.75) !important;
                border-color: #FFFFFF !important;
            }

            /* =========================================================
               5. CORRECTION RADICALE DU CONTENEUR BLANC DE L'UPLOADER
               ========================================================= */
            div[data-testid="stFileUploader"],
            section[data-testid="stFileUploaderDropzone"],
            div[data-baseweb="file-uploader"] {
                background-color: #230E3D !important;
                border: 2px dashed #EC4899 !important;
                border-radius: 12px !important;
                padding: 20px !important;
            }

            div[data-testid="stFileUploader"] * {
                color: #FFFFFF !important;
            }

            div[data-testid="stFileUploader"] small {
                color: #CBD5E1 !important;
            }

            div[data-testid="stFileUploader"] button {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
                border-radius: 8px !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                box-shadow: 0 4px 12px rgba(236, 72, 153, 0.4) !important;
            }

            /* =========================================================
               6. EXPANDERS & CARTES
               ========================================================= */
            div[data-testid="stExpander"], details {
                background: #230E3D !important;
                border: 1px solid rgba(236, 72, 153, 0.3) !important;
                border-radius: 12px !important;
            }

            div[data-testid="stExpander"] summary, details summary {
                background-color: #230E3D !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
            }

            div[data-testid="stExpanderDetails"], details > div {
                background-color: rgba(15, 5, 29, 0.6) !important;
                color: #FFFFFF !important;
            }

            .pavel-card-grid, .zapio-card {
                background: rgba(23, 10, 46, 0.75) !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                border-radius: 16px !important;
                padding: 18px !important;
            }
            
            .zapio-badge, .pavel-counter-badge {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                color: #FFFFFF !important;
                padding: 4px 12px !important;
                border-radius: 20px !important;
                font-size: 0.75rem !important;
                font-weight: 700 !important;
            }

            /* =========================================================
               7. ONGLETS — PILULES (même design que Connexion / Inscription)
                  Sélecteurs multiples : compatible toutes versions de Streamlit
               ========================================================= */
            [role="tablist"],
            div[data-baseweb="tab-list"],
            [data-testid="stTabs"] > div:first-child {
                gap: 10px !important;
                background: transparent !important;
                padding: 4px 0 16px 0 !important;
                flex-wrap: wrap !important;
                overflow: visible !important;
                border-bottom: none !important;
                box-shadow: none !important;
            }

            /* Suppression du soulignement natif (rouge/rose) */
            div[data-baseweb="tab-highlight"],
            div[data-baseweb="tab-border"],
            [data-testid="stTabHighlight"],
            [data-testid="stTabBorder"] {
                display: none !important;
                height: 0 !important;
                background: transparent !important;
            }
            button[role="tab"]::after,
            button[data-baseweb="tab"]::after,
            [data-testid="stTab"]::after {
                display: none !important;
            }

            /* Onglet inactif */
            button[role="tab"],
            button[data-baseweb="tab"],
            button[data-testid="stTab"] {
                background: #230E3D !important;
                background-image: none !important;
                border: 1px solid rgba(236, 72, 153, 0.4) !important;
                border-radius: 50px !important;
                padding: 10px 22px !important;
                height: auto !important;
                min-height: 0 !important;
                margin: 0 !important;
                box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3) !important;
                transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease !important;
                opacity: 1 !important;
            }

            button[role="tab"] p,
            button[role="tab"] div,
            button[role="tab"] span,
            button[data-baseweb="tab"] p,
            button[data-baseweb="tab"] div,
            button[data-testid="stTab"] p,
            button[data-testid="stTab"] div {
                color: #FFFFFF !important;
                font-weight: 700 !important;
                font-size: 0.9rem !important;
                margin: 0 !important;
                opacity: 1 !important;
            }

            button[role="tab"]:hover,
            button[data-baseweb="tab"]:hover,
            button[data-testid="stTab"]:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 22px rgba(236, 72, 153, 0.55) !important;
                border-color: #EC4899 !important;
            }

            /* Onglet actif : dégradé rose/violet */
            button[role="tab"][aria-selected="true"],
            button[data-baseweb="tab"][aria-selected="true"],
            button[data-testid="stTab"][aria-selected="true"] {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                border: 1px solid rgba(255, 255, 255, 0.45) !important;
                box-shadow: 0 6px 20px rgba(236, 72, 153, 0.55) !important;
            }

            div[data-baseweb="tab-panel"],
            [role="tabpanel"] {
                padding-top: 8px !important;
            }

            /* =========================================================
               8. CALENDRIER DÉROULANT (st.date_input) & LISTES DÉROULANTES
               ========================================================= */
            div[data-baseweb="popover"] > div {
                background: transparent !important;
                border-radius: 18px !important;
                box-shadow: 0 18px 50px rgba(0, 0, 0, 0.6) !important;
            }

            div[data-baseweb="calendar"] {
                background: linear-gradient(160deg, #2A104D 0%, #170A2E 100%) !important;
                border: 1px solid rgba(236, 72, 153, 0.45) !important;
                border-radius: 18px !important;
                padding: 10px !important;
                color: #FFFFFF !important;
            }

            div[data-baseweb="calendar"] * {
                color: #FFFFFF !important;
                font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif !important;
            }

            div[data-baseweb="calendar"] div[role="heading"] {
                font-weight: 800 !important;
                letter-spacing: 0.3px !important;
            }

            div[data-baseweb="calendar"] button {
                background: rgba(236, 72, 153, 0.15) !important;
                border-radius: 50% !important;
                border: 1px solid rgba(236, 72, 153, 0.35) !important;
            }

            div[data-baseweb="calendar"] [role="columnheader"],
            div[data-baseweb="calendar"] abbr {
                color: #F9A8D4 !important;
                font-weight: 700 !important;
                text-decoration: none !important;
                text-transform: uppercase !important;
                font-size: 0.72rem !important;
                letter-spacing: 0.8px !important;
            }

            div[data-baseweb="calendar"] div[role="gridcell"] > div,
            div[data-baseweb="calendar"] [aria-label^="Choose"],
            div[data-baseweb="calendar"] [aria-label^="Selected"] {
                border-radius: 50% !important;
                font-weight: 600 !important;
                transition: background 0.2s ease, transform 0.2s ease !important;
            }

            div[data-baseweb="calendar"] [aria-label^="Choose"]:hover {
                background: rgba(236, 72, 153, 0.35) !important;
                transform: scale(1.08) !important;
            }

            div[data-baseweb="calendar"] [aria-selected="true"],
            div[data-baseweb="calendar"] [aria-label^="Selected"] {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                box-shadow: 0 4px 14px rgba(236, 72, 153, 0.6) !important;
                border-radius: 50% !important;
            }

            div[data-baseweb="calendar"] [aria-disabled="true"] {
                opacity: 0.35 !important;
            }

            ul[role="listbox"], div[data-baseweb="menu"] {
                background: #230E3D !important;
                border: 1px solid rgba(236, 72, 153, 0.4) !important;
                border-radius: 12px !important;
            }

            ul[role="listbox"] li, div[data-baseweb="menu"] li {
                background: transparent !important;
                color: #FFFFFF !important;
            }

            ul[role="listbox"] li:hover, div[data-baseweb="menu"] li:hover,
            ul[role="listbox"] li[aria-selected="true"] {
                background: rgba(236, 72, 153, 0.3) !important;
            }

            /* =========================================================
               9. CALENDRIER MENSUEL PREMIUM (grille Lun → Dim)
               ========================================================= */
            .pc-cal-title {
                text-align: center;
                font-size: 1.35rem;
                font-weight: 800;
                color: #FFFFFF;
                letter-spacing: 0.4px;
                padding-top: 6px;
            }
            .pc-cal-title span { color: #EC4899; }

            .pc-cal-wrap {
                background: linear-gradient(160deg, rgba(42, 16, 77, 0.85) 0%, rgba(23, 10, 46, 0.9) 100%);
                border: 1px solid rgba(236, 72, 153, 0.35);
                border-radius: 20px;
                padding: 16px;
                margin: 12px 0 18px 0;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.45);
            }

            .pc-cal-grid {
                display: grid;
                grid-template-columns: repeat(7, minmax(0, 1fr));
                gap: 8px;
            }

            .pc-cal-dow {
                text-align: center;
                font-size: 0.72rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 1px;
                color: #F9A8D4;
                padding: 6px 0 4px 0;
            }

            .pc-cal-cell {
                min-height: 92px;
                background: #230E3D;
                border: 1px solid rgba(236, 72, 153, 0.22);
                border-radius: 14px;
                padding: 8px;
                overflow: hidden;
                transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
            }
            .pc-cal-cell:hover {
                transform: translateY(-2px);
                border-color: #EC4899;
                box-shadow: 0 8px 22px rgba(236, 72, 153, 0.35);
            }
            .pc-cal-cell.empty {
                background: transparent;
                border: 1px dashed rgba(255, 255, 255, 0.06);
                box-shadow: none;
                transform: none;
            }
            .pc-cal-cell.weekend { background: #2A104D; }

            .pc-cal-cell.today {
                border: 1px solid rgba(255, 255, 255, 0.55);
                background: linear-gradient(135deg, rgba(236, 72, 153, 0.35) 0%, rgba(139, 92, 246, 0.35) 100%);
                box-shadow: 0 0 18px rgba(236, 72, 153, 0.5);
            }

            .pc-cal-num {
                display: inline-block;
                min-width: 26px;
                height: 26px;
                line-height: 26px;
                text-align: center;
                border-radius: 50%;
                font-size: 0.85rem;
                font-weight: 800;
                color: #FFFFFF;
            }
            .pc-cal-cell.today .pc-cal-num {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%);
                box-shadow: 0 3px 10px rgba(236, 72, 153, 0.6);
            }

            .pc-cal-ev {
                display: flex;
                align-items: center;
                gap: 5px;
                margin-top: 4px;
                font-size: 0.68rem;
                font-weight: 600;
                color: #F1E8FF;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            .pc-cal-ev i {
                flex: 0 0 7px;
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%);
            }
            .pc-cal-more {
                margin-top: 4px;
                font-size: 0.65rem;
                font-weight: 700;
                color: #F9A8D4;
            }

            @media (max-width: 640px) {
                .pc-cal-wrap { padding: 8px; }
                .pc-cal-grid { gap: 4px; }
                .pc-cal-cell { min-height: 54px; padding: 4px; border-radius: 10px; }
                .pc-cal-ev { display: none; }
                .pc-cal-cell.has-ev::after {
                    content: "";
                    display: block;
                    width: 7px; height: 7px;
                    margin: 4px auto 0 auto;
                    border-radius: 50%;
                    background: #EC4899;
                }
                .pc-cal-more { display: none; }
                .pc-cal-dow { font-size: 0.6rem; letter-spacing: 0; }
            }
        </style>
    """, unsafe_allow_html=True)
