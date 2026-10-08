import streamlit as st
import streamlit.components.v1 as components
import os

def render_prompts_module():
    # Chemin vers ton fichier HTML
    html_file_path = os.path.join(os.path.dirname(__file__), "..", "assets", "snippets_component.html")
    
    # Lecture du fichier HTML
    if os.path.exists(html_file_path):
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_code = f.read()
        
        # Affichage du composant HTML interactif dans Streamlit
        components.html(html_code, height=900, scrolling=True)
    else:
        # Fallback au cas où le fichier HTML est placé directement à la racine
        try:
            with open("snippets_component.html", "r", encoding="utf-8") as f:
                html_code = f.read()
            components.html(html_code, height=900, scrolling=True)
        except FileNotFoundError:
            st.error("Le fichier snippets_component.html est introuvable. Assure-toi de l'avoir ajouté dans ton dépôt GitHub.")
