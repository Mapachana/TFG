from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app_dash import app
from apps_dash import app1, app2, paginaSIS, paginaSI, paginaSIR, ajuste_parametros, paginaSI_continuo, paginaSIR_continuo, paginaSIS_continuo


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/apps/modeloSIS':
        return paginaSIS.layout
    elif pathname == '/apps/modeloSI':
        return paginaSI.layout
    elif pathname == '/apps/modeloSIR':
        return paginaSIR.layout
    elif pathname == '/apps/modeloSI_continuo':
        return paginaSI_continuo.layout
    elif pathname == '/apps/modeloSIR_continuo':
        return paginaSIR_continuo.layout
    elif pathname == '/apps/modeloSIS_continuo':
        return paginaSIS_continuo.layout
    elif pathname == '/apps/ajuste_datos':
        return ajuste_parametros.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=False)