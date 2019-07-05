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

button_style={'position':'relative','border-radius':'50%','bottom':'30px','color':'white','padding':'14px 40px','background-color':'#4289f4','margin':'auto','display':'block'}


@app.callback([Output('alert-fade','children'),Output('alert-fade','is_open')],[Input('add_router','n_clicks')],[State('input','value'),State('username','value'),State('password','value')])
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
                pass
            exit()
        print("submitted")
        output="Router Added!"
        alert=True
        
    return output,alert




def get_tab_child(router_id):#change here!
    return {'props': {'children': None, 'id': router_id, 'label': 'ROUTER '+router_id, 'tab_id': router_id}, 'type': 'Tab', 'namespace': 'dash_bootstrap_components/_components'}

@app.callback(Output('index','children'),[Input('add','n_clicks_timestamp'),Input('view','n_clicks_timestamp'),Input('map','n_clicks_timestamp')])
def from_index(add,view,map_):
    if add:
        return add_router_layout()   
    if view:
        return home_page()
    if map_:
        return map_layout()

    else:
        raise PreventUpdate



'''
@app.callback(Output('script','src'),[Input('close','n_clicks')])
def close_tabs(n_clicks):
    if n_clicks:
        return 'assets\\myscript.js'
    return ''
'''

#print(app.config['suppress_callback_exceptions'],app.config.suppress_callback_exceptions,app.suppress_callback_exceptions)
@app.callback([Output('tabs','children'),Output('tabs','active_tab'),Output('session','data')],[Input('close','n_clicks')],[State('tabs','active_tab'),State('tabs','children'),State('session','data')])  #comment in dash.py line 975 "raise duplicateoutput"
def close_tabs(n_clicks,tab_id,tablist,data):
    if n_clicks:
        tab=get_tab_child(tab_id)
        #print(data,tab_id)
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
'''
def close_dash(router_id):
    def close_dash_sub(n_clicks,tablist,data):
        if n_clicks:
            if tablist[tablist.index(get_tab_child(router_id))+1] ==None:
                tab_id=tablist[tablist.index(get_tab_child(router_id))-1]['props']['id']
            else:
                tab_id=tablist[tablist.index(get_tab_child(router_id))+1]['props']['id']
            
            tablist.remove(get_tab_child(router_id))
            data.pop(router_id)
        return tablist,data,tab_id
    return close_dash_sub



for router_id in get_list_of_routers():
    app.callback([Output('dash_tabs','children'),
                Output('session','data'),
                Output('tabs','tab_id')],[Input('close'+router_id,'n_clicks')],
                [State('dash_tabs','children'),State('session','data')]
    )(close_dash(router_id))
           
'''

    
  