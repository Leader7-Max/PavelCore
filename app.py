import sys
import os
import re
import time
import uuid
import html
import importlib
import logging
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
from modules.database import load_events_from_db

# Authentification Supabase : l'app démarre même si le module est indisponible
try:
    from modules.auth import supabase_signup, supabase_login
except Exception as _auth_exc:
    logging.exception("Module d'authentification indisponible : %s", _auth_exc)

    def supabase_signup(*args, **kwargs):
        return False, "Service d'authentification indisponible. Vérifiez la configuration Supabase."

    def supabase_login(*args, **kwargs):
        return False, "Service d'authentification indisponible. Vérifiez la configuration Supabase."

init_session_state()

# CSS global (à rappeler à chaque exécution : Streamlit retire l'élément sinon)
try:
    from assets.styles import inject_custom_design
    inject_custom_design()
except Exception:
    logging.exception("Injection du design global impossible")

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


def esc(value) -> str:
    """Échappe une valeur avant de l'insérer dans du HTML (unsafe_allow_html)."""
    return html.escape("" if value is None else str(value))


# ── Import paresseux des vues, avec isolation des erreurs ─
def _view(module: str, func: str):
    try:
        mod = importlib.import_module(f"views.{module}")
        target = getattr(mod, func)
    except Exception as exc:  # inclut SyntaxError, ImportError, etc.
        logging.exception("Chargement impossible de views.%s.%s", module, func)

        def error_placeholder(*args, **kwargs):
            st.error(
                f"⚠️ Erreur de chargement : Impossible de charger la vue "
                f"`views.{module}` (fonction `{func}`). Détails : {exc}"
            )
        return error_placeholder

    def safe_view(*args, **kwargs):
        try:
            return target(*args, **kwargs)
        except Exception as exc:  # st.rerun()/st.stop() ne sont pas des Exception
            logging.exception("Erreur d'exécution dans views.%s.%s", module, func)
            st.error(f"⚠️ La vue `{module}` a rencontré une erreur : {exc}")

    return safe_view


# ── CSS des boutons Connexion / Inscription & Cartes Succès ─
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

/* Design Card Message Succès Inscription */
.pavel-auth-success-card {
    background: linear-gradient(135deg, rgba(35, 14, 61, 0.95) 0%, rgba(23, 10, 46, 0.95) 100%) !important;
    border: 1px solid rgba(236, 72, 153, 0.5) !important;
    border-radius: 16px !important;
    padding: 18px 20px !important;
    margin-top: 15px !important;
    box-shadow: 0 8px 25px rgba(236, 72, 153, 0.25) !important;
    display: flex !important;
    align-items: center !important;
    gap: 15px !important;
}

/* Design Card Connexion Réussie */
.pavel-login-success-banner {
    background: linear-gradient(135deg, rgba(30, 10, 60, 0.95) 0%, rgba(15, 5, 30, 0.98) 100%) !important;
    border: 2px solid #EC4899 !important;
    border-radius: 16px !important;
    padding: 18px 22px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 0 25px rgba(236, 72, 153, 0.4), inset 0 0 15px rgba(139, 92, 246, 0.2) !important;
    display: flex !important;
    align-items: center !important;
    gap: 18px !important;
    transition: opacity 0.8s ease-out;
}

/* Design Card Coffre-Fort Sécurisé */
.pavel-vault-success-banner {
    background: linear-gradient(135deg, rgba(30, 10, 60, 0.95) 0%, rgba(15, 5, 30, 0.98) 100%) !important;
    border: 2px solid #EC4899 !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 0 25px rgba(236, 72, 153, 0.4), inset 0 0 15px rgba(139, 92, 246, 0.2) !important;
    display: flex !important;
    align-items: center !important;
    gap: 20px !important;
}

