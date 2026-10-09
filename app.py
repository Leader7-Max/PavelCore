import streamlit as st
import sqlite3
import os
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

# =========================================================
# 2. GESTION DE LA BASE DE DONNÉES SQLITE
# =========================================================
DB_NAME = "pavelcore.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Table des utilisateurs
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pin TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'User'
        )
    ''')
    # Table des événements
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            titre TEXT NOT NULL,
            categorie TEXT,
            date_evt TEXT,
            heure_evt TEXT,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    # Comptes par défaut si la base est vide
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (name, pin, role) VALUES ('Pavel Yonta', '123456', 'Admin')")
        c.execute("INSERT INTO users (name, pin, role) VALUES ('Doris Ebongue', '654321', 'User')")
    conn.commit()
    conn.close()

init_db()

def authenticate_user(pin):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, role FROM users WHERE pin = ?", (pin,))
    user = c.fetchone()
    conn.close()
    return user

def add_user(name, pin, role="User"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, pin, role) VALUES (?, ?, ?)", (name, pin, role))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def save_event(user_id, titre, categorie, date_evt, heure_evt, description):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO events (user_id, titre, categorie, date_evt, heure_evt, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, titre, categorie, str(date_evt), str(heure_evt), description))
    conn.commit()
    conn.close()

def get_user_events(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT titre, categorie, date_evt, heure_evt, description FROM events WHERE user_id = ? ORDER BY id DESC", (user_id,))
    events = c.fetchall()
    conn.close()
    return events

# =========================================================
# 3. INITIALISATION DU SESSION_STATE
# =========================================================
if "app_theme" not in st.session_state:
    st.session_state.app_theme = "light"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# =========================================================
# 4. INJECTION DU CSS DYNAMIQUE
# =========================================================
inject_custom_design(st.session_state.app_theme)

# =========================================================
# 5. EN-TÊTE ET SÉLECTEUR DE THÈME
# =========================================================
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    if st.session_state.authenticated:
        st.caption(f"⚡ **PavelCore** Workspace — Connecté : **{st.session_state.current_user['name']}**")
    else:
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
# 6. ÉCRAN D'AUTHENTIFICATION & CREATION DE COMPTE
# =========================================================
if not st.session_state.authenticated:
    tab_login, tab_register = st.tabs(["🔒 Connexion PIN", "➕ Créer un Compte"])
    
    with tab_login:
        st.subheader("Connexion Espace Personnel")
        with st.form("login_form", clear_on_submit=False):
            pin_input = st.text_input(
                "PIN de sécurité", 
                type="password", 
                placeholder="Ex: 123456",
                key="pin_field"
            )
            submit_login = st.form_submit_button("Se connecter", use_container_width=True)
            
            if submit_login:
                user = authenticate_user(pin_input)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.current_user = {"id": user[0], "name": user[1], "role": user[2]}
                    st.success(f"Bienvenue {user[1]} !")
                    st.rerun()
                else:
                    st.error("PIN individuel non reconnu. Veuillez vérifier vos accès.")

    with tab_register:
        st.subheader("Nouveau Compte Utilisateur")
        with st.form("register_form", clear_on_submit=True):
            new_name = st.text_input("Nom / Prénom", placeholder="Ex: Jean Dupont")
            new_pin = st.text_input("Définir un PIN unique (4 à 6 chiffres)", type="password", placeholder="Ex: 987654")
            submit_reg = st.form_submit_button("Créer mon compte", use_container_width=True)
            
            if submit_reg:
                if new_name.strip() and new_pin.strip():
                    if add_user(new_name.strip(), new_pin.strip()):
                        st.success("Compte créé avec succès ! Connectez-vous avec votre PIN.")
                    else:
                        st.error("Ce PIN est déjà attribué à un autre utilisateur. Choisissez-en un autre.")
                else:
                    st.warning("Veuillez remplir tous les champs.")

    st.stop()

# =========================================================
# 7. ESPACE DE TRAVAIL INDIVIDUEL (APPRÈS CONNEXION)
# =========================================================
user_info = st.session_state.current_user

# Bouton de déconnexion
if st.sidebar.button("🔴 Déconnexion"):
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.rerun()

st.title(f"👋 Espace Personnel : {user_info['name']}")

tab_event, tab_calendar, tab_prompts = st.tabs([
    "➕ Mon Événement", 
    "📅 Mon Calendrier Personnel",
    "💻 Mes Prompts Code"
])

# ---- ONGLET 1 : AJOUTER UN ÉVÉNEMENT ----
with tab_event:
    st.subheader("Planifier un événement dans votre agenda")
    
    col_titre, col_cat = st.columns(2)
    with col_titre:
        titre = st.text_input("Titre de l'événement / Rappel", placeholder="Ex: Réunion de projet")
    with col_cat:
        categorie = st.selectbox("Catégorie", ["Business / Travail", "Événement / DJ", "Personnel", "Urgent"])

    col_date, col_heure, col_notif = st.columns(3)
    with col_date:
        date_evt = st.date_input("Date")
    with col_heure:
        heure_evt = st.time_input("Heure")
    with col_notif:
        notification = st.selectbox("Rappel", ["Alarme Digitale", "Notification Silencieuse", "Email"])

    description = st.text_area("Description / Notes privées", placeholder="Notes confidentielles...")
    
    if st.button("Enregistrer dans mon agenda", key="btn_save_event"):
        if titre.strip():
            save_event(user_info["id"], titre, categorie, date_evt, heure_evt, description)
            st.success(f"Événement '{titre}' enregistré dans votre calendrier !")
            st.rerun()
        else:
            st.warning("Veuillez saisir au moins un titre.")

# ---- ONGLET 2 : CALENDRIER PERSONNEL ----
with tab_calendar:
    st.subheader(f"Agenda privé de {user_info['name']}")
    
    my_events = get_user_events(user_info["id"])
    
    if my_events:
        for evt in my_events:
            titre, cat, date_e, heure_e, desc = evt
            with st.expander(f"📌 {titre} — {date_e} à {heure_e}"):
                st.write(f"**Catégorie :** {cat}")
                st.write(f"**Notes :** {desc if desc else 'Aucune description'}")
    else:
        st.info("Vous n'avez aucun événement enregistré dans votre espace.")

# ---- ONGLET 3 : PROMPTS PERSONNELS ----
with tab_prompts:
    st.subheader("Bibliothèque de Prompts Privée")
    prompt_title = st.text_input("Titre du Prompt", placeholder="Ex: Script Python Custom")
    langage = st.selectbox("Langage", ["Python", "JavaScript / React", "HTML5 / CSS3", "SQL", "Flutter / Flet"])
    
    if st.button("Sauvegarder", key="btn_save_prompt"):
        st.success("Prompt sauvegardé dans votre espace individuel !")
