import sqlite3
import password

def create_database():
    conn = sqlite3.connect('cocreate.db')
    cursor = conn.cursor()

    # Users table creation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            content_type TEXT,
            target_audience TEXT,
            additional_context TEXT,
            generations TEXT
        )
    ''')

    # Generations table creation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat TEXT NOT NULL
        )
    ''')
    
    cursor.close()
    conn.commit()
    conn.close()

def create_user(_username, _password, _content_type, _target_audience, _additional_context):
    conn = sqlite3.connect('cocreate.db')
    cursor = conn.cursor()

    password_hash = password.hash_password(_password)

    # Insert a new user
    cursor.execute('''
        INSERT INTO users (username, password, content_type, target_audience, additional_context)
        VALUES (?, ?, ?, ?, ?)
    ''', (_username, password_hash, _content_type, _target_audience, _additional_context))

    cursor.close()
    conn.commit()
    conn.close()