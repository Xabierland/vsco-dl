# vsco-dl
Descarga todas las fotos de un perfil de VSCO rápidamente.
Este no es un proyecto serio, simplemente lo he hecho para aprender web scraping, eres libre para hacer lo que quieras con el.

## Instalaccion y uso

    1. Instalar Python
        > https://www.python.org/downloads/
    2. Instalar las librerias
        > pip3 install -r requirements.txt
    3. Ejecutar el script
        > python3 vsco-dl.py
        
## Flags

    1. -t X.X
        > Tiempo de espera que se da a la pagina WEB, a menor tiempo mas rapida es la lectura del HTML pero en conexiones lentas puede causar la perdida de datos.
    2. -H
        > Cuando tiene esta flag el navegador se ejecuta en modo headerless
