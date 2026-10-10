import streamlit as st

def render_dev_ia_module():
    # Initialisation sécurisée des états de session si absents
    for key in ["saved_ai_prompts", "saved_claude_prompts", "saved_code_snippets"]:
        if key not in st.session_state:
            st.session_state[key] = []

    sub_tab = st.pills(
        "Navigation Dev",
        options=["🤖 Prompts AI Code", "🧠 Prompts Claude", "💻 Snippets Code"],
        default="🤖 Prompts AI Code",
        label_visibility="collapsed"
    )
    
    if sub_tab == "🤖 Prompts AI Code":
        st.markdown('''
            <div class="sub-section-header">
                <span class="zapio-badge">INTELLIGENCE ARTIFICIELLE</span>
                <h1 style="color: #FFF; font-size: 1.8rem; margin: 5px 0 0 0;">🤖 Prompts AI Code</h1>
            </div>
        ''', unsafe_allow_html=True)
        
        with st.form("form_ai_code", clear_on_submit=True):
            title = st.text_input("Titre")
            prompt = st.text_area("Contenu du Prompt")
            if st.form_submit_button("Enregistrer"):
                if title and prompt:
                    st.session_state.saved_ai_prompts.append({"title": title, "lang": "python", "prompt": prompt})
                    st.toast("🤖 Prompt IA enregistré !", icon="✅")
                    st.rerun()
                else:
                    st.warning("Veuillez remplir tous les champs.")

        for p in st.session_state.saved_ai_prompts:
            st.markdown(f'<div class="zapio-card"><h3 style="color:#FFF;">{p["title"]}</h3>', unsafe_allow_html=True)
            st.code(p['prompt'], language=p['lang'])
            st.markdown('</div>', unsafe_allow_html=True)

    elif sub_tab == "🧠 Prompts Claude":
        st.markdown('''
            <div class="sub-section-header">
                <span class="zapio-badge">EXPERTISE & SYSTEM PROMPTS</span>
                <h1 style="color: #FFF; font-size: 1.8rem; margin: 5px 0 0 0;">🧠 Prompts Claude</h1>
            </div>
        ''', unsafe_allow_html=True)
        
        with st.form("form_claude", clear_on_submit=True):
            title = st.text_input("Titre")
            user_prompt = st.text_area("User Prompt")
            if st.form_submit_button("Sauvegarder"):
                if title and user_prompt:
                    st.session_state.saved_claude_prompts.append({"title": title, "user": user_prompt})
                    st.toast("🧠 Prompt Claude sauvegardé !", icon="✅")
                    st.rerun()
                else:
                    st.warning("Veuillez remplir tous les champs.")

        for c in st.session_state.saved_claude_prompts:
            st.markdown(f'<div class="zapio-card"><h3 style="color:#FFF;">{c["title"]}</h3>', unsafe_allow_html=True)
            st.code(c['user'], language='python')
            st.markdown('</div>', unsafe_allow_html=True)

    elif sub_tab == "💻 Snippets Code":
        st.markdown('''
            <div class="sub-section-header">
                <span class="zapio-badge">BIBLIOTHÈQUE DE CODE</span>
                <h1 style="color: #FFF; font-size: 1.8rem; margin: 5px 0 0 0;">💻 Snippets de Code</h1>
            </div>
        ''', unsafe_allow_html=True)
        
        with st.form("form_code", clear_on_submit=True):
            title = st.text_input("Nom")
            code_content = st.text_area("Code")
            if st.form_submit_button("Enregistrer"):
                if title and code_content:
                    st.session_state.saved_code_snippets.append({"title": title, "code": code_content})
                    st.toast("💻 Snippet de code enregistré !", icon="✅")
                    st.rerun()
                else:
                    st.warning("Veuillez remplir tous les champs.")

        for cd in st.session_state.saved_code_snippets:
            st.markdown(f'<div class="zapio-card"><h3 style="color:#FFF;">{cd["title"]}</h3>', unsafe_allow_html=True)
            st.code(cd['code'], language='python')
            st.markdown('</div>', unsafe_allow_html=True)
