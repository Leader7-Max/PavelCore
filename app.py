import sys
import os
import re
import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import streamlit.components.v1 as components

# Correctif pour Streamlit Cloud
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration de la page
st.set_page_config(
    page_title="PavelCore — Workspace & Agenda Premium",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from assets.styles import inject_custom_design
inject_custom_design()

# Détecteur automatique de langage
def detect_language(code):
    if not code or not isinstance(code, str):
        return "python"
    
    code_lower = code.lower().strip()
    
    if re.search(r'<!doctype html>|<html|<div|<span|<body|<p>|<a href', code_lower):
        return "html"
    elif re.search(r'\{\s*color:|margin:|padding:|background-color:|font-family:|border-radius:', code_lower):
        return "css"
    elif re.search(r'\b(select|insert into|update|delete from|create table|where|group by|order by|join)\b', code_lower):
        return "sql"
    elif re.search(r'\b(const|let|var|function|console\.log|document\.|window\.|export default|import react)\b', code_lower):
        return "javascript"
    elif "<?php" in code_lower or re.search(r'\$[a-zA-Z_][a-zA-Z0-9_]*\s*=', code):
        return "php"
    elif code_lower.startswith("{") and code_lower.endswith("}") and ":" in code_lower:
        return "json"
    elif re.search(r'\b(def |import |from |st\.|print\(|self\.|elif |class )\b', code_lower):
        return "python"
    
    return "python"

LANG_MAP = {
    "Python": "python",
    "Détection Automatique": "auto",
    "JavaScript / React": "javascript",
    "HTML5": "html",
    "CSS3 / TailWind": "css",
    "SQL": "sql",
    "PHP / WordPress": "php",
    "Flutter / Flet": "python",
    "JSON / Config": "json"
}

# Global State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "agenda_events" not in st.session_state:
    st.session_state.agenda_events = [
        {"title": "Lancement Application PavelCore", "date": date(2026, 10, 25), "time": time(10, 0), "category": "Dev & Tech", "desc": "Mise en ligne globale sur Streamlit Cloud", "ringtone": "Alarme Digitale"},
        {"title": "Session DJ & Mixing Event", "date": date(2026, 10, 28), "time": time(21, 30), "category": "Événement DJ / Prestation", "desc": "Préparation set Afrobeat & Zouglou", "ringtone": "Bip Futuriste"}
    ]

if "saved_ai_prompts" not in st.session_state:
    st.session_state.saved_ai_prompts = []

if "saved_claude_prompts" not in st.session_state:
    st.session_state.saved_claude_prompts = []

if "saved_code_snippets" not in st.session_state:
    st.session_state.saved_code_snippets = []

if "saved_image_prompts" not in st.session_state:
    st.session_state.saved_image_prompts = []

if "saved_ideas" not in st.session_state:
    st.session_state.saved_ideas = []

if "saved_current_projects" not in st.session_state:
    st.session_state.saved_current_projects = []

if "saved_future_projects" not in st.session_state:
    st.session_state.saved_future_projects = []

if "saved_links" not in st.session_state:
    st.session_state.saved_links = []

if "saved_zip_files" not in st.session_state:
    st.session_state.saved_zip_files = []

if "saved_api_keys" not in st.session_state:
    st.session_state.saved_api_keys = []

if "saved_user_credentials" not in st.session_state:
    st.session_state.saved_user_credentials = []


# ----------------------------------------------------
# 1. AUTHENTIFICATION
# ----------------------------------------------------
if not st.session_state.authenticated:
    st.markdown("""
        <div style="text-align: center; margin-top: 30px; margin-bottom: 25px;">
            <h1 style="font-size: 2.8rem; margin-bottom: 5px;">
                <span style="color: #FFFFFF;">pavel</span><span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; padding
