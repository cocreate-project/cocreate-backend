import sqlite3

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
            generations TEXT,
        )
    ''')

    # Generations table creation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat TEXT NOT NULL,
        )
    ''')
    
    cursor.close()
    conn.commit()
    conn.close()