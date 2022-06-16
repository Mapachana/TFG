from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app_dash import app
from apps_dash import paginaSIS, paginaSI, paginaSIR, ajuste_parametros, paginaSI_continuo, paginaSIR_continuo, paginaSIS_continuo


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# Paginas que se van a mostrar y sus urls
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/modeloSIS': # modelo SIS discreto
        return paginaSIS.layout
    elif pathname == '/apps/modeloSI': # modelo SI discreto
        return paginaSI.layout
    elif pathname == '/apps/modeloSIR': # modelo SIR discreto
        return paginaSIR.layout
    elif pathname == '/apps/modeloSI_continuo': # modelo SI continuo
        return paginaSI_continuo.layout
    elif pathname == '/apps/modeloSIR_continuo': # modelo SIR continuo
        return paginaSIR_continuo.layout
    elif pathname == '/apps/modeloSIS_continuo': # modelo SIS continuo
        return paginaSIS_continuo.layout
    elif pathname == '/apps/ajuste_datos': # ajuste de datos de fichero
        return ajuste_parametros.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8050', debug=False)
