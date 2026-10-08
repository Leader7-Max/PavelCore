import streamlit as st
import streamlit.components.v1 as components
import os

def render_prompts_module():
    # Liste de tous les chemins possibles où le fichier HTML pourrait se trouver
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "assets", "snippets_component.html"),
        os.path.join(os.path.dirname(__file__), "..", "snippets_component.html"),
        os.path.join(os.getcwd(), "assets", "snippets_component.html"),
        os.path.join(os.getcwd(), "snippets_component.html"),
    ]

    html_code = None

    # Parcourir les chemins pour trouver le fichier
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                html_code = f.read()
            break

    # Affichage du composant si le fichier est trouvé
    if html_code:
        components.html(html_code, height=950, scrolling=True)
    else:
        st.error("⚠️ Le fichier `snippets_component.html` est introuvable.")
        st.info("Vérifie que le fichier est bien présent dans ton dépôt GitHub (soit à la racine, soit dans le dossier `assets/`).")
