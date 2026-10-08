import streamlit as st
import streamlit.components.v1 as components
import os

def render_prompts_module():
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "assets", "snippets_component.html"),
        os.path.join(os.path.dirname(__file__), "..", "snippets_component.html"),
        os.path.join(os.getcwd(), "assets", "snippets_component.html"),
        os.path.join(os.getcwd(), "snippets_component.html"),
    ]

    html_code = None

    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                html_code = f.read()
            break

    if html_code:
        components.html(html_code, height=950, scrolling=True)
    else:
        st.error("⚠️ Le fichier `snippets_component.html` est introuvable.")
        st.info("Vérifie que le fichier est bien présent dans ton dépôt GitHub.")
