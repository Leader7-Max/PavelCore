import streamlit as st
import streamlit.components.v1 as components
import os

@st.cache_data
def load_html_component(file_path):
    """Charge et met en cache le contenu du composant HTML."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return None

def render_prompts_module():
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "assets", "snippets_component.html"),
        os.path.join(os.path.dirname(__file__), "..", "snippets_component.html"),
        os.path.join(os.getcwd(), "assets", "snippets_component.html"),
        os.path.join(os.getcwd(), "snippets_component.html"),
    ]

    html_code = None
    for path in possible_paths:
        html_code = load_html_component(path)
        if html_code:
            break

    if html_code:
        components.html(html_code, height=950, scrolling=True)
    else:
        st.error("⚠️ Le fichier `snippets_component.html` est introuvable.")
        st.info("Vérifie que le fichier est bien présent dans ton dossier `assets/` sur GitHub.")
