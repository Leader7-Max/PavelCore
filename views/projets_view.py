import html
import streamlit as st
from datetime import date, time
from modules.database import add_event_to_db, delete_event_from_db, clear_all_events_db, load_events_from_db
from modules.calendar_ui import render_month_calendar
from modules.notifier import render_notifier


def _fmt_date(value):
    return value.strftime("%d/%m/%Y") if hasattr(value, "strftime") else str(value)


def _fmt_time(value):
    return value.strftime("%H:%M") if hasattr(value, "strftime") else str(value)[:5]


def render_agenda_view(sub_title_color="#FFF", card_bg="#170A2E", card_border="#2B1552", header_box_bg="#1E0A3C", header_box_text="#A78BFA", text_color="#F8FAFC"):
    """Gère l'affichage complet du module Agenda connecté à SQLite et cloisonné par utilisateur."""

    # Récupération sécurisée du user_id de la session
    user_id = st.session_state.user_info["id"] if st.session_state.get("user_info") else 0

    st.markdown(f"<h2 style='color: {sub_title_color}; margin-top: 10px;'>📅 Espace Agenda & Planning</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {text_color}; opacity: 0.8;'>Gérez vos événements, rendez-vous et plannings en toute sécurité.</p>", unsafe_allow_html=True)

    # Rafraîchissement des événements de l'utilisateur
    st.session_state.agenda_events = load_events_from_db(user_id)

    # Panneau notifications & sonneries + moteur d'alarmes
    render_notifier(st.session_state.agenda_events)

    tab_vue, tab_ajout = st.tabs(["📋 Liste & Calendrier", "➕ Ajouter un Événement"])

    with tab_vue:
        # Calendrier mensuel premium
        render_month_calendar(st.session_state.agenda_events)

        st.markdown("### Vos Événements Enregistrés")
        if not st.session_state.agenda_events:
            st.info("Aucun événement dans votre agenda pour le moment.")
        else:
            for ev in st.session_state.agenda_events:
                with st.container():
                    title = html.escape(str(ev.get("title") or ""))
                    category = html.escape(str(ev.get("category") or "Général"))
                    desc = html.escape(str(ev.get("desc") or "Aucune description"))
                    ringtone = html.escape(str(ev.get("ringtone") or "Standard"))
                    st.markdown(f"""
                        <div style="background-color: {card_bg}; border: 1px solid {card_border}; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                            <h4 style="color: {sub_title_color}; margin: 0 0 5px 0;">{title}</h4>
                            <p style="margin: 0; font-size: 0.9rem; color: #CBD5E1;">📅 Date : {_fmt_date(ev['date'])} à {_fmt_time(ev['time'])} | 🏷️ Catégorie : {category} | 🔔 {ringtone}</p>
                            <p style="margin: 5px 0 0 0; font-size: 0.85rem; color: #94A3B8;">📝 {desc}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    if st.button("🗑️ Supprimer", key=f"del_ev_{ev['id']}"):
                        delete_event_from_db(ev['id'], user_id)
                        st.session_state.agenda_events = load_events_from_db(user_id)
                        st.toast("Événement supprimé avec succès.", icon="🗑️")
                        st.rerun()

            if st.button("⚠️ Vider tout l'agenda", type="secondary"):
                clear_all_events_db(user_id)
                st.session_state.agenda_events = load_events_from_db(user_id)
                st.toast("Agenda vidé.", icon="🧹")
                st.rerun()

    with tab_ajout:
        st.markdown("### Créer un nouvel événement")
        with st.form("agenda_add_form"):
            title = st.text_input("Titre de l'événement", placeholder="Ex: Réunion client, Session DJ...")
            ev_date = st.date_input("Date", value=date.today(), format="DD/MM/YYYY")
            ev_time = st.time_input("Heure", value=time(12, 0))
            category = st.selectbox("Catégorie", ["Général", "Professionnel", "Musique / DJ", "Personnel", "Urgent"])
            desc = st.text_area("Description / Notes", placeholder="Détails de l'événement...")
            ringtone = st.selectbox("Sonnette d'alarme", ["Standard", "Doux", "Énergique", "Futuriste", "Silencieux"])
            st.caption("🔔 Testez les sonneries avec les boutons ▶ du panneau « Notifications & sonneries » en haut de l'agenda.")

            submit_ev = st.form_submit_button("Enregistrer l'événement", use_container_width=True)
            if submit_ev:
                if title.strip():
                    add_event_to_db(user_id, title, ev_date, ev_time, category, desc, ringtone)
                    st.session_state.agenda_events = load_events_from_db(user_id)
                    st.toast("✅ Événement ajouté avec succès dans votre espace personnel.", icon="🎉")
                    st.rerun()
                else:
                    st.error("Le titre de l'événement est obligatoire.")
