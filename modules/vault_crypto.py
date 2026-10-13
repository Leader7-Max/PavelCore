import base64
import hashlib
import hmac
import os
import streamlit as st

PREFIX = "enc:v1:"


class VaultKeyError(RuntimeError):
    """Clé de chiffrement absente, trop courte ou bibliothèque manquante."""


def _master_key() -> bytes:
    key = None
    try:
        key = st.secrets.get("VAULT_MASTER_KEY")
    except Exception:
        key = None
    key = key or os.environ.get("VAULT_MASTER_KEY")
    if not key or len(str(key)) < 24:
        raise VaultKeyError(
            "La clé de chiffrement VAULT_MASTER_KEY est absente ou trop courte "
            "(24 caractères minimum). Ajoutez-la dans les Secrets de l'application."
        )
    return str(key).encode("utf-8")


def _fernet(user_id):
    try:
        from cryptography.fernet import Fernet
    except ImportError as exc:
        raise VaultKeyError(
            "Le paquet `cryptography` n'est pas installé. Ajoutez-le à requirements.txt."
        ) from exc
    # Clé dérivée par utilisateur : une ligne copiée vers un autre compte reste illisible
    derived = hmac.new(_master_key(), f"pavelcore-vault:{user_id}".encode("utf-8"), hashlib.sha256).digest()
    return Fernet(base64.urlsafe_b64encode(derived))


def vault_status():
    """Retourne (ok, message) : le chiffrement est-il opérationnel ?"""
    try:
        _fernet("check")
        return True, ""
    except VaultKeyError as exc:
        return False, str(exc)


def is_encrypted(value) -> bool:
    return isinstance(value, str) and value.startswith(PREFIX)


def encrypt_secret(user_id, plaintext: str) -> str:
    token = _fernet(user_id).encrypt(str(plaintext).encode("utf-8")).decode("utf-8")
    return PREFIX + token


def decrypt_secret(user_id, stored):
    """Retourne le texte clair, la valeur telle quelle si elle est ancienne (non chiffrée),
    ou None si le déchiffrement est impossible."""
    if stored is None:
        return ""
    if not is_encrypted(stored):
        return stored
    try:
        return _fernet(user_id).decrypt(stored[len(PREFIX):].encode("utf-8")).decode("utf-8")
    except Exception:
        return None
