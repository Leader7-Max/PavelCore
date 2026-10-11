const EVENTS = __EVENTS__;
const $ = id => document.getElementById(id);

// Fenêtre parente (même origine) pour notifications, bannière et stockage
const P = (function(){ try { void window.parent.document; return window.parent; } catch(e){ return window; } })();
const N = P.Notification || window.Notification || null;
const store = {
  get: k => { try { return P.localStorage.getItem(k); } catch(e){ return null; } },
  set: (k,v) => { try { P.localStorage.setItem(k,v); } catch(e){} }
};
const pad = n => String(n).padStart(2,"0");
const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

// ───────────── SONNERIES (Web Audio, aucun fichier) ─────────────
let ctx = null, loopTimer = null;
function audio(){
  if(!ctx){ const AC = window.AudioContext || window.webkitAudioContext; if(AC) ctx = new AC(); }
  if(ctx && ctx.state === "suspended") ctx.resume();
  return ctx;
}
function beep(f, s, d, type, v, f2){
  const o = ctx.createOscillator(), g = ctx.createGain();
  o.type = type; o.frequency.setValueAtTime(f, s);
  if(f2) o.frequency.exponentialRampToValueAtTime(f2, s + d);
  g.gain.setValueAtTime(0.0001, s);
  g.gain.exponentialRampToValueAtTime(v, s + 0.02);
  g.gain.exponentialRampToValueAtTime(0.0001, s + d);
  o.connect(g); g.connect(ctx.destination); o.start(s); o.stop(s + d + 0.05);
}
const TONES = {
  "Standard":  t => { [0,0.45,0.9].forEach(k => { beep(880,t+k,0.18,"sine",0.4); beep(880,t+k+0.2,0.18,"sine",0.4); }); return 1.5; },
  "Doux":      t => { [523.25,659.25,783.99,1046.5].forEach((f,i) => beep(f,t+i*0.35,1.1,"sine",0.25)); return 2; },
  "Énergique": t => { for(let i=0;i<8;i++) beep(i%2?1318:988, t+i*0.14, 0.12, "square", 0.22); return 1.3; },
  "Futuriste": t => { beep(300,t,0.5,"sawtooth",0.2,1800); beep(1800,t+0.5,0.4,"sawtooth",0.15,400);
                      [660,880,1320,1760].forEach((f,i) => beep(f,t+1+i*0.12,0.3,"triangle",0.25)); return 2; }
};
function stopRing(){ if(loopTimer){ clearTimeout(loopTimer); loopTimer = null; } }
function ring(name, loops){
  const c = audio(); if(!c) return;
  const fn = TONES[name] || TONES["Standard"];
  stopRing();
  let n = 0;
  const once = () => {
    const dur = fn(c.currentTime + 0.05); n++;
    if(n >= loops){ loopTimer = null; return; }
    loopTimer = setTimeout(once, (dur + 0.6) * 1000);
  };
  once();
}

// ───────────── ALERTES ─────────────
function evTime(ev){
  const d = String(ev.date).split("-").map(Number), t = String(ev.time).split(":").map(Number);
  const at = new Date(d[0], d[1]-1, d[2], t[0]||0, t[1]||0, 0).getTime();
  return isNaN(at) ? null : at;
}
const fmtDate = ev => { const d = String(ev.date).split("-"); return d[2]+"/"+d[1]+"/"+d[0]; };
const leadLabel = m => m >= 1440 ? "1 jour" : (m >= 60 ? (m/60)+" h" : m+" min");

