from dash.dependencies import Input, Output,State
import pandas as pd
import numpy as np
from app import app
import math
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import os
from db import get_router_id,get_list_of_routers,get_col
from layouts import home_page
from sys import exit
import dash_bootstrap_components as dbc


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




def get_tab_child(router_id):
    return {'props': {'children': None,'id':router_id, 'label': 'ROUTER '+router_id.replace('_','.'), 'value': router_id,'className': 'custom-tab', 'selected_className': 'custom-tab--selected'}, 'type': 'Tab', 'namespace': 'dash_core_components'}


@app.callback(Output('index','children'),[Input('add','n_clicks_timestamp'),Input('view','n_clicks_timestamp')])
def from_index(add,view):
    if add:
        style={'display':'block','margin-left':'auto','margin-top':'50px','border-color':'#4289f4','margin-right':'auto'}
        alert={'display':'block','margin-left':'auto','background':'#b2cdf7','color':'#4289f4','margin-right':'auto','textAlign':'center','width':'50%'}
        global button_style
        return html.Div([dbc.Alert(id="alert-fade",dismissable=True,is_open=False,style=alert),
                        dcc.Input(id='username',value='Username',n_submit=0,style=style),
                        dcc.Input(id='password',value='Password',type='password',n_submit=0,style=style),
                        dcc.Input(id='input',value='Router',n_submit=0,style=style),
                        html.Button(id='add_router',children="Add",n_clicks=0,style={**button_style,**style}),
                        ],style={'position':'relative'})    
    if view:
        return home_page()
    else:
        raise PreventUpdate


@app.callback([Output('tabs','children'),
               Output('tabs','value')],[Input('table','active_cell')],[
                                                                     State('tabs','children')])
def generate_dashboard_tabs(cell,children)
    if cell:
        router_id=get_router_id(cell['row'])
        
        if get_tab_child(router_id) not in children:
            children.append(dcc.Tab(label='ROUTER '+router_id.replace('_','.'),id=router_id,value=router_id,className='custom-tab',
                selected_className='custom-tab--selected'))
        
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
                    dcc.Tab(label='Dashboard',value='dash'+router_id,id='dash'+router_id)],'dash'+router_id
            elif time==t_nw:
                label='Network Health'
                val='nw'+router_id
            elif time==t_sw:
                label='Software Health'
                val='sw'+router_id
            else:
                label='Hardware Health'
                val='hw'+router_id
            if {'props': {'children': None,'id':val, 'label': label, 'value': val,'className':'custom-tab_sub',
                'selected_className':'custom-tab--selected_sub'}, 'type': 'Tab', 'namespace': 'dash_core_components'} not in children:
                children.append(dcc.Tab(label=label,id=val,value=val,className='custom-tab_sub',
                selected_className='custom-tab--selected_sub'))
        return children,val
            
        
    return generate_nw_details_tabs_sub
    
for router_id in get_list_of_routers():
    app.callback(
        [Output('dash_tabs'+router_id,'children'),
        Output('dash_tabs'+router_id,'value')],
        [Input('reset'+router_id,'n_clicks_timestamp'),
        Input('b_nw'+router_id,'n_clicks_timestamp'),
        Input('b_sw'+router_id,'n_clicks_timestamp'),
        Input('b_hw'+router_id,'n_clicks_timestamp')],
        [State('dash_tabs'+router_id,'children'),
        State('dash_tabs'+router_id,'value')]
    )(generate_nw_details_tabs(router_id))
'''
def close_dash(router_id):
    def close_dash_sub(n_clicks,tablist,data):
        if n_clicks:
            if tablist[tablist.index(get_tab_child(router_id))+1] ==None:
                value=tablist[tablist.index(get_tab_child(router_id))-1]['props']['id']
            else:
                value=tablist[tablist.index(get_tab_child(router_id))+1]['props']['id']
            
            tablist.remove(get_tab_child(router_id))
            data.pop(router_id)
        return tablist,data,value
    return close_dash_sub



for router_id in get_list_of_routers():
    app.callback([Output('dash_tabs','children'),
                Output('session','data'),
                Output('tabs','value')],[Input('close'+router_id,'n_clicks')],
                [State('dash_tabs','children'),State('session','data')]
    )(close_dash(router_id))
           
'''

    
  