import os
import streamlit as st
from supabase import create_client, Client

# Récupération des clés depuis les secrets Streamlit (ou variables d'environnement)
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", ""))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", ""))

@st.cache_resource
def init_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("⚠️ Les clés Supabase (SUPABASE_URL et SUPABASE_KEY) ne sont pas configurées.")
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()
