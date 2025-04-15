import jwt
import os
from flask import Blueprint, request
from .utils import db, validate, password

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.post("/login")
def login():
    data = request.json
    if not data:
        return {"success": False, "message": "No data provided"}, 400
    if "username" not in data:
        data["username"] = ""
    if "password" not in data:
        data["password"] = ""
    user = db.get_user_by_username(data["username"].lower())
    if not user["success"]:
        return user, 400
    if not password.verify_password(data["password"], db.get_user_password_by_id(user["user"][0])):
        return {"success": False, "message": "Invalid password"}, 400
    encoded_jwt = jwt.encode({"id": user["user"][0]}, os.getenv("JWT_SECRET"), algorithm="HS256")
    return {"success": True, "message": "Login successful", "access_token": encoded_jwt, "data": list(user["user"])}, 200

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
    user = db.get_user_by_username(create_user["username"])
    encoded_jwt = jwt.encode({"id": user["user"][0]}, os.getenv("JWT_SECRET"), algorithm="HS256")
    return {"success": True, "message": "Register successful", "access_token": encoded_jwt, "data": list(user["user"])}, 200
