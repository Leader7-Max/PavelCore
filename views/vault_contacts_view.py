import streamlit as st
from modules.security import encrypt_data, decrypt_data

def render_vault_view(sub_title_color="#FFF", desc_color="#CBD5E1"):
    """Gère le coffre-fort sécurisé (Clés API et Mots de passe) avec chiffrement."""
    sub_tab = st.pills(
        "Navigation Coffre-Fort",
        options=["🔐 Clés API", "🔑 Identifiants & Mots de passe"],
        default="🔐 Clés API",
        label_visibility="collapsed",
        key="pills_vault"
    )
    
    # Initialisation sécurisée dans l'état si non existant
    if "saved_api_keys" not in st.session_state:
        st.session_state.saved_api_keys = []
    if "saved_user_credentials" not in st.session_state:
        st.session_state.saved_user_credentials = []

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
                    # Chiffrement de la clé API avant stockage
                    encrypted_key = encrypt_data(api_key)
                    st.session_state.saved_api_keys.append({"service": service, "key": encrypted_key})
                    st.toast("🔐 Clé API chiffrée et sauvegardée en toute sécurité !", icon="✅")
                    st.rerun()
                else:
                    st.warning("Veuillez remplir tous les champs.")
                    
        for ak in st.session_state.saved_api_keys:
            # Déchiffrement de la clé à la volée pour l'affichage (ou masquage sécurisé)
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
                    # Chiffrement du mot de passe avant stockage
                    encrypted_password = encrypt_data(password)
                    st.session_state.saved_user_credentials.append({
                        "site": site, 
                        "user": username, 
                        "pass": encrypted_password
                    })
                    st.toast("🔑 Identifiants chiffrés et enregistrés avec succès !", icon="✅")
                    st.rerun()
                else:
                    st.warning("Veuillez remplir tous les champs.")
                    
        for uc in st.session_state.saved_user_credentials:
            # Déchiffrement du mot de passe à la volée
            decrypted_password = decrypt_data(uc['pass'])
            st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{uc["site"]}</h3><p style="color:{desc_color};"><b>Identifiant:</b> {uc["user"]}</p>', unsafe_allow_html=True)
            st.code(decrypted_password, language='text')
            st.markdown('</div>', unsafe_allow_html=True)

def render_contacts_view(sub_title_color="#FFF", desc_color="#CBD5E1"):
    """Gère le carnet de contacts et les modèles d'emails."""
    sub_tab = st.pills(
        "Navigation Contacts",
        options=["🎴 Carnet de Contacts", "📧 Modèles d'Emails & Scripts"],
        default="🎴 Carnet de Contacts",
        label_visibility="collapsed",
        key="pills_contacts"
    )
    
    # Initialisation sécurisée dans l'état si non existant
    if "saved_contacts" not in st.session_state:
        st.session_state.saved_contacts = []
    if "saved_email_templates" not in st.session_state:
        st.session_state.saved_email_templates = []

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
                    st.session_state.saved_contacts.append({
                        "name": fullname,
                        "email": email_contact,
                        "phone": phone,
                        "cat": category,
                        "notes": notes
                    })
                    st.toast("🎴 Contact sauvegardé !", icon="✅")
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
        
        with st.form("form_email_tpl", clear_on_submit=True):
            title = st.text_input("Titre du modèle (ex: Relance devis DJ, Prospection)")
            subject = st.text_input("Objet du mail")
            body = st.text_area("Corps du message / Script")
            if st.form_submit_button("Sauvegarder le modèle"):
                if title and body:
                    st.session_state.saved_email_templates.append({
                        "title": title,
                        "subject": subject,
                        "body": body
                    })
                    st.toast("📧 Modèle d'email sauvegardé !", icon="✅")
                    st.rerun()
                else:
                    st.warning("Veuillez renseigner le titre et le corps du message.")
                    
        for et in st.session_state.saved_email_templates:
            st.markdown(f'<div class="zapio-card"><h3 style="color:{sub_title_color};">{et["title"]}</h3><p style="color:{desc_color};"><b>Objet:</b> {et["subject"]}</p>', unsafe_allow_html=True)
            st.code(et['body'], language='markdown')
            st.markdown('</div>', unsafe_allow_html=True)
