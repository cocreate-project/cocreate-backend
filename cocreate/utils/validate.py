import jwt
import os
from . import db


def is_username_valid(username="") -> dict:
    if not username:
        return {"success": False, "message": "Username cannot be empty."}
    if len(username) < 3 or len(username) > 20:
        return {
            "success": False,
            "message": "Username must be between 3 and 20 characters.",
        }
    if not username.isalnum():
        return {
            "success": False,
            "message": "Username can only contain letters and numbers.",
        }
    return {"success": True, "message": "Username is valid."}


def is_password_valid(password="") -> dict:
    if not password:
        return {"success": False, "message": "Password cannot be empty."}
    if len(password) < 8:
        return {
            "success": False,
            "message": "Password must be at least 8 characters long.",
        }
    if len(password) > 80:
        return {
            "success": False,
            "message": "Password must be at most 80 characters long.",
        }
    if not any(char.isdigit() for char in password):
        return {
            "success": False,
            "message": "Password must contain at least one digit.",
        }
    if not any(char.isalpha() for char in password):
        return {
            "success": False,
            "message": "Password must contain at least one letter.",
        }
    return {"success": True, "message": "Password is valid."}


def validate_jwt(token="") -> dict:
    """
    Validates a JWT token and returns the user information if valid.

    Args:
        token (str): The JWT token to validate

    Returns:
        dict: A dictionary with success status and user object if successful
    """
    if not token:
        return {"success": False, "message": "Token cannot be empty."}

    try:
        # Decode token
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        user_id = payload.get("id")

        if not user_id:
            return {"success": False, "message": "Invalid token format."}

        # Verify user exists and get user information
        user_result = db.get_user_by_id(user_id)
        if not user_result["success"]:
            return {"success": False, "message": "Invalid token - user not found."}

        # Return the successful result with user object
        return {
            "success": True,
            "message": "Token is valid.",
            "user": user_result["user"],
        }

    except jwt.ExpiredSignatureError:
        return {"success": False, "message": "Token expired."}

    except jwt.InvalidTokenError:
        return {"success": False, "message": "Invalid token."}

    except Exception as e:
        return {"success": False, "message": f"Error validating token: {str(e)}"}
