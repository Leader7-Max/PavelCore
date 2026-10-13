import streamlit as st

_DEFAULTS = {
    "authenticated": False,
    "user_info": None,
    "current_view": "home",
    "theme_mode": "Sombre Nuit",
    "auth_mode": "login",
    "direct_agenda": False,
}

_LIST_KEYS = (
    "saved_prompts_library",
    "saved_media_files",
    "agenda_events",
    "saved_contacts",
    "saved_current_projects",
    "saved_future_projects",
    "saved_api_keys",
    "saved_user_credentials",
)


def init_session_state():
    """Initialise toutes les variables de session globales de PavelCore."""
    if "modules" not in st.session_state:
        st.session_state["modules"] = {}

    for key, value in _DEFAULTS.items():
        st.session_state.setdefault(key, value)

    for key in _LIST_KEYS:
        st.session_state.setdefault(key, [])
