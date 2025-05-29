import os

def log_generate():
    print("Creando archivo")
    # Obtener la ruta absoluta al directorio raíz del proyecto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(base_dir, "bitacora.log")
    with open(log_path, "a", encoding="utf-8") as archivo:
        print("Prueba", file=archivo)
