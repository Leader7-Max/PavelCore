import streamlit as st

def render_ideas():
    st.markdown("""
        <div style="margin-bottom: 20px;">
            <h2 style="color: #00F2FE; margin:0;">💡 Boîte à Idées & Concepts</h2>
            <p style="color: #8E9BAE;">Capturez vos réflexions, opportunités et visions futures.</p>
        </div>
    """, unsafe_allow_html=True)

    if "ideas" not in st.session_state:
        st.session_state.ideas = [
            {"title": "Application Web Flet & Python", "category": "Tech", "note": "Créer une app desktop locale ultra rapide."},
            {"title": "Concept Marketing Musical", "category": "Événementiel", "note": "Organiser une soirée à thème Afrobeat & Zouglou."}
        ]

    with st.form("add_idea"):
        title = st.text_input("Titre de l'idée")
        category = st.selectbox("Domaine", ["Tech & Dev", "Musique & Event", "Business", "Personnel"])
        note = st.text_area("Détail / Notes de réflexion")
        if st.form_submit_button("Sauvegarder l'Idée"):
            if title:
                st.session_state.ideas.append({"title": title, "category": category, "note": note})
                st.toast("Idée enregistrée !", icon="💡")
                st.rerun()

    st.markdown("---")
    st.markdown("### Mes Idées Sauvegardées")
    for i in st.session_state.ideas:
        st.markdown(f"""
            <div class="glass-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="color:#00F2FE; margin:0;">{i['title']}</h4>
                    <span class="badge">{i['category']}</span>
                </div>
                <p style="color:#E0E6ED; margin-top:10px;">{i['note']}</p>
            </div>
        """, unsafe_allow_html=True)
