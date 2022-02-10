#./app/app.py
from flask import Flask, render_template

app = Flask(__name__)

# Ruta / (home) de la pagina          
@app.route('/')
def hello_world():
    return render_template('index.html')

# Ruta para cada uno de los modelos basicos, de momento todas devuelven home
@app.route('/modelosi')
def modelosi():
    return render_template('index.html')

@app.route('/modelosir')
def modelosir():
    return render_template('index.html')

@app.route('/modelosis')
def modelosis():
    return render_template('index.html')


