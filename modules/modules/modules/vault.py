import streamlit as st

def render_vault():
    st.markdown("""
        <div style="margin-bottom: 20px;">
            <h2 style="color: #00F2FE; margin:0;">🔐 Coffre-Fort, Mails & Contacts</h2>
            <p style="color: #8E9BAE;">Espace sécurisé pour documents importants, identifiants et carnet d'adresses.</p>
        </div>
    """, unsafe_allow_html=True)

    if "vault_items" not in st.session_state:
        st.session_state.vault_items = []

    tab1, tab2 = st.tabs(["📄 Documents & Notes Secrètes", "🎇 Contacts Privés"])

    with tab1:
        with st.form("add_vault_item"):
            item_name = st.text_input("Intitulé du document / Note")
            item_secret = st.text_area("Contenu sensible / Code d'accès")
            if st.form_submit_button("Ajouter au Coffre Fort"):
                if item_name and item_secret:
                    st.session_state.vault_items.append({"title": item_name, "content": item_secret})
                    st.toast("Élément sécurisé ajouté !", icon="🔐")
                    st.rerun()

        st.markdown("### Vos Éléments Sécurisés")
        for item in st.session_state.vault_items:
            with st.expander(f"🔒 {item['title']}"):
                st.code(item['content'], language="text")

    with tab2:
        st.info("Section Annuaire de contacts d'urgence & VIP.")
