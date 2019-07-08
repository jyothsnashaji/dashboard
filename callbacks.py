from dash.dependencies import Input, Output,State
import pandas as pd
import numpy as np
from app import app
import math
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate,DuplicateCallbackOutput
import os
from db import get_router_id,get_list_of_routers,get_col
from layouts import home_page,map_layout,add_router_layout
from sys import exit
import dash_bootstrap_components as dbc
from contextlib import suppress
import collections
app.config['suppress_callback_exceptions']=True



@app.callback(Output('alert-fade','is_open'),[Input('add_router','n_clicks')],[State('input','value'),State('username','value'),State('password','value')])
def add_router(n_submit,val,username,password):
    output=""
    alert=False
    if n_submit:
        pid=os.fork()
        
        if not pid:
            if val=='7.28.93.1':
                
                os.system('python data_collection.py '+val+' '+username+' '+password)
            elif val=='7.28.93.3':
                
                os.system('python data_collection2.py '+val+' '+username+' '+password)
            else:
                os.system('python collect_data.py '+val+' '+username+' '+password)
            exit()
        print("submitted")
        
        alert=True
        
    return alert




def get_tab_child(router_id):#change here!
    return {'props': {'children': None, 'id': router_id, 'label': 'ROUTER '+router_id.replace('_','.'), 'tab_id': router_id}, 'type': 'Tab', 'namespace': 'dash_bootstrap_components/_components'}

@app.callback([Output('index','children'),Output('add','active'),Output('view','active'),Output('map','active')],[Input('add','n_clicks_timestamp'),Input('view','n_clicks_timestamp'),Input('map','n_clicks_timestamp')])
def from_index(add,view,map_):
    times=np.array([add,view,map_])
    print(times)
    times=times[times!=None]
        
    if times.size:
        time=np.max(times)
        if time==add:
            return add_router_layout(),True,False,False 
        if time==view:
            return home_page(),False,True,False
        if time==map_:
            return map_layout(),False,False,True

    else:
        return home_page(),False,True,False





#print(app.config['suppress_callback_exceptions'],app.config.suppress_callback_exceptions,app.suppress_callback_exceptions)
@app.callback([Output('tabs','children'),Output('tabs','active_tab'),Output('session','data')],[Input('close','n_clicks')],[State('tabs','active_tab'),State('tabs','children'),State('session','data')])  #comment in dash.py line 975 "raise duplicateoutput"
def close_tabs(n_clicks,tab_id,tablist,data):
    if n_clicks:
        tab=get_tab_child(tab_id)
        print(tablist)
        del data[tab_id]
        try:
           val= tablist[tablist.index(tab)-1]['props']['id']
        except:
           val= tablist[tablist.index(tab)+1]['props']['id']
        #print(tablist)
        del tablist[tablist.index(tab)]
        return tablist,val,data
    else:
        raise PreventUpdate



@app.callback([Output('tabs','children'),
               Output('tabs','active_tab')],[Input('table','active_cell')],[
                                                                     State('tabs','children')])
def generate_dashboard_tabs(cell,children):
    
    if cell:
        router_id=get_router_id(cell['row'])
        #print(children)
        if get_tab_child(router_id) not in children:
            children.append(dbc.Tab(label='ROUTER '+router_id.replace('_','.'),id=router_id,tab_id=router_id))
           
        
        return children,router_id


    else:
        raise PreventUpdate



def generate_nw_details_tabs(router_id):
    def generate_nw_details_tabs_sub(t_r,t_nw,t_sw,t_hw,children,val):
        times=np.array([t_r,t_nw,t_sw,t_hw])
        times=times[times!=None]
        
        if times.size:
            time=np.max(times)
            if time==t_r:
                return [
                    dbc.Tab(label='Dashboard',tab_id='dash'+router_id,id='dash'+router_id)],'dash'+router_id
            elif time==t_nw:
                label='Network Health'
                val='nw'+router_id
            elif time==t_sw:
                label='Software Health'
                val='sw'+router_id
            else:
                label='Hardware Health'
                val='hw'+router_id
            print(children)
            if {'props': {'children': None,'id':val, 'label': label, 'tab_id': val}, 'type': 'Tab', 'namespace': 'dash_bootstrap_components/_components'} not in children:
                children.append(dbc.Tab(label=label,id=val,tab_id=val))
        return children,val
            
        
    return generate_nw_details_tabs_sub
    
for router_id in get_list_of_routers():
    app.callback(
        [Output('dash_tabs'+router_id,'children'),
        Output('dash_tabs'+router_id,'active_tab')],
        [Input('reset'+router_id,'n_clicks_timestamp'),
        Input('b_nw'+router_id,'n_clicks_timestamp'),
        Input('b_sw'+router_id,'n_clicks_timestamp'),
        Input('b_hw'+router_id,'n_clicks_timestamp')],
        [State('dash_tabs'+router_id,'children'),
        State('dash_tabs'+router_id,'tab_id')]
    )(generate_nw_details_tabs(router_id))
