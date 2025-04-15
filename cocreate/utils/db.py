import sqlite3
from .password import hash

def create_database() -> None:
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

def create_user(_username="", _password="", _content_type="", _target_audience="", _additional_context=""):
    conn = sqlite3.connect('cocreate.db')
    cursor = conn.cursor()

    try:
        password_hash = hash(_password)
        formatted_username = _username.lower()

        cursor.execute('''
            INSERT INTO users (username, password, content_type, target_audience, additional_context, generations)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (formatted_username, password_hash, _content_type, _target_audience, _additional_context, "[]"))

        conn.commit()
        return {"success": True, "message": f"User {formatted_username} created.", "username": formatted_username}

    except sqlite3.IntegrityError:
        return {"success": False, "message": "User already exists."}

    finally:
        cursor.close()
        conn.close()

def get_user_by_id(id):
    conn = sqlite3.connect('cocreate.db')
    cursor = conn.cursor()

    try:
        user = cursor.execute('SELECT id, username, content_type, target_audience, additional_context, generations FROM users WHERE id = ?', [str(id)]).fetchone()

        if user is None:
            return {"success": False, "message": "User not found."}

        return {"success": True, "message": "User found.", "user": user}

    except sqlite3.Error as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

    finally:
        cursor.close()
        conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect('cocreate.db')
    cursor = conn.cursor()

    try:
        user = cursor.execute('SELECT id, username, content_type, target_audience, additional_context, generations FROM users WHERE username = ?', [username]).fetchone()

        if user is None:
            return {"success": False, "message": "User not found."}

        return {"success": True, "message": "User found.", "user": user}

    except sqlite3.Error as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

    finally:
        cursor.close()
        conn.close()

def get_user_password_by_id(id):
    conn = sqlite3.connect('cocreate.db')
    cursor = conn.cursor()

    password = cursor.execute('SELECT password FROM users WHERE id = ?', [str(id)]).fetchone()

    cursor.close()
    conn.commit()
    conn.close()

    return password[0]