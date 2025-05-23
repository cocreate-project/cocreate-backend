from flask import Blueprint, request
from .utils import validate, db

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
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    generations = db.get_generations_by_user_id(user["id"])

    if len(generations["data"]) == 0:
        return {
            "success": False,
            "message": "No generations found for this user.",
        }

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
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    generation = db.get_generation_by_gen_id(user["id"], gen_id)

    if not generation["success"]:
        return {"success": False, "message": "Generation not found for this user."}, 404

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
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    # Get generation ID from request
    generation_id = request.json.get("gen_id")
    if not generation_id:
        return {"success": False, "message": "Generation ID is required"}, 400

    # Save generation to database
    save_result = db.save_generation(user["id"], generation_id)
    if not save_result["success"]:
        return {"success": False, "message": save_result["message"]}, 500

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
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    # Get generation ID from request
    generation_id = request.json.get("gen_id")
    if not generation_id:
        return {"success": False, "message": "Generation ID is required"}, 400

    # Unsave generation from database
    unsave_result = db.unsave_generation(user["id"], generation_id)
    if not unsave_result["success"]:
        return {"success": False, "message": unsave_result["message"]}, 500

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
        return {"success": False, "message": "Authorization token required"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    saved_generations = db.get_saved_generations_by_user_id(user["id"])

    if len(saved_generations["data"]) == 0:
        return {
            "success": False,
            "message": "No saved generations found for this user.",
        }

    return {
        "success": True,
        "message": "Saved generations found.",
        "saved_generations": saved_generations["data"],
    }