
def log_generate():
    print("Creando archivo")
    archivo = open("../bitacora.log", "a")
    print(f"Prueba", file=archivo)
    archivo.close()
