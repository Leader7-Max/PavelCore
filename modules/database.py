import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime, date, time

from modules.vault_crypto import encrypt_secret, decrypt_secret, is_encrypted, VaultKeyError

DB_NAME = "pavelcore_workspace.db"


def get_connection():
    """Conservée pour compatibilité (sauvegardes, etc.)."""
    return sqlite3.connect(DB_NAME, timeout=10, check_same_thread=False)


@contextmanager
def _db():
    """Connexion avec commit/rollback automatiques et fermeture garantie."""
    conn = sqlite3.connect(DB_NAME, timeout=10)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _uid(user_id) -> str:
    return str(user_id)


def init_db():
    """Crée les tables et index (exécuté une seule fois au chargement du module)."""
    with _db() as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                event_date TEXT NOT NULL,
                event_time TEXT NOT NULL,
                category TEXT,
                description TEXT,
                ringtone TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                service TEXT NOT NULL,
                encrypted_key TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                site TEXT NOT NULL,
                username TEXT NOT NULL,
                encrypted_password TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                category TEXT,
                notes TEXT
            )
        ''')
        for table in ("events", "api_keys", "credentials", "contacts"):
            conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{table}_user ON {table}(user_id)")


init_db()


# ═════════════════ AGENDA ═════════════════
def load_events_from_db(user_id):
    with _db() as conn:
        rows = conn.execute(
            "SELECT id, title, event_date, event_time, category, description, ringtone "
            "FROM events WHERE user_id = ? ORDER BY event_date, event_time",
            (_uid(user_id),),
        ).fetchall()

    events = []
    for row in rows:
        try:
            ev_date = datetime.strptime(row[2], "%Y-%m-%d").date()
        except (ValueError, TypeError):
            logging.warning("Date invalide pour l'événement %s : %r", row[0], row[2])
            ev_date = date.today()
        try:
            ev_time = datetime.strptime(row[3], "%H:%M").time()
        except (ValueError, TypeError):
            logging.warning("Heure invalide pour l'événement %s : %r", row[0], row[3])
            ev_time = time(12, 0)

        events.append({
            "id": row[0], "title": row[1], "date": ev_date, "time": ev_time,
            "category": row[4], "desc": row[5], "ringtone": row[6],
        })
    return events


def add_event_to_db(user_id, title, ev_date, ev_time, category, desc, ringtone):
    with _db() as conn:
        conn.execute(
            "INSERT INTO events (user_id, title, event_date, event_time, category, description, ringtone) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (_uid(user_id), title.strip(), ev_date.strftime("%Y-%m-%d"), ev_time.strftime("%H:%M"),
             category, desc, ringtone),
        )


def delete_event_from_db(event_id, user_id=None):
    """Si user_id est fourni, seul le propriétaire peut supprimer l'événement."""
    with _db() as conn:
        if user_id is None:
            conn.execute("DELETE FROM events WHERE id = ?", (event_id,))
        else:
            conn.execute("DELETE FROM events WHERE id = ? AND user_id = ?", (event_id, _uid(user_id)))


def clear_all_events_db(user_id):
    with _db() as conn:
        conn.execute("DELETE FROM events WHERE user_id = ?", (_uid(user_id),))


# ═════════════════ COFFRE-FORT (chiffré) ═════════════════
def migrate_vault_to_encrypted(user_id) -> int:
    """Chiffre les anciens secrets enregistrés en clair. Idempotent. Retourne le nombre de lignes migrées."""
    uid, migrated = _uid(user_id), 0
    try:
        with _db() as conn:
            for table, col in (("api_keys", "encrypted_key"), ("credentials", "encrypted_password")):
                rows = conn.execute(f"SELECT id, {col} FROM {table} WHERE user_id = ?", (uid,)).fetchall()
                for row_id, value in rows:
                    if value and not is_encrypted(value):
                        conn.execute(
                            f"UPDATE {table} SET {col} = ? WHERE id = ?",
                            (encrypt_secret(user_id, value), row_id),
                        )
                        migrated += 1
    except VaultKeyError:
        return 0
    return migrated


def load_api_keys_from_db(user_id):
    with _db() as conn:
        rows = conn.execute(
            "SELECT id, service, encrypted_key FROM api_keys WHERE user_id = ? ORDER BY id",
            (_uid(user_id),),
        ).fetchall()
    return [{"id": r[0], "service": r[1], "key": decrypt_secret(user_id, r[2])} for r in rows]


def add_api_key_to_db(user_id, service, secret):
    token = encrypt_secret(user_id, secret)  # lève VaultKeyError : jamais de stockage en clair
    with _db() as conn:
        conn.execute(
            "INSERT INTO api_keys (user_id, service, encrypted_key) VALUES (?, ?, ?)",
            (_uid(user_id), service.strip(), token),
        )


def delete_api_key_from_db(key_id, user_id):
    with _db() as conn:
        conn.execute("DELETE FROM api_keys WHERE id = ? AND user_id = ?", (key_id, _uid(user_id)))


def load_credentials_from_db(user_id):
    with _db() as conn:
        rows = conn.execute(
            "SELECT id, site, username, encrypted_password FROM credentials WHERE user_id = ? ORDER BY id",
            (_uid(user_id),),
        ).fetchall()
    return [{"id": r[0], "site": r[1], "user": r[2], "pass": decrypt_secret(user_id, r[3])} for r in rows]


def add_credential_to_db(user_id, site, username, password):
    token = encrypt_secret(user_id, password)
    with _db() as conn:
        conn.execute(
            "INSERT INTO credentials (user_id, site, username, encrypted_password) VALUES (?, ?, ?, ?)",
            (_uid(user_id), site.strip(), username.strip(), token),
        )


def delete_credential_from_db(cred_id, user_id):
    with _db() as conn:
        conn.execute("DELETE FROM credentials WHERE id = ? AND user_id = ?", (cred_id, _uid(user_id)))


# ═════════════════ CONTACTS ═════════════════
def load_contacts_from_db(user_id):
    with _db() as conn:
        rows = conn.execute(
            "SELECT id, name, email, phone, category, notes FROM contacts WHERE user_id = ? ORDER BY name COLLATE NOCASE",
            (_uid(user_id),),
        ).fetchall()
    return [{"id": r[0], "name": r[1], "email": r[2], "phone": r[3], "cat": r[4], "notes": r[5]} for r in rows]


def add_contact_to_db(user_id, name, email, phone, category, notes):
    with _db() as conn:
        conn.execute(
            "INSERT INTO contacts (user_id, name, email, phone, category, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (_uid(user_id), name.strip(), email.strip(), phone.strip(), category, notes),
        )


def delete_contact_from_db(contact_id, user_id):
    with _db() as conn:
        conn.execute("DELETE FROM contacts WHERE id = ? AND user_id = ?", (contact_id, _uid(user_id)))
