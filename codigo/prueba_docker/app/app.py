#./app/app.py
from flask import Flask, render_template
import random
import math

import funciones

app = Flask(__name__)
          
@app.route('/')
def hello_world():
    return '<p>Hello, World!</p> <p> Una lista de urls interesantes son:</p><ul><li>localhost:5000/ordena/3-2-4</li><li>localhost:5000/erastotenes/5</li><li>localhost:5000/fibonacci/numero.txt</li><li>localhost:5000/cadena/10</li><li>localhost:5000/regex/ana@correo.es</li><li>localhost:5000/figuras</li></ul>'

# Asumo que la lista se pasa como 1-2-3-5
@app.route('/ordena/<lista>')
def burbuja(lista):
    vector = lista.split('-')
    for i in range(len(vector)):
        vector[i] = int(vector[i])

    for i in range(len(vector)):
        for j in range(len(vector)):
            if vector[i] < vector[j]:
                aux = vector[i]
                vector[i] = vector[j]
                vector[j] = aux

    res = funciones.listToString(vector)
    return res

@app.route('/erastotenes/<num>')
def erastotenes(num):
    num = int(num)
    long = int(math.sqrt(num))+1

    vec = [False for i in range(0, num)]
    vector_resultado = []

    for i in range(2, long):
        for j in range(i, int(num/i)+1):
            if (i*j) < num:
                vec[i*j] = True

    for i in range(2, num):
        if not vec[i]:
            vector_resultado.append(i)
    res = funciones.listToString(vector_resultado)
    return res

@app.route('/fibonacci/<fichero>')
def fibonacci_file(fichero):
    fichero_r = open(fichero, "r")
    n = int(fichero_r.read())
    fichero_r.close()

    salida = open("salida.txt", "w")
    salida.write(str(funciones.fibonacci(n)))
    salida.close()

    return "Se ha escrito el fichero"

@app.route('/cadena/<n>')
def cadena(n):
    n = int(n)
    vec = [random.randint(0,2) for i in range(0,n)]
    res = ""

    for i in range(0,n):
        if vec[i] == 0:
            vec[i] = "["
        else:
            vec[i] = "]"

    res = res + "<p> La cadena generada es " + funciones.listToString(vec) + "</p>"

    contador = 0
    valido = True
    for i in range(0,n):
        if vec[i] == "[":
            contador = contador + 1
        else:
            contador = contador -1
        
        if contador < 0:
            valido = False

    if contador > 0:
        valido = False

    if valido:
        res = res + "<p> Cadena válida </p>"
    else:
        res = res + "<p> Cadena NO válida </p>"

    return res


@app.route('/regex/<exp>')
def comprobar_regex(exp):
    res = ""
    if funciones.validar_nombre(exp):
        res = res + "<p>" + exp + " es un nombre"
    else:
        res = res + "<p>" + exp + " NO es un nombre"

    if funciones.validar_email(exp):
        res = res + "<p>" + exp + " es un email"
    else:
        res = res + "<p>" + exp + " NO es un email"

    if funciones.validar_tarjeta(exp):
        res = res + "<p>" + exp + " es una tarjeta"
    else:
        res = res + "<p>" + exp + " NO es una tarjeta"

    return res
    


@app.errorhandler(404)
def page_not_found(e):
    return "La has liado, esto es un 404, revisa la URL", 404

@app.route('/figuras')
def figuras():
    return render_template('figuras.html')




