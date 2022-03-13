# Página web

> Por Ana Buendía Ruiz-Azuaga

## ¿Cómo se lanza?

Hay dos maneras de lanzarla, usando docker o manualmente.

## Usando docker

Si tenemos instalado docker podemos lanzar la aplicación usando docker (y, para más comodidad, docker-compose), para lo cuál en el directorio raíz primero construimos el contenedor:

```bash
docker-compose build
```

Y una vez construido (basta construirlo una vez) para lanzarlo usamos

```bash
docker-compose up
```

## Ejecutarlo manualmente

### Dependencias

Hay que instalar los paquetes indicados en [https://plotly.com/python/getting-started/](https://plotly.com/python/getting-started/).
También es necesario instalar numpy y pandas.

Además hay que instalar [flask](https://flask.palletsprojects.com/en/2.0.x/) (debería bastar con pip install flask) y especificar la carpeta de flask app con `export FLASK_APP=app`.

### Cómo se usa

Nos situamos dentro de la carpeta app, que es donde se encuentran los archivos de la página web en sí.

Primero lanzamos dash, para lo que en el directorio raiz ejecutamos:

```bash
python3 index_dash.py
```

Para ejecutar el fichero de la pagina web, en el directorio `app` donde está el fichero y ejecutar:

```bash
flask run
```

Después hay que abrir tu navegador de internet e ir a la dirección que se indica en tu terminal (debería indicar el puerto).
En mi caso `localhost:5000`.