import os
import sqlite3
from datetime import date, time

def test_database_connection():
    """Vérifie que la base SQLite peut être initialisée et interrogée."""
    db_path = "pavelcore_workspace.db"
    
    # Connexion de test
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Création d'une table de test
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
    # Vérification que le fichier existe
    assert os.path.exists(db_path)
