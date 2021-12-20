import plotly.graph_objects as go # or plotly.express as px
import numpy as np
import pandas as pd

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash()

# Declaramos la figura
fig = go.Figure() 


# Función que actualiza la grafica, recibe como argumento los parametros (input) y devuelve la grafica (output)
@app.callback(
    Output("graph", "figure"), 
    [Input("N", "value")],
    [Input("alfa", "value")],
    [Input("gamma", "value")],
    [Input("S0", "value")],
    [Input("I0", "value")],
    [Input("T", "value")])
def calcular_modelo(N, alfa, gamma, S0, I0, T):
    # Convierto a int o float los parametros
    N = int(N)

    alfa = float(alfa)
    gamma = float(gamma)

    S0 = int(S0)
    I0 = int(I0)

    T0 = 0
    T = int(T)

    secciones = 200 #deltaT en realidad es (T-T0)/secciones

    deltaT = (T-T0)/secciones

    tiempo = np.linspace(T0, T, secciones)

    S = np.linspace(T0, T, secciones)
    I = np.linspace(T0, T, secciones)

    S[0] = S0
    I[0] = I0

    # Calculo los datos a representar
    for j in range (secciones-1):
        S[j+1] = S[j]*(1-(alfa*deltaT/N)*I[j])+gamma*deltaT*I[j]
        I[j+1] = I[j]*(1-gamma*deltaT+(alfa*deltaT/N)*S[j])

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
    return fig


# Html a mostrar, primero estan los parametros para hacer el input y despues la grafica
app.layout = html.Div([
    html.Label("N:"),
    dcc.Input(
            id="N".format('text'),
            type='text',
            placeholder="100".format('text'),
            value="100"
        ),
    html.Br(),
    html.Label("Alfa:"),
    dcc.Input(
            id="alfa".format('text'),
            type='text',
            placeholder="0.1".format('text'),
            value="0.1"
        ),
    html.Br(),
    html.Label("Gamma:"),
    dcc.Input(
            id="gamma".format('text'),
            type='text',
            placeholder="0.01".format('text'),
            value="0.01"
        ),
    html.Br(),
    html.Label("S0:"),
    dcc.Input(
            id="S0".format('text'),
            type='text',
            placeholder="95".format('text'),
            value="95"
        ),
    html.Br(),
    html.Label("I0:"),
    dcc.Input(
            id="I0".format('text'),
            type='text',
            placeholder="5".format('text'),
            value="5"
        ),
    html.Br(),
    html.Label("T:"),
    dcc.Input(
            id="T".format('text'),
            type='text',
            placeholder="150".format('text'),
            value="150"
        ),
    html.Br(),
    dcc.Graph(id="graph", figure=fig)
])


app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter