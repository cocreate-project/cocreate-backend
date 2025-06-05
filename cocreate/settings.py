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
        log.append(f"{datetime.now()} No se pudo eliminar la cuenta: Token de autorización requerido.")
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} No se pudo eliminar la cuenta: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]
    
    # Delete user account
    delete_result = db.delete_user(user["id"])
    if not delete_result["success"]:
        log.append(f"{datetime.now()} No se pudo eliminar la cuenta del usuario {user['username']}: {delete_result['message']}")
        return delete_result, 400
    
    log.append(f"{datetime.now()} Cuenta del usuario {user['username']} eliminada con éxito.")

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
        log.append(f"{datetime.now()} No se pudo actualizar el tipo de contenido: Token de autorización requerido.")
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} No se pudo actualizar el tipo de contenido: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    data = request.json or {}
    content_type = data.get("content_type", "")

    if not content_type:
        log.append(f"{datetime.now()} No se pudo actualizar el tipo de contenido: El tipo de contenido no puede estar vacío.")
        return {"success": False, "message": "Content type cannot be empty"}, 400

    # Extract user from validation result
    user = validation_result["user"]
    
    # Update user content type
    update_result = db.update_user_content_type(user["id"], content_type)
    if not update_result["success"]:
        log.append(f"{datetime.now()} No se pudo actualizar el tipo de contenido para el usuario {user['username']}: {update_result['message']}")
        return update_result, 400

    log.append(f"{datetime.now()} Tipo de contenido del usuario {user['username']} actualizado a: {content_type}.")

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
        log.append(f"{datetime.now()} No se pudo actualizar el público objetivo: Token de autorización requerido.")
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} No se pudo actualizar el público objetivo: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    data = request.json or {}
    target_audience = data.get("target_audience", "")

    if not target_audience:
        log.append(f"{datetime.now()} No se pudo actualizar el público objetivo: El público objetivo no puede estar vacío.")
        return {"success": False, "message": "Target audience cannot be empty"}, 400

    # Extract user from validation result
    user = validation_result["user"]
    
    # Update user target audience
    update_result = db.update_user_target_audience(user["id"], target_audience)
    if not update_result["success"]:
        log.append(f"{datetime.now()} No se pudo actualizar el público objetivo del usuario {user['username']}: {update_result['message']}")
        return update_result, 400
    
    log.append(f"{datetime.now()} Público objetivo del usuario {user['username']} actualizado a: {target_audience}.")

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
        log.append(f"{datetime.now()} No se pudo actualizar el contexto adicional: Token de autorización requerido.")
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} No se pudo actualizar el contexto adicional: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    data = request.json or {}
    additional_context = data.get("additional_context", "")
    
    # Extract user from validation result
    user = validation_result["user"]
    
    # Update user additional context
    update_result = db.update_user_additional_context(user["id"], additional_context)
    if not update_result["success"]:
        log.append(f"{datetime.now()} No se pudo actualizar el contexto adicional del usuario {user['username']}: {update_result['message']}")
        return update_result, 400
    
    if additional_context:
        log.append(f"{datetime.now()} Contexto adicional del usuario {user['username']} aactualizado a: {additional_context}.")
    else:
        log.append(f"{datetime.now()} Contexto adicional del usuario {user['username']} vaciado.")

    return {
        "success": True,
        "message": "Additional context updated successfully",
    }, 200