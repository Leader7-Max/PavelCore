import streamlit as st
from modules.database import load_events_from_db

def init_session_state():
    """Initialise l'état global et charge les données de l'application PavelCore."""
    
    # Gestion du thème visuel
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "Sombre Nuit"

    # Navigation par onglets ou vues principales
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Dashboard"

    # Chargement automatique des événements de l'agenda depuis la base de données SQLite
    if "agenda_events" not in st.session_state:
        st.session_state.agenda_events = load_events_from_db()
        
    # Onglet actif de l'agenda (vue calendrier, liste ou ajout)
    if "agenda_active_tab" not in st.session_state:
        st.session_state.agenda_active_tab = "vue"

    # Confirmation de suppression dans l'agenda
    if "confirm_delete_agenda_idx" not in st.session_state:
        st.session_state.confirm_delete_agenda_idx = None
        
    # Navigation directe si activée
    if "direct_agenda" not in st.session_state:
        st.session_state.direct_agenda = False
