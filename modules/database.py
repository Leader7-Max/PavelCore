import sqlite3
from datetime import datetime, date, time

DB_NAME = "pavelcore_workspace.db"

def get_connection():
    """Établit la connexion avec la base de données SQLite."""
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    """Initialise la base de données et crée les tables nécessaires si elles n'existent pas."""
    conn = get_connection()
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()

def load_events_from_db():
    """Charge tous les événements de la base de données vers l'application."""
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
            "id": row[0],
            "title": row[1],
            "date": ev_date,
            "time": ev_time,
            "category": row[4],
            "desc": row[5],
            "ringtone": row[6]
        })
    return events

def add_event_to_db(title, ev_date, ev_time, category, desc, ringtone):
    """Enregistre un nouvel événement dans SQLite."""
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
    """Supprime un événement de la base de données par son ID."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

def clear_all_events_db():
    """Vide entièrement la table des événements."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events")
    conn.commit()
    conn.close()
