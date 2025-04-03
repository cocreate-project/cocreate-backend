# CoCreate

## Entorno virtual

Para crear un entorno virtual, se debe usar el comando `python -m venv .venv`.

De esta manera, se creara el directorio `.venv/`.

Para acceder al entorno virtual, se debe ejecutar el comando `.\.venv\Scripts\activate`.

Luego de esto, al inicio de la nueva linea de la terminal, deberia verse el siguiente texto `(.venv)`, esto significa que estamos dentro del entorno virtual.

Para salir, simplemente se debe escribir el comando `deactivate`.

## Dependencias

Para instalar las dependencias, se debe acceder al entorno virtual, y ejecutar el comando `pip install -r ./requirements.txt`.

## Iniciar el proyecto

Para levantar el proyecto, se debe acceder al entorno virtual, y ejecutar el comando `python app.py`.
