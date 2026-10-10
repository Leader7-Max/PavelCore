from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

def load_or_create_key():
    """Charge la clé de chiffrement ou en génère une nouvelle si elle n'existe pas."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

def encrypt_data(plain_text):
    """Chiffre un texte sensible (mot de passe, clé API)."""
    if not plain_text:
        return ""
    key = load_or_create_key()
    f = Fernet(key)
    encrypted_token = f.encrypt(plain_text.encode())
    return encrypted_token.decode()

def decrypt_data(encrypted_text):
    """Déchiffre un texte pour l'afficher ou l'utiliser."""
    if not encrypted_text:
        return ""
    try:
        key = load_or_create_key()
        f = Fernet(key)
        decrypted_token = f.decrypt(encrypted_text.encode())
        return decrypted_token.decode()
    except Exception:
        return "Erreur de déchiffrement"
