from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app_dash import app
from apps_dash import app1, app2, paginaSIS


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
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)