import plotly.graph_objects as go # or plotly.express as px
import numpy as np
import pandas as pd
import re

import dash

from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app_dash import app

# Declaramos la figura
fig = go.Figure() 
figSI = go.Figure()
figSR = go.Figure()
figIR = go.Figure()


# Funcion para preprocesar el input en modo texto para formato y nulos
def preprocesar_input(N, alfa, gamma, S0, I0, R0, T):
    # Regex ed int o float
    pattern = re.compile("^[+-]?((\d+(\.\d+)?)|(\.\d+))$")
    
    # Reemplazo cualquier coma , por punto .
    N = N.replace(',', '.')
    alfa = alfa.replace(',', '.')
    gamma = gamma.replace(',', '.')
    S0 = S0.replace(',', '.')
    I0 = I0.replace(',', '.')
    R0 = R0.replace(',', '.')
    T = T.replace(',', '.')

    # Si algun valor introducido no es int o float lo pongo a 0
    if not bool(pattern.match(N)):
        N = '0'
    if not bool(pattern.match(alfa)):
        alfa = '0'
    if not bool(pattern.match(gamma)):
        gamma = '0'
    if not bool(pattern.match(S0)):
        S0 = '0'
    if not bool(pattern.match(I0)):
        I0 = '0'
    if not bool(pattern.match(R0)):
        R0 = '0'
    if not bool(pattern.match(T)):
        T = '10'

    # Si añguno de los valores enteros tiene decimales lo trunco
    aux = N.split('.')
    N = aux[0]
    aux = S0.split('.')
    S0 = aux[0]
    aux = I0.split('.')
    I0 = aux[0]
    aux = R0.split('.')
    R0 = aux[0]
    aux = T.split('.')
    T = aux[0]

    if int(S0) + int(I0) + int(R0) != N:
        N = int(S0) + int(I0) + int(R0)


    return N, alfa, gamma, S0, I0, R0, T


# Función que actualiza la grafica, recibe como argumento los parametros (input) y devuelve la grafica (output)
@app.callback(
    Output("N_SIR", "value"),
    Output("graph-SIR", "figure"),
    Output("graph-av-SI", "figure"),
    Output("graph-av-SR", "figure"),
    Output("graph-av-IR", "figure"),
    [Input("N_SIR", "value")],
    [Input("alfa", "value")],
    [Input("gamma", "value")],
    [Input("S0", "value")],
    [Input("I0", "value")],
    [Input("R0", "value")],
    [Input("T", "value")])
