from flask import Blueprint, request
from .utils import db, validate, log
from datetime import datetime

bp = Blueprint("settings", __name__, url_prefix="/settings")

@bp.delete("/delete-account")
def delete_user():
    """
    Delete a user's account.

    Headers:
        Authorization: Bearer <jwt_token> - Required. JWT token for user authentication

    Returns:
        200 OK: {
            "success": true, 
            "message": "Account deleted successfully"
        }
        401 Unauthorized: {"success": false, "message": "Authorization token required" or validation error}
    """

    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} Failed to delete account: Authorization token required.")
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} Failed to delete account: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]
    
    # Delete user account
    delete_result = db.delete_user(user["id"])
    if not delete_result["success"]:
        log.append(f"{datetime.now()} Failed to delete account for user {user['username']}: {delete_result['message']}")
        return delete_result, 400
    
    log.append(f"{datetime.now()} User {user['username']} account deleted successfully.")

    return {
        "success": True,
        "message": "Account deleted successfully",
    }, 200

@bp.post("/content-type")
def update_content_type():
    """Update a user's content type preference.
    
    Headers:
        Authorization: Bearer <jwt_token> - Required. JWT token for user authentication
        
    Request Body:
        {
            "content_type": "string" - Required. The content type preference to set
        }
        
    Returns:
        200 OK: {
            "success": true, 
            "message": "Content type updated successfully"
        }
        400 Bad Request: {"success": false, "message": "Content type cannot be empty" or error_message}
        401 Unauthorized: {"success": false, "message": "Authorization token required" or validation error}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} Failed to update content type: Authorization token required.")
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} Failed to update content type: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    data = request.json or {}
    content_type = data.get("content_type", "")

    if not content_type:
        log.append(f"{datetime.now()} Failed to update content type: Content type cannot be empty.")
        return {"success": False, "message": "Content type cannot be empty"}, 400

    # Extract user from validation result
    user = validation_result["user"]
    
    # Update user content type
    update_result = db.update_user_content_type(user["id"], content_type)
    if not update_result["success"]:
        log.append(f"{datetime.now()} Failed to update content type for user {user['username']}: {update_result['message']}")
        return update_result, 400

    log.append(f"{datetime.now()} User {user['username']} content type set to: {content_type}.")

    return {
        "success": True,
        "message": "Content type updated successfully",
    }, 200


@bp.post("/target")
def update_target_audience():
    """Update a user's target audience preference.
    
    Headers:
        Authorization: Bearer <jwt_token> - Required. JWT token for user authentication
        
    Request Body:
        {
            "target_audience": "string" - Required. The target audience preference to set
        }
        
    Returns:
        200 OK: {
            "success": true, 
            "message": "Target audience updated successfully"
        }
        400 Bad Request: {"success": false, "message": "Target audience cannot be empty" or error_message}
        401 Unauthorized: {"success": false, "message": "Authorization token required" or validation error}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} Failed to update target audience: Authorization token required.")
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} Failed to update target audience: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    data = request.json or {}
    target_audience = data.get("target_audience", "")

    if not target_audience:
        log.append(f"{datetime.now()} Failed to update target audience: Target audience cannot be empty.")
        return {"success": False, "message": "Target audience cannot be empty"}, 400

    # Extract user from validation result
    user = validation_result["user"]
    
    # Update user target audience
    update_result = db.update_user_target_audience(user["id"], target_audience)
    if not update_result["success"]:
        log.append(f"{datetime.now()} Failed to update target audience for user {user['username']}: {update_result['message']}")
        return update_result, 400
    
    log.append(f"{datetime.now()} User {user['username']} target audience set to: {target_audience}.")

    return {
        "success": True,
        "message": "Target audience updated successfully",
    }, 200


@bp.post("/additional-context")
def update_additional_context():
    """Update a user's additional context preference.
    
    Headers:
        Authorization: Bearer <jwt_token> - Required. JWT token for user authentication
        
    Request Body:
        {
            "additional_context": "string" - Required. The additional context to set (can be empty string)
        }
        
    Returns:
        200 OK: {
            "success": true, 
            "message": "Additional context updated successfully"
        }
        400 Bad Request: {"success": false, "message": error_message}
        401 Unauthorized: {"success": false, "message": "Authorization token required" or validation error}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} Failed to update additional context: Authorization token required.")
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} Failed to update additional context: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    data = request.json or {}
    additional_context = data.get("additional_context", "")
    
    # Extract user from validation result
    user = validation_result["user"]
    
    # Update user additional context
    update_result = db.update_user_additional_context(user["id"], additional_context)
    if not update_result["success"]:
        log.append(f"{datetime.now()} Failed to update additional context for user {user['username']}: {update_result['message']}")
        return update_result, 400
    
    if additional_context:
        log.append(f"{datetime.now()} User {user['username']} additional context set to: {additional_context}.")
    else:
        log.append(f"{datetime.now()} User {user['username']} additional context cleared.")

    return {
        "success": True,
        "message": "Additional context updated successfully",
    }, 200