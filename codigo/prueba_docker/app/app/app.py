#./app/app.py
from flask import Flask, render_template

app = Flask(__name__)

# Ruta / (home) de la pagina          
@app.route('/')
def hello_world():
    return render_template('index.html')

# Ruta para cada uno de los modelos basicos, de momento todas devuelven home
@app.route('/modeloSI')
def modeloSI():
    return render_template('modeloSI.html')

@app.route('/modeloSIR')
def modeloSIR():
    return render_template('modeloSIR.html')

@app.route('/modeloSIS')
def modeloSIS():
    return render_template('modeloSIS.html')


