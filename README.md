# Modelos discretos en epidemiología

> Ana Buendía Ruiz-Azuaga

## ¿Qué es?

La epidemiología se encarga estudia el control, causa y los patrones de las enfermedades en grupos de personas. Hablamos de una epidemia cuando tenemos brotes espontáneos de una enfermedad o situaciones endémicas, en las que la enfermedad está siempre presente.

En este proyecto se han estudiado los principales modelos matemáticos de la epidemiología, en su versión tanto discreta como continua. Además, se ha desarrollado software para visualizar el comportamiento de cada uno de estos modelos, así como permitir ajustar datos subidos por el usuario mediante estos.

![](./redaccion_tfg/figures/logo.png)

## Guía de instalación y uso

Para ejecutar este proyecto, comienza por descargar los archivos fuente del repositorio. Esto puede hacerse descargando el repositorio directamente desde la web de github o clonando el repositorio (más información sobre cómo clonar un repositorio [aquí](https://docs.github.com/es/repositories/creating-and-managing-repositories/cloning-a-repository)).

Tenemos varias opciones para instalar y ejecutar el software, basta elegir una. Se recomienda instalar y lanzar el software.

### 1. Construyendo la imagen de docker

Una vez clonado o descargado, nos situamos en `código/web_plotsir`, y abrimos una terminal.

Podemos lanzar la aplicación usando docker (y, para más comodidad, docker-compose), para lo cuál primero construimos el contenedor:

```bash
docker-compose build
```

Y una vez construido (basta construirlo una vez) para lanzarlo usamos:

```bash
docker run -t -p 5000:5000 -p 8050:8050 mapachana/plotsir:latest
```

### 2. Descargando la imagen de docker hub

La imagen del contenedor se encuentra [aquí](https://hub.docker.com/repository/docker/mapachana/plotsir).

Vamos a bajarnos la imagen del contenedor en docker hub ejecutando:

```bash
docker pull mapachana/plotsir:latest
```

Y finalmente la lanzamos mediante:

```bash
docker run -t -p 5000:5000 -p 8050:8050 mapachana/plotsir:latest
```