function banner(ev, text){
  try {
    const D = P.document;
    const old = D.getElementById("pavel-alarm"); if(old) old.remove();
    const b = D.createElement("div"); b.id = "pavel-alarm";
    b.style.cssText = "position:fixed;top:16px;left:50%;transform:translateX(-50%);z-index:999999;width:420px;max-width:92vw;"
      + "background:linear-gradient(135deg,#EC4899,#8B5CF6);color:#fff;border:1px solid rgba(255,255,255,.5);"
      + "border-radius:18px;padding:16px 18px;box-shadow:0 18px 50px rgba(0,0,0,.6);font-family:Inter,sans-serif";
    b.innerHTML = '<div style="font-weight:800;font-size:1.05rem">⏰ ' + esc(ev.title) + '</div>'
                + '<div style="opacity:.95;margin-top:4px;font-size:.9rem">' + esc(text) + '</div>';
    const btn = D.createElement("button"); btn.textContent = "🔕 Arrêter";
    btn.style.cssText = "margin-top:12px;background:#170A2E;color:#fff;font-weight:700;border:1px solid rgba(255,255,255,.4);border-radius:50px;padding:8px 18px;cursor:pointer";
    btn.onclick = () => { try { stopRing(); } catch(e){} b.remove(); };
    b.appendChild(btn); D.body.appendChild(b);
    setTimeout(() => { if(b.parentNode) b.remove(); }, 60000);
  } catch(e){}
}

function fire(ev, lead){
  const when = fmtDate(ev) + " à " + ev.time;
  const text = (lead > 0 ? "Dans " + leadLabel(lead) + " — " : "C'est l'heure — ") + when;
  try { if(N && N.permission === "granted"){ new N("⏰ " + ev.title, { body: text + (ev.desc ? "\n" + ev.desc : ""), tag: "pavel-" + ev.id, requireInteraction: true }); } } catch(e){}
  try { if(navigator.vibrate) navigator.vibrate([300,150,300,150,300]); } catch(e){}
  banner(ev, text);
  if(ev.ringtone !== "Silencieux") ring(ev.ringtone, 5);
}

// ───────────── MOTEUR DE VÉRIFICATION ─────────────
function check(){
  const now = Date.now(), offMin = parseInt($("offset").value, 10) || 0, off = offMin * 60000;
  let fired = {}; try { fired = JSON.parse(store.get("pavel_fired") || "{}"); } catch(e){}
  let next = null, changed = false;
  EVENTS.forEach(ev => {
    const at = evTime(ev); if(at === null) return;
    const trig = at - off, key = ev.id + "|" + ev.date + "|" + ev.time + "|" + offMin;
    if(now >= trig && now - trig <= 600000){
      if(!fired[key]){ fired[key] = now; changed = true; fire(ev, offMin); }
    } else if(trig > now && (!next || trig < next.trig)){
      next = { ev: ev, trig: trig, at: at };
    }
  });
  Object.keys(fired).forEach(k => { if(now - fired[k] > 3*86400000){ delete fired[k]; changed = true; } });
  if(changed) store.set("pavel_fired", JSON.stringify(fired));
  renderStatus(next);
}

function renderStatus(next){
  let perm = "Notifications à activer";
  if(!N) perm = "Notifications système non supportées (alerte visuelle + son actifs)";
  else if(N.permission === "granted") perm = "Notifications système activées";
  else if(N.permission === "denied") perm = "Notifications bloquées par le navigateur (alerte visuelle + son actifs)";
  const snd = (ctx && ctx.state === "running") ? "Son prêt" : "Son à activer";
  let nxt = "Aucune alarme à venir";
  if(next){
    const d = new Date(next.at);
    nxt = "⏭ Prochaine alarme : " + esc(next.ev.title) + " — " + pad(d.getDate()) + "/" + pad(d.getMonth()+1) + "/" + d.getFullYear() + " à " + pad(d.getHours()) + ":" + pad(d.getMinutes());
  }
  $("status").innerHTML = nxt + "<br>" + perm + " · " + snd;
}

// ───────────── INTERFACE ─────────────
Object.keys(TONES).forEach(name => {
  const b = document.createElement("button"); b.className = "ghost"; b.textContent = "▶ " + name;
  b.onclick = () => ring(name, 1);
  $("tests").appendChild(b);
});

$("offset").value = store.get("pavel_offset") || "0";
$("offset").onchange = () => { store.set("pavel_offset", $("offset").value); check(); };

$("enable").onclick = async () => {
  audio();
  try { if(N && N.permission === "default") await N.requestPermission(); } catch(e){}
  ring("Doux", 1);
  check();
};

try { P.document.addEventListener("click", () => { audio(); }, true); } catch(e){}

check();
setInterval(check, 5000);
