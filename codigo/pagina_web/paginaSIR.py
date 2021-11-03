import plotly.graph_objects as go # or plotly.express as px
import numpy as np
import pandas as pd

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash()

fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )

@app.callback(
    Output("graph", "figure"), 
    [Input("dropdownalfa", "value")],
    [Input("dropdowngamma", "value")])
def calcular_modelo(alfa, gamma):
    N = 100

    S0 = 95
    I0 = 5

    T0 = 0
    T = 150

    secciones = 200 #deltaT en realidad es (T-T0)/secciones

    deltaT = (T-T0)/secciones

    tiempo = np.linspace(T0, T, secciones)

    S = np.linspace(T0, T, secciones)
    I = np.linspace(T0, T, secciones)

    S[0] = S0
    I[0] = I0

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


app.layout = html.Div([
    html.P("Alfa:"),
    dcc.Dropdown(
        id="dropdownalfa",
        options=[
            {'label': x, 'value': x}
            for x in [0.01, 0.1, 0.5]
        ],
        value=0.1,
        clearable=False,
    ),
    html.P("Gamma:"),
    dcc.Dropdown(
        id="dropdowngamma",
        options=[
            {'label': x, 'value': x}
            for x in [0.01, 0.1, 0.5]
        ],
        value=0.01,
        clearable=False,
    ),
    dcc.Graph(id="graph", figure=fig)
])


app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter