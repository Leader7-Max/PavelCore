import streamlit as st
from modules.supabase_client import supabase

def supabase_signup(email: str, password: str):
    """Inscription via Supabase Auth (déclenche l'e-mail de confirmation si activé)"""
    if not supabase:
        return False, "Client Supabase non initialisé."
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        # Si Supabase renvoie un utilisateur sans session immédiate, c'est qu'une confirmation par e-mail est requise
        return True, "✨ Inscription réussie ! Un e-mail de confirmation vous a été envoyé. Veuillez vérifier votre boîte de réception."
    except Exception as e:
        return False, f"Erreur d'inscription : {str(e)}"

def supabase_login(email: str, password: str):
    """Connexion via Supabase Auth"""
    if not supabase:
        return False, "Client Supabase non initialisé."
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user_info = {
            "id": response.user.id,
            "email": response.user.email
        }
        return True, user_info
    except Exception as e:
        return False, "Identifiants invalides ou e-mail non confirmé."
