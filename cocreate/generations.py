from flask import Blueprint, request
from .utils import validate, db

bp = Blueprint("generations", __name__, url_prefix="/generations")


@bp.get("/")
def get_generations():
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
