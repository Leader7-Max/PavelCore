import streamlit as st
import os

def render_media_view(sub_title_color="#FFF", uploads_dir="uploaded_files"):
    """Gère l'affichage et l'upload des médias, fichiers et liens externes."""
    
    st.markdown(f'''
        <div class="sub-section-header">
            <span class="zapio-badge">STOCKAGE & RESSOURCES</span>
            <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">📁 Images, ZIP, APK & Documents</h1>
        </div>
    ''', unsafe_allow_html=True)

    sub_tab = st.pills(
        "Type de fichier",
        options=["📤 Envoyer un fichier", "🔗 Lien externe (Drive, Web)"],
        default="📤 Envoyer un fichier",
        label_visibility="collapsed"
    )

    if sub_tab == "📤 Envoyer un fichier":
        uploaded_file = st.file_uploader(
            "Choisissez un fichier à sauvegarder (Images, ZIP, APK, PDFs, DOCX, TXT...)",
            type=["png", "jpg", "jpeg", "gif", "zip", "rar", "apk", "pdf", "docx", "txt", "csv"]
        )
        file_title = st.text_input("Nom / Titre personnalisé pour le fichier")
        file_category = st.selectbox("Catégorie de fichier", ["🖼️ Images & Visuels", "📦 Fichiers ZIP / Archives", "📱 Applications APK", "📄 Documents & PDFs", "🔗 Liens Utiles"])

        if st.button("💾 Enregistrer le fichier"):
            if uploaded_file is not None and file_title:
                os.makedirs(uploads_dir, exist_ok=True)
                file_path = os.path.join(uploads_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                st.session_state.saved_media_files.append({
                    "title": file_title,
                    "filename": uploaded_file.name,
                    "path": file_path,
                    "size": f"{round(uploaded_file.size / (1024 * 1024), 2)} MB",
                    "type": file_category,
                    "is_local": True
                })
                st.toast("📁 Fichier sauvegardé avec succès !", icon="✅")
                st.rerun()
            else:
                st.warning("Veuillez charger un fichier et renseigner un titre.")

    elif sub_tab == "🔗 Lien externe (Drive, Web)":
        with st.form("form_external_link", clear_on_submit=True):
            ext_title = st.text_input("Titre du lien ou fichier")
            ext_url = st.text_input("URL directe (ex: Google Drive, Dropbox, Lien web)")
            ext_cat = st.selectbox("Catégorie", ["🖼️ Images & Visuels", "📦 Fichiers ZIP / Archives", "📱 Applications APK", "📄 Documents & PDFs", "🔗 Liens Utiles"])
            ext_desc = st.text_area("Description du fichier")
            if st.form_submit_button("Enregistrer le lien"):
                if ext_title and ext_url:
                    st.session_state.saved_media_files.append({
                        "title": ext_title,
                        "url": ext_url,
                        "desc": ext_desc,
                        "type": ext_cat,
                        "is_local": False
                    })
                    st.toast("🔗 Lien sauvegardé avec succès !", icon="✅")
                    st.rerun()

    st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 25px 0;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{sub_title_color};'>📚 Fichiers & Médias Enregistrés</h3>", unsafe_allow_html=True)

    if not st.session_state.saved_media_files:
        st.info("Aucun fichier n'a été enregistré pour le moment.")

    for item in st.session_state.saved_media_files:
        st.markdown(f'''
            <div class="zapio-card">
                <span class="zapio-badge" style="font-size:0.7rem;">{item["type"]}</span>
                <h3 style="color:{sub_title_color}; margin-top:5px;">{item["title"]}</h3>
        ''', unsafe_allow_html=True)

        if item.get("is_local", False):
            st.caption(f"Fichier : {item['filename']} | Taille : {item['size']}")
            if os.path.exists(item["path"]):
                with open(item["path"], "rb") as file_data:
                    st.download_button(
                        label=f"📥 Télécharger {item['filename']}",
                        data=file_data,
                        file_name=item["filename"],
                        use_container_width=True
                    )
        else:
            st.write(f"Description : {item.get('desc', '')}")
            st.markdown(f'<a href="{item["url"]}" target="_blank" style="color:#EC4899; font-weight:600;">🌐 Ouvrir / Télécharger via le lien</a>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
