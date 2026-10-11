import streamlit as st

def init_session_state():
    """Initialise toutes les variables globales nécessaires dans le st.session_state de PavelCore."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if "user_info" not in st.session_state:
        st.session_state.user_info = None

    if "current_view" not in st.session_state:
        st.session_state.current_view = "home"

    if "agenda_events" not in st.session_state:
        st.session_state.agenda_events = []

    if "saved_prompts_library" not in st.session_state:
        st.session_state.saved_prompts_library = []

    if "saved_code_snippets" not in st.session_state:
        st.session_state.saved_code_snippets = []

    if "saved_ideas" not in st.session_state:
        st.session_state.saved_ideas = []

    if "saved_current_projects" not in st.session_state:
        st.session_state.saved_current_projects = []

    if "saved_future_projects" not in st.session_state:
        st.session_state.saved_future_projects = []

    if "saved_links" not in st.session_state:
        st.session_state.saved_links = []

    if "saved_media_files" not in st.session_state:
        st.session_state.saved_media_files = []

    if "saved_api_keys" not in st.session_state:
        st.session_state.saved_api_keys = []

    if "saved_user_credentials" not in st.session_state:
        st.session_state.saved_user_credentials = []

    if "saved_contacts" not in st.session_state:
        st.session_state.saved_contacts = []

    if "saved_email_templates" not in st.session_state:
        st.session_state.saved_email_templates = []
