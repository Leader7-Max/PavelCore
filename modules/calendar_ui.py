import calendar
import html
from datetime import date, datetime
import streamlit as st

MOIS = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet",
        "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
JOURS = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]


def _to_date(value):
    """Accepte date, datetime ou texte (AAAA-MM-JJ / JJ/MM/AAAA)."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(str(value), fmt).date()
        except ValueError:
            continue
    return None


def _prev_month():
    if st.session_state.cal_month == 1:
        st.session_state.cal_month, st.session_state.cal_year = 12, st.session_state.cal_year - 1
    else:
        st.session_state.cal_month -= 1


def _next_month():
    if st.session_state.cal_month == 12:
        st.session_state.cal_month, st.session_state.cal_year = 1, st.session_state.cal_year + 1
    else:
        st.session_state.cal_month += 1


def _today_month():
    t = date.today()
    st.session_state.cal_month, st.session_state.cal_year = t.month, t.year


def render_month_calendar(events):
    """Affiche une grille mensuelle premium avec les événements de l'agenda."""
    today = date.today()
    st.session_state.setdefault("cal_month", today.month)
    st.session_state.setdefault("cal_year", today.year)
    year, month = st.session_state.cal_year, st.session_state.cal_month

    # Regroupe les événements par jour
    by_day = {}
    for ev in events or []:
        d = _to_date(ev.get("date"))
        if d and d.year == year and d.month == month:
            by_day.setdefault(d.day, []).append(ev)

    c1, c2, c3, c4 = st.columns([1, 3, 1, 1.4])
    c1.button("◀", key="cal_prev", on_click=_prev_month)
    c2.markdown(f'<div class="pc-cal-title">{MOIS[month - 1]} <span>{year}</span></div>',
                unsafe_allow_html=True)
    c3.button("▶", key="cal_next", on_click=_next_month)
    c4.button("Aujourd'hui", key="cal_today", on_click=_today_month)

    parts = ['<div class="pc-cal-wrap"><div class="pc-cal-grid">']
    parts += [f'<div class="pc-cal-dow">{j}</div>' for j in JOURS]

    for week in calendar.Calendar(firstweekday=0).monthdayscalendar(year, month):
        for idx, day in enumerate(week):
            if day == 0:
                parts.append('<div class="pc-cal-cell empty"></div>')
                continue
            classes = ["pc-cal-cell"]
            if idx >= 5:
                classes.append("weekend")
            if date(year, month, day) == today:
                classes.append("today")
            day_events = by_day.get(day, [])
            if day_events:
                classes.append("has-ev")

            cell = [f'<div class="{" ".join(classes)}"><span class="pc-cal-num">{day}</span>']
            for ev in day_events[:2]:
                label = html.escape(str(ev.get("title", "")))
                cell.append(f'<div class="pc-cal-ev" title="{label}"><i></i>{label}</div>')
            if len(day_events) > 2:
                cell.append(f'<div class="pc-cal-more">+{len(day_events) - 2} autre(s)</div>')
            cell.append('</div>')
            parts.append("".join(cell))

    parts.append('</div></div>')
    st.markdown("".join(parts), unsafe_allow_html=True)
