"""Diagnostic des fichiers réellement déployés (ouvrir l'application avec ?diag=1, connecté).

Compare chaque fichier du dépôt à la version livrée (manifest.json) et détecte
les erreurs de syntaxe / d'indentation AVANT qu'elles ne fassent planter une page.
Aucun secret n'est lu ni affiché.
"""
import ast
import hashlib
import json
import platform
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
EXTENSIONS = {".py", ".js", ".toml"}
SKIP_PARTS = {".git", "__pycache__", "venv", ".venv", "node_modules", "uploaded_files"}


def _read_normalized(path: Path) -> bytes:
    # Fins de ligne normalisées : un fichier enregistré sous Windows donne le même résultat
    return path.read_bytes().replace(b"\r\n", b"\n")


def _fingerprint(path: Path) -> dict:
    data = _read_normalized(path)
    info = {"lines": data.count(b"\n") + (0 if data.endswith(b"\n") or not data else 1),
            "sha": hashlib.sha256(data).hexdigest()[:10], "syntax": "OK"}
    if path.suffix == ".py":
        try:
            ast.parse(data.decode("utf-8"), filename=path.name)
        except SyntaxError as exc:
            snippet = (exc.text or "").strip()
            info["syntax"] = f"❌ {type(exc).__name__} ligne {exc.lineno}" + (f" : {snippet}" if snippet else "")
        except UnicodeDecodeError:
            info["syntax"] = "❌ encodage invalide (UTF-8 attendu)"
    else:
        info["syntax"] = "—"
    return info


def scan_project():
    """Retourne {chemin_relatif: empreinte} pour tous les fichiers suivis du projet."""
    found = {}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in EXTENSIONS:
            continue
        rel_parts = path.relative_to(ROOT).parts
        if any(part in SKIP_PARTS for part in rel_parts) or path.name == "secrets.toml":
            continue
        found[path.relative_to(ROOT).as_posix()] = _fingerprint(path)
    return found


def load_manifest():
    try:
        return json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    except Exception:
        return None


def compare(found: dict, manifest):
    """Construit les lignes du tableau et les compteurs de problèmes."""
    expected = (manifest or {}).get("files", {})
    rows, problems = [], 0
    for rel, info in found.items():
        if rel in expected:
            exp = expected[rel]
            if info["sha"] == exp["sha"]:
                status = "✅ identique à la version livrée"
            else:
                status = f"⚠️ DIFFÉRENT (attendu {exp['lines']} lignes, trouvé {info['lines']})"
                problems += 1
        else:
            status = "— non suivi"
        if info["syntax"].startswith("❌"):
            problems += 1
        rows.append({"Fichier": rel, "Lignes": info["lines"], "Empreinte": info["sha"],
                     "Syntaxe": info["syntax"], "État": status})
    for rel, exp in expected.items():
        if rel not in found:
            rows.append({"Fichier": rel, "Lignes": 0, "Empreinte": "-", "Syntaxe": "-",
                         "État": "❌ ABSENT du dépôt"})
            problems += 1
    return rows, problems


def render_diagnostics(app_build: str = "?"):
    found = scan_project()
    manifest = load_manifest()
    rows, problems = compare(found, manifest)

    st.markdown("### 🩺 Diagnostic des fichiers déployés")
    st.caption(
        f"Build de app.py : {app_build} · Version livrée (manifest) : "
        f"{(manifest or {}).get('build', 'manifest.json absent')} · "
        f"Python {platform.python_version()} · Streamlit {getattr(st, '__version__', '?')}"
    )
    if manifest is None:
        st.warning("manifest.json est absent : impossible de comparer aux fichiers livrés (la syntaxe est vérifiée).")
    if problems:
        st.error(f"{problems} problème(s) détecté(s) : remplacez les fichiers marqués ⚠️ ou ❌ par ceux fournis.")
    else:
        st.success("Tous les fichiers suivis sont identiques à la version livrée et sans erreur de syntaxe.")

    # Les cas problématiques d'abord
    rows.sort(key=lambda r: (not (r["État"].startswith(("⚠️", "❌")) or r["Syntaxe"].startswith("❌")), r["Fichier"]))
    st.table(rows)

    try:
        from modules.vault_crypto import vault_status
        vault_ok, _ = vault_status()
    except Exception:
        vault_ok = False
    try:
        from modules.supabase_client import supabase
        supabase_ok = bool(supabase)
    except Exception:
        supabase_ok = False
    st.caption(
        f"Chiffrement du Coffre-Fort : {'✅ actif' if vault_ok else '❌ clé VAULT_MASTER_KEY absente'} · "
        f"Client Supabase : {'✅ initialisé' if supabase_ok else '❌ non initialisé'}"
    )
