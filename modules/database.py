import sqlite3
from datetime import datetime, date, time

DB_NAME = "pavelcore_workspace.db"

def get_connection():
    """Établit la connexion avec la base de données SQLite."""
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    """Initialise la base de données et crée toutes les tables nécessaires."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table Agenda
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            event_date TEXT NOT NULL,
            event_time TEXT NOT NULL,
            category TEXT,
            description TEXT,
            ringtone TEXT
        )
    ''')
    
    # Table Clés API (Coffre-fort)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            encrypted_key TEXT NOT NULL
        )
    ''')
    
    # Table Identifiants / Mots de passe (Coffre-fort)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL
        )
    ''')
    
    # Table Contacts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            category TEXT,
            notes TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# --- GESTION AGENDA ---
def load_events_from_db():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, event_date, event_time, category, description, ringtone FROM events")
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

def add_event_to_db(title, ev_date, ev_time, category, desc, ringtone):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events (title, event_date, event_time, category, description, ringtone)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, ev_date.strftime("%Y-%m-%d"), ev_time.strftime("%H:%M"), category, desc, ringtone))
    conn.commit()
    conn.close()

def delete_event_from_db(event_id):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

def clear_all_events_db():
    """Supprime tous les événements de la base de données."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events")
    conn.commit()
    conn.close()

# --- GESTION COFFRE-FORT (API Keys & Credentials) ---
def load_api_keys_from_db():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, service, encrypted_key FROM api_keys")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "service": r[1], "key": r[2]} for r in rows]

def add_api_key_to_db(service, encrypted_key):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO api_keys (service, encrypted_key) VALUES (?, ?)", (service, encrypted_key))
    conn.commit()
    conn.close()

def load_credentials_from_db():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, site, username, encrypted_password FROM credentials")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "site": r[1], "user": r[2], "pass": r[3]} for r in rows]

def add_credential_to_db(site, username, encrypted_password):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO credentials (site, username, encrypted_password) VALUES (?, ?, ?)", (site, username, encrypted_password))
    conn.commit()
    conn.close()

# --- GESTION CONTACTS ---
def load_contacts_from_db():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone, category, notes FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "email": r[2], "phone": r[3], "cat": r[4], "notes": r[5]} for r in rows]

def add_contact_to_db(name, email, phone, category, notes):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, email, phone, category, notes) VALUES (?, ?, ?, ?, ?)", (name, email, phone, category, notes))
    conn.commit()
    conn.close()
