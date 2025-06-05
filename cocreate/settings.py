from flask import Blueprint, request
from .utils import db, validate

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
            "message": "Cuenta eliminada con éxito"
        }
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
    
    # Delete user account
    delete_result = db.delete_user(user["id"])
    if not delete_result["success"]:
        return delete_result, 400

    return {
        "success": True,
        "message": "Cuenta eliminada con éxito",
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
            "message": "Tipo de contenido actualizado con éxito"
        }
        400 Bad Request: {"success": false, "message": "El tipo de contenido no puede estar vacío" or error_message}
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

    data = request.json or {}
    content_type = data.get("content_type", "")

    if not content_type:
        return {"success": False, "message": "El tipo de contenido no puede estar vacío"}, 400

    # Extract user from validation result
    user = validation_result["user"]
    
    # Update user content type
    update_result = db.update_user_content_type(user["id"], content_type)
    if not update_result["success"]:
        return update_result, 400

    return {
        "success": True,
        "message": "Tipo de contenido actualizado con éxito",
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
            "message": "Público objetivo actualizado con éxito"
        }
        400 Bad Request: {"success": false, "message": "El público objetivo no puede estar vacío" or error_message}
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

    data = request.json or {}
    target_audience = data.get("target_audience", "")

    if not target_audience:
        return {"success": False, "message": "El público objetivo no puede estar vacío"}, 400

    # Extract user from validation result
    user = validation_result["user"]
    
    # Update user target audience
    update_result = db.update_user_target_audience(user["id"], target_audience)
    if not update_result["success"]:
        return update_result, 400

    return {
        "success": True,
        "message": "Público objetivo actualizado con éxito",
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
            "message": "Contexto adicional actualizado con éxito"
        }
        400 Bad Request: {"success": false, "message": error_message}
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

    data = request.json or {}
    additional_context = data.get("additional_context", "")
    
    # Extract user from validation result
    user = validation_result["user"]
    
    # Update user additional context
    update_result = db.update_user_additional_context(user["id"], additional_context)
    if not update_result["success"]:
        return update_result, 400

    return {
        "success": True,
        "message": "Contexto adicional actualizado con éxito",
    }, 200