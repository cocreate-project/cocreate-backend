import jwt
import os
from flask import Blueprint, request
from .utils import db, validate, password, log
from datetime import datetime

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/login")
def login():
    """Handle user login and generate JWT token on success.
    
    Request Body:
        {
            "username": "string" - Required. The user's username
            "password": "string" - Required. The user's password
        }
        
    Returns:
        200 OK: {
            "success": true, 
            "message": "Login successful", 
            "access_token": "<jwt_token>",
            "user": {user_object}
        }
        400 Bad Request: {"success": false, "message": error_message}
    """
    data = request.json or {}

    username = data.get("username", "").lower()
    pwd = data.get("password", "")

    # Validate user exists
    user_result = db.get_user_by_username(username)
    if not user_result["success"]:
        log.append(f"{datetime.now()} Intento de inicio de sesión fallido para el usuario {username}: Usuario no encontrado.")
        return user_result, 400

    # Validate password
    user = user_result["user"]
    stored_password = db.get_user_password_by_id(user["id"])
    if not password.valid(pwd, stored_password):
        log.append(f"{datetime.now()} Intento de inicio de sesión fallido para el usuario {username}: Contraseña inválida.")
        return {"success": False, "message": "Invalid password"}, 400

    # Generate JWT token
    encoded_jwt = jwt.encode(
        {"id": user["id"]}, os.getenv("JWT_SECRET"), algorithm="HS256"
    )
    
    # Log successful login
    log.append(f"{datetime.now()} Usuario {username} inició sesión con éxito.")

    return {
        "success": True,
        "message": "Login successful",
        "access_token": encoded_jwt,
        "user": user,
    }, 200


@bp.post("/register")
def register():
    """Register a new user and return JWT token on success.
    
    Request Body:
        {
            "username": "string" - Required. The username for the new account
            "password": "string" - Required. The password for the new account
        }
        
    Returns:
        200 OK: {
            "success": true, 
            "message": "Registration successful", 
            "access_token": "<jwt_token>",
            "user": {user_object}
        }
        400 Bad Request: {"success": false, "message": error_message}
    """
    data = request.json or {}

    username = data.get("username", "").lower()
    pwd = data.get("password", "")

    # Validate username
    username_validation = validate.is_username_valid(username)
    if not username_validation["success"]:
        log.append(f"{datetime.now()} Intento de registro fallido para el usuario {username}: {username_validation['message']}")
        return username_validation, 400

    # Validate password
    password_validation = validate.is_password_valid(pwd)
    if not password_validation["success"]:
        log.append(f"{datetime.now()} Intento de registro fallido para el usuario {username}: {password_validation['message']}")
        return password_validation, 400

    # Create user
    create_result = db.create_user(username, pwd)
    if not create_result["success"]:
        log.append(f"{datetime.now()} Intento de registro fallido para el usuario {username}: {create_result['message']}")
        return create_result, 400

    # Get user and generate token
    user_result = db.get_user_by_username(create_result["username"])
    user = user_result["user"]
    encoded_jwt = jwt.encode(
        {"id": user["id"]}, os.getenv("JWT_SECRET"), algorithm="HS256"
    )

    log.append(f"{datetime.now()} Usuario {username} registrado con éxito.")

    return {
        "success": True,
        "message": "Registration successful",
        "access_token": encoded_jwt,
        "user": user,
    }, 200



@bp.post("/update-password")
def update_password():
    """Update user password.

    Headers:
        Authorization: Bearer <jwt_token> - Required. JWT token for user authentication
    
    Request Body:
        {
            "password": "string" - Required. The new password for the account
        }
        
    Returns:
        200 OK: {
            "success": true, 
            "message": "Password updated successfully"
        }
        400 Bad Request: {"success": false, "message": "Password cannot be empty."}
        401 Unauthorized: {"success": false, "message": "Authorization token required" or validation error}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} No se pudo actualizar la contraseña: Token de autorización requerido.")
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} No se pudo actualizar la contraseña: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    data = request.json or {}
    new_pwd = data.get("password", "")

    if not new_pwd:
        log.append(f"{datetime.now()} No se pudo actualizar la contraseña para el usuario {user['username']}: La contraseña no puede estar vacía.")
        return {"success": False, "message": "Password cannot be empty."}, 400
    
    # Update user account password
    update_password_result = db.update_user_password_by_id(user["id"], new_pwd)
    if not update_password_result["success"]:
        log.append(f"{datetime.now()} No se pudo actualizar la contraseña para el usuario {user['username']}: {update_password_result['message']}")
        return update_password_result, 401
    log.append(f"{datetime.now()} La contraseña del usuario {user['username']} ha sido actualizada con éxito.")

    return {
        "success": True,
        "message": "Password updated successfully"
    }, 200
