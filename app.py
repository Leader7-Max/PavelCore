import streamlit as st
from assets.styles import inject_custom_design

# 1. Configuration de la page Streamlit
st.set_page_config(
    page_title="PavelCore Digital Workspace",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Initialisation du thème dans st.session_state
if "app_theme" not in st.session_state:
    st.session_state.app_theme = "dark"  # Thème par défaut à l'ouverture

# 3. Injection directe du CSS correspondant
inject_custom_design(st.session_state.app_theme)

# 4. EN-TÊTE : Sélecteur de Thème visible DÈS L'OUVERTURE
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.caption("⚡ **PavelCore** Workspace")

with header_col2:
    # Sélecteur de thème immédiatement interactif
    selected_theme_label = "🌙 Sombre" if st.session_state.app_theme == "dark" else "☀️ Clair"
    theme_toggle = st.radio(
        "Thème",
        options=["🌙 Sombre", "☀️ Clair"],
        index=0 if st.session_state.app_theme == "dark" else 1,
        horizontal=True,
        label_visibility="collapsed",
        key="global_theme_toggle"
    )
    
    # Prise en compte immédiate du changement
    new_theme = "dark" if theme_toggle == "🌙 Sombre" else "light"
    if new_theme != st.session_state.app_theme:
        st.session_state.app_theme = new_theme
        st.rerun()

st.divider()

# =========================================================
# 5. SUITE DU CODE (AUTHENTIFICATION PIN / CONTENU)
# =========================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔒 Authentification Master PIN")
    pin_input = st.text_input("Saisissez votre PIN de sécurité", type="password")
    if st.button("Se connecter"):
        # Logique de vérification du PIN...
        pass
    st.stop()  # S'arrête ici tant que le PIN n'est pas validé
