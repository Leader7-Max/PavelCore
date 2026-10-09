import streamlit as st
import calendar
from datetime import date, time, datetime

MONTH_NAMES_FR = [
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]

def render_agenda_module():
    if st.session_state.get("direct_agenda", False) or st.query_params.get("app", None) == "agenda":
        if st.button("← Retour / Quitter l'Agenda", key="back_from_direct_agenda", type="secondary"):
            st.session_state.direct_agenda = False
            st.rerun()

    st.markdown('<div style="margin-top: 10px; margin-bottom: 20px;"><span class="zapio-badge">📅 AGENDA AUTONOME & HORS-LIGNE</span><h2 style="margin-top: 10px; font-size: 2rem; color: #FFF;">Agenda & Calendrier Interactif</h2></div>', unsafe_allow_html=True)
    col_btn1, col_btn2, col_clear = st.columns([2.3, 2.5, 2])
    
    with col_btn1:
        if st.button("📅 Vue Calendrier Mensuel", type="primary" if st.session_state.agenda_active_tab == "vue" else "secondary", use_container_width=True, key="nav_btn_vue"):
            st.session_state.agenda_active_tab = "vue"
            st.rerun()

    with col_btn2:
        if st.button("➕ Programmer un Événement", type="primary" if st.session_state.agenda_active_tab == "add" else "secondary", use_container_width=True, key="nav_btn_add"):
            st.session_state.agenda_active_tab = "add"
            st.rerun()

    with col_clear:
        if st.session_state.agenda_events:
            if st.button("🗑️ Vider tout l'agenda", key="clear_all_events"):
                st.session_state.agenda_events = []
                st.toast("🗑️ Agenda vidé avec succès.", icon="ℹ️")
                st.rerun()

    st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

    if st.session_state.agenda_active_tab == "vue":
        today = date.today()
        current_year = today.year
        available_years = list(range(2025, current_year + 15))
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            selected_month_idx = st.selectbox("Mois", range(1, 13), format_func=lambda x: MONTH_NAMES_FR[x-1], index=today.month - 1)
        with col_m2:
            default_year_idx = available_years.index(current_year) if current_year in available_years else 1
            selected_year = st.selectbox("Année", available_years, index=default_year_idx)

        st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
        days_header = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        cols_h = st.columns(7)
        for idx, h in enumerate(days_header):
            cols_h[idx].markdown(f'<div class="calendar-header-box">{h}</div>', unsafe_allow_html=True)

        events_by_day = {}
        for ev in st.session_state.agenda_events:
            if ev['date'].month == selected_month_idx and ev['date'].year == selected_year:
                day_num = ev['date'].day
                if day_num not in events_by_day:
                    events_by_day[day_num] = []
                events_by_day[day_num].append(ev)

        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(selected_year, selected_month_idx)

        for week in month_days:
            cols_w = st.columns(7)
            for day_idx, day_num in enumerate(week):
                if day_num == 0:
                    cols_w[day_idx].markdown('<div class="calendar-day-box" style="background:rgba(100,100,100,0.1); border:1px solid rgba(100,100,100,0.2); opacity:0.3;"></div>', unsafe_allow_html=True)
                else:
                    is_today = (day_num == today.day and selected_month_idx == today.month and selected_year == today.year)
                    day_events = events_by_day.get(day_num, [])
                    border_color = "#EC4899" if is_today else "#8B5CF6"
                    bg_color = "linear-gradient(135deg, #3B1578 0%, #261245 100%)" if is_today else "#170A2E"
                    
                    event_html = ""
                    for ev_item in day_events[:2]:
                        event_html += f'<div style="background:#F43F5E; color:#FFF; font-size:0.6rem; font-weight:800; border-radius:3px; padding:1px 3px; margin-top:3px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">⏰ {ev_item["time"].strftime("%H:%M")} - {ev_item["title"]}</div>'

                    day_marker = '📌' if is_today else ''
                    day_color = '#EC4899' if is_today else '#F8FAFC'
                    
                    cols_w[day_idx].markdown(
                        f'<div class="calendar-day-box" style="background:{bg_color}; border:1px solid {border_color};">'
                        f'<div style="display:flex; justify-content:space-between; align-items:center;">'
                        f'<span style="font-weight:800; font-size:0.85rem; color:{day_color};">{day_num} {day_marker}</span>'
                        f'</div>{event_html}</div>', 
                        unsafe_allow_html=True
                    )

    elif st.session_state.agenda_active_tab == "add":
        with st.form("add_event_form"):
            st.markdown("<h3 style='color: #FFF;'>Planifier une nouvelle date</h3>", unsafe_allow_html=True)
            title = st.text_input("Titre de l'événement / Rappel", placeholder="Ex: Prestation DJ / Réunion")
            c_date, c_time = st.columns(2)
            with c_date:
                event_date = st.date_input("Date", value=date.today())
            with c_time:
                event_time = st.time_input("Heure exacte", value=time(12, 0))
            category = st.selectbox("Catégorie", ["Business / Travail", "Dev & Tech", "Personnel", "Rendez-vous Urgent", "Événement DJ / Prestation"])
            desc = st.text_area("Notes complémentaires")
            if st.form_submit_button("🔔 Ajouter au Calendrier"):
                if title:
                    st.session_state.agenda_events.append({"title": title, "date": event_date, "time": event_time, "category": category, "desc": desc, "ringtone": "Alarme Digitale"})
                    st.session_state.agenda_active_tab = "vue"
                    st.toast("✅ Événement ajouté avec succès !", icon="🎉")
                    st.rerun()
