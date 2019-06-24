import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import pandas as pd
from app import app
from layouts import index_page,router_dash,router_details
import callbacks as cb
import re

app.layout = html.Div([
                html.Div(id='n_clicks_prev',children='0',style={'display':'none'}),
                dcc.Tabs(id='tabs',children=[
                    dcc.Tab(children=index_page)
                ])
])
    
   


@app.callback(Output('tabs','children'),[Input('button','n_clicks'),Input('table','selected_rows')],[State('n_clicks_prev','children'),State('tabs','children')])
def generate_dashboard(n_clicks,selected_rows,n_clicks_prev,children):
    if (n_clicks>int(n_clicks_prev)):
        router_id=cb.get_router_id(selected_rows)
        children.append(dcc.Tab(label=str(router_id),id=str(router_id),value=str(router_id),children=router_dash(router_id)))
    return children


@app.callback(Output('n_clicks_prev','children'),[Input('button','n_clicks')],[State('n_clicks_prev','children')])
def update_n_clicks(n_clicks,n_clicks_prev):
    if (n_clicks>int(n_clicks_prev)):
        n_clicks_prev=str(n_clicks)
    return n_clicks_prev    


if __name__ == '__main__':
    app.run_server(debug=True)

