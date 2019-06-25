from dash.dependencies import Input, Output,State
import pandas as pd
from app import app
import math
import dash_core_components as dcc

@app.callback(Output('tabs','children'),[Input('button','n_clicks')],[State('table','selected_rows'),State('tabs','children')])
def generate_dashboard_tabs(n_clicks,selected_rows,children):
    if n_clicks:
        router_id=get_router_id(selected_rows)
        children.append(dcc.Tab(label=str(router_id),id=str(router_id),value=str(router_id)))
    return children

@app.callback(Output('dash_tabs1','children'),[Input('b_nw1','n_clicks')],[State('dash_tabs1','children')])
def generate_details_tabs(n_clicks,children):
    if n_clicks:
        children.append(dcc.Tab(label='Network Health',id='nw1',value='nw1'))
    return children
    


def get_list_of_routers():
    df=pd.read_csv('Routerdata.csv')
    df=df.sort_values('Router_id')
    return df['Router_id'].unique()


def get_network_col():
    return 'Network Health'

def get_hardware_col():
    return 'Hardware Health'

def get_software_col():
    return 'Software Health'




def get_router_id(selected_rows):
    df=pd.read_csv('Routerdata.csv')
    df=df.sort_values('Router_id')
    temp=df['Router_id'].unique()
    return temp[selected_rows[0]]
    

    
  