import streamlit as st
from modules.security import encrypt_data, decrypt_data
from modules.database import (
    load_api_keys_from_db, add_api_key_to_db,
    load_credentials_from_db, add_credential_to_db,
    load_contacts_from_db, add_contact_to_db
)

def render_vault_view(sub_title_color="#FFF", desc_color="#CBD5E1"):
    """Gère le coffre-fort sécurisé (Clés API et Mots de passe) connecté à SQLite."""
    sub_tab = st.pills(
        "Navigation Coffre-Fort",
        options=["🔐 Clés API", "🔑 Identifiants & Mots de passe"],
        default="🔐 Clés API",
        label_visibility="collapsed",
        key="pills_vault"
    )
    
    if sub_tab == "🔐 Clés API":
        st.markdown(f'''
            <div class="sub-section-header">
                <span class="zapio-badge">SÉCURITÉ & CREDENTIALS</span>
                <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🔐 Clés d'API & Tokens</h1>
            </div>
        ''', unsafe_allow_html=True)
        
        with st.form("form_api_keys", clear_on_submit=True):
            service = st.text_input("Nom du Service (ex: OpenAI, GitHub)")
            api_key = st.text_input("Clé API / Token Secret", type="password")
            if st.form_submit_button("🔒 Sauvegarder la clé"):
                if service and api_key:
                    encrypted_key = encrypt_data(api_key)
                    add_api_key_to_db(service, encrypted_key)
                    st.session_state.saved_api_keys = load_api_keys_from_db()
                    st.toast("🔐 Clé API chiffrée et sauvegardée en base !", icon="✅")
                    st.rerun()
                else:
                    st.warning("Veuillez remplir tous les champs.")
                    
        for ak in st.session_state.saved_api_keys:
            decrypted_key = decrypt_data(ak['key'])
            st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{ak["service"]}</h3>', unsafe_allow_html=True)
            st.code(decrypted_key, language='text')
            st.markdown('</div>', unsafe_allow_html=True)

    elif sub_tab == "🔑 Identifiants & Mots de passe":
        st.markdown(f'''
            <div class="sub-section-header">
                <span class="zapio-badge">GESTIONNAIRE D'ACCÈS</span>
                <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🔑 Identifiants & Mots de passe</h1>
            </div>
        ''', unsafe_allow_html=True)
        
        with st.form("form_creds", clear_on_submit=True):
            site = st.text_input("Plateforme / Site web")
            username = st.text_input("Identifiant / Email")
            password = st.text_input("Mot de passe", type="password")
            if st.form_submit_button("Enregistrer les accès"):
                if site and username and password:
                    encrypted_password = encrypt_data(password)
                    add_credential_to_db(site, username, encrypted_password)
                    st.session_state.saved_user_credentials = load_credentials_from_db()
                    st.toast("🔑 Identifiants chiffrés et enregistrés en base !", icon="✅")
                    st.rerun()
                else:
                    st.warning("Veuillez remplir tous les champs.")
                    
        for uc in st.session_state.saved_user_credentials:
            decrypted_password = decrypt_data(uc['pass'])
            st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{uc["site"]}</h3><p style="color:{desc_color};"><b>Identifiant:</b> {uc["user"]}</p>', unsafe_allow_html=True)
            st.code(decrypted_password, language='text')
            st.markdown('</div>', unsafe_allow_html=True)

def render_contacts_view(sub_title_color="#FFF", desc_color="#CBD5E1"):
    """Gère le carnet de contacts connecté à SQLite."""
    sub_tab = st.pills(
        "Navigation Contacts",
        options=["🎴 Carnet de Contacts", "📧 Modèles d'Emails & Scripts"],
        default="🎴 Carnet de Contacts",
        label_visibility="collapsed",
        key="pills_contacts"
    )
    
    if sub_tab == "🎴 Carnet de Contacts":
        st.markdown(f'''
            <div class="sub-section-header">
                <span class="zapio-badge">RÉPERTOIRE PROFESSIONNEL</span>
                <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🎴 Carnet de Contacts</h1>
            </div>
        ''', unsafe_allow_html=True)
        
        with st.form("form_contacts", clear_on_submit=True):
            fullname = st.text_input("Nom & Prénom / Entreprise")
            email_contact = st.text_input("Adresse Email")
            phone = st.text_input("Numéro de Téléphone")
            category = st.selectbox("Catégorie", ["Client", "Partenaire / Prestataire", "VIP", "Personnel"])
            notes = st.text_area("Notes / Rôle")
            if st.form_submit_button("Ajouter le contact"):
                if fullname:
                    add_contact_to_db(fullname, email_contact, phone, category, notes)
                    st.session_state.saved_contacts = load_contacts_from_db()
                    st.toast("🎴 Contact sauvegardé en base !", icon="✅")
                    st.rerun()
                else:
                    st.warning("Veuillez renseigner au moins le nom du contact.")
                    
        for ct in st.session_state.saved_contacts:
            st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{ct["name"]} <span class="zapio-badge" style="font-size:0.7rem;">{ct["cat"]}</span></h3><p style="color:{desc_color};">📧 {ct["email"]} | 📞 {ct["phone"]}</p><p style="color:{desc_color}; font-size:0.85rem;">{ct["notes"]}</p></div>', unsafe_allow_html=True)

    elif sub_tab == "📧 Modèles d'Emails & Scripts":
        st.markdown(f'''
            <div class="sub-section-header">
                <span class="zapio-badge">COMMUNICATION & TEMPLATES</span>
                <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">📧 Modèles d'Emails & Scripts</h1>
            </div>
        ''', unsafe_allow_html=True)
        # (Tu peux également connecter cette partie à SQLite si tu le souhaites par la suite)
        st.info("Module de templates d'emails actif.")
