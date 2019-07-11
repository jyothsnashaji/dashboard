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
from layouts import home_page,map_layout,add_router_layout,router_details,router_dash_layout
from sys import exit
import dash_bootstrap_components as dbc
from contextlib import suppress
import collections
app.config['suppress_callback_exceptions']=True


#adds router, start python script, displays dialog
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

#navigates between tabs in main page
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




#close tabs,change to next open tab, if none home. delete data from session
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


#open new router tab on selection from table
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


#navigate between dashboard, and health graph pages
def generate_nw_details_tabs(router_id):
    def generate_nw_details_tabs_sub(t_r,t_nw,t_sw,t_hw,ts):
        times=np.array([t_r,t_nw,t_sw,t_hw])
        times=times[times!=None]
        
        if times.size:
            time=np.max(times)
            if time==t_r:
                return router_dash_layout(router_id),True,False,False,False
            elif time==t_nw:
                return router_details(router_id,'network'),False,True,False,False
            elif time==t_sw:
                return router_details(router_id,'software'),False,False,True,False
            else:
                return router_details(router_id,'hardware'),False,False,False,True
            
        return router_dash_layout(router_id),True,False,False,False
            
        
    return generate_nw_details_tabs_sub
    
for router_id in get_list_of_routers():
    app.callback(
        [Output('dash_contents'+router_id,'children'),
        Output('dash'+router_id,'active'),
        Output('nw'+router_id,'active'),
        Output('sw'+router_id,'active'),
        Output('hw'+router_id,'active')],
        [Input('dash'+router_id,'n_clicks_timestamp'),
        Input('nw'+router_id,'n_clicks_timestamp'),
        Input('sw'+router_id,'n_clicks_timestamp'),
        Input('hw'+router_id,'n_clicks_timestamp'),
        Input("update","n_intervals")]
    )(generate_nw_details_tabs(router_id))
