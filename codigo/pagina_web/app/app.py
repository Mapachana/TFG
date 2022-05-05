#./app/app.py
import os
import shutil
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from pandas import DataFrame, read_csv
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './files'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



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

@app.route('/modeloSI_continuo')
def modeloSI_continuo():
    return render_template('modeloSI_continuo.html')

@app.route('/modeloSIR_continuo')
def modeloSIR_continuo():
    return render_template('modeloSIR_continuo.html')

@app.route('/modeloSIS_continuo')
def modeloSIS_continuo():
    return render_template('modeloSIS_continuo.html')

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/notacion')
def notacion():
    return render_template('notacion.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/ajustar_fichero/<fichero>', methods=['GET', 'POST'])
def ajustar_fichero(fichero):
    # Leo el fichero subido y lo muestro en terminal
    fichero_subido = app.config['UPLOAD_FOLDER']+"/"+fichero
    df = read_csv(fichero_subido)
    print(df)

    shutil.copy(fichero_subido, "./fichero_ajuste/actual.csv")

    return render_template('ajustar_fichero.html')

@app.route('/ajuste_archivo', methods=['GET', 'POST'])
def ajuste_archivo():
    error = ""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        file.seek(0, os.SEEK_END)
        if file.tell() == 0 or file.filename == '':
            error = "No se ha seleccionado ningún fichero."

            return render_template('ajuste_datos.html', error=error)
        file.seek(0) # Vuelvo a poner el puntero al inicio para poder trabajar con el
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return redirect(url_for('ajustar_fichero', fichero=filename))

    return render_template('ajuste_datos.html', error=error)

