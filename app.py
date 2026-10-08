import streamlit as st
from assets.styles import inject_custom_design

# =========================================================
# 1. CONFIGURATION DE LA PAGE
# =========================================================
st.set_page_config(
    page_title="PavelCore Digital Workspace",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# PIN de sécurité Master (Modifiez par votre PIN réel ou st.secrets["MASTER_PIN"])
MASTER_PIN = "1234"

# =========================================================
# 2. INITIALISATION DU SESSION_STATE
# =========================================================
if "app_theme" not in st.session_state:
    st.session_state.app_theme = "light"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# =========================================================
# 3. INJECTION DU CSS DYNAMIQUE (THÈME SELECTIONNÉ)
# =========================================================
inject_custom_design(st.session_state.app_theme)

# =========================================================
# 4. EN-TÊTE : BASCULE DE THÈME DÈS L'OUVERTURE
# =========================================================
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.caption("⚡ **PavelCore** Workspace")

with header_col2:
    theme_toggle = st.radio(
        "Thème",
        options=["🌙 Sombre", "☀️ Clair"],
        index=0 if st.session_state.app_theme == "dark" else 1,
        horizontal=True,
        label_visibility="collapsed",
        key="global_theme_selector"
    )
    
    selected_theme = "dark" if theme_toggle == "🌙 Sombre" else "light"
    if selected_theme != st.session_state.app_theme:
        st.session_state.app_theme = selected_theme
        st.rerun()

st.divider()

# =========================================================
# 5. ECRAN D'AUTHENTIFICATION MASTER PIN
# =========================================================
if not st.session_state.authenticated:
    st.subheader("🔒 Authentification Master PIN")
    
    with st.form("login_form", clear_on_submit=False):
        pin_input = st.text_input(
            "Saisissez votre PIN de sécurité", 
            type="password", 
            placeholder="Ex: 1234",
            key="pin_field"
        )
        submit_button = st.form_submit_button("Se connecter", use_container_width=True)
        
        if submit_button:
            if pin_input == MASTER_PIN:
                st.session_state.authenticated = True
                st.success("Connexion réussie !")
                st.rerun()
            else:
                st.error("PIN incorrect. Veuillez réessayer.")

    # Bloque l'exécution ici tant que l'utilisateur n'est pas connecté
    st.stop()

# =========================================================
# 6. ESPACE DE TRAVAIL PAVELCORE (ACCESSIBLE APRES CONNEXION)
# =========================================================

# Option de déconnexion dans le header de l'espace membre
st.sidebar.button("Déconnexion", on_click=lambda: st.session_state.update({"authenticated": False}))

st.title("⚡ PavelCore Workspace")

tab_event, tab_calendar, tab_prompts = st.tabs([
    "➕ Ajouter un Événement", 
    "📅 Vue Calendrier & Liste",
    "💻 Prompt Code & Outils"
])

# ---- ONGLET 1 : AJOUTER UN ÉVÉNEMENT ----
with tab_event:
    st.subheader("Planifier un événement")
    
    col_titre, col_cat = st.columns(2)
    with col_titre:
        titre = st.text_input("Titre de l'événement / Rappel", placeholder="Ex: Réunion projet Reborn Beauty")
    with col_cat:
        categorie = st.selectbox("Catégorie", ["Business / Travail", "Événement / DJ", "Personnel", "Urgent"])

    col_date, col_heure, col_notif = st.columns(3)
    with col_date:
        date_evt = st.date_input("Date (Jour / Mois / Année)")
    with col_heure:
        heure_evt = st.time_input("Heure de l'événement")
    with col_notif:
        notification = st.selectbox("Sonnerie & Notification", ["Alarme Digitale", "Notification Silencieuse", "Email"])

    description = st.text_area("Description / Notes supplémentaires", placeholder="Détails, liens ou instructions...")
    
    if st.button("Enregistrer l'événement", key="btn_save_event"):
        st.success(f"Événement '{titre}' planifié avec succès pour le {date_evt} !")

# ---- ONGLET 2 : VUE CALENDRIER ----
with tab_calendar:
    st.subheader("Vos événements planifiés")
    st.info("Aucun événement à venir pour aujourd'hui.")

# ---- ONGLET 3 : PROMPT CODE ----
with tab_prompts:
    st.subheader("Bibliothèque de Prompts & Code")
    prompt_title = st.text_input("Titre du Prompt Code", placeholder="Ex: Script CSS Streamlit Custom")
    langage = st.selectbox("Langage / Framework ciblé", ["Python", "JavaScript / React", "HTML5 / CSS3", "SQL", "Flutter / Flet"])
    
    if st.button("Générer / Sauvegarder Prompt", key="btn_save_prompt"):
        st.success("Prompt sauvegardé dans PavelCore !")
