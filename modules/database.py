import sqlite3
import hashlib
import os
from datetime import datetime, date, time

DB_NAME = "pavelcore_workspace.db"

def get_connection():
    """Établit la connexion avec la base de données SQLite."""
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def hash_password(password: str, salt: bytes = None) -> tuple[str, str]:
    """Hache un mot de passe avec SHA-256 et un sel unique."""
    if salt is None:
        salt = os.urandom(16)
    else:
        salt = bytes.fromhex(salt)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return pwd_hash.hex(), salt.hex()

def verify_password(password: str, stored_hash: str, stored_salt: str) -> bool:
    """Vérifie si un mot de passe correspond au hash stocké."""
    pwd_hash, _ = hash_password(password, stored_salt)
    return pwd_hash == stored_hash

def init_db():
    """Initialise la base de données et crée toutes les tables nécessaires."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            event_date TEXT NOT NULL,
            event_time TEXT NOT NULL,
            category TEXT,
            description TEXT,
            ringtone TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            service TEXT NOT NULL,
            encrypted_key TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            site TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            category TEXT,
            notes TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# --- GESTION UTILISATEURS ---
def create_user_db(email: str, password: str) -> tuple[bool, str]:
    init_db()
    email_clean = email.strip().lower()
    if not email_clean or not password:
        return False, "Veuillez remplir tous les champs."
    
    pwd_hash, salt = hash_password(password)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password_hash, salt, created_at) VALUES (?, ?, ?, ?)",
                       (email_clean, pwd_hash, salt, now_str))
        conn.commit()
        conn.close()
        return True, "Compte créé avec succès ! Vous pouvez vous connecter."
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Cet e-mail est déjà utilisé."

def authenticate_user_db(email: str, password: str) -> tuple[bool, dict | str]:
    init_db()
    email_clean = email.strip().lower()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, password_hash, salt FROM users WHERE email = ?", (email_clean,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return False, "Adresse e-mail ou mot de passe incorrect."
    
    user_id, user_email, stored_hash, stored_salt = row
    if verify_password(password, stored_hash, stored_salt):
        return True, {"id": user_id, "email": user_email}
    return False, "Adresse e-mail ou mot de passe incorrect."

# --- GESTION AGENDA (Filtré par user_id) ---
def load_events_from_db(user_id: int):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, event_date, event_time, category, description, ringtone FROM events WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    events = []
    for row in rows:
        try:
            ev_date = datetime.strptime(row[2], "%Y-%m-%d").date()
        except ValueError:
            ev_date = date.today()
        try:
            ev_time = datetime.strptime(row[3], "%H:%M").time()
        except ValueError:
            ev_time = time(12, 0)
            
        events.append({
            "id": row[0], "title": row[1], "date": ev_date, "time": ev_time,
            "category": row[4], "desc": row[5], "ringtone": row[6]
        })
    return events

def add_event_to_db(user_id: int, title, ev_date, ev_time, category, desc, ringtone):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events (user_id, title, event_date, event_time, category, description, ringtone)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, title, ev_date.strftime("%Y-%m-%d"), ev_time.strftime("%H:%M"), category, desc, ringtone))
    conn.commit()
    conn.close()

def delete_event_from_db(event_id: int):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

# --- GESTION COFFRE-FORT (Filtré par user_id) ---
def load_api_keys_from_db(user_id: int):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, service, encrypted_key FROM api_keys WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "service": r[1], "key": r[2]} for r in rows]

def add_api_key_to_db(user_id: int, service, encrypted_key):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO api_keys (user_id, service, encrypted_key) VALUES (?, ?, ?)", (user_id, service, encrypted_key))
    conn.commit()
    conn.close()

def load_credentials_from_db(user_id: int):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, site, username, encrypted_password FROM credentials WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "site": r[1], "user": r[2], "pass": r[3]} for r in rows]

def add_credential_to_db(user_id: int, site, username, encrypted_password):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO credentials (user_id, site, username, encrypted_password) VALUES (?, ?, ?, ?)", (user_id, site, username, encrypted_password))
    conn.commit()
    conn.close()

# --- GESTION CONTACTS (Filtré par user_id) ---
def load_contacts_from_db(user_id: int):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone, category, notes FROM contacts WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "email": r[2], "phone": r[3], "cat": r[4], "notes": r[5]} for r in rows]

def add_contact_to_db(user_id: int, name, email, phone, category, notes):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (user_id, name, email, phone, category, notes) VALUES (?, ?, ?, ?, ?, ?)", (user_id, name, email, phone, category, notes))
    conn.commit()
    conn.close()
