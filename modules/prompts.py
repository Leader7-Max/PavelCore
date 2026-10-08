import streamlit as st

def render_prompts_module():
    st.markdown("""
        <div style="margin-bottom: 25px;">
            <h2 style="color: #00F2FE; margin-bottom: 0;">⚡ Gestionnaire de Prompts & Code</h2>
            <p style="color: #8E9BAE; font-size: 0.9rem;">Sauvegarde, organise et copie tes snippets et instructions en un clic.</p>
        </div>
    """, unsafe_allow_html=True)

    # Base de données temporaire en session (à connecter avec Supabase)
    if "snippets" not in st.session_state:
        st.session_state.snippets = [
            {
                "id": 1,
                "title": "Prompt Génération Logo Neon",
                "category": "Prompt LLM",
                "content": "Create a modern minimalist vector logo for a tech app named 'PavelCore'. Cyberpunk style, neon cyan and deep purple color palette, dark dark background, sleek lines, 8k resolution --ar 1:1",
                "tags": ["Midjourney", "Design", "Logo"]
            },
            {
                "id": 2,
                "title": "Connexion Supabase Python",
                "category": "Python",
                "content": "from supabase import create_client, Client\n\nurl: str = st.secrets['SUPABASE_URL']\nkey: str = st.secrets['SUPABASE_KEY']\nsupabase: Client = create_client(url, key)",
                "tags": ["Backend", "Database", "API"]
            }
        ]

    # Formulaire d'ajout dans un Expandable
    with st.expander("➕ Ajouter un nouveau Prompt / Snippet Code"):
        with st.form("add_snippet_form"):
            title = st.text_input("Titre de la ressource", placeholder="ex: Script de sauvegarde SQL")
            category = st.selectbox("Langage / Catégorie", ["Python", "JavaScript", "SQL", "HTML/CSS", "Prompt LLM", "Prompt Midjourney", "Autre"])
            tags_input = st.text_input("Tags (séparés par des virgules)", placeholder="ex: Midjourney, Design, UI")
            content = st.text_area("Contenu du Code ou du Prompt", height=150, placeholder="Colle ton code ou ton prompt ici...")
            
            submitted = st.form_submit_button("Sauvegarder dans PavelCore")
            
            if submitted:
                if title and content:
                    new_item = {
                        "id": len(st.session_state.snippets) + 1,
                        "title": title,
                        "category": category,
                        "content": content,
                        "tags": [t.strip() for t in tags_input.split(",")] if tags_input else []
                    }
                    st.session_state.snippets.append(new_item)
                    st.toast("Snippet enregistré avec succès !", icon="🔐")
                    st.rerun()
                else:
                    st.error("Le titre et le contenu sont obligatoires.")

    st.markdown("---")

    # Barre de recherche et filtres
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("🔍 Rechercher par titre, tag ou contenu...", placeholder="Tape un mot-clé...")
    with col_filter:
        selected_cat = st.selectbox("Filtrer par catégorie", ["Toutes"] + ["Python", "JavaScript", "SQL", "HTML/CSS", "Prompt LLM", "Prompt Midjourney", "Autre"])

    # Affichage des éléments
    filtered_snippets = st.session_state.snippets

    if selected_cat != "Toutes":
        filtered_snippets = [s for s in filtered_snippets if s["category"] == selected_cat]

    if search_query:
        query = search_query.lower()
        filtered_snippets = [
            s for s in filtered_snippets 
            if query in s["title"].lower() or query in s["content"].lower() or any(query in t.lower() for t in s["tags"])
        ]

    st.markdown(f"**{len(filtered_snippets)}** ressource(s) trouvée(s)")

    # Boucle d'affichage des cartes
    for item in filtered_snippets:
        st.markdown(f"""
            <div class="glass-card" style="padding: 18px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <h4 style="color: #00F2FE; margin: 0;">{item['title']}</h4>
                    <span class="badge">{item['category']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Affichage avec coloration syntaxique selon la catégorie
        lang = "python" if item["category"] == "Python" else ("javascript" if item["category"] == "JavaScript" else "text")
        st.code(item["content"], language=lang)
        
        # Tags sous le bloc de code
        if item["tags"]:
            tags_html = " ".join([f"<span style='color: #8E9BAE; font-size: 0.8rem; margin-right: 8px;'>#{t}</span>" for t in item["tags"]])
            st.markdown(tags_html, unsafe_allow_html=True)
