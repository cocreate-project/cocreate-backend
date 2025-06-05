from google import genai
from pydantic import BaseModel
import os
from flask import Blueprint, request
from .utils import validate, db

bp = Blueprint("generate", __name__, url_prefix="/generate")


@bp.post("/video-script")
def video_script():
    """Generate a video script based on the provided prompt and user parameters.

    Headers:
        Authorization: Bearer <jwt_token> - JWT token for user authentication

    Request Body:
        {
            "prompt": "string" - Required. The topic for the video script
        }

    Returns:
        200 OK: {"success": true, "message": "<generated script>"}
        400 Bad Request: {"success": false, "message": "El prompt no puede estar vacío"}
        401 Unauthorized: {"success": false, "message": "Token de autorización requerido" or validation error}
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_AI_STUDIO_API_KEY"))

    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return {"success": False, "message": "Token de autorización requerido"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        return {"success": False, "message": validation_result["message"]}, 401

    prompt = request.get_json()["prompt"]

    if not prompt:
        return {"success": False, "message": "El prompt no puede estar vacío"}, 400

    # Extract user from validation result
    user = validation_result["user"]

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(
            f"Genera un guion en español para un video sobre {prompt}. "
            f"Este es mi tipo de contenido: {user.get('content_type')}. "
            f"Este es mi publico objetivo: {user.get('target_audience')}. "
            f"Este es el contexto adicional que quiero incluir: {user.get('additional_context')}. "
            "Solo responde con el guion, estructuralo en parrafos con las timestamps correspondientes en formato (HH:MM:SS), "
            "no uses emojis, ni texto innecesario."
        ),
    )

    db.create_generation(user["id"], "video_script", response.text)

    return {"success": True, "message": response.text}, 200


@bp.post("/content-idea")
def content_idea():
    """Generate content ideas based on the provided prompt and user parameters.

    Headers:
        Authorization: Bearer <jwt_token> - JWT token for user authentication

    Request Body:
        {
            "prompt": "string" - Required. The topic for content ideas generation
        }

    Returns:
        200 OK: {"success": true, "message": "<generated ideas>"}
        400 Bad Request: {"success": false, "message": "El prompt no puede estar vacío"}
        401 Unauthorized: {"success": false, "message": "Token de autorización requerido" or validation error}
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_AI_STUDIO_API_KEY"))

    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return {"success": False, "message": "Token de autorización requerido"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        return {"success": False, "message": validation_result["message"]}, 401

    prompt = request.get_json()["prompt"]

    if not prompt:
        return {"success": False, "message": "El prompt no puede estar vacío"}, 400

    # Extract user from validation result
    user = validation_result["user"]

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(
            f"Genera 5 ideas de contenido en español sobre {prompt}. "
            f"Este es mi tipo de contenido: {user.get('content_type')}. "
            f"Este es mi publico objetivo: {user.get('target_audience')}. "
            f"Este es el contexto adicional que quiero incluir: {user.get('additional_context')}. "
            "Por cada idea, incluye un título creativo y una breve descripción de qué podría incluir. "
            "Enumera las ideas de 1 a 5."
        ),
    )

    db.create_generation(user["id"], "content_idea", response.text)

    return {"success": True, "message": response.text}, 200


