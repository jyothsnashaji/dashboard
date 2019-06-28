import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import pandas as pd
from app import app
from layouts import index_page,router_dash,router_details,router_dash_layout
import callbacks 
import re
from db import get_list_of_routers

app.layout = html.Div([
                html.Div(children="HEALTH MONITOR DASHBOARD",style={'height':'100px','background': '#00bcd4',"textAlign":'center','paddingTop':'30px','font-size':'30px','font':'Comic Sans MS Header','color':'#4289f4'}),
                dcc.Tabs(id='tabs',value="index_page",parent_className='custom-tabs',className='custom-tabs-container',colors={'primary':'red','background':'white','border':'white'},children=[
                    dcc.Tab(id="index_page",className='custom-tab',label='HOME',
                selected_className='custom-tab--selected',value="index_page"),
                    ]),
           
                dcc.Store(id='session',storage_type='session'),
                html.Div(id='content',key='None',style={'height':'100%','bottom':'0px'}),
                html.Img(src=app.get_asset_url('download.png'),style={'height':'50px','width':'100px','position':'relative','paddingLeft':'20px','bottom':'0px'})
                ])



@app.callback([Output('content','children'),
              Output('content','key'),
              Output('session','data')
              ],[Input('tabs','value')],[State('content','children'),
                                        State('content','key'),
                                        State('session','data'),
                                        State('tabs','children'),
                                        State('session','modified_timestamp')])
def display_dashboards(value,layout,key,data,tablist,ts):
    
    if ts is None:
        data={}
        data['index_page']=index_page
        return index_page,'index_page',data
    else:
       
        
        
            
        if(value!='index_page'):
            temp=data.get(value,router_dash(int(value)))
        else:
            temp=index_page
        data[key]=layout
        
        return temp,value,data
    
def generate_display_details(router_id):
    def display_details(value):
        if value=='dash'+str(router_id):
            return router_dash_layout(router_id)
        elif value=='nw'+str(router_id):
            return router_details(router_id,'Network Health')
        elif value=='hw'+str(router_id):
            return router_details(router_id,'Hardware Health')
        elif value=='sw'+str(router_id):
            return router_details(router_id,'Software Health')
        else:
            return html.Div("404"+value+' '+str(router_id))
    return display_details

for router_id in get_list_of_routers():
    app.callback(
        Output('dash_contents'+str(router_id),'children'),
        [Input('dash_tabs'+str(router_id),'value')]
    )(generate_display_details(router_id))
    



if __name__ == '__main__':
    app.run_server(debug=True)

