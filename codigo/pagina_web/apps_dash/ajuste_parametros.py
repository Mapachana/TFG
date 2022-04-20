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
        value=modelos_ajuste_disponibles[0],
        clearable=False
    ),
    dcc.Graph(id="ajuste", figure=fig2),
    html.Div(id="parametros"),
    html.Div(id="errores")
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

# Asumo que el I0 no lo sabes y R0 tampoco
def solucion_SIR(t, alfa, gamma, I0, R0):
    N = t[0]
    secciones = len(t)-1
    deltaT = 1
    
    I = np.empty(secciones)
    R = np.empty(secciones)
    
    I[0] = I0
    R[0] = R0

    for j in range (secciones-1):
        I[j+1] = I[j]*(1-gamma*deltaT+(alfa*deltaT/N)*(N-I[j]-R[j]))
        R[j+1] = R[j]+gamma*deltaT*I[j]

    
    res = np.concatenate((I, R))
    return res

# Asumo que el I0 no lo sabes 
def solucion_SIS(t, alfa, gamma, I0):
    N = t[0]
    secciones = len(t)-1
    deltaT = 1

    I = np.empty(secciones)
    
    I[0] = I0

    for j in range (secciones-1):
        I[j+1] = I[j]*(1-gamma*deltaT+(alfa*deltaT/N)*(N-I[j]))
        
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
    
    print(valor_menu)
    respuesta_params = ""
    respuesta_errores = ""
    
    indep = np.concatenate([np.array([N]), np.array(df['tiempo'].tolist())], axis=None)

    if(valor_menu == modelos_ajuste_disponibles[0]): # Modelo SI
        print("a")
    
        popt, pcov = curve_fit(solucion_SI, indep, df['I'], bounds=((0, 0), (np.inf, N)))

        perr = np.sqrt(pcov.diagonal())
        print("a")

        # Hago la representacion grafica con los parametros obtenidos 
        I_ajuste = solucion_SI(indep, popt[0], popt[1])
        S_ajuste = N - I_ajuste
        respuesta_params = html.P(["Los parámetros estimados con el ajuste elegido son:", html.Br(), "alfa: {}".format(popt[0]), html.Br(), "I0: {}".format(popt[1])])
        respuesta_errores = html.P(["ERRORES AUN SIN HACER BIEN"])
    elif(valor_menu == modelos_ajuste_disponibles[1]): # Modelo SIR
        print("b")

        if 'R' in df.columns:
            datos_comp = np.concatenate([np.array(df['I'].tolist()), np.array(df['R'].tolist())], axis=None)
        else:
            datos_comp = np.concatenate([np.array(df['I'].tolist()), np.zeros(secciones)], axis=None)

        popt, pcov = curve_fit(solucion_SIR, indep, datos_comp, bounds=((0, 0, 0, 0), (np.inf, np.inf, N, N)))

        perr = np.sqrt(pcov.diagonal())

        soluciones = solucion_SIR(indep, popt[0], popt[1], popt[2], popt[3])
        I_ajuste, R_ajuste = soluciones[:secciones], soluciones[secciones:]
        S_ajuste = N-I_ajuste-R_ajuste

        respuesta_params = html.P(["Los parámetros estimados con el ajuste elegido son:", html.Br(), "alfa: {}".format(popt[0]), html.Br(), "gamma: {}".format(popt[1]), html.Br(), "I0: {}".format(popt[2]), html.Br(), "R0: {}".format(popt[3])])
        respuesta_errores = html.P(["ERRORES AUN SIN HACER BIEN"])
    elif(valor_menu == modelos_ajuste_disponibles[2]): # Modelo SIS
        print("c")

        # comprobar bound de gamma
        print("COMPROBAR BOUND DE GAMMA")
        popt, pcov = curve_fit(solucion_SIS, indep, df['I'], bounds=((0, 0, 0), (np.inf, np.inf, N)))

        perr = np.sqrt(pcov.diagonal())

        I_ajuste = solucion_SIS(indep, popt[0], popt[1], popt[2])
        S_ajuste = N - I_ajuste
        respuesta_params = html.P(["Los parámetros estimados con el ajuste elegido son:", html.Br(), "alfa: {}".format(popt[0]), html.Br(), "gamma: {}".format(popt[1]), html.Br(), "I0: {}".format(popt[2])])
        respuesta_errores = html.P(["ERRORES AUN SIN HACER BIEN"])
    else: # Mejor modelo
        print("d")


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
        if (valor_menu == modelos_ajuste_disponibles[1]):
            fig2.add_scatter(x=df['tiempo'], y=R_ajuste, mode="lines", name="Recuperados ajuste")

    print(respuesta_params)
    print(respuesta_errores)
    return fig, respuesta_params, respuesta_errores, fig2

