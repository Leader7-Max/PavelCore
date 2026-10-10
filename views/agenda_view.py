import streamlit as st
import streamlit.components.v1 as components
import calendar
from datetime import datetime, date, time

def render_agenda_view(sub_title_color="#FFF", card_bg="#170A2E", card_border="#2B1552", header_box_bg="#1E0A3C", header_box_text="#A78BFA", text_color="#F8FAFC"):
    """Gère l'affichage complet du module Agenda, Calendrier et Liste des tâches."""
    
    MONTH_NAMES_FR = [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ]

    query_params = st.query_params
    if st.session_state.get("direct_agenda", False) or query_params.get("app", None) == "agenda":
        if st.button("← Retour / Quitter l'Agenda", key="back_from_direct_agenda", type="secondary"):
            st.session_state.direct_agenda = False
            st.rerun()

    st.markdown(f'<div style="margin-top: 10px; margin-bottom: 20px;"><span class="zapio-badge">📅 AGENDA AUTONOME & HORS-LIGNE</span><h2 style="margin-top: 10px; font-size: 2rem; color: {sub_title_color};">Agenda & Calendrier Interactif</h2></div>', unsafe_allow_html=True)
    
    # Navigation par onglets (Ajout d'une vue Liste)
    col_btn1, col_btn2, col_btn3, col_clear = st.columns([2, 2, 2, 2])
    
    with col_btn1:
        if st.button("📅 Calendrier", type="primary" if st.session_state.agenda_active_tab == "vue" else "secondary", use_container_width=True, key="nav_btn_vue"):
            st.session_state.agenda_active_tab = "vue"
            st.rerun()

    with col_btn2:
        if st.button("📋 Liste des tâches", type="primary" if st.session_state.agenda_active_tab == "liste" else "secondary", use_container_width=True, key="nav_btn_liste"):
            st.session_state.agenda_active_tab = "liste"
            st.rerun()

    with col_btn3:
        if st.button("➕ Programmer", type="primary" if st.session_state.agenda_active_tab == "add" else "secondary", use_container_width=True, key="nav_btn_add"):
            st.session_state.agenda_active_tab = "add"
            st.rerun()

    with col_clear:
        if st.session_state.agenda_events:
            if st.button("🗑️ Vider tout", key="clear_all_events"):
                st.session_state.agenda_events = []
                st.toast("🗑️ Agenda vidé avec succès.", icon="ℹ️")
                st.rerun()

    st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

    # 1. VUE CALENDRIER
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
        header_html = "".join([f'<div style="background:{header_box_bg}; color:{header_box_text}; text-align:center; padding:6px 2px; border-radius:6px; font-weight:700; font-size:0.75rem; border:1px solid {card_border}; box-sizing:border-box;">{h}</div>' for h in days_header])

        events_by_day = {}
        for ev in st.session_state.agenda_events:
            if ev['date'].month == selected_month_idx and ev['date'].year == selected_year:
                day_num = ev['date'].day
                if day_num not in events_by_day:
                    events_by_day[day_num] = []
                events_by_day[day_num].append(ev)

        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(selected_year, selected_month_idx)

        cells_html = ""
        for week in month_days:
            for day_num in week:
                if day_num == 0:
                    cells_html += '<div style="min-height:65px; border-radius:6px; padding:4px; background:rgba(100,100,100,0.05); opacity:0.15; border:1px solid transparent; box-sizing:border-box;"></div>'
                else:
                    is_today = (day_num == today.day and selected_month_idx == today.month and selected_year == today.year)
                    day_events = events_by_day.get(day_num, [])
                    border_color = "#EC4899" if is_today else "#8B5CF6"
                    bg_color = "linear-gradient(135deg, #3B1578 0%, #261245 100%)" if is_today else card_bg
                    
                    max_visible_events = 2
                    visible_events = day_events[:max_visible_events]
                    hidden_count = len(day_events) - max_visible_events

                    event_html = ""
                    for ev_item in visible_events:
                        event_html += f'<div style="background:#F43F5E; color:#FFF; font-size:0.45rem; font-weight:800; border-radius:3px; padding:1px 2px; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">⏰ {ev_item["time"].strftime("%H:%M")}</div>'
                    if hidden_count > 0:
                        event_html += f'<div style="background:#A78BFA; color:#1E0A3C; font-size:0.4rem; font-weight:800; border-radius:3px; padding:1px; margin-top:1px; text-align:center;">+{hidden_count}</div>'

                    day_marker = '📌' if is_today else ''
                    day_color = '#EC4899' if is_today else text_color
                    
                    cells_html += f'''
                        <div style="min-height:65px; border-radius:6px; padding:4px; background:{bg_color}; border:1px solid {border_color}; display:flex; flex-direction:column; justify-content:flex-start; box-sizing:border-box;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span style="font-weight:800; font-size:0.75rem; color:{day_color};">{day_num} {day_marker}</span>
                            </div>
                            {event_html}
                        </div>
                    '''

        calendar_full_html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    background-color: transparent;
                    margin: 0;
                    padding: 0;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                }}
                .calendar-grid {{
                    display: grid !important;
                    grid-template-columns: repeat(7, 1fr) !important;
                    gap: 4px !important;
                    width: 100% !important;
                    box-sizing: border-box !important;
                }}
            </style>
        </head>
        <body>
            <div class="calendar-grid">
                {header_html}
                {cells_html}
            </div>
        </body>
        </html>
        '''
        components.html(calendar_full_html, height=420, scrolling=False)

    # 2. VUE LISTE DES TÂCHES
    elif st.session_state.agenda_active_tab == "liste":
        st.markdown(f"<h3 style='color: {sub_title_color};'>📋 Liste de toutes les tâches programmées</h3>", unsafe_allow_html=True)
        
        if not st.session_state.agenda_events:
            st.info("Aucune tâche ou événement enregistré pour le moment. Cliquez sur 'Programmer' pour en ajouter.")
        else:
            # Tri des événements par date et heure
            sorted_events = sorted(st.session_state.agenda_events, key=lambda x: (x['date'], x['time']))
            
            for idx, ev in enumerate(sorted_events):
                st.markdown(f'''
                    <div class="zapio-card" style="border-left: 5px solid #EC4899;">
                        <span class="zapio-badge">{ev["category"]}</span>
                        <h4 style="margin-top:8px; color:{sub_title_color};">{ev["title"]}</h4>
                        <p style="margin: 4px 0; font-size: 0.9rem;">📅 <b>Date :</b> {ev["date"].strftime("%d/%m/%Y")} | ⏰ <b>Heure :</b> {ev["time"].strftime("%H:%M")}</p>
                        <p style="margin: 4px 0; font-size: 0.85rem; opacity: 0.8;">💬 {ev.get("desc", "Aucune note complémentaire.")}</p>
                    </div>
                ''', unsafe_allow_html=True)
                
                # Option de suppression individuelle d'une tâche
                if st.button(f"🗑️ Supprimer cette tâche", key=f"del_ev_{idx}", type="secondary"):
                    st.session_state.agenda_events.remove(ev)
                    st.toast("🗑️ Tâche supprimée avec succès.", icon="ℹ️")
                    st.rerun()

    # 3. ONGLET PROGRAMMER
    elif st.session_state.agenda_active_tab == "add":
        with st.form("add_event_form", clear_on_submit=True):
            st.markdown(f"<h3 style='color: {sub_title_color};'>Planifier une nouvelle date</h3>", unsafe_allow_html=True)
            title = st.text_input("Titre de l'événement / Rappel", placeholder="Ex: Prestation DJ / Réunion")
            c_date, c_time = st.columns(2)
            with c_date:
                event_date = st.date_input("Date", value=date.today())
            with c_time:
                event_time = st.time_input("Heure exacte", value=time(12, 0))
            c_cat, c_ring = st.columns(2)
            with c_cat:
                category = st.selectbox("Catégorie", ["Business / Travail", "Dev & Tech", "Personnel", "Rendez-vous Urgent", "Événement DJ / Prestation"])
            with c_ring:
                ringtone = st.selectbox("Sonnerie", ["Alarme Digitale", "Bip Futuriste", "Douce Mélodie", "Silence"])
            desc = st.text_area("Notes complémentaires")
            
            if st.form_submit_button("🔔 Ajouter au Calendrier"):
                if title:
                    st.session_state.agenda_events.append({"title": title, "date": event_date, "time": event_time, "category": category, "desc": desc, "ringtone": ringtone})
                    st.session_state.agenda_active_tab = "liste" # Redirige directement vers la liste pour voir la tâche ajoutée
                    st.toast("✅ Événement ajouté avec succès !", icon="🎉")
                    st.rerun()
                else:
                    st.warning("Veuillez saisir un titre pour l'événement.")
