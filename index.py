import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import pandas as pd
from app import app
from layouts import index_page,router_dash,router_details,router_dash_layout
import callbacks as cb
import re

app.layout = html.Div([
                html.Div(id='n_clicks_prev',children='0',style={'display':'none'}),
                dcc.Tabs(id='tabs',value="index_page",children=[
                    dcc.Tab(id="index_page",value="index_page", label='Routers'),
                    ]),
                html.Div(id='content')
                ])
    

@app.callback(Output('content','children'),[Input('tabs','value')])
def display_dashboards(value):
    if(value=='index_page'):
        return index_page
    else:
        return router_dash(int(value))
 

@app.callback(Output('dash_contents','children'),[Input('dash_tabs1','value')])
def display_details(value):
    if value=='dash1':
        return router_dash_layout(1)
    elif value=='nw1':
        return router_details(1,'Network Health')
    elif value=='hw1':
        return router_details(1,'Hardware Health')
    elif value=='sw1':
        return router_details(1,'Software health')
    else:
        return html.Div("404")



if __name__ == '__main__':
    app.run_server(debug=True)

