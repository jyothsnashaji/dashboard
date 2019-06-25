from dash.dependencies import Input, Output,State
import pandas as pd
import numpy as np
from app import app
import math
import dash_core_components as dcc
import dash_html_components as html

@app.callback(Output('tabs','children'),[Input('button','n_clicks')],[State('table','selected_rows'),State('tabs','children')])
def generate_dashboard_tabs(n_clicks,selected_rows,children):
    if n_clicks:
        router_id=get_router_id(selected_rows)
        children.append(dcc.Tab(label=str(router_id),id=str(router_id),value=str(router_id)))
    return children

def get_list_of_routers():
    df=pd.read_csv('Routerdata.csv')
    df=df.sort_values('Router_id')
    return df['Router_id'].unique()

def generate_nw_details_tabs(router_id):
    def generate_nw_details_tabs_sub(t_r,t_nw,t_sw,t_hw,children):
        times=np.array([t_r,t_nw,t_sw,t_hw])
        times=times[times!=None]
        
        if times.size:
            time=np.max(times)
            if time==t_r:
                return [
                    dcc.Tab(label='Dashboard',value='dash'+str(router_id),id='dash'+str(router_id))]
            elif time==t_nw:
                label='Network Health'
                val='nw'+str(router_id)
            elif time==t_sw:
                label='Software Health'
                val='sw'+str(router_id)
            else:
                label='Hardware Health'
                val='hw'+str(router_id)
            children.append(dcc.Tab(label=label,id=val,value=val))
        return children
    return generate_nw_details_tabs_sub
    
for router_id in get_list_of_routers():
    app.callback(
        Output('dash_tabs'+str(router_id),'children'),
        [Input('reset'+str(router_id),'n_clicks_timestamp'),
        Input('b_nw'+str(router_id),'n_clicks_timestamp'),
        Input('b_sw'+str(router_id),'n_clicks_timestamp'),
        Input('b_hw'+str(router_id),'n_clicks_timestamp')],
        [State('dash_tabs'+str(router_id),'children')]
    )(generate_nw_details_tabs(router_id))
    

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
    

    
  