import sqlite3
from . import password
from . import format


def create_database() -> None:
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    # Users table creation
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            content_type TEXT,
            target_audience TEXT,
            additional_context TEXT,
            generations TEXT
        )
    """
    )

    # Generations table creation
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat TEXT NOT NULL
        )
    """
    )

    cursor.close()
    conn.commit()
    conn.close()


def create_generation(_id=0, _chat=""):
    if id == 0:
        return

    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        user = get_user_by_id(_id)["user"]

        user_generations = user["generations"]

        print(user_generations)

        cursor.execute("INSERT INTO generations (chat) VALUES (?)", [_chat])

        gen_id = cursor.lastrowid

        user_generations.append(gen_id)

        cursor.execute("UPDATE users SET generations = ? WHERE id = ?", [str(user_generations), _id])

        conn.commit()

        return {
            "success": True,
            "message": f"Generation saved."
        }

    except sqlite3.IntegrityError:
        return {"success": False, "message": "Generation already exists."}

    finally:
        cursor.close()
        conn.close()


def create_user(
    _username="",
    _password="",
    _content_type="",
    _target_audience="",
    _additional_context="",
):
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        password_hash = password.hash(_password)
        formatted_username = _username.lower()

        cursor.execute(
            """
            INSERT INTO users (username, password, content_type, target_audience, additional_context, generations)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                formatted_username,
                password_hash,
                _content_type,
                _target_audience,
                _additional_context,
                "[]",
            ),
        )

        conn.commit()
        return {
            "success": True,
            "message": f"User {formatted_username} created.",
            "username": formatted_username,
        }

    except sqlite3.IntegrityError:
        return {"success": False, "message": "User already exists."}

    finally:
        cursor.close()
        conn.close()


def get_user_by_id(id):
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        user = cursor.execute(
            "SELECT id, username, content_type, target_audience, additional_context, generations FROM users WHERE id = ?",
            [str(id)],
        ).fetchone()

        if user is None:
            return {"success": False, "message": "User not found."}

        return {
            "success": True,
            "message": "User found.",
            "user": format.user_data(user),
        }

    except sqlite3.Error as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

    finally:
        cursor.close()
        conn.close()


def get_user_by_username(username):
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        user = cursor.execute(
            "SELECT id, username, content_type, target_audience, additional_context, generations FROM users WHERE username = ?",
            [username],
        ).fetchone()

        if user is None:
            return {"success": False, "message": "User not found."}

        return {
            "success": True,
            "message": "User found.",
            "user": format.user_data(user),
        }

    except sqlite3.Error as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

    finally:
        cursor.close()
        conn.close()


def get_user_password_by_id(id):
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    password = cursor.execute(
        "SELECT password FROM users WHERE id = ?", [str(id)]
    ).fetchone()

    cursor.close()
    conn.commit()
    conn.close()

    return password[0]


def update_user_content_type(user_id, content_type):
    """Update a user's content type preference."""
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET content_type = ?
            WHERE id = ?
            """,
            (content_type, str(user_id)),
        )

        if cursor.rowcount == 0:
            return {"success": False, "message": "User not found."}

        conn.commit()
        return {"success": True, "message": "Content type updated successfully."}

    except sqlite3.Error as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

    finally:
        cursor.close()
        conn.close()


def update_user_target_audience(user_id, target_audience):
    """Update a user's target audience preference."""
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET target_audience = ?
            WHERE id = ?
            """,
            (target_audience, str(user_id)),
        )

        if cursor.rowcount == 0:
            return {"success": False, "message": "User not found."}

        conn.commit()
        return {"success": True, "message": "Target audience updated successfully."}

    except sqlite3.Error as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

    finally:
        cursor.close()
        conn.close()


def update_user_additional_context(user_id, additional_context):
    """Update a user's additional context."""
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET additional_context = ?
            WHERE id = ?
            """,
            (additional_context, str(user_id)),
        )

        if cursor.rowcount == 0:
            return {"success": False, "message": "User not found."}

        conn.commit()
        return {"success": True, "message": "Additional context updated successfully."}

    except sqlite3.Error as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

    finally:
        cursor.close()
        conn.close()
