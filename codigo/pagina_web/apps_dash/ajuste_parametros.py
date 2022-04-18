import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

import plotly.express as px
import plotly.graph_objects as go # or plotly.express as px


from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app_dash import app

# Inicializo figuras
fig = go.Figure()
fig2 = go.Figure()


modelos_ajuste_disponibles = ["Modelo SI", "Modelo SIR", "Modelo SIS", "Mejor modelo"]


layout = html.Div([
    dcc.Graph(id="scat", figure=fig),
    html.P("Selecciona el modelo con el que se van a ajustar los datos:"),
    dcc.Dropdown(
        id='selector_modelo_ajuste',
        options=[
            {'label': '{}'.format(i), 'value': i} for i in modelos_ajuste_disponibles
        ],
        value=modelos_ajuste_disponibles[0]
    ),
    html.Div(id="parametros"),
    html.Div(id="errores"),
    dcc.Graph(id="ajuste", figure=fig2)
])


def solucion_SI(t, alfa, I0):
    N = t[0]
    secciones = len(t)-1
    deltaT = 1
    I = np.empty(secciones)
    
    I[0] = I0

    for j in range (secciones-1):
        I[j+1] = I[j]*(1+(alfa*deltaT/N)*(N-I[j]))
        
    return I

@app.callback(
    Output('scat', 'figure'),
    Output('parametros', 'children'),
    Output('errores', 'children'),
    Output('ajuste', 'figure'),
    Input('selector_modelo_ajuste', 'value'))
def funcion(valor_menu):
    # Leo dataframe
    df = pd.read_csv("./app/fichero_ajuste/actual.csv")

    # Añado columna de tiempo para representacion
    secciones = len(df.index)
    deltaT = 1
    N = df.loc[0].at["S"]+df.loc[0].at["I"]

    tiempo = np.linspace(0, len(df.index), len(df.index))
    df['tiempo'] = tiempo

    # Actualizo primera grafica
    fig = px.scatter()
    fig.update_layout(title='Representación de los datos del fichero',
                        xaxis_title='Tiempo',
                        yaxis_title='Número de individuos')


    fig.add_scatter(x=df["tiempo"], y=df["S"], mode="markers", name="Susceptibles")
    fig.add_scatter(x=df["tiempo"], y=df["I"], mode="markers", name="Infectados")

    #print(df.columns)
    if 'R' in df.columns:
        N += df.loc[0].at["R"]
        fig.add_scatter(x=df["tiempo"], y=df["R"], mode="markers", name="Recuperados")

    # Calculo ajuste
    indep = np.concatenate([np.array([N]), np.array(df['tiempo'].tolist())], axis=None)
    
    popt, pcov = curve_fit(solucion_SI, indep, df['I'], bounds=((0, 0), (np.inf, N)))

    perr = np.sqrt(pcov.diagonal())

    # Hago la representacion grafica con los parametros obtenidos 
    I_ajuste = solucion_SI(indep, popt[0], popt[1])
    S_ajuste = N - I_ajuste

    fig2 = px.scatter()
    fig2.update_layout(title='Ajuste de los datos del fichero',
                        xaxis_title='Tiempo',
                        yaxis_title='Número de individuos')


    fig2.add_scatter(x=df["tiempo"], y=df["S"], mode="markers", name="Susceptibles datos")
    fig2.add_scatter(x=df['tiempo'], y=S_ajuste, mode="lines", name="Susceptibles ajuste")
    fig2.add_scatter(x=df["tiempo"], y=df["I"], mode="markers", name="Infectados datos")
    fig2.add_scatter(x=df['tiempo'], y=I_ajuste, mode="lines", name="Infectados ajuste")


    if 'R' in df.columns:
        fig2.add_scatter(x=df["tiempo"], y=df["R"], mode="markers", name="Recuperados datos")
        #fig2.add_scatter(x=df['tiempo'], y=R_ajuste, mode="lines", name="Recuperados ajuste")


    return fig, 'El parametro alfa vale: {} e I0 vale: {}'.format(popt[0], popt[1]), 'El error para alfa es {} y para I0 es {}'.format(perr[0], perr[1]), fig2

