import streamlit as st
from modules.database import load_events_from_db, load_api_keys_from_db, load_credentials_from_db, load_contacts_from_db

def init_session_state():
    """Initialise l'état global et charge les données persistantes de PavelCore."""
    
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "Sombre Nuit"

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Dashboard"

    # Chargement persistant Agenda
    if "agenda_events" not in st.session_state:
        st.session_state.agenda_events = load_events_from_db()
        
    if "agenda_active_tab" not in st.session_state:
        st.session_state.agenda_active_tab = "vue"

    # Chargement persistant Coffre-fort (Clés API & Mots de passe)
    if "saved_api_keys" not in st.session_state:
        st.session_state.saved_api_keys = load_api_keys_from_db()

    if "saved_user_credentials" not in st.session_state:
        st.session_state.saved_user_credentials = load_credentials_from_db()

    # Chargement persistant Contacts
    if "saved_contacts" not in st.session_state:
        st.session_state.saved_contacts = load_contacts_from_db()
        
    if "confirm_delete_agenda_idx" not in st.session_state:
        st.session_state.confirm_delete_agenda_idx = None
        
    if "direct_agenda" not in st.session_state:
        st.session_state.direct_agenda = False
