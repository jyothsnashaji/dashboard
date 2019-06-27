from dash.dependencies import Input, Output,State
import pandas as pd
import numpy as np
from app import app
import math
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

def get_tab_child(router_id):
    return {'props': {'children': None,'id':router_id, 'label': 'ROUTER '+router_id, 'value': router_id,'className': 'custom-tab', 'selected_className': 'custom-tab--selected'}, 'type': 'Tab', 'namespace': 'dash_core_components'}

@app.callback([Output('tabs','children'),
               Output('tabs','value')],[Input('table','active_cell')],[
                                                                     State('tabs','children')])
def generate_dashboard_tabs(cell,children):
    if cell:
        
        router_id=str(get_router_id(cell['row']))
        
        if get_tab_child(router_id) not in children:
            children.append(dcc.Tab(label='ROUTER '+router_id,id=router_id,value=router_id,className='custom-tab',
                selected_className='custom-tab--selected'))
        
        return children,router_id
            
    else:
        raise PreventUpdate

def get_list_of_routers():
    df=pd.read_csv('Routerdata.csv')
    df=df.sort_values('Router_id')
    return df['Router_id'].unique()

def generate_nw_details_tabs(router_id):
    def generate_nw_details_tabs_sub(t_r,t_nw,t_sw,t_hw,children,val):
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
            if {'props': {'children': None,'id':val, 'label': label, 'value': val,'className':'custom-tab_sub',
                'selected_className':'custom-tab--selected_sub'}, 'type': 'Tab', 'namespace': 'dash_core_components'} not in children:
                children.append(dcc.Tab(label=label,id=val,value=val,className='custom-tab_sub',
                selected_className='custom-tab--selected_sub'))
        return children,val
            
        
    return generate_nw_details_tabs_sub
    
for router_id in get_list_of_routers():
    app.callback(
        [Output('dash_tabs'+str(router_id),'children'),
        Output('dash_tabs'+str(router_id),'value')],
        [Input('reset'+str(router_id),'n_clicks_timestamp'),
        Input('b_nw'+str(router_id),'n_clicks_timestamp'),
        Input('b_sw'+str(router_id),'n_clicks_timestamp'),
        Input('b_hw'+str(router_id),'n_clicks_timestamp')],
        [State('dash_tabs'+str(router_id),'children'),
        State('dash_tabs'+str(router_id),'value')]
    )(generate_nw_details_tabs(router_id))
'''
def close_dash(router_id):
    def close_dash_sub(n_clicks,tablist,data):
        if n_clicks:
            if tablist[tablist.index(get_tab_child(str(router_id)))+1] ==None:
                value=tablist[tablist.index(get_tab_child(str(router_id)))-1]['props']['id']
            else:
                value=tablist[tablist.index(get_tab_child(str(router_id)))+1]['props']['id']
            
            tablist.remove(get_tab_child(str(router_id)))
            data.pop(str(router_id))
        return tablist,data,value
    return close_dash_sub



for router_id in get_list_of_routers():
    app.callback([Output('dash_tabs','children'),
                Output('session','data'),
                Output('tabs','value')],[Input('close'+str(router_id),'n_clicks')],
                [State('dash_tabs','children'),State('session','data')]
    )(close_dash(router_id))
           
'''
def get_network_col():
    return 'Network Health'

def get_hardware_col():
    return 'Hardware Health'

def get_software_col():
    return 'Software Health'




def get_router_id(row):
    df=pd.read_csv('Routerdata.csv')
    df=df.sort_values('Router_id')
    temp=df['Router_id'].unique()
    return temp[row]
    

    
  