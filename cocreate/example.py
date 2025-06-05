from flask import Blueprint

bp = Blueprint("example", __name__, url_prefix="/example")

@bp.get("")
def hello_world():
    return {"success": True, "message": "example"}