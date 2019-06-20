import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import pandas as pd
from app import app
from layouts import index_page,router_dash,router_details
import callbacks 
import re

app.layout = html.Div([
    dcc.Location(id='url',pathname="Routers", refresh=False),
    html.Div(id='content'),
    html.Div(id="router_id",style={'display':'none'})
])

@app.callback(Output('content', 'children'),
              [Input('url', 'pathname'),Input('router_id','children')])
def display_page(pathname,router_id):
    
    if pathname == 'Routers':
        return index_page()
    elif pathname == '/Dashboard':
        return router_dash(router_id)
    elif re.findall(r'_Health$',pathname):
        strip=pathname.split('/')
        split=strip[1].split('_')
        return router_details(router_id,split[0]+' '+split[1])
    else:
        return '404'



if __name__ == '__main__':
    app.run_server(debug=True)

