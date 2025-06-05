import jwt
import os
from . import db


def is_username_valid(username="") -> dict:
    if not username:
        return {"success": False, "message": "El usuario no puede estar vacío."}
    if len(username) < 3 or len(username) > 20:
        return {
            "success": False,
            "message": "El nombre de usuario debe tener entre 3 y 20 caracteres.",
        }
    if not username.isalnum():
        return {
            "success": False,
            "message": "El nombre de usuario solo puede contener letras y números.",
        }
    return {"success": True, "message": "Nombre de usuario válido."}


def is_password_valid(password="") -> dict:
    if not password:
        return {"success": False, "message": "La contraseña no puede estar vaía."}
    if len(password) < 8:
        return {
            "success": False,
            "message": "La contraseña debe tener al menos 8 caracteres.",
        }
    if len(password) > 80:
        return {
            "success": False,
            "message": "La contraseña debe tener como máximo 80 caracteres.",
        }
    if not any(char.isdigit() for char in password):
        return {
            "success": False,
            "message": "La contraseña debe contener al menos un dígito.",
        }
    if not any(char.isalpha() for char in password):
        return {
            "success": False,
            "message": "La contraseña debe contener al menos una letra.",
        }
    return {"success": True, "message": "Contraseña válida."}


def validate_jwt(token="") -> dict:
    """
    Validates a JWT token and returns the user information if valid.

    Args:
        token (str): The JWT token to validate

    Returns:
        dict: A dictionary with success status and user object if successful
    """
    if not token:
        return {"success": False, "message": "El token no puede estar vacío."}

    try:
        # Decode token
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        user_id = payload.get("id")

        if not user_id:
            return {"success": False, "message": "Formato del token inválido."}

        # Verify user exists and get user information
        user_result = db.get_user_by_id(user_id)
        if not user_result["success"]:
            return {"success": False, "message": "Token inválido - no se encuentra el usuario."}

        # Return the successful result with user object
        return {
            "success": True,
            "message": "Token válido.",
            "user": user_result["user"],
        }

    except jwt.ExpiredSignatureError:
        return {"success": False, "message": "Token expirado."}

    except jwt.InvalidTokenError:
        return {"success": False, "message": "Token inválido."}

    except Exception as e:
        return {"success": False, "message": f"Error al validar el token: {str(e)}"}
