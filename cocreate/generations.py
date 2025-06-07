from flask import Blueprint, request
from .utils import validate, db, log
from datetime import datetime

bp = Blueprint("generations", __name__, url_prefix="/generations")


@bp.get("")
def get_generations():
    """Retrieve all generations for the authenticated user.
    
    Request Headers:
        Authorization: Bearer <jwt_token> - Required. JWT token for authentication
        
    Returns:
        200 OK: {
            "success": true,
            "message": "Generaciones encontradas",
            "generations": [array_of_generation_objects]
        }
        401 Unauthorized: {"success": false, "message": error_message}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} No se pudo obtener generaciones: Token de autorización requerido.")
        return {"success": False, "message": "Token de autorización requerido"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} No se pudo obtener generaciones: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    generations = db.get_generations_by_user_id(user["id"])

    if len(generations["data"]) == 0:
        log.append(f"{datetime.now()} El usuario {user['username']} intentó obtener generaciones pero no se encontró ninguna.")
        return {
            "success": False,
            "message": "No se encontraron generaciones para este usuario",
        }
    
    log.append(f"{datetime.now()} El usuario {user['username']} obtuvo sus generaciones con éxito.")

    return {
        "success": True,
        "message": "Generaciones encontradas",
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
            "message": "Generación encontrada",
            "generation": generation_object
        }
        401 Unauthorized: {"success": false, "message": error_message}
        404 Not Found: {"success": false, "message": error_message}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} No se pudo obtener la generación {gen_id}: Token de autorización requerido.")
        return {"success": False, "message": "Token de autorización requerido"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} No se pudo obtener la generación {gen_id}: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    generation = db.get_generation_by_gen_id(user["id"], gen_id)

    if not generation["success"]:
        log.append(f"{datetime.now()} El usuario {user['username']} intentó obtener la generación {gen_id} pero no se encontró.")
        return {"success": False, "message": "No se encontró la generación para este usuario"}, 404

    log.append(f"{datetime.now()} El usuario {user['username']} obtuvo la generación {gen_id} con éxito.")

    return {
        "success": True,
        "message": "Generación encontrada",
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
        200 OK: {"success": true, "message": "La generación ha sido añadida a la lista de favoritos"}
        400 Bad Request: {"success": false, "message": error_message}
        401 Unauthorized: {"success": false, "message": error_message}
        500 Server Error: {"success": false, "message": error_message}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} No se pudo guardar una generación: Token de autorización requerido.")
        return {"success": False, "message": "Token de autorización requerido"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} No se pudo guardar una: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    # Get generation ID from request
    generation_id = request.json.get("gen_id")
    if not generation_id:
        log.append(f"{datetime.now()} El usuario {user['username']} no pudo guardar una generación: ID de la generación requerido.")
        return {"success": False, "message": "ID de la generación requerido"}, 400

    # Save generation to database
    save_result = db.save_generation(user["id"], generation_id)
    if not save_result["success"]:
        log.append(f"{datetime.now()} El usuario {user['username']} no pudo guardar la generación {generation_id}: {save_result['message']}")
        return {"success": False, "message": save_result["message"]}, 500
    
    log.append(f"{datetime.now()} El usuario {user['username']} guardó la generación {generation_id} con éxito.")

    return {"success": True, "message": "La generación ha sido añadida a la lista de favoritos"}

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
        200 OK: {"success": true, "message": "La generación ha sido removida de la lista de favoritos"}
        400 Bad Request: {"success": false, "message": error_message}
        401 Unauthorized: {"success": false, "message": error_message}
        500 Server Error: {"success": false, "message": error_message}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} No se pudo guardar una generación: Token de autorización requerido.")
        return {"success": False, "message": "Token de autorización requerido"}, 401

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
        log.append(f"{datetime.now()} El usuario {user['username']} no pudo remover una generación: ID de la generación requerido.")
        return {"success": False, "message": "ID de la generación requerido"}, 400

    # Unsave generation from database
    unsave_result = db.unsave_generation(user["id"], generation_id)
    if not unsave_result["success"]:
        log.append(f"{datetime.now()} El usuario {user['username']} no pudo remover la generación {generation_id}: {unsave_result['message']}")
        return {"success": False, "message": unsave_result["message"]}, 500
    
    log.append(f"{datetime.now()} El usuario {user['username']} removió la generación {generation_id} con éxito.")

    return {"success": True, "message": "La generación ha sido removida de la lista de favoritos"}

@bp.get("/saved")
def get_saved_generations():
    """Retrieve all saved generations for the authenticated user.
    
    Request Headers:
        Authorization: Bearer <jwt_token> - Required. JWT token for authentication
        
    Returns:
        200 OK: {
            "success": true,
            "message": "Generaciones favoritas encontradas",
            "saved_generations": [array_of_saved_generation_objects]
        }
        401 Unauthorized: {"success": false, "message": error_message}
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} No se pudo obtener las generaciones guardadas: Token de autorización requerido.")
        return {"success": False, "message": "Token de autorización requerido"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} No se pudo obtener las generaciones guardadas: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    saved_generations = db.get_saved_generations_by_user_id(user["id"])

    if len(saved_generations["data"]) == 0:
        log.append(f"{datetime.now()} El usuario {user['username']} intentó obtener las generaciones guardadas pero no se encontró ninguna.")
        return {
            "success": False,
            "message": "No se encontraron generaciones favoritas para este usuario",
        }
    
    log.append(f"{datetime.now()} El usuario {user['username']} obtuvo las generaciones guardadas con éxito.")

    return {
        "success": True,
        "message": "Generaciones favoritas encontradas",
        "saved_generations": saved_generations["data"],
    }


