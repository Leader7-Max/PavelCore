import sys
import os
import re
import time
import importlib
import streamlit as st

# ── Chemins ────────────────────────────────────────────────
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# ── Config page (doit être le 1er appel Streamlit) ────────
st.set_page_config(
    page_title="PavelCore — Workspace & Agenda Premium",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from modules.state import init_session_state
from modules.database import create_user_db, authenticate_user_db

init_session_state()

# ── CSS : injecté une seule fois par session ──────────────
if not st.session_state.get("_css_ready"):
    try:
        from assets.styles import inject_custom_design
        inject_custom_design()
        st.session_state["_css_ready"] = True
    except Exception:
        pass
else:
    # Streamlit supprime le CSS si l'élément n'est pas rendu : on le ré-injecte
    # de façon légère (sans recalcul coûteux).
    try:
        from assets.styles import inject_custom_design
        inject_custom_design()
    except Exception:
        pass

UPLOADS_DIR = os.path.join(ROOT_DIR, "uploaded_files")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# ── Thème ──────────────────────────────────────────────────
THEMES = {
    "Blanc Épuré": dict(
        text_color="#0F172A", sub_title_color="#0F172A", desc_color="#475569",
        header_box_bg="#F1F5F9", header_box_text="#475569",
        card_border="#E2E8F0", card_bg="#FFFFFF",
    ),
    "Sombre Nuit": dict(
        text_color="#F8FAFC", sub_title_color="#FFF", desc_color="#CBD5E1",
        header_box_bg="#1E0A3C", header_box_text="#A78BFA",
        card_border="#2B1552", card_bg="#170A2E",
    ),
}
T = THEMES.get(st.session_state.get("theme_mode", "Sombre Nuit"), THEMES["Sombre Nuit"])
text_color, sub_title_color, desc_color = T["text_color"], T["sub_title_color"], T["desc_color"]
header_box_bg, header_box_text = T["header_box_bg"], T["header_box_text"]
card_border, card_bg = T["card_border"], T["card_bg"]

# ── Import paresseux des vues (seulement après login) ─────
def _view(module: str, func: str):
    return getattr(importlib.import_module(f"views.{module}"), func)

# ── Sécurité login : anti force brute ─────────────────────
MAX_ATTEMPTS, LOCK_SECONDS = 5, 60
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def _locked_for() -> int:
    until = st.session_state.get("lock_until", 0)
    return max(0, int(until - time.time()))

# ── Callbacks (exécutés AVANT le rerun : 1 seul cycle) ────
def do_login():
    email = st.session_state.get("login_email", "").strip().lower()
    pwd = st.session_state.get("login_pass", "")
    st.session_state.auth_msg = None

    if _locked_for() > 0:
        st.session_state.auth_msg = ("error", f"Trop de tentatives. Réessayez dans {_locked_for()} s.")
        return
    if not EMAIL_RE.match(email) or not pwd:
        st.session_state.auth_msg = ("warning", "Renseignez un email valide et votre mot de passe.")
        return

    ok, res = authenticate_user_db(email, pwd)
    if ok:
        st.session_state.authenticated = True
        st.session_state.user_info = res
        st.session_state.login_attempts = 0
        st.session_state.pop("login_pass", None)   # ne pas garder le mot de passe en session
        st.session_state.flash = f"🔓 Bienvenue, {res['email']} !"
    else:
        n = st.session_state.get("login_attempts", 0) + 1
        st.session_state.login_attempts = n
        if n >= MAX_ATTEMPTS:
            st.session_state.lock_until = time.time() + LOCK_SECONDS
            st.session_state.login_attempts = 0
        st.session_state.auth_msg = ("error", res)

def do_signup():
    email = st.session_state.get("signup_email", "").strip().lower()
    p1 = st.session_state.get("signup_pass", "")
    p2 = st.session_state.get("signup_confirm_pass", "")
    st.session_state.auth_msg = None

    if not EMAIL_RE.match(email):
        st.session_state.auth_msg = ("warning", "Adresse email invalide.")
    elif len(p1) < 8:
        st.session_state.auth_msg = ("warning", "Le mot de passe doit contenir au moins 8 caractères.")
    elif p1 != p2:
        st.session_state.auth_msg = ("error", "Les deux mots de passe ne correspondent pas.")
    else:
        ok, msg = create_user_db(email, p1)
        if ok:
            st.session_state.auth_msg = ("success", msg + " Vous pouvez maintenant vous connecter.")
            st.session_state.pop("signup_pass", None)
            st.session_state.pop("signup_confirm_pass", None)
        else:
            st.session_state.auth_msg = ("error", msg)

def do_logout():
    for k in ("authenticated", "user_info"):
        st.session_state[k] = False if k == "authenticated" else None
    st.session_state.current_view = "home"
    st.session_state.flash = "🔒 Déconnexion effectuée."

def go_direct_agenda():
    st.session_state.direct_agenda = True

def go_home():
    st.session_state.current_view = "home"

def show_auth_msg():
    msg = st.session_state.get("auth_msg")
    if msg:
        getattr(st, msg[0])(msg[1])

# ── Message flash (toast) affiché une fois ────────────────
if st.session_state.get("flash"):
    st.toast(st.session_state.pop("flash"))

# ── Recherche globale isolée : ne relance pas toute la page ─
@st.fragment
def render_global_search():
    q_raw = st.text_input(
        "⚡ Recherche Rapide Universelle",
        placeholder="🔍 Tapez un mot-clé (ex: Flyer, Python, DJ, Client, Prompt...)",
        key="global_search_input",
    )
    q = q_raw.strip().lower()
    if not q:
        return

    ss = st.session_state
    count = 0
    st.markdown(f"### 🔎 Résultats pour : *'{q_raw}'*")

    def card(badge, title, extra=""):
        st.markdown(
            f'<div class="zapio-card"><span class="zapio-badge">{badge}</span>'
            f'<h4 style="margin-top:5px;">{title}</h4>{extra}</div>',
            unsafe_allow_html=True,
        )

    prompts = [p for p in ss.saved_prompts_library
               if q in p["title"].lower() or q in p["prompt"].lower() or q in p["category"].lower()]
    if prompts:
        st.markdown("#### 🧠 Prompts & IA")
        for it in prompts:
            count += 1
            card(it["category"], it["title"])
            st.code(it["prompt"], language="markdown")

    files = [f for f in ss.saved_media_files
             if q in f["title"].lower() or q in f.get("filename", "").lower()
             or q in f.get("type", "").lower() or q in f.get("desc", "").lower()]
    if files:
        st.markdown("#### 📁 Médias & Fichiers")
        for it in files:
            count += 1
            card(it["type"], it["title"])

    events = [e for e in ss.agenda_events
              if q in e["title"].lower() or q in e.get("desc", "").lower() or q in e.get("category", "").lower()]
    if events:
        st.markdown("#### 📅 Agenda & Événements")
        for it in events:
            count += 1
            card(it["category"], it["title"], f'<p>Date : {it["date"]} à {it["time"]}</p>')

    contacts = [c for c in ss.saved_contacts
                if q in c["name"].lower() or q in c.get("email", "").lower()
                or q in c.get("phone", "").lower() or q in c.get("notes", "").lower()]
    if contacts:
        st.markdown("#### 🎴 Contacts")
        for it in contacts:
            count += 1
            card(it["cat"], it["name"], f'<p>📧 {it.get("email","")} | 📞 {it.get("phone","")}</p>')

    projects = [p for p in ss.saved_current_projects + ss.saved_future_projects
                if q in p["name"].lower() or q in p.get("desc", "").lower() or q in p.get("client", "").lower()]
    if projects:
        st.markdown("#### 🚀 Projets")
        for it in projects:
            count += 1
            card("Projet", it["name"])

    if count == 0:
        st.warning("Aucun élément ne correspond à votre recherche.")
    st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 25px 0;'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ROUTAGE
# ══════════════════════════════════════════════════════════
is_direct_agenda_link = st.query_params.get("app") == "agenda"

if is_direct_agenda_link or st.session_state.get("direct_agenda", False):
    _view("agenda_view", "render_agenda_view")(
        sub_title_color, card_bg, card_border, header_box_bg, header_box_text, text_color
    )

# ── ÉCRAN D'AUTHENTIFICATION ──────────────────────────────
elif not st.session_state.get("authenticated", False):
    st.markdown(
        f'<div style="text-align:center;margin:25px 0 20px;"><h1 style="font-size:2.8rem;margin-bottom:5px;">'
        f'<span style="color:{text_color};">pavel</span>'
        f'<span style="background:linear-gradient(135deg,#EC4899,#8B5CF6);color:#FFF;padding:2px 10px;'
        f'border-radius:8px;font-size:2rem;margin-left:6px;">CORE</span></h1>'
        f'<div style="margin-top:10px;"><span class="zapio-badge">🔮 Workspace Centralisé & Sécurisé</span></div></div>',
        unsafe_allow_html=True,
    )

    _, col, _ = st.columns([1, 2, 1])
    with col:
        tab_login, tab_signup = st.tabs(["🔑 Connexion", "✨ Inscription"])

        with tab_login:
            with st.form("login_form", border=False):
                st.text_input("Adresse Email", placeholder="votre.email@exemple.com", key="login_email")
                st.text_input("Mot de passe", type="password", placeholder="••••••••", key="login_pass")
                st.form_submit_button(
                    "Se connecter au Workspace", use_container_width=True,
                    type="primary", on_click=do_login,
                )
            show_auth_msg()

        with tab_signup:
            with st.form("signup_form", border=False):
                st.text_input("Adresse Email", placeholder="nom@exemple.com", key="signup_email")
                st.text_input("Créer un mot de passe (8 caractères min.)", type="password",
                              placeholder="••••••••", key="signup_pass")
                st.text_input("Confirmer le mot de passe", type="password",
                              placeholder="••••••••", key="signup_confirm_pass")
                st.form_submit_button(
                    "S'inscrire et rejoindre PavelCore", use_container_width=True,
                    type="primary", on_click=do_signup,
                )
            show_auth_msg()

        st.button("📅 Accéder directement à l'Agenda (Hors-ligne / Démo)",
                  use_container_width=True, type="secondary", on_click=go_direct_agenda)

# ── APPLICATION (utilisateur connecté) ────────────────────
else:
    col_logo, col_user, col_logout = st.columns([2, 2, 1])
    with col_logo:
        st.markdown(
            f'<h1 style="font-size:1.3rem;margin:0;display:flex;align-items:center;gap:6px;">'
            f'<span style="color:{text_color};">pavel</span>'
            f'<span style="background:linear-gradient(135deg,#EC4899,#8B5CF6);color:#FFF;padding:2px 6px;'
            f'border-radius:6px;font-size:0.85rem;">CORE</span>'
            f'<span class="zapio-badge-green" style="font-size:0.55rem;">● Live</span></h1>',
            unsafe_allow_html=True,
        )
    with col_user:
        email = (st.session_state.get("user_info") or {}).get("email", "Membre")
        st.markdown(
            f'<div style="text-align:center;color:{desc_color};font-size:0.85rem;padding-top:5px;">'
            f'👤 Connecté en tant que : <strong style="color:{sub_title_color};">{email}</strong></div>',
            unsafe_allow_html=True,
        )
    with col_logout:
        st.button("🔒 Déconnexion", use_container_width=True, type="secondary", on_click=do_logout)

    st.markdown("<hr style='border-color:rgba(236,72,153,0.2);margin:15px 0;'>", unsafe_allow_html=True)
    render_global_search()

    current = st.session_state.current_view
    if current == "home":
        _view("home_view", "render_home_view")()
        _view("backup_view", "render_backup_view")(sub_title_color)
    else:
        st.button("← Retour au Tableau de Bord", key="back_to_home_universal",
                  type="secondary", on_click=go_home)
        st.markdown(f"<h2 style='color:#EC4899;margin-top:15px;'>Espace : {current}</h2>", unsafe_allow_html=True)

        if current == "Agenda":
            _view("agenda_view", "render_agenda_view")(
                sub_title_color, card_bg, card_border, header_box_bg, header_box_text, text_color)
        elif current == "Prompts & IA":
            _view("dev_ia_view", "render_dev_ia_view")(sub_title_color)
        elif current == "Projets":
            _view("projets_view", "render_projets_view")(sub_title_color, desc_color)
        elif current == "Médias & Fichiers":
            _view("media_view", "render_media_view")(sub_title_color, UPLOADS_DIR)
        elif current == "Coffre-Fort":
            _view("vault_contacts_view", "render_vault_view")(sub_title_color, desc_color)
        elif current == "Contacts & Emails":
            _view("vault_contacts_view", "render_contacts_view")(sub_title_color, desc_color)
        elif current == "Sauvegarde":
            _view("backup_view", "render_backup_view")(sub_title_color)
