import jwt
import os
from flask import Blueprint, request
from .utils import db, validate, password

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
            "message": "Inicio de sesión exitoso", 
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
        return user_result, 400

    # Validate password
    user = user_result["user"]
    stored_password = db.get_user_password_by_id(user["id"])
    if not password.valid(pwd, stored_password):
        return {"success": False, "message": "Contraseña inválida"}, 400

    # Generate JWT token
    encoded_jwt = jwt.encode(
        {"id": user["id"]}, os.getenv("JWT_SECRET"), algorithm="HS256"
    )
    
    return {
        "success": True,
        "message": "Inicio de sesión exitoso",
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
            "message": "Registro exitoso", 
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
        return username_validation, 400

    # Validate password
    password_validation = validate.is_password_valid(pwd)
    if not password_validation["success"]:
        return password_validation, 400

    # Create user
    create_result = db.create_user(username, pwd)
    if not create_result["success"]:
        return create_result, 400

    # Get user and generate token
    user_result = db.get_user_by_username(create_result["username"])
    user = user_result["user"]
    encoded_jwt = jwt.encode(
        {"id": user["id"]}, os.getenv("JWT_SECRET"), algorithm="HS256"
    )

    return {
        "success": True,
        "message": "Registro exitoso",
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
            "message": "Contraseña actualizada correctamente"
        }
        400 Bad Request: {"success": false, "message": "La contraseña no puede estar vacía"}
        401 Unauthorized: {"success": false, "message": "Token de autorización requerido" or validation error}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return {"success": False, "message": "Token de autorización requerido"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    data = request.json or {}
    new_pwd = data.get("password", "")

    if not new_pwd:
        return {"success": False, "message": "La contraseña no puede estar vacía"}, 400
    
    # Update user account password
    update_password_result = db.update_user_password_by_id(user["id"], new_pwd)
    if not update_password_result["success"]:
        return update_password_result, 401
    
    
    return {
        "success": True,
        "message": "Contraseña actualizada correctamente"
    }, 200
