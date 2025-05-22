import jwt
import os
from flask import Blueprint, request
from .utils import db, validate, password

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.get("/")
def get_user_data():
    """Get user data.
        
    Returns:
        200 OK: {
        'id': ,
        'username':'',
        'content_type': '',
        'target_audience': '',
        'additional_context': '',
        'generations': [],
        'favorite_generations': []
    }
        400 Bad Request: {"success": false, "message": error_message}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]
    
    return {
        "success": True,
        "message": "User found.",
        "user": user
    }, 200