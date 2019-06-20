import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layouts import index_page,router_dash
import callbacks

app.layout = html.Div([
    dcc.Location(id='url',pathname="/Routers", refresh=False),
    html.Div(id='content')
])

@app.callback(Output('content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/Routers':
        return index_page
    elif pathname == '/Dashboard':
        return router_dash 
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)

