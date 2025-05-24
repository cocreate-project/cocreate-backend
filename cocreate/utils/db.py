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
            generations TEXT,
            favorite_generations TEXT
        )
    """
    )

    # Generations table creation
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            chat TEXT NOT NULL
        )
    """
    )

    cursor.close()
    conn.commit()
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
            INSERT INTO users (username, password, content_type, target_audience, additional_context, generations, favorite_generations)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                formatted_username,
                password_hash,
                _content_type,
                _target_audience,
                _additional_context,
                "[]",
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
            "SELECT id, username, content_type, target_audience, additional_context, generations, favorite_generations FROM users WHERE id = ?",
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
            "SELECT id, username, content_type, target_audience, additional_context, generations, favorite_generations FROM users WHERE username = ?",
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

def update_user_password_by_id(user_id, new_password):
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        password_hash = password.hash(new_password)

        cursor.execute(
            """
            UPDATE users
            SET password = ?
            WHERE id = ?
            """,
            (password_hash, str(user_id)),
        )

        if cursor.rowcount == 0:
            return {"success": False, "message": "User not found."}
        
        conn.commit()

        user = cursor.execute(
            "SELECT * FROM users WHERE id = ?", [str(user_id)]
        ).fetchone()

        return {
            "success": True,
            "message": "Password updated successfully."
        }
        
    except sqlite3.Error as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

    finally:
        cursor.close()
        conn.close()


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


def delete_user(user_id):
    """Delete a user from the database."""
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM users
            WHERE id = ?
            """,
            (str(user_id),),
        )

        if cursor.rowcount == 0:
            return {"success": False, "message": "User not found."}

        conn.commit()
        return {"success": True, "message": "User deleted successfully."}

    except sqlite3.Error as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

    finally:
        cursor.close()
        conn.close()


def create_generation(_id=0, _type="unknown", _chat=""):
    if _id == 0:
        return

    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        user = get_user_by_id(_id)["user"]

        user_generations = user["generations"]

        cursor.execute(
            "INSERT INTO generations (type, chat) VALUES (?, ?)", [_type, _chat]
        )

        gen_id = cursor.lastrowid

        user_generations.append(gen_id)

        gen_string = "["
        for i in range(0, len(user_generations)):
            if i == len(user_generations) - 1:
                gen_string += str(user_generations[i])
            else:
                gen_string += str(user_generations[i]) + ", "

        gen_string += "]"

        cursor.execute(
            "UPDATE users SET generations = ? WHERE id = ?", [gen_string, _id]
        )

        conn.commit()

        return {"success": True, "message": f"Generation saved."}

    except sqlite3.IntegrityError:
        return {"success": False, "message": "Generation already exists."}

    finally:
        cursor.close()
        conn.close()


def get_generations_by_user_id(user_id):
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        generations = cursor.execute(
            "SELECT * FROM generations WHERE id IN (SELECT json_each.value FROM users, json_each(generations) WHERE users.id = ?)",
            [str(user_id)],
        ).fetchall()

        if generations is None:
            return {"success": False, "message": "Generations not found."}

        return {
            "success": True,
            "message": "Generations found.",
            "data": format.generation_data(generations),
        }

    except sqlite3.Error as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

    finally:
        cursor.close()
        conn.close()


def get_generation_by_gen_id(user_id, gen_id):
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        generation = cursor.execute(
            "SELECT * FROM generations WHERE id IN (SELECT json_each.value FROM users, json_each(generations) WHERE users.id = ?) AND id = ?",
            [str(user_id), str(gen_id)],
        ).fetchone()

        if generation is None:
            return {"success": False, "message": "Generation not found for this user."}

        return {
            "success": True,
            "message": "Generation found.",
            "data": format.generation_data([generation]),
        }

    except sqlite3.Error as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

    finally:
        cursor.close()
        conn.close()


def save_generation(user_id, generation_id):
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        user = get_user_by_id(user_id)["user"]

        user_generations = user["generations"]
        user_saved_generations = user["favorite_generations"]

        if int(generation_id) in user_saved_generations:
            return {"success": False, "message": "Generation already saved."}

        if int(generation_id) not in user_generations:
            return {"success": False, "message": "Generation not found."}

        user_saved_generations.append(int(generation_id))

        gen_string = "["
        for i in range(0, len(user_saved_generations)):
            if i == len(user_saved_generations) - 1:
                gen_string += str(user_saved_generations[i])
            else:
                gen_string += str(user_saved_generations[i]) + ", "

        gen_string += "]"

        cursor.execute(
            "UPDATE users SET favorite_generations = ? WHERE id = ?",
            [gen_string, user_id],
        )

        conn.commit()

        return {"success": True, "message": f"Generation favorited."}

    except sqlite3.IntegrityError:
        return {"success": False, "message": "Generation already exists."}

    finally:
        cursor.close()
        conn.close()


def unsave_generation(user_id, generation_id):
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        user = get_user_by_id(user_id)["user"]

        user_saved_generations = user["favorite_generations"]

        if int(generation_id) not in user_saved_generations:
            return {"success": False, "message": "Generation not found in saved."}

        user_saved_generations.remove(int(generation_id))

        gen_string = "["
        for i in range(0, len(user_saved_generations)):
            if i == len(user_saved_generations) - 1:
                gen_string += str(user_saved_generations[i])
            else:
                gen_string += str(user_saved_generations[i]) + ", "

        gen_string += "]"

        cursor.execute(
            "UPDATE users SET favorite_generations = ? WHERE id = ?",
            [gen_string, user_id],
        )

        conn.commit()

        return {"success": True, "message": f"Generation unfavorited."}

    except sqlite3.Error as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

    finally:
        cursor.close()
        conn.close()


def get_saved_generations_by_user_id(user_id):
    conn = sqlite3.connect("cocreate.db")
    cursor = conn.cursor()

    try:
        generations = cursor.execute(
            "SELECT * FROM generations WHERE id IN (SELECT json_each.value FROM users, json_each(favorite_generations) WHERE users.id = ?)",
            [str(user_id)],
        ).fetchall()

        if generations is None:
            return {"success": False, "message": "Generations not found."}

        return {
            "success": True,
            "message": "Generations found.",
            "data": format.generation_data(generations),
        }

    except sqlite3.Error as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

    finally:
        cursor.close()
        conn.close()
