from flask import Blueprint, request
from .utils import validate, log
from datetime import datetime

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.get("/")
def get_user_data():
    """Get user profile data for the authenticated user.
    
    Request Headers:
        Authorization: "Bearer <jwt_token>" - Required. The JWT token for authentication
        
    Returns:
        200 OK: {
            "success": true,
            "message": "User found.",
            "user": {
                "id": int,
                "username": string,
                "content_type": string,
                "target_audience": string,
                "additional_context": string,
                "generations": array,
                "favorite_generations": array
            }
        }
        401 Unauthorized: {"success": false, "message": error_message}
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

    log.append(f"{datetime.now()} User {user['username']} data retrieved successfully.")
    
    return {
        "success": True,
        "message": "User found.",
        "user": user
    }, 200