@bp.get("/export")
def export_generations():
    """Retrieve all generations for the authenticated user and export them to a JSON file.
    
    Request Headers:
        Authorization: Bearer <jwt_token> - Required. JWT token for authentication
        
    Returns:
        200 OK: {
            "success": true,
            "message": "Generaciones exportadas",
            "generations": [array_of_generation_objects]
        }
        401 Unauthorized: {"success": false, "message": error_message}
        500 Internal Server Error: {"success": false, "message": error_message}
    """
    import os, json

    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        log.append(f"{datetime.now()} No se pudo obtener generaciones: Token de autorización requerido.")
        return {"success": False, "message": "Token de autorización requerido"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        log.append(f"{datetime.now()} No se pudo obtener generaciones: {validation_result['message']}")
        return {"success": False, "message": validation_result["message"]}, 401

    # Extract user from validation result
    user = validation_result["user"]

    generations = db.get_generations_by_user_id(user["id"])

    if len(generations["data"]) == 0:
        log.append(f"{datetime.now()} El usuario {user['username']} intentó obtener generaciones pero no se encontró ninguna.")
        return {
            "success": False,
            "message": "No se encontraron generaciones para este usuario",
        }
    
    log.append(f"{datetime.now()} El usuario {user['username']} obtuvo sus generaciones con éxito.")

    path = "exported_generations"
    if not os.path.exists(path):
        os.makedirs(path)
    filename = f"{user['username']}_generations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    full_path = os.path.join(path, filename)

    try:
        json_file = open(full_path, "w", encoding="utf-8")
        try:
            json.dump(generations["data"], json_file, ensure_ascii=False, indent=4)
        except Exception as e:
            log.append(f"{datetime.now()} Error al escribir en el archivo: {str(e)}")
            return {
                "success": False,
                "message": f"Error al exportar generaciones: {str(e)}"
            }, 500
        finally:
            json_file.close()
    except PermissionError:
        log.append(f"{datetime.now()} Error al exportar generaciones: Permiso denegado al escribir en el archivo {full_path}.")
        return {
            "success": False,
            "message": f"Error al exportar generaciones: Permiso denegado al escribir en el archivo {full_path}."
        }, 500
    except Exception as e:
        log.append(f"{datetime.now()} Error al exportar generaciones: {str(e)}")
        return {
            "success": False,
            "message": f"Error al exportar generaciones: {str(e)}"
        }, 500
    finally:
        log.append(f"{datetime.now()} El usuario {user['username']} exportó sus generaciones a {filename} con éxito.")
        return {
            "success": True,
            "message": "Generaciones exportadas",
            "generations": generations["data"],
         }, 200
