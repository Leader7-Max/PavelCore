import streamlit as st

def init_session_state():
    """Initialise toutes les variables de session globales de PavelCore."""
    
    # Correction du KeyError 'modules'
    if "modules" not in st.session_state:
        st.session_state["modules"] = {}

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "user_info" not in st.session_state:
        st.session_state.user_info = None

    if "current_view" not in st.session_state:
        st.session_state.current_view = "home"

    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "Sombre Nuit"

    if "saved_prompts_library" not in st.session_state:
        st.session_state.saved_prompts_library = []

    if "saved_media_files" not in st.session_state:
        st.session_state.saved_media_files = []

    if "agenda_events" not in st.session_state:
        st.session_state.agenda_events = []

    if "saved_contacts" not in st.session_state:
        st.session_state.saved_contacts = []

    if "saved_current_projects" not in st.session_state:
        st.session_state.saved_current_projects = []

    if "saved_future_projects" not in st.session_state:
        st.session_state.saved_future_projects = []
