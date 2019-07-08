import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import pandas as pd
from app import app
from layouts import index_page,router_dash,router_details,router_dash_layout
import callbacks 
import re
from db import get_list_of_routers
import dash_bootstrap_components as dbc




app.layout = html.Div([
                
                html.Div(children="HEALTH MONITOR DASHBOARD",style={'height':'100px','background': 'rgb(0, 189, 236)',"textAlign":'center','paddingTop':'30px','font-size':'30px','font':'Comic Sans MS Header','color':'white'}),
                dbc.Tabs(id='tabs',active_tab="index_page",children=[
                    dbc.Tab(id="index_page",label='HOME',tab_id="index_page")
                ]),


                html.Button(id='close',children='x',hidden=True,className='close'),
                dcc.Store(id='session',storage_type='session'),
                html.Div(id='content',key='None',style={'height':'100%','bottom':'0px'}),
                html.Img(src=app.get_asset_url('download1.png'),style={'height':'100px','width':'110px','position':'absolute','paddingLeft':'25px','top':'0px'}),
                html.Img(src=app.get_asset_url('a3.gif'),style={'height':'70px','width':'100px','position':'absolute','right':'40px','top':'15px'})
                ])



@app.callback([Output('content','children'),
              Output('content','key'),
              Output('session','data'),
              Output('close','hidden')
              ],[Input('tabs','active_tab')],[State('content','children'),
                                        State('content','key'),
                                        State('session','data'),
                                        State('session','modified_timestamp')])
def display_dashboards(value,layout,key,data,ts):
    hidden=True
    if ts is None:
        data={}
        data['index_page']=index_page
        return index_page,'index_page',data,hidden
    else:
       
        if(value!='index_page'):
            temp=data.get(value,router_dash(value))
            data[value]=temp
            hidden=False
            

        else:
            temp=index_page
            
        if (data[key]):
            data[key]=layout
        return temp,value,data,hidden
    
def generate_display_details(router_id):
    def display_details(value,ts):
        if value=='dash'+router_id:
            #print("displaying layout")
            return router_dash_layout(router_id)
        elif value=='nw'+router_id:
            return router_details(router_id,'cpu')
        elif value=='hw'+router_id:
            return router_details(router_id,'cpu')
        elif value=='sw'+router_id:
            return router_details(router_id,'cpu')
        else:
            return html.Div("404"+value+' '+router_id)
    return display_details

for router_id in get_list_of_routers():
    app.callback(
        Output('dash_contents'+router_id,'children'),
        [Input('dash_tabs'+router_id,'active_tab'),
        Input('update','n_intervals')]
    )(generate_display_details(router_id))
    



if __name__ == '__main__':
    app.run_server(debug=True,port=5555)

