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

st.set_page_config(
    page_title="PavelCore — Workspace & Agenda Premium",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from modules.state import init_session_state
from modules.database import create_user_db, authenticate_user_db, load_events_from_db

init_session_state()

# CSS global (à rappeler à chaque exécution : Streamlit retire l'élément sinon)
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

# ── Import paresseux des vues (chargées seulement si utilisées) ─
def _view(module: str, func: str):
    return getattr(importlib.import_module(f"views.{module}"), func)

# ── CSS des boutons Connexion / Inscription (votre design) ─
AUTH_SWITCH_CSS = """
<style>
.st-key-auth_switch [data-testid="stHorizontalBlock"]{
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 10px !important;
}
.st-key-auth_switch [data-testid="stColumn"],
.st-key-auth_switch [data-testid="column"]{
    min-width: 0 !important;
    flex: 1 1 0 !important;
    width: auto !important;
}
.st-key-auth_switch button{
    width: 100% !important;
    border-radius: 50px !important;
    padding: 12px 8px !important;
    box-shadow: 0 4px 12px rgba(236,72,153,0.3) !important;
    transition: none !important;
}
.st-key-auth_switch button p{
    color: #FFF !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    margin: 0 !important;
}
/* Bouton actif */
.st-key-auth_switch button[kind="primary"],
.st-key-auth_switch button[data-testid="stBaseButton-primary"]{
    background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
}
/* Bouton inactif */
.st-key-auth_switch button[kind="secondary"],
.st-key-auth_switch button[data-testid="stBaseButton-secondary"]{
    background: #230E3D !important;
    border: 1px solid rgba(236,72,153,0.4) !important;
}
</style>
"""

# ── Moteur d'alarmes invisible (toutes les rubriques sauf l'Agenda) ─
ENGINE_CSS = """
<style>
.st-key-pc_engine{
    position: absolute !important;
    width: 1px !important; height: 1px !important;
    overflow: hidden !important; opacity: 0 !important;
    pointer-events: none !important; margin: 0 !important; padding: 0 !important;
}
</style>
"""

# ── Sécurité login : anti force brute ─────────────────────
MAX_ATTEMPTS, LOCK_SECONDS = 5, 60
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def _locked_for() -> int:
    return max(0, int(st.session_state.get("lock_until", 0) - time.time()))

# ── Callbacks (exécutés avant le rerun : un seul cycle) ───
def set_auth_mode(mode: str):
    st.session_state.auth_mode = mode
    st.session_state.auth_msg = None

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
        st.session_state.pop("login_pass", None)
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
    elif len(p1) < 6:
        st.session_state.auth_msg = ("warning", "Le mot de passe doit contenir au moins 6 caractères.")
    elif p1 != p2:
        st.session_state.auth_msg = ("error", "Les deux mots de passe ne correspondent pas.")
    else:
        ok, msg = create_user_db(email, p1)
        if ok:
            st.session_state.auth_msg = ("success", msg)
            st.session_state.pop("signup_pass", None)
            st.session_state.pop("signup_confirm_pass", None)
        else:
            st.session_state.auth_msg = ("error", msg)

def do_logout():
    st.session_state.authenticated = False
    st.session_state.user_info = None
    st.session_state.current_view = "home"
    st.session_state.flash = "🔒 Déconnexion effectuée."

def go_direct_agenda():
    st.session_state.direct_agenda = True

def leave_demo_agenda():
    st.session_state.direct_agenda = False
    st.query_params.clear()          # retire ?app=agenda

def go_home():
    st.session_state.current_view = "home"

def show_auth_msg():
    msg = st.session_state.get("auth_msg")
    if msg:
        getattr(st, msg[0])(msg[1])

def run_background_alarms():
    """Les alarmes sonnent dans toutes les rubriques. L'Agenda affiche son propre panneau (un seul moteur actif)."""
    user = st.session_state.get("user_info")
    if not user:
        return
    from modules.notifier import render_notifier
    with st.container(key="pc_engine"):
        st.markdown(ENGINE_CSS, unsafe_allow_html=True)
        render_notifier(load_events_from_db(user["id"]), show_panel=False)

# Toast affiché une seule fois
if st.session_state.get("flash"):
    st.toast(st.session_state.pop("flash"))

# ── Recherche globale isolée (ne relance pas toute la page) ─
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
    st.markdown(f"### 🔎 Résultats de recherche pour : *'{q_raw}'*")

    def has(value) -> bool:
        """Recherche tolérante aux valeurs vides (None) venant de la base."""
        return q in str(value or "").lower()

    def card(badge, title, extra=""):
        st.markdown(
            f'<div class="zapio-card"><span class="zapio-badge">{badge}</span>'
            f'<h4 style="margin-top:5px;">{title}</h4>{extra}</div>',
            unsafe_allow_html=True,
        )

    prompts = [p for p in ss.saved_prompts_library
               if has(p.get("title")) or has(p.get("prompt")) or has(p.get("category"))]
    if prompts:
        st.markdown("#### 🧠 Prompts & IA")
        for it in prompts:
            count += 1
            card(it.get("category", ""), it.get("title", ""))
            st.code(it.get("prompt", ""), language="markdown")

    files = [f for f in ss.saved_media_files
             if has(f.get("title")) or has(f.get("filename")) or has(f.get("type")) or has(f.get("desc"))]
    if files:
        st.markdown("#### 📁 Médias & Fichiers")
        for it in files:
            count += 1
            card(it.get("type", ""), it.get("title", ""))

    events = [e for e in ss.agenda_events
              if has(e.get("title")) or has(e.get("desc")) or has(e.get("category"))]
    if events:
        st.markdown("#### 📅 Agenda & Événements")
        for it in events:
            count += 1
            card(it.get("category") or "Général", it.get("title", ""),
                 f'<p>Date: {it.get("date", "")} à {it.get("time", "")}</p>')

    contacts = [c for c in ss.saved_contacts
                if has(c.get("name")) or has(c.get("email")) or has(c.get("phone")) or has(c.get("notes"))]
    if contacts:
        st.markdown("#### 🎴 Contacts")
        for it in contacts:
            count += 1
            card(it.get("cat") or "Contact", it.get("name", ""),
                 f'<p>📧 {it.get("email") or ""} | 📞 {it.get("phone") or ""}</p>')

    projects = [p for p in ss.saved_current_projects + ss.saved_future_projects
                if has(p.get("name")) or has(p.get("desc")) or has(p.get("client"))]
    if projects:
        st.markdown("#### 🚀 Projets")
        for it in projects:
            count += 1
            card("Projet", it.get("name", ""))

    if count == 0:
        st.warning("Aucun élément ne correspond à votre recherche.")
    st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 25px 0;'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ROUTAGE
# ══════════════════════════════════════════════════════════
is_direct_agenda_link = st.query_params.get("app") == "agenda"

# ── AGENDA DÉMO (avec bouton retour) ──────────────────────
if is_direct_agenda_link or st.session_state.get("direct_agenda", False):
    back_label = "← Retour au Tableau de Bord" if st.session_state.get("authenticated") else "← Retour à la connexion"
    st.button(back_label, key="back_from_demo_agenda", type="secondary", on_click=leave_demo_agenda)

    _view("agenda_view", "render_agenda_view")(
        sub_title_color, card_bg, card_border, header_box_bg, header_box_text, text_color
    )

# ── ÉCRAN D'AUTHENTIFICATION ──────────────────────────────
elif not st.session_state.get("authenticated", False):
    st.markdown(
        f'<div style="text-align: center; margin-top: 25px; margin-bottom: 20px;">'
        f'<h1 style="font-size: 2.8rem; margin-bottom: 5px;">'
        f'<span style="color: {text_color};">pavel</span>'
        f'<span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; '
        f'padding: 2px 10px; border-radius: 8px; font-size: 2rem; margin-left: 6px;">CORE</span></h1>'
        f'<div style="margin-top: 10px;"><span class="zapio-badge">🔮 Workspace Centralisé & Sécurisé</span></div></div>',
        unsafe_allow_html=True,
    )

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    _, col, _ = st.columns([1, 2, 1])
    with col:
