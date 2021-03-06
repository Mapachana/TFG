import plotly.graph_objects as go # or plotly.express as px
import numpy as np
import pandas as pd
import re

from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app_dash import app

# Declaramos la figura
fig = go.Figure()
figSI = go.Figure() 


def preprocesar_input(N, alfa, gamma, S0, I0, T):
    ''' Funcion para preprocesar el input en modo texto para formato y nulos '''
    # Regex ed int o float
    pattern = re.compile("^[+-]?((\d+(\.\d+)?)|(\.\d+))$")
    
    # Reemplazo cualquier coma , por punto .
    N = N.replace(',', '.')
    alfa = alfa.replace(',', '.')
    gamma = gamma.replace(',', '.')
    S0 = S0.replace(',', '.')
    I0 = I0.replace(',', '.')
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
    if not bool(pattern.match(T)):
        T = '10'

    # Si añguno de los valores enteros tiene decimales lo trunco
    aux = N.split('.')
    N = aux[0]
    aux = S0.split('.')
    S0 = aux[0]
    aux = I0.split('.')
    I0 = aux[0]
    aux = T.split('.')
    T = aux[0]

    if int(S0) + int(I0) != N:
        N = int(S0) + int(I0)


    return N, alfa, gamma, S0, I0, T


@app.callback(
    Output("N_SIS_cont", "value"),
    Output("graph-SIS_cont", "figure"),
    Output("graphSIS-av-SI_cont", "figure"),
    [Input("N_SIS_cont", "value")],
    [Input("alfa", "value")],
    [Input("gamma", "value")],
    [Input("S0", "value")],
    [Input("I0", "value")],
    [Input("T", "value")])
def calcular_modelo(N_SIS, alfa, gamma, S0, I0, T):
    ''' Función que actualiza la grafica '''

    N, alfa, gamma, S0, I0, T = preprocesar_input(N_SIS, alfa, gamma, S0, I0, T)
    
    # Convierto a int o float los parametros
    N = int(N)

    alfa = float(alfa)
    gamma = float(gamma)

    S0 = int(S0)
    I0 = int(I0)

    T0 = 0
    T = int(T)

    if S0 + I0 != N:
        N = S0 + I0

    secciones = 200 #deltaT en realidad es (T-T0)/secciones

    deltaT = (T-T0)/secciones

    tiempo = np.linspace(T0, T, secciones)

    S = np.linspace(T0, T, secciones)
    I = np.linspace(T0, T, secciones)

    S[0] = S0
    I[0] = I0

    # Calculo los datos a representar
    for j in range (secciones-1):
        S[j+1] = S[j]+deltaT*(-(alfa/N)*S[j]*I[j]+gamma*I[j])
        I[j+1] = I[j]+deltaT*(I[j]*(alfa/N *S[j] -gamma))

    # Figura
    dfS = pd.DataFrame({'tiempo':tiempo, 'Susceptibles':S})
    dfI = pd.DataFrame({'tiempo':tiempo, 'Infectados':I})

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tiempo, y=S,
                        mode='lines',
                        name='Susceptibles'))
    fig.add_trace(go.Scatter(x=tiempo, y=I,
                        mode='lines',  #lines+markers
                        name='Infectados'))

    fig.update_layout(title='Modelo SIS',
                    xaxis_title='Tiempo',
                    yaxis_title='Susceptibles/Infectados')

    # Figura avanzada, I sobre S

    df = pd.DataFrame({'Susceptibles':S, 'Infectados':I})

    figSI = go.Figure()
    figSI.add_trace(go.Scatter(x=S, y=I,
                        mode='lines'))

    figSI.update_layout(title='Modelo SIS, variación de infectados en términos de los susceptibles.',
                    xaxis_title='Susceptibles',
                    yaxis_title='Infectados')

    
    return str(N), fig, figSI


# Elementos html para modificar los parámetros
parametros = html.Div([
    html.Div([
        html.Label("N: "),
        html.Label("Alfa: "),
        html.Label("Gamma: "),
        html.Label("S0: "),
        html.Label("I0: "),
        html.Label("T: "),
    ],
    style={'display': 'flex', 'flex-direction': 'column', 'font-size': '18px'}),
    html.Div([
        dcc.Input(
            id="N_SIS_cont".format('text'),
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
    dcc.Graph(id="graph-SIS_cont", figure=fig),
    dcc.Graph(id="graphSIS-av-SI_cont", figure=figSI)
])



# Regex sacada de https://codereview.stackexchange.com/questions/223970/a-regex-pattern-that-matches-all-forms-of-integers-and-decimal-numbers-in-python
