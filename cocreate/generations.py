from flask import Blueprint, request
from .utils import validate, db, log
from datetime import datetime

bp = Blueprint("generations", __name__, url_prefix="/generations")


@bp.get("/")
def get_generations():
    """Retrieve all generations for the authenticated user.
    
    Request Headers:
        Authorization: Bearer <jwt_token> - Required. JWT token for authentication
        
    Returns:
        200 OK: {
            "success": true,
            "message": "Generations found.",
            "generations": [array_of_generation_objects]
        }
        401 Unauthorized: {"success": false, "message": error_message}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} Failed to retrieve generations: Authorization token required.")
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} Failed to retrieve generations: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    generations = db.get_generations_by_user_id(user["id"])

    if len(generations["data"]) == 0:
        log.append(f"{datetime.now()} User {user['username']} attempted to retrieve generations but found none.")
        return {
            "success": False,
            "message": "No generations found for this user.",
        }
    
    log.append(f"{datetime.now()} User {user['username']} retrieved generations successfully.")

    return {
        "success": True,
        "message": "Generations found.",
        "generations": generations["data"],
    }


@bp.get("/<int:gen_id>")
def get_generation_by_gen_id(gen_id):
    """Retrieve a generation for the authenticated user by its ID.
    
    Request Headers:
        Authorization: Bearer <jwt_token> - Required. JWT token for authentication
        
    Returns:
        200 OK: {
            "success": true,
            "message": "Generation found.",
            "generation": generation_object
        }
        401 Unauthorized: {"success": false, "message": error_message}
        404 Not Found: {"success": false, "message": error_message}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} Failed to retrieve generation {gen_id}: Authorization token required.")
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} Failed to retrieve generation {gen_id}: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    generation = db.get_generation_by_gen_id(user["id"], gen_id)

    if not generation["success"]:
        log.append(f"{datetime.now()} User {user['username']} attempted to retrieve generation {gen_id} but it was not found.")
        return {"success": False, "message": "Generation not found for this user."}, 404

    log.append(f"{datetime.now()} User {user['username']} retrieved generation {gen_id} successfully.")

    return {
        "success": True,
        "message": "Generation found.",
        "generation": generation["data"],
    }, 200


@bp.post("/save")
def save_generation():
    """Save a generation for the authenticated user.
    
    Request Headers:
        Authorization: Bearer <jwt_token> - Required. JWT token for authentication
        
    Request Body:
        {
            "gen_id": int - Required. The ID of the generation to save
        }
        
    Returns:
        200 OK: {"success": true, "message": "Generation saved successfully."}
        400 Bad Request: {"success": false, "message": error_message}
        401 Unauthorized: {"success": false, "message": error_message}
        500 Server Error: {"success": false, "message": error_message}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} Failed to save generation: Authorization token required.")
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} Failed to save generation: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    # Get generation ID from request
    generation_id = request.json.get("gen_id")
    if not generation_id:
        log.append(f"{datetime.now()} User {user['username']} failed to save generation: Generation ID is required.")
        return {"success": False, "message": "Generation ID is required"}, 400

    # Save generation to database
    save_result = db.save_generation(user["id"], generation_id)
    if not save_result["success"]:
        log.append(f"{datetime.now()} User {user['username']} failed to save generation {generation_id}: {save_result['message']}")
        return {"success": False, "message": save_result["message"]}, 500
    
    log.append(f"{datetime.now()} User {user['username']} saved generation {generation_id} successfully.")

    return {"success": True, "message": "Generation saved successfully."}

@bp.post("/unsave")
def unsave_generation():
    """Remove a saved generation for the authenticated user.
    
    Request Headers:
        Authorization: Bearer <jwt_token> - Required. JWT token for authentication
        
    Request Body:
        {
            "gen_id": int - Required. The ID of the generation to unsave
        }
        
    Returns:
        200 OK: {"success": true, "message": "Generation unsaved successfully."}
        400 Bad Request: {"success": false, "message": error_message}
        401 Unauthorized: {"success": false, "message": error_message}
        500 Server Error: {"success": false, "message": error_message}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} Failed to unsave generation: Authorization token required.")
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} Failed to unsave generation: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    # Get generation ID from request
    generation_id = request.json.get("gen_id")
    if not generation_id:
        log.append(f"{datetime.now()} User {user['username']} failed to unsave generation: Generation ID is required.")
        return {"success": False, "message": "Generation ID is required"}, 400

    # Unsave generation from database
    unsave_result = db.unsave_generation(user["id"], generation_id)
    if not unsave_result["success"]:
        log.append(f"{datetime.now()} User {user['username']} failed to unsave generation {generation_id}: {unsave_result['message']}")
        return {"success": False, "message": unsave_result["message"]}, 500
    
    log.append(f"{datetime.now()} User {user['username']} unsaved generation {generation_id} successfully.")

    return {"success": True, "message": "Generation unsaved successfully."}

@bp.get("/saved")
def get_saved_generations():
    """Retrieve all saved generations for the authenticated user.
    
    Request Headers:
        Authorization: Bearer <jwt_token> - Required. JWT token for authentication
        
    Returns:
        200 OK: {
            "success": true,
            "message": "Saved generations found.",
            "saved_generations": [array_of_saved_generation_objects]
        }
        401 Unauthorized: {"success": false, "message": error_message}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} Failed to retrieve saved generations: Authorization token required.")
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} Failed to retrieve saved generations: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    saved_generations = db.get_saved_generations_by_user_id(user["id"])

    if len(saved_generations["data"]) == 0:
        log.append(f"{datetime.now()} User {user['username']} attempted to retrieve saved generations but found none.")
        return {
            "success": False,
            "message": "No saved generations found for this user.",
        }
    
    log.append(f"{datetime.now()} User {user['username']} retrieved saved generations successfully.")

    return {
        "success": True,
        "message": "Saved generations found.",
        "saved_generations": saved_generations["data"],
    }