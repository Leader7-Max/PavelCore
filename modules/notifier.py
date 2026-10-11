def render_notifier(events, height=270, show_panel=True):
    """Affiche le panneau Notifications & sonneries et lance le moteur d'alarmes (navigateur).
    show_panel=False : moteur invisible (utilisé dans les autres rubriques)."""
    payload = []
    for ev in events or []:
        d, t = ev.get("date"), ev.get("time")
        d_str = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
        t_str = t.strftime("%H:%M") if hasattr(t, "strftime") else str(t)[:5]
        payload.append({
            "id": ev.get("id", 0),
            "title": ev.get("title") or "Événement",
            "date": d_str,
            "time": t_str,
            "desc": ev.get("desc") or "",
            "ringtone": ev.get("ringtone") or "Standard",
        })
    data = json.dumps(payload[:300], ensure_ascii=False).replace("</", "<\\/")
    code = _TEMPLATE.replace("__EVENTS__", data)
    if not show_panel:
        code = code.replace('<div class="panel">', '<div class="panel" style="display:none">')
        height = 1
    components.html(code, height=height)