/* Disparition automatique de la bannière de bienvenue (5 s visible, puis fondu 0,8 s) */
.pavel-welcome-wrap {
    overflow: hidden;
    animation: pavelWelcomeFade 5.8s ease-out forwards;
}
@keyframes pavelWelcomeFade {
    0%, 86% { opacity: 1; max-height: 240px; }
    100%    { opacity: 0; max-height: 0; }
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

# ── Styles des cartes, injectés aussi dans l'application connectée ─
# (conteneur invisible : aucun espace ajouté dans la mise en page)
APP_CSS = """
<style>
.st-key-pc_css{
    position: absolute !important;
    width: 1px !important; height: 1px !important;
    overflow: hidden !important; opacity: 0 !important;
    pointer-events: none !important; margin: 0 !important; padding: 0 !important;
}
</style>
""" + AUTH_SWITCH_CSS

# ── Sécurité login : anti force brute (côté session) ──────
# NB : la vraie limitation de débit doit rester activée côté Supabase.
MAX_ATTEMPTS, LOCK_SECONDS = 5, 60
EMAIL_RE = re.compile(r"^[^@\s<>\"']+@[^@\s<>\"']+\.[^@\s<>\"']+$")
ALARM_CACHE_TTL = 30  # secondes
VALID_VIEWS = {
    "home", "Agenda", "Prompts & IA", "Projets",
    "Médias & Fichiers", "Coffre-Fort", "Contacts & Emails", "Sauvegarde",
}


def _locked_for() -> int:
    return max(0, int(st.session_state.get("lock_until", 0) - time.time()))


# ── Callbacks Supabase ────────────────────────────────────
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

    ok, res = supabase_login(email, pwd)
    if ok:
        st.session_state.authenticated = True
        st.session_state.user_info = res
        st.session_state.login_attempts = 0
        st.session_state.pop("login_pass", None)
        st.session_state.pop("_alarm_cache", None)
        st.session_state.welcome_banner_msg = f"🔓 Bienvenue dans votre Workspace sécurisé, {res['email']} !"
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
        ok, msg = supabase_signup(email, p1)
        if ok:
            st.session_state.auth_msg = ("success", msg)
            st.session_state["login_email"] = email
            st.session_state.pop("signup_email", None)
            st.session_state.pop("signup_pass", None)
            st.session_state.pop("signup_confirm_pass", None)
            st.session_state.auth_mode = "login"
        else:
            st.session_state.auth_msg = ("error", msg)


def do_logout():
    # Révocation de la session Supabase si la fonction existe dans modules/auth.py
    try:
        auth_module = importlib.import_module("modules.auth")
        sign_out = getattr(auth_module, "supabase_logout", None)
        if callable(sign_out):
            sign_out()
    except Exception:
        logging.exception("Déconnexion Supabase impossible")

    # Remise à zéro complète : aucune donnée de l'utilisateur ne reste en session
    keep = {"theme_mode"}
    for key in list(st.session_state.keys()):
        if key not in keep:
            del st.session_state[key]
    st.session_state.flash = "🔒 Déconnexion effectuée."


def go_direct_agenda():
    st.session_state.direct_agenda = True
    # Identifiant privé par session démo : l'agenda n'est plus partagé entre visiteurs
    if not st.session_state.get("authenticated") and not st.session_state.get("user_info"):
        st.session_state.user_info = {"id": f"demo-{uuid.uuid4().hex[:12]}", "email": "demo", "demo": True}


def leave_demo_agenda():
    st.session_state.direct_agenda = False
    if (st.session_state.get("user_info") or {}).get("demo"):
        st.session_state.user_info = None
    st.query_params.clear()


def go_home():
    st.session_state.current_view = "home"


def show_auth_msg():
    msg = st.session_state.get("auth_msg")
    if not msg:
        return
    kind, text = msg[0], msg[1]
    if kind == "success":
        st.markdown(
            f"""
                <div class="pavel-auth-success-card">
                    <div style="font-size: 1.8rem; background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); 
                                border-radius: 50%; width: 42px; height: 42px; display: flex; 
                                align-items: center; justify-content: center; box-shadow: 0 0 10px rgba(236,72,153,0.6);">
                        ✨
                    </div>
                    <div>
                        <strong style="color: #FFFFFF; font-size: 0.95rem; display: block; margin-bottom: 2px;">
                            Vérification requise
                        </strong>
                        <span style="color: #CBD5E1; font-size: 0.85rem;">
                            {esc(text)}
                        </span>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )
    elif kind in ("error", "warning", "info"):
        getattr(st, kind)(text)
    else:
        st.error(text)


# ── Alarmes : événements mis en cache 30 s (évite une lecture à chaque clic) ─
def _alarm_events(user_id):
    cache = st.session_state.get("_alarm_cache")
    now = time.time()
    if cache and cache.get("uid") == user_id and now - cache.get("t", 0) < ALARM_CACHE_TTL:
        return cache["events"]
    events = load_events_from_db(user_id)
    st.session_state["_alarm_cache"] = {"uid": user_id, "t": now, "events": events}
    return events


def _sync_alarm_cache():
    """Après l'Agenda (qui vient de recharger les événements), on réutilise ces données."""
    user = st.session_state.get("user_info")
    if user:
        st.session_state["_alarm_cache"] = {
            "uid": user["id"],
            "t": time.time(),
            "events": list(st.session_state.get("agenda_events", [])),
        }


def run_background_alarms():
    user = st.session_state.get("user_info")
    if not user:
        return
    try:
        from modules.notifier import render_notifier
        with st.container(key="pc_engine"):
            st.markdown(ENGINE_CSS, unsafe_allow_html=True)
            render_notifier(_alarm_events(user["id"]), show_panel=False)
    except Exception as exc:
        st.session_state["alarm_engine_error"] = str(exc)
        logging.exception("Erreur dans le moteur d'alarmes d'arrière-plan")


if st.session_state.get("flash"):
    st.toast(st.session_state.pop("flash"))


# ── Recherche globale isolée ──────────────────────────────
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

    def items(key):
        return ss.get(key) or []

    def has(value) -> bool:
        return q in str(value or "").lower()

    def card(badge, title, extra=""):
        st.markdown(
            f'<div class="zapio-card"><span class="zapio-badge">{esc(badge)}</span>'
            f'<h4 style="margin-top:5px;">{esc(title)}</h4>{extra}</div>',
            unsafe_allow_html=True,
        )

    prompts = [p for p in items("saved_prompts_library")
               if has(p.get("title")) or has(p.get("prompt")) or has(p.get("category"))]
    if prompts:
        st.markdown("#### 🧠 Prompts & IA")
        for it in prompts:
            count += 1
            card(it.get("category", ""), it.get("title", ""))
            st.code(it.get("prompt", ""), language="markdown")

    files = [f for f in items("saved_media_files")
             if has(f.get("title")) or has(f.get("filename")) or has(f.get("type")) or has(f.get("desc"))]
    if files:
        st.markdown("#### 📁 Médias & Fichiers")
        for it in files:
            count += 1
            card(it.get("type", ""), it.get("title", ""))

    events = [e for e in items("agenda_events")
              if has(e.get("title")) or has(e.get("desc")) or has(e.get("category"))]
    if events:
        st.markdown("#### 📅 Agenda & Événements")
        for it in events:
            count += 1
            card(it.get("category") or "Général", it.get("title", ""),
                 f'<p>Date: {esc(it.get("date", ""))} à {esc(it.get("time", ""))}</p>')

    contacts = [c for c in items("saved_contacts")
                if has(c.get("name")) or has(c.get("email")) or has(c.get("phone")) or has(c.get("notes"))]
    if contacts:
        st.markdown("#### 🎴 Contacts")
        for it in contacts:
            count += 1
            card(it.get("cat") or "Contact", it.get("name", ""),
                 f'<p>📧 {esc(it.get("email"))} | 📞 {esc(it.get("phone"))}</p>')

    projects = [p for p in items("saved_current_projects") + items("saved_future_projects")
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

# ── AGENDA DÉMO ───────────────────────────────────────────
if is_direct_agenda_link or st.session_state.get("direct_agenda", False):
    # Lien direct ?app=agenda sans session : on attribue aussi un identifiant démo privé
    if not st.session_state.get("authenticated") and not st.session_state.get("user_info"):
        st.session_state.user_info = {"id": f"demo-{uuid.uuid4().hex[:12]}", "email": "demo", "demo": True}

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
        f'<div style="margin-top: 10px;"><span class="zapio-badge">🔮 Workspace Centralisé & Sécurisé (Supabase Auth)</span></div></div>',
        unsafe_allow_html=True,
    )

    _, col_top_btn, _ = st.columns([1, 2, 1])
    with col_top_btn:
        st.button(
            "📅 Accéder directement à l'Agenda (Hors-ligne / Démo)",
            key="btn_direct_agenda_top",
            use_container_width=True, type="secondary", on_click=go_direct_agenda,
        )
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown(AUTH_SWITCH_CSS, unsafe_allow_html=True)
        mode = st.session_state.auth_mode

        with st.container(key="auth_switch"):
            b1, b2 = st.columns(2)
            with b1:
                st.button(
                    "🔑 Connexion", key="btn_mode_login", use_container_width=True,
                    type="primary" if mode == "login" else "secondary",
                    on_click=set_auth_mode, args=("login",),
                )
            with b2:
                st.button(
                    "✨ Inscription", key="btn_mode_signup", use_container_width=True,
                    type="primary" if mode == "signup" else "secondary",
                    on_click=set_auth_mode, args=("signup",),
                )

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        if mode == "login":
            with st.form("login_form"):
                st.text_input("Adresse Email", placeholder="votre.email@exemple.com", key="login_email")
                st.text_input("Mot de passe", type="password", placeholder="••••••••", key="login_pass")
                st.form_submit_button(
                    "Se connecter au Workspace", use_container_width=True, on_click=do_login
                )
        else:
            with st.form("signup_form"):
                st.text_input("Adresse Email", placeholder="nom@exemple.com", key="signup_email")
                st.text_input("Créer un mot de passe", type="password", placeholder="••••••••", key="signup_pass")
                st.text_input("Confirmer le mot de passe", type="password", placeholder="••••••••", key="signup_confirm_pass")
                st.form_submit_button(
                    "S'inscrire et rejoindre PavelCore", use_container_width=True, on_click=do_signup
                )

        show_auth_msg()

# ── APPLICATION (utilisateur connecté) ────────────────────
else:
    # Styles des cartes (bienvenue, Coffre-Fort) : conteneur invisible, sans espace ajouté
    with st.container(key="pc_css"):
        st.markdown(APP_CSS, unsafe_allow_html=True)

    col_logo, col_user, col_logout = st.columns([2, 2, 1])
    with col_logo:
        st.markdown(
            f'<h1 style="font-size: 1.3rem; margin: 0; display: flex; align-items: center; gap: 6px;">'
            f'<span style="color: {text_color};">pavel</span>'
            f'<span style="background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); color: #FFF; '
            f'padding: 2px 6px; border-radius: 6px; font-size: 0.85rem;">CORE</span>'
            f'<span class="zapio-badge-green" style="font-size: 0.55rem;">● Live (Supabase)</span></h1>',
            unsafe_allow_html=True,
        )
    with col_user:
        email = (st.session_state.get("user_info") or {}).get("email", "Membre")
        st.markdown(
            f'<div style="text-align: center; color: {desc_color}; font-size: 0.85rem; padding-top: 5px;">'
            f'👤 Connecté en tant que : <strong style="color: {sub_title_color};">{esc(email)}</strong></div>',
            unsafe_allow_html=True,
        )
    with col_logout:
        st.button("🔒 Déconnexion", use_container_width=True, type="secondary", on_click=do_logout)

    st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 15px 0;'>", unsafe_allow_html=True)

    if st.session_state.get("welcome_banner_msg"):
        welcome_text = st.session_state.pop("welcome_banner_msg")
        st.markdown(
            f"""
            <div class="pavel-welcome-wrap">
            <div id="pavel-welcome-toast" class="pavel-login-success-banner">
                <div style="font-size: 2.2rem; background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); 
                            border-radius: 14px; width: 52px; height: 52px; display: flex; 
                            align-items: center; justify-content: center; box-shadow: 0 0 15px rgba(236,72,153,0.6);
                            border: 1px solid rgba(255,255,255,0.4);">
                    🔓
                </div>
                <div style="flex-grow: 1;">
                    <span class="zapio-badge" style="margin-bottom: 4px; display: inline-block;">✨ Authentification Réussie</span>
                    <h3 style="color: #FFFFFF; margin: 0 0 2px 0; font-size: 1.15rem;">Connexion établie</h3>
                    <p style="color: #CBD5E1; font-size: 0.86rem; margin: 0;">{esc(welcome_text)}</p>
                </div>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_global_search()

    current = st.session_state.get("current_view", "home")
    if current not in VALID_VIEWS:
        current = "home"
        st.session_state.current_view = "home"

    if current != "Agenda":
        run_background_alarms()

    if current == "home":
        _view("home_view", "render_home_view")()
        _view("backup_view", "render_backup_view")(sub_title_color)
    else:
        st.button("← Retour au Tableau de Bord", key="back_to_home_universal",
                  type="secondary", on_click=go_home)

        if current == "Coffre-Fort":
            st.markdown(
                """
                <div class="pavel-vault-success-banner">
                    <div style="font-size: 2.5rem; background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); 
                                border-radius: 14px; width: 60px; height: 60px; display: flex; 
                                align-items: center; justify-content: center; box-shadow: 0 0 20px rgba(236,72,153,0.7);
                                border: 1px solid rgba(255,255,255,0.4);">
                        🔐
                    </div>
                    <div style="flex-grow: 1;">
                        <span class="zapio-badge" style="margin-bottom: 6px; display: inline-block;">🔒 Accès Sécurisé & Chiffré</span>
                        <h3 style="color: #FFFFFF; margin: 0 0 4px 0; font-size: 1.25rem;">Coffre-Fort Déverrouillé avec Succès</h3>
                        <p style="color: #CBD5E1; font-size: 0.88rem; margin: 0;">
                            Vos clés API, mots de passe et secrets sont protégés par un cryptage robuste et des verrous inviolables.
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(f"<h2 style='color: #EC4899; margin-top: 15px;'>Espace : {esc(current)}</h2>", unsafe_allow_html=True)

        if current == "Agenda":
            _view("agenda_view", "render_agenda_view")(
                sub_title_color, card_bg, card_border, header_box_bg, header_box_text, text_color)
            _sync_alarm_cache()
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
