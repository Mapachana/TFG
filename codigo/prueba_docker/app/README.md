# Página web
> Por Ana Buendía Ruiz-Azuaga

## Dependencias

Hay que instalar los paquetes indicados en [https://plotly.com/python/getting-started/](https://plotly.com/python/getting-started/).
También es necesario instalar numpy y pandas.

Además hay que instalar [flask](https://flask.palletsprojects.com/en/2.0.x/) (debería bastar con pip install flask) y especificar la carpeta de flask app con `export FLASK_APP=app`.

## Cómo se usa

Primero lanzamos dash, para lo que en el directorio raiz ejecutamos:
```bash
python3 paginaSIS.py
```

Para ejecutar el fichero de la pagina web, en el directorio `app` donde está el fichero y ejecutar:

```bash
flask run
```

Después hay que abrir tu navegador de internet e ir a la dirección que se indica en tu terminal (debería indicar el puerto).
En mi caso `localhost:5000`.

Debería cargar una página con la gráfica del modelo SIS donde puedes modificar los valores de alfa y gamma recalculando el modelo en tiempo real.
