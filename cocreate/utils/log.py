import os

def generate():
    print("Creando archivo")
    # Obtener la ruta absoluta al directorio raíz del proyecto
    base_dir = os.path.abspath(os.path.join(__file__, "../../.."))
    if not os.path.exists(base_dir):
        raise FileNotFoundError(f"El directorio base no existe: {base_dir}")
    # Crear el archivo de log en el directorio raíz
    log_path = os.path.join(base_dir, "cocreate.log")
    with open(log_path, "a", encoding="utf-8") as archivo:
        print("Prueba", file=archivo)