def calcular_modelo(N_SIR, alfa, gamma, S0, I0, R0, T):

    N, alfa, gamma, S0, I0, R0, T = preprocesar_input(N_SIR, alfa, gamma, S0, I0, R0, T)
    
    # Convierto a int o float los parametros
    N = int(N)

    alfa = float(alfa)
    gamma = float(gamma)

    S0 = int(S0)
    I0 = int(I0)
    R0 = int(R0)

    T0 = 0
    T = int(T)

    if S0 + I0 + R0 != N:
        N = S0 + I0 + R0

    secciones = 200 #deltaT en realidad es (T-T0)/secciones

    deltaT = (T-T0)/secciones

    tiempo = np.linspace(T0, T, secciones)

    S = np.linspace(T0, T, secciones)
    I = np.linspace(T0, T, secciones)
    R = np.linspace(T0, T, secciones)

    S[0] = S0
    I[0] = I0
    R[0] = R0

    # Calculo los datos a representar
    for j in range (secciones-1):
        S[j+1] = S[j]*(1-(alfa*deltaT/N)*I[j])
        I[j+1] = I[j]*(1-gamma*deltaT+(alfa*deltaT/N)*S[j])
        R[j+1] = R[j]+gamma*deltaT*I[j]

    # Figura
    dfS = pd.DataFrame({'tiempo':tiempo, 'Susceptibles':S})
    dfI = pd.DataFrame({'tiempo':tiempo, 'Infectados':I})
    dfR = pd.DataFrame({'tiempo':tiempo, 'Recuperados':R})


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tiempo, y=S,
                        mode='lines',
                        name='Susceptibles'))
    fig.add_trace(go.Scatter(x=tiempo, y=I,
                        mode='lines',  #lines+markers
                        name='Infectados'))
    fig.add_trace(go.Scatter(x=tiempo, y=R,
                        mode='lines',  #lines+markers
                        name='Recuperados'))

    fig.update_layout(title='Modelo SIR',
                    xaxis_title='Tiempo',
                    yaxis_title='Susceptibles/Infectados/Recuperados')

    # Figuras avanzadas

    # Infectados sobre susceptibles

    figSI = go.Figure()

    dfSI = pd.DataFrame({'Susceptibles':S, 'Infectados':I})

    figSI.add_trace(go.Scatter(x=S, y=I,
                        mode='lines'))

    figSI.update_layout(title='Modelo SIR, variación de infectados en función de susceptibles',
                    xaxis_title='Susceptibles',
                    yaxis_title='Infectados')

    # Recuperados en funcion de susceptibles
    figSR = go.Figure()

    dfSR = pd.DataFrame({'Susceptibles':S, 'Recuperados':R})

    figSR.add_trace(go.Scatter(x=S, y=R,
                        mode='lines'))

    figSR.update_layout(title='Modelo SIR, variación de recuperados en función de susceptibles',
                    xaxis_title='Susceptibles',
                    yaxis_title='Recuperados')

    # Recuperados en funcion de infectados
    figIR = go.Figure()

    dfIR = pd.DataFrame({'Infectados':I, 'Recuperados':R})

    figIR.add_trace(go.Scatter(x=I, y=R,
                        mode='lines'))

    figIR.update_layout(title='Modelo SIR, variación de recuperados en función de infectados',
                    xaxis_title='Infectados',
                    yaxis_title='Recuperados')


    return str(N), fig, figSI, figSR, figIR


# Elementos html para modificar los parámetros
parametros = html.Div([
    html.Div([
        html.Label("N: "),
        html.Label("Alfa: "),
        html.Label("Gamma: "),
        html.Label("S0: "),
        html.Label("I0: "),
        html.Label("R0: "),
        html.Label("T: "),
    ],
    style={'display': 'flex', 'flex-direction': 'column', 'font-size': '18px'}),
    html.Div([
        dcc.Input(
            id="N_SIR".format('text'),
            type='text',
            placeholder="100".format('text'),
            value="100"
        ),
        dcc.Input(
            id="alfa".format('text'),
            type='text',
            placeholder="0.1".format('text'),
            value="0.1"
        ),
         dcc.Input(
            id="gamma".format('text'),
            type='text',
            placeholder="0.01".format('text'),
            value="0.01"
        ),
        dcc.Input(
            id="S0".format('text'),
            type='text',
            placeholder="95".format('text'),
            value="95"
        ),
        dcc.Input(
            id="I0".format('text'),
            type='text',
            placeholder="5".format('text'),
            value="5"
        ),
        dcc.Input(
            id="R0".format('text'),
            type='text',
            placeholder="0".format('text'),
            value="0"
        ),
        dcc.Input(
            id="T".format('text'),
            type='text',
            placeholder="150".format('text'),
            value="150"
        )
    ],
    style={'display': 'flex', 'flex-direction': 'column'})
],
style={'display': 'flex', 'flex-direction': 'row'}
)

# Html a mostrar, primero estan los parametros para hacer el input y despues la grafica
layout = html.Div([
    parametros,
    dcc.Graph(id="graph-SIR", figure=fig),
    dcc.Graph(id="graph-av-SI", figure=figSI),
    dcc.Graph(id="graph-av-SR", figure=figSR),
    dcc.Graph(id="graph-av-IR", figure=figIR)
])


#app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter

# Regex sacada de https://codereview.stackexchange.com/questions/223970/a-regex-pattern-that-matches-all-forms-of-integers-and-decimal-numbers-in-python
