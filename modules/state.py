import streamlit as st
from modules.database import load_events_from_db, load_api_keys_from_db, load_credentials_from_db, load_contacts_from_db

def init_session_state():
    """Initialise l'état global et charge les données persistantes de l'utilisateur actif dans PavelCore."""
    
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "Sombre Nuit"

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Dashboard"

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "user_info" not in st.session_state:
        st.session_state.user_info = None

    if "current_view" not in st.session_state:
        st.session_state.current_view = "home"

    # Récupération de l'ID utilisateur si connecté (ou ID par défaut 0 / mode hors-ligne)
    user_id = st.session_state.user_info["id"] if st.session_state.get("user_info") else 0

    # Chargement persistant Agenda filtré par utilisateur
    if "agenda_events" not in st.session_state:
        st.session_state.agenda_events = load_events_from_db(user_id)
        
    if "agenda_active_tab" not in st.session_state:
        st.session_state.agenda_active_tab = "vue"

    # Chargement persistant Coffre-fort (Clés API & Mots de passe) filtré par utilisateur
    if "saved_api_keys" not in st.session_state:
        st.session_state.saved_api_keys = load_api_keys_from_db(user_id)

    if "saved_user_credentials" not in st.session_state:
        st.session_state.saved_user_credentials = load_credentials_from_db(user_id)

    # Chargement persistant Contacts filtré par utilisateur
    if "saved_contacts" not in st.session_state:
        st.session_state.saved_contacts = load_contacts_from_db(user_id)

    # Initialisations des autres listes si absentes
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
    if "saved_email_templates" not in st.session_state:
        st.session_state.saved_email_templates = []
