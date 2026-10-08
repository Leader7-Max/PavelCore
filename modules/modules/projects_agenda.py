import streamlit as st
import pandas as pd

def render_projects_agenda():
    st.markdown("""
        <div style="margin-bottom: 20px;">
            <h2 style="color: #00F2FE; margin:0;">📅 Projets & Agenda Ultra-Moderne</h2>
            <p style="color: #8E9BAE;">Planification, suivi de projets et rappels d'échéances.</p>
        </div>
    """, unsafe_allow_html=True)

    if "projects" not in st.session_state:
        st.session_state.projects = [
            {"name": "PavelCore App", "status": "En cours", "deadline": "2026-10-25", "priority": "Haute", "desc": "Développement du coffre-fort"},
            {"name": "Reborn Beauty Platform", "status": "En cours", "deadline": "2026-11-15", "priority": "Moyenne", "desc": "Marketplace e-commerce"}
        ]

    tab1, tab2 = st.tabs(["🚀 Suivi de Projets", "📆 Agenda & Échéances"])

    with tab1:
        with st.expander("➕ Créer un nouveau Projet"):
            with st.form("new_project_form"):
                p_name = st.text_input("Nom du Projet")
                p_status = st.selectbox("Statut", ["Idée", "Planifié", "En cours", "Terminé"])
                p_priority = st.selectbox("Priorité", ["Basse", "Moyenne", "Haute", "Urgente"])
                p_deadline = st.date_input("Échéance ciblé")
                p_desc = st.text_area("Description / Jalons")
                
                if st.form_submit_button("Enregistrer le projet"):
                    if p_name:
                        st.session_state.projects.append({
                            "name": p_name, "status": p_status, "deadline": str(p_deadline),
                            "priority": p_priority, "desc": p_desc
                        })
                        st.toast("Projet créé avec succès !", icon="🚀")
                        st.rerun()

        st.markdown("### Mes Projets Actifs")
        for p in st.session_state.projects:
            color = "#00F2FE" if p["status"] == "En cours" else "#10B981"
            st.markdown(f"""
                <div class="glass-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="color:{color}; margin:0;">{p['name']}</h3>
                        <span class="badge">{p['priority']}</span>
                    </div>
                    <p style="color:#8E9BAE; margin:10px 0;">{p['desc']}</p>
                    <div style="display:flex; gap:15px; font-size:0.85rem; color:#E0E6ED;">
                        <span>📌 Statut : <b>{p['status']}</b></span>
                        <span>⏱️ Échéance : <b>{p['deadline']}</b></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### Vue Calendrier des Échéances")
        df = pd.DataFrame(st.session_state.projects)
        if not df.empty:
            st.dataframe(df[["name", "deadline", "priority", "status"]], use_container_width=True)
