import os
from datetime import datetime

def generate():
    # Obtener la ruta absoluta al directorio raíz del proyecto
    base_dir = os.path.abspath(os.path.join(__file__, "../../.."))
    if not os.path.exists(base_dir):
        raise FileNotFoundError(f"El directorio base no existe: {base_dir}")
    # Crear el archivo de log en el directorio raíz
    log_path = os.path.join(base_dir, "cocreate.log")
    with open(log_path, "a", encoding="utf-8") as archivo:
        print(f"{datetime.now()} El archivo de registro se cargó correctamente.", file=archivo)


def append(str): 
    archivo = open("cocreate.log", "a", encoding="utf-8")
    print(str, file=archivo)
    archivo.close()