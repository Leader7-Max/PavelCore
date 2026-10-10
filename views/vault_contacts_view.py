import streamlit as st
from modules.database import (
    load_api_keys_from_db, add_api_key_to_db,
    load_credentials_from_db, add_credential_to_db,
    load_contacts_from_db, add_contact_to_db
)

def render_vault_view(sub_title_color="#FFF", desc_color="#CBD5E1"):
    """Gère l'affichage et l'ajout sécurisé dans le Coffre-Fort cloisonné par utilisateur."""
    
    # Récupération sécurisée du user_id de la session
    user_id = st.session_state.user_info["id"] if st.session_state.get("user_info") else 0

    st.markdown(f"<h2 style='color: {sub_title_color}; margin-top: 10px;'>🔐 Coffre-Fort Sécurisé</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {desc_color};'>Stockez vos clés API et identifiants de manière chiffrée et isolée.</p>", unsafe_allow_html=True)

    # Rafraîchissement des données de l'utilisateur
    st.session_state.saved_api_keys = load_api_keys_from_db(user_id)
    st.session_state.saved_user_credentials = load_credentials_from_db(user_id)

    tab_api, tab_cred = st.tabs(["🔑 Clés API", "🔑 Identifiants & Mots de passe"])

    with tab_api:
        st.markdown("### Vos Clés API Enregistrées")
        if not st.session_state.saved_api_keys:
            st.info("Aucune clé API enregistrée.")
        else:
            for item in st.session_state.saved_api_keys:
                st.code(f"Service: {item['service']} | Clé: {item['key']}", language="text")

        st.markdown("---")
        st.markdown("### Ajouter une clé API")
        with st.form("api_key_form"):
            service_name = st.text_input("Nom du Service (ex: OpenAI, GitHub, Stripe)")
            api_key_val = st.text_input("Clé Secrète", type="password")
            submit_api = st.form_submit_button("Enregistrer la Clé API", use_container_width=True)
            if submit_api:
                if service_name.strip() and api_key_val.strip():
                    add_api_key_to_db(user_id, service_name, api_key_val)
                    st.session_state.saved_api_keys = load_api_keys_from_db(user_id)
                    st.toast("✅ Clé API enregistrée en toute sécurité.", icon="🔒")
                    st.rerun()
                else:
                    st.error("Tous les champs sont obligatoires.")

    with tab_cred:
        st.markdown("### Vos Identifiants Enregistrés")
        if not st.session_state.saved_user_credentials:
            st.info("Aucun identifiant enregistré.")
        else:
            for item in st.session_state.saved_user_credentials:
                st.markdown(f"- **{item['site']}** (Utilisateur : `{item['user']}`)")

        st.markdown("---")
        st.markdown("### Ajouter des identifiants")
        with st.form("cred_form"):
            site_name = st.text_input("Site / Application")
            username = st.text_input("Nom d'utilisateur / Email")
            password = st.text_input("Mot de passe", type="password")
            submit_cred = st.form_submit_button("Enregistrer les Identifiants", use_container_width=True)
            if submit_cred:
                if site_name.strip() and username.strip() and password.strip():
                    add_credential_to_db(user_id, site_name, username, password)
                    st.session_state.saved_user_credentials = load_credentials_from_db(user_id)
                    st.toast("✅ Identifiants enregistrés avec succès.", icon="🔒")
                    st.rerun()
                else:
                    st.error("Veuillez remplir tous les champs.")

def render_contacts_view(sub_title_color="#FFF", desc_color="#CBD5E1"):
    """Gère l'affichage et l'ajout dans le carnet de contacts cloisonné par utilisateur."""
    
    # Récupération sécurisée du user_id de la session
    user_id = st.session_state.user_info["id"] if st.session_state.get("user_info") else 0

    st.markdown(f"<h2 style='color: {sub_title_color}; margin-top: 10px;'>🎴 Contacts & Répertoire</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {desc_color};'>Gérez vos contacts professionnels et personnels.</p>", unsafe_allow_html=True)

    # Rafraîchissement des contacts de l'utilisateur
    st.session_state.saved_contacts = load_contacts_from_db(user_id)

    st.markdown("### Vos Contacts")
    if not st.session_state.saved_contacts:
        st.info("Aucun contact enregistré.")
    else:
        for c in st.session_state.saved_contacts:
            st.markdown(f"""
                <div style="background-color: #170A2E; border: 1px solid #2B1552; padding: 12px; border-radius: 8px; margin-bottom: 8px;">
                    <h4 style="margin: 0; color: {sub_title_color};">{c['name']} <span style="font-size: 0.8rem; background: #8B5CF6; color: #FFF; padding: 2px 6px; border-radius: 4px;">{c['cat']}</span></h4>
                    <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #CBD5E1;">📧 {c['email']} | 📞 {c['phone']}</p>
                    <p style="margin: 3px 0 0 0; font-size: 0.85rem; color: #94A3B8;">📝 {c['notes']}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Ajouter un Contact")
    with st.form("contact_form"):
        name = st.text_input("Nom complet")
        email = st.text_input("Adresse Email")
        phone = st.text_input("Numéro de Téléphone")
        category = st.selectbox("Catégorie", ["Client", "Partenaire", "Prestataire", "Personnel", "Autre"])
        notes = st.text_area("Notes / Remarques")
        submit_contact = st.form_submit_button("Enregistrer le Contact", use_container_width=True)
        
        if submit_contact:
            if name.strip():
                add_contact_to_db(user_id, name, email, phone, category, notes)
                st.session_state.saved_contacts = load_contacts_from_db(user_id)
                st.toast("✅ Contact enregistré avec succès !", icon="🎴")
                st.rerun()
            else:
                st.error("Le nom du contact est obligatoire.")