@bp.post("/newsletter")
def newsletter():
    """Generate newsletter content based on the provided prompt and user parameters.

    Headers:
        Authorization: Bearer <jwt_token> - JWT token for user authentication

    Request Body:
        {
            "prompt": "string" - Required. The topic for the newsletter content
        }

    Returns:
        200 OK: {"success": true, "message": {"subject": "<subject>", "title": "<title>", "content": ["<section1>", "<section2>"]}}
        400 Bad Request: {"success": false, "message": "El prompt no puede estar vacío"}
        401 Unauthorized: {"success": false, "message": "Token de autorización requerido" or validation error}
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_AI_STUDIO_API_KEY"))

    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return {"success": False, "message": "Token de autorización requerido"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        return {"success": False, "message": validation_result["message"]}, 401

    prompt = request.get_json()["prompt"]

    if not prompt:
        return {"success": False, "message": "El prompt no puede estar vacío"}, 400

    # Extract user from validation result
    user = validation_result["user"]

    class NewsletterResponse(BaseModel):
        subject: str
        title: str
        content: list[str]

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(
            f"Genera el contenido para un newsletter en español sobre {prompt}. "
            f"Este es mi tipo de contenido: {user.get('content_type')}. "
            f"Este es mi publico objetivo: {user.get('target_audience')}. "
            f"Este es el contexto adicional que quiero incluir: {user.get('additional_context')}. "
            "El newsletter debe incluir un asunto atractivo, un titulo e introduccion, 2-3 secciones de contenido principal, y una conclusión con llamado a la acción."
        ),
        config={
            "response_mime_type": "application/json",
            "response_schema": NewsletterResponse,
        },
    )

    db.create_generation(user["id"], "newsletter", response.text)

    return {
        "success": True,
        "message": {
            "subject": response.parsed.subject,
            "title": response.parsed.title,
            "content": response.parsed.content,
        },
    }, 200


@bp.post("/thread")
def thread():
    """Generate X (Twitter) thread content based on the provided prompt and user parameters.

    Headers:
        Authorization: Bearer <jwt_token> - JWT token for user authentication

    Request Body:
        {
            "prompt": "string" - Required. The topic for the Twitter thread
        }

    Returns:
        200 OK: {"success": true, "message": "<generated thread content>"}
        400 Bad Request: {"success": false, "message": "El prompt no puede estar vacío"}
        401 Unauthorized: {"success": false, "message": "Token de autorización requerido" or validation error}
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_AI_STUDIO_API_KEY"))

    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return {"success": False, "message": "Token de autorización requerido"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        return {"success": False, "message": validation_result["message"]}, 401

    prompt = request.get_json()["prompt"]

    if not prompt:
        return {"success": False, "message": "El prompt no puede estar vacío"}, 400

    # Extract user from validation result
    user = validation_result["user"]

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(
            f"Genera un hilo de X (anteriormente Twitter) en español sobre {prompt}. "
            f"Este es mi tipo de contenido: {user.get('content_type')}. "
            f"Este es mi publico objetivo: {user.get('target_audience')}. "
            f"Este es el contexto adicional que quiero incluir: {user.get('additional_context')}. "
            "El hilo debe tener entre 5 y 8 tweets, debes devolver cada uno en un array de strings. "
            "Asegúrate que cada tweet sea conciso y no exceda los 280 caracteres. "
            "El primer tweet debe captar la atención y el último debe incluir un llamado a la acción."
        ),
        config={
            "response_mime_type": "application/json",
            "response_schema": list[str],
        },
    )

    db.create_generation(user["id"], "thread", response.text)

    return {"success": True, "message": response.parsed}, 200


@bp.post("/change-tone")
def change_tone():
    """Change the tone of provided text based on user parameters.

    Headers:
        Authorization: Bearer <jwt_token> - JWT token for user authentication

    Request Body:
        {
            "text": "string" - Required. The text to be rewritten with a different tone
            "tone": "string" - Optional. The desired tone (defaults to "profesional")
        }

    Returns:
        200 OK: {"success": true, "message": "<rewritten text>"}
        400 Bad Request: {"success": false, "message": "El texto no puede estar vacío"}
        401 Unauthorized: {"success": false, "message": "Token de autorización requerido" or validation error}
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_AI_STUDIO_API_KEY"))

    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return {"success": False, "message": "Token de autorización requerido"}, 401

    token = auth_header.split(" ")[1]

    # Validate JWT token
    validation_result = validate.validate_jwt(token)
    if not validation_result["success"]:
        return {"success": False, "message": validation_result["message"]}, 401

    data = request.get_json()
    text = data.get("text", "")
    tone = data.get("tone", "profesional")

    if not text:
        return {"success": False, "message": "El texto no puede estar vacío"}, 400

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(
            f'Reescribe el siguiente texto en español con un tono {tone}: "{text}". '
            "Mantén la intención y el mensaje principal, pero adapta el lenguaje y estilo para reflejar el tono solicitado. "
            "Solo responde con el texto reescrito, sin explicaciones adicionales."
        ),
    )

    return {"success": True, "message": response.text}, 200
