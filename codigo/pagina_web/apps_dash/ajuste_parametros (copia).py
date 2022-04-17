import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app_dash import app

N = 100

S0 = 99
I0 = 1

alfa = 0.1

T0 = 0
T = 100

#deltaT en realidad es (T-T0)/secciones
deltaT = 1

tiempo = np.arange(T0, T, deltaT)

secciones = tiempo.size

layout = html.Div([
    html.H3('Prueba ajustes de datos'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='perr'),
    dcc.Link('Go to App 2', href='/apps/app2')
])




def solucion_SI(t, alfa, I0):   
    I = np.empty(secciones)
    
    I[0] = I0

    for j in range (secciones-1):
        I[j+1] = I[j]*(1+(alfa*deltaT/N)*(N-I[j]))
        
    return I

@app.callback(
    Output('perr', 'children'),
    Input('app-1-dropdown', 'value'),
    Input('submit-val', 'n_clicks'))
def funcion(valor_menu, n_clicks):


    S = np.empty(secciones)
    I = np.empty(secciones)

    S[0] = S0
    I[0] = I0

    for j in range (secciones-1):
        S[j+1] = S[j]*(1-(alfa*deltaT/N)*I[j])
        I[j+1] = I[j]*(1+(alfa*deltaT/N)*S[j])



    I_ruido = I+np.random.randn(secciones)*5
    popt, pcov = curve_fit(solucion_SI, tiempo, I_ruido, bounds=((0, 0), (np.inf, N)))

    print(popt)
    print("\n")
    print(pcov)

    perr = np.sqrt(pcov.diagonal())
    print(perr)

    # lectura de un fichero con los datos
    fichero_subido = "./app/files/prueba2.txt"
    f = open(fichero_subido, "r")

    print(f.read())


    return 'You have selected "{}"'.format(perr[0])