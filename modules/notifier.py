import json
from pathlib import Path
import streamlit as st

_ENGINE_JS = Path(__file__).parent / "notifier_assets" / "engine.js"

_PANEL = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  body{margin:0;font-family:Inter,-apple-system,'Segoe UI',sans-serif;color:#fff;background:transparent}
  .panel{background:linear-gradient(160deg,#2A104D 0%,#170A2E 100%);border:1px solid rgba(236,72,153,.4);
         border-radius:16px;padding:14px 16px;box-shadow:0 8px 28px rgba(0,0,0,.4)}
  h4{margin:0 0 6px 0;font-size:1rem}
  .row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:10px}
  button{cursor:pointer;color:#fff;font-weight:700;font-size:.8rem;border-radius:50px;padding:9px 16px;
         border:1px solid rgba(255,255,255,.35);transition:transform .2s,box-shadow .2s}
  button:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(236,72,153,.55)}
  button.pill{background:linear-gradient(135deg,#EC4899 0%,#8B5CF6 100%)}
  button.ghost{background:#230E3D;border:1px solid rgba(236,72,153,.4)}
  select{background:#230E3D;color:#fff;border:1px solid rgba(236,72,153,.4);border-radius:10px;
         padding:8px 10px;font-size:.8rem;font-weight:600}
  #status{font-size:.78rem;color:#CBD5E1;margin-top:10px;line-height:1.5}
</style></head><body>
<div class="panel">
  <h4>🔔 Notifications &amp; sonneries</h4>
  <div class="row">
    <button class="pill" id="enable">🔔 Activer notifications &amp; son</button>
    <select id="offset" title="Prévenir à l'avance">
      <option value="0">À l'heure de l'événement</option>
      <option value="5">5 min avant</option>
      <option value="10">10 min avant</option>
      <option value="15">15 min avant</option>
      <option value="30">30 min avant</option>
      <option value="60">1 h avant</option>
      <option value="1440">1 jour avant</option>
    </select>
  </div>
  <div class="row" id="tests"></div>
  <div class="row"><button class="pill" id="testalarm">⏰ Tester l'alarme (3 s)</button></div>
  <div id="status"></div>
</div>
<script>__SCRIPT__</script>
</body></html>"""


def _render_html(code: str, height: int):
    """components.html est déprécié dans les versions récentes de Streamlit :
    on l'utilise tant qu'il existe, sinon on bascule automatiquement sur st.iframe."""
    try:
        import streamlit.components.v1 as components
        components.html(code, height=height)
    except Exception:
        st.iframe(code, height=height)


def render_notifier(events, height=300, show_panel=True):
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
    script = _ENGINE_JS.read_text(encoding="utf-8").replace("__EVENTS__", data)
    code = _PANEL.replace("__SCRIPT__", script)

    if not show_panel:
        code = code.replace('<div class="panel">', '<div class="panel" style="display:none">')
        height = 1

    _render_html(code, height)
