import streamlit as st

def render_dev_ia_view(sub_title_color="#FFF"):
    """Gère l'affichage de la bibliothèque de prompts et d'intelligence artificielle."""
    
    PROMPT_CATEGORIES = [
        "🎨 Génération d'images (Midjourney, DALL-E, Flux)",
        "✏️ Modification & Retouche d'images",
        "🤖 Développement & Code AI",
        "🧠 System Prompts (Claude & ChatGPT)",
        "🎵 Création Musicale & Paroles (Suno, Udio)",
        "📝 Rédaction de Contenu & Marketing"
    ]

    st.markdown(f'''
        <div class="sub-section-header">
            <span class="zapio-badge">INTELLIGENCE ARTIFICIELLE</span>
            <h1 style="color: {sub_title_color}; font-size: 1.8rem; margin: 5px 0 0 0;">🧠 Bibliothèque Centrale de Prompts IA</h1>
        </div>
    ''', unsafe_allow_html=True)
    
    with st.form("form_add_prompt", clear_on_submit=True):
        p_title = st.text_input("Titre du Prompt")
        p_cat = st.selectbox("Catégorie", PROMPT_CATEGORIES)
        p_content = st.text_area("Contenu du Prompt / Instruction")
        if st.form_submit_button("Enregistrer le Prompt"):
            if p_title and p_content:
                st.session_state.saved_prompts_library.append({
                    "title": p_title,
                    "category": p_cat,
                    "prompt": p_content
                })
                st.toast("🧠 Prompt enregistré avec succès !", icon="✅")
                st.rerun()
            else:
                st.warning("Veuillez renseigner un titre et un contenu.")

    st.markdown("<hr style='border-color: rgba(236,72,153,0.2); margin: 20px 0;'>", unsafe_allow_html=True)
    selected_cat_filter = st.selectbox("🔍 Filtrer par catégorie :", ["Tous les prompts"] + PROMPT_CATEGORIES)
    
    for pr in st.session_state.saved_prompts_library:
        if selected_cat_filter == "Tous les prompts" or pr["category"] == selected_cat_filter:
            st.markdown(f'''
                <div class="zapio-card">
                    <span class="zapio-badge" style="font-size: 0.7rem;">{pr["category"]}</span>
                    <h3 style="color:{sub_title_color}; margin-top: 5px;">{pr["title"]}</h3>
                </div>
            ''', unsafe_allow_html=True)
            st.code(pr["prompt"], language="markdown")
