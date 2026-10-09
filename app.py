# Entête des jours de la semaine
            days_header = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
            cols_h = st.columns(7)
            for idx, h in enumerate(days_header):
                cols_h[idx].markdown(f'<div class="calendar-header-box">{h}</div>', unsafe_allow_html=True)

            st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)

            # Affichage dynamique des semaines
            for week in month_days:
                cols_w = st.columns(7)
                for day_idx, day_num in enumerate(week):
                    if day_num == 0:
                        cols_w[day_idx].markdown('<div class="calendar-day-box" style="background:rgba(20,9,35,0.4); border:1px solid #261245; opacity:0.3;"></div>', unsafe_allow_html=True)
                    else:
                        is_today = (day_num == today.day and selected_month_idx == today.month and selected_year == today.year)
                        day_events = events_by_day.get(day_num, [])
                        
                        border_color = "#EC4899" if is_today else "#5B21B6"
                        bg_color = "linear-gradient(135deg, #3B1578 0%, #261245 100%)" if is_today else "#1E0A3C"
                        
                        max_visible_events = 2
                        visible_events = day_events[:max_visible_events]
                        hidden_count = len(day_events) - max_visible_events

                        event_html = ""
                        for ev_item in visible_events:
                            event_html += f'<div style="background:#F43F5E; color:#FFF; font-size:0.6rem; font-weight:800; border-radius:3px; padding:1px 3px; margin-top:3px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">⏰ {ev_item["time"].strftime("%H:%M")} - {ev_item["title"]}</div>'

                        if hidden_count > 0:
                            event_html += f'<div style="background:#A78BFA; color:#1E0A3C; font-size:0.55rem; font-weight:800; border-radius:3px; padding:1px 2px; margin-top:2px; text-align:center;">+{hidden_count}</div>'

                        day_marker = '📌' if is_today else ''
                        day_color = '#EC4899' if is_today else '#FFF'
                        
                        cols_w[day_idx].markdown(
                            f'<div class="calendar-day-box" style="background:{bg_color}; border:1px solid {border_color};">'
                            f'<div style="display:flex; justify-content:space-between; align-items:center;">'
                            f'<span class="calendar-day-number" style="font-weight:800; font-size:0.85rem; color:{day_color};">{day_num} {day_marker}</span>'
                            f'</div>{event_html}</div>', 
                            unsafe_allow_html=True
                        )
