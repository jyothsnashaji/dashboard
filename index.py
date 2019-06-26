import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import pandas as pd
from app import app
from layouts import index_page,router_dash,router_details,router_dash_layout
import callbacks as cb
import re


app.layout = html.Div([
               
                dcc.Tabs(id='tabs',value="index_page",children=[
                    dcc.Tab(id="index_page",value="index_page", label='Routers'),
                    ]),
               # dcc.Store(id='session',storage_type='session'),
                html.Div(id='content')
                ])



@app.callback(Output('content','children'),[Input('tabs','value')]#,[State('session','data'),
                                                                    #State('contents','children'),
                                                                   # State('session','modified_timestamp')]
                                                                   )
def display_dashboards(value):#,data,children,ts):
    if(value=='index_page'):
        return index_page
    else:
        return router_dash(int(value))
    '''
    if ts is None:
        data['index_page']=index_page
        return index_page
    else:
        return data.get(value,router_dash(int(value)))
    '''
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

for router_id in cb.get_list_of_routers():
    app.callback(
        Output('dash_contents'+str(router_id),'children'),
        [Input('dash_tabs'+str(router_id),'value')]
    )(generate_display_details(router_id))
    



if __name__ == '__main__':
    app.run_server(debug=True)

