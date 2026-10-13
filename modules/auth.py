import logging
import time
import streamlit as st
from modules.supabase_client import supabase

# ⚠️ `supabase` est un client partagé par tous les utilisateurs de l'application.
# Ne l'utilisez QUE pour l'authentification : sign_in_with_password y mémorise la session
# du dernier connecté. Pour lire/écrire des données, il faudra un client par session.


def _signup_error(exc: Exception) -> str:
    msg = str(exc).lower()
    if "already" in msg or "registered" in msg:
        return "Cette adresse e-mail est déjà utilisée."
    if "password" in msg and any(w in msg for w in ("weak", "least", "short", "characters")):
        return "Mot de passe trop faible : utilisez au moins 8 caractères avec lettres et chiffres."
    if "rate" in msg or "too many" in msg or "429" in msg:
        return "Trop de demandes. Patientez quelques minutes avant de réessayer."
    if "invalid" in msg and "email" in msg:
        return "Adresse e-mail invalide."
    return "Inscription impossible pour le moment. Réessayez dans quelques instants."


def supabase_signup(email: str, password: str):
    """Inscription via Supabase Auth (déclenche l'e-mail de confirmation si activé)."""
    if not supabase:
        return False, "Service d'authentification indisponible."
    try:
        response = supabase.auth.sign_up({"email": email.strip().lower(), "password": password})
        if getattr(response, "session", None):
            return True, "✨ Inscription réussie ! Vous pouvez vous connecter."
        return True, ("✨ Inscription réussie ! Un e-mail de confirmation vous a été envoyé. "
                      "Veuillez vérifier votre boîte de réception.")
    except Exception as exc:
        logging.warning("Échec d'inscription Supabase (%s) : %s", type(exc).__name__, str(exc)[:160])
        return False, _signup_error(exc)


def _is_timeout(exc: Exception) -> bool:
    msg = str(exc).lower()
    return (type(exc).__name__ in ("ReadTimeout", "ConnectTimeout", "TimeoutException", "PoolTimeout")
            or "timed out" in msg or "timeout" in msg)


def supabase_login(email: str, password: str):
    """Connexion via Supabase Auth (un nouvel essai automatique en cas de délai dépassé)."""
    if not supabase:
        return False, "Service d'authentification indisponible."

    last_exc = None
    for attempt in range(2):
        try:
            response = supabase.auth.sign_in_with_password(
                {"email": email.strip().lower(), "password": password}
            )
            user = getattr(response, "user", None)
            if not user:
                return False, "Identifiants invalides ou e-mail non confirmé."
            return True, {"id": str(user.id), "email": user.email}
        except Exception as exc:
            last_exc = exc
            if attempt == 0 and _is_timeout(exc):
                logging.warning("Connexion Supabase : délai dépassé, nouvel essai")
                time.sleep(1.0)
                continue
            break

    logging.warning("Échec de connexion Supabase (%s) : %s", type(last_exc).__name__, str(last_exc)[:160])
    msg = str(last_exc).lower()
    if "rate" in msg or "too many" in msg or "429" in msg:
        return False, "Trop de tentatives. Patientez quelques minutes avant de réessayer."
    if _is_timeout(last_exc) or any(w in msg for w in ("connection", "network", "getaddrinfo", "resolution")):
        return False, ("Le service d'authentification ne répond pas. Réessayez dans un instant "
                       "(si cela persiste, vérifiez que le projet Supabase n'est pas en pause).")
    return False, "Identifiants invalides ou e-mail non confirmé."


def supabase_logout():
    """Révoque la session Supabase côté serveur (appelée à la déconnexion)."""
    if not supabase:
        return
    try:
        supabase.auth.sign_out()
    except Exception:
        logging.warning("Déconnexion Supabase : échec silencieux")
