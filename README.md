# Aplicación Web Interna – Piloto

Aplicación web interna desarrollada en Python utilizando Flask.  
El objetivo es validar el uso con la gerencia en una primera etapa, con un alcance acotado y sin exposición a internet.

## Alcance
- Uso interno.
- Un usuario principal (gerencia) y acceso eventual del desarrollador.
- No maneja credenciales corporativas ni datos sensibles.
- Persistencia local de datos (archivo JSON).

## Tecnologías
- Python 3.x
- Flask
- Waitress (para ejecución en entorno Windows)

## Estructura del proyecto
- app.py: archivo principal de la aplicación.
- templates/: vistas HTML utilizadas por Flask.
- data/: carpeta destinada a persistencia local (no versionada).

## Ejecución (entorno local / piloto)
1. Crear entorno virtual (opcional).
2. Instalar dependencias:
   pip install -r requirements.txt
3. Ejecutar la aplicación:
   python app.py  
   o bien  
   waitress-serve --host=0.0.0.0 --port=8080 app:app

## Configuración
La aplicación utiliza variables de entorno para configuración sensible.
Ejemplo:
- SECRET_KEY
- DATA_PATH

Ver archivo .env.example.

## Notas
Este repositorio corresponde a un piloto interno.  
En caso de adopción, se prevé una evolución a una versión formal con autenticación corporativa y almacenamiento en base de datos gestionada.
