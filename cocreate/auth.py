from flask import Blueprint, request
from .utils import db, validate

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.post("/login")
def login():
    data = request.json
    if not data:
        return {"success": False, "message": "No data provided"}, 400
    if "username" not in data or "password" not in data:
        return {"success": False, "message": "Missing username or password"}, 400
    return {"success": True, "message": "data"}, 200

@bp.post("/register")
def register():
    data = request.json
    if not data:
        return {"success": False, "message": "No data provided"}, 400
    if "username" not in data:
        data["username"] = ""
    if "password" not in data:
        data["password"] = ""
    is_username_valid = validate.is_username_valid(data["username"])
    if not is_username_valid["success"]:
        return is_username_valid, 400
    is_password_valid = validate.is_password_valid(data["password"])
    if not is_password_valid["success"]:
        return is_password_valid, 400
    create_user = db.create_user(data["username"], data["password"])
    if not create_user["success"]:
        return create_user, 400
    return create_user, 200