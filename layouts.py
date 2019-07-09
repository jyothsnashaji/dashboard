import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
import math
import plotly.graph_objs as go
from plotly import tools
import app
from dash.dependencies import Input, Output,State
from db import get_list_of_routers,get_col
import numpy as np
import datetime as dt
import plotly
import dash_bootstrap_components as dbc

'''

'''
def home_page():
    return html.Div([
                    
                    dash_table.DataTable(id='table',columns=[{'name':'Choose a Router','id':'Router_id'}],
                                                    data=[{'Router_id':i.replace('_','.')} for i in get_list_of_routers()] ,
                                                    style_cell={'textAlign':'center'},style_table={'margin':'auto','width':'30%','paddingTop':'20px'},style_as_list_view=True)
                                                    
                                                    
     
                
               
],id='main')


index_page=html.Div([dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink(id='view',children="Check Router Health", active=True, href="#")),
        dbc.NavItem(dbc.NavLink(id='add',children="Add Router", href="#")),
        dbc.NavItem(dbc.NavLink(id='map',children="View Routers", href="#"))
        
    ],
    pills=True,style={'margin':'auto','width':'40%'}
),html.Div(id='index',children=home_page())],style={'paddingTop':'20px'})

def map_layout():
    token="pk.eyJ1IjoianNoYWppIiwiYSI6ImNqeG13N29hZjA0M2UzbnBrcHR4c2MweDUifQ.1ug21CZIfFS7KPCDX-rJVA"
    lat = [12.937591,12.935666 ]
    lon = [77.672863, 77.694879]
  
    data = [
    go.Scattermapbox(
        lat=lat,
        lon=lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            symbol='circle',
            size=14,
            color='red'
        ),
        text=[i.replace("_",'.') for i in get_list_of_routers()],
    )
    ]

    layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=lat[0],
            lon=lon[0]
        ),
        pitch=0,
        zoom=10
    ),
    )
    fig = go.Figure(data=data, layout=layout )
    return html.Div([
        dcc.Graph(id='map_g',figure=fig)
    ])




def add_router_layout():
    style={'display':'block','margin-left':'auto','margin-top':'50px','border-color':'#4289f4','margin-right':'auto'}
    alert={'display':'block','margin-left':'auto','background':'#b2cdf7','color':'#4289f4','margin-right':'auto','textAlign':'center','width':'50%'}
    
    return html.Div([dbc.Modal(
            [
                dbc.ModalHeader("Router Added"),
                dbc.ModalBody("Wait for a few moments for changes to reflect"),
                dbc.ModalFooter(
                    "Click to close"
                ),
            ],
            id="alert-fade",
            size="sm",
        ),
                        dcc.Input(id='username',value='Username',n_submit=0,style=style),
                        dcc.Input(id='password',value='Password',type='password',n_submit=0,style=style),
                        dcc.Input(id='input',value='Router',n_submit=0,style=style),
                        html.Button(id='add_router',children="Add",n_clicks=0,style=style),
                        ],style={'position':'relative'}) 


def router_dash_layout(router_id):
    
    
    return html.Div([
                
                       

                html.Div([
                html.Div([
                    
                    dcc.Graph(id="g_sum"+router_id,figure=update_gaugemeter("Summary",router_id)
                    ),
        
                    html.Button(id="reset"+router_id,n_clicks=0,children="Reset")
                        
            
                ],style={'width':'50%','display':'inline-block'}),
                html.Div([
                    dcc.Graph(id="g_nw"+router_id,figure=update_gaugemeter("Network Health",router_id),
                            ),
                    
                    html.Button(id="b_nw"+router_id,n_clicks=0,children="Details")
                        
            
                ],style={'width':'50%','display':'inline-block'})]),
                html.Div([
                html.Div([
                    dcc.Graph(id="g_sw"+router_id,figure=update_gaugemeter("Hardware Health",router_id)),
                    html.Button(id="b_sw"+router_id,n_clicks=0,children="Details")
            
                ],style={'width':'50%','display':'inline-block'}),
                html.Div([
                    dcc.Graph(id="g_hw"+router_id,figure=update_gaugemeter("Software Health",router_id)),
                    
                    html.Button(id="b_hw"+router_id,n_clicks=0,children="Details")
            
                ],style={'width':'50%','display':'inline-block'})
                ])
            ],style={'position':'relative'})
        

def router_dash1(router_id):
    return html.Div([
                dcc.Interval(id="update",n_intervals=0,interval=60000),
                dbc.Tabs(id='dash_tabs'+router_id,active_tab='dash'+router_id,children=[
                    dbc.Tab(label='Dashboard',tab_id='dash'+router_id,id='dash'+router_id)]),
                
                html.Div(id='dash_contents'+router_id)
                ])
def router_dash(router_id):
    return html.Div([dcc.Interval(id="update",n_intervals=0,interval=60000),
    dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink(id='dash'+router_id,children="Dashboard", active=True, href="#")),
        dbc.NavItem(dbc.NavLink(id='nw'+router_id,children="Network Health", href="#")),
        dbc.NavItem(dbc.NavLink(id='hw'+router_id,children="Hardware Health", href="#")),
        dbc.NavItem(dbc.NavLink(id='sw'+router_id,children="Software Health", href="#"))
        
    ],
    pills=True,style={'margin':'auto','width':'50%'}
    ),html.Div(id='dash_contents'+router_id,children=router_dash_layout(router_id))],style={'paddingTop':'20px'})  
        
def update_gaugemeter(param,router_id):
    
    score=np.mean(np.array(list(map(int,get_col("cpu",router_id)))))
    xco=0.24-0.15*math.cos(math.radians(1.8*score))
    yco=0.5+0.15*math.sin(math.radians(1.8*score))
    base_chart = {
    "values": [40, 10, 10, 10],
    "domain": {"x": [0, .48]},
    "marker": {
        "colors": [
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)'
        ],
        "line": {
            "width": 1
        }
    },
    "name": "Gauge",
    "hole": .4,
    "type": "pie",
    "direction": "clockwise",
    "rotation": 108,
    "showlegend": False,
    "hoverinfo": "none",

    }
        
    meter_chart_1 = {
    "values": [50,18,16,16],
    "labels": [" ", "Normal", "Warning", "Critical"],
    "marker": {
        'colors': [
            'rgb(255,255,255)',
            'rgb(191, 255, 0)',
            'rgb(255, 255, 0)',
            'rgb(255, 0, 0)'
        ]
    },
    "domain": {"x": [0, 0.48]},
    "name": "Gauge",
    "hole": .3,
    "type": "pie",
    "direction": "clockwise",
    "rotation": 90,
    "showlegend": False,
    "textinfo": "label",
    "textposition": "inside",
    "hoverinfo": "none"
    }
    base_chart['marker']['line']['width'] = 0
    layout = {
    'title':{
        'text':param,
        'size':'20px',
        'color':'#4289f4',
        'pad':{
                'top':'50px'
        }

    },
    'xaxis': {
        'showticklabels': False,
        'showgrid': False,
        'zeroline': False,
    },
    'yaxis': {
        'showticklabels': False,
        'showgrid': False,
        'zeroline': False,
    },
    'shapes': [
        {
            'type': 'path',
            #'path': 'M 0.239 0.5 L 0.19 0.5 L 0.241 0.5 C Z',
            'path':'M 0.239 0.5 L '+str(xco) +' '+str(yco) +' L 0.241 0.5 C Z',
            'fillcolor': 'rgba(0,0,0)',
            'line': {
                'width': 0.5
            },
            'xref': 'paper',
            'yref': 'paper'
        }
    ],
    'annotations': [
        {
            'xref': 'paper',
            'yref': 'paper',
            'x': 0.23,
            'y': 0.45,
            'text': 'Score = '+str(round(score,2)),
            'font':{'size':'20px','color':'#4289f4'},
            'showarrow': False,
            'align':'center'
        }
    ]
    }   


    fig = {"data": [base_chart, meter_chart_1],
       "layout": layout}
    return fig


def router_details(router_id,param):
  

    trace11=go.Scatter(x=get_col('date',router_id),y=get_col('cpu',router_id),mode='lines',name="Actual") 
    trace12=go.Scatter(x=get_col('date',router_id),y=get_col('pred_cpu',router_id),mode='lines',name="Predicted") 

    trace21=go.Scatter(x=get_col('date',router_id),y=get_col('cpu',router_id),mode='lines',name="Actual") 
    trace22=go.Scatter(x=get_col('date',router_id),y=get_col('pred_cpu',router_id),mode='lines',name="Predicted") 
    
    trace31=go.Scatter(x=get_col('date',router_id),y=get_col('cpu',router_id),mode='lines',name="Actual") 
    trace32=go.Scatter(x=get_col('date',router_id),y=get_col('pred_cpu',router_id),mode='lines',name="Predicted") 
    
    trace41=go.Scatter(x=get_col('date',router_id),y=get_col('cpu',router_id),mode='lines',name="Actual") 
    trace42=go.Scatter(x=get_col('date',router_id),y=get_col('pred_cpu',router_id),mode='lines',name="Predicted") 
        

    fig = tools.make_subplots(rows=2, cols=2, subplot_titles=('A',"B","C","D"))

    fig.append_trace(trace11, 1, 1)
    fig.append_trace(trace12, 1, 1)
    fig.append_trace(trace21, 1, 2)
    fig.append_trace(trace31, 2, 1)
    fig.append_trace(trace41, 2, 2)
    fig.append_trace(trace22, 1, 2)
    fig.append_trace(trace32, 2, 1)
    fig.append_trace(trace42, 2, 2)



    fig['layout']['yaxis1'].update(title='A')
    fig['layout']['yaxis2'].update(title='B')
    fig['layout']['yaxis3'].update(title='C')
    fig['layout']['yaxis4'].update(title='D')
    fig['layout']['title'].update(text=param)

    layout=html.Div([

            html.Div([
                
                
                dcc.Graph(id='graph',figure=fig)
            ])
        
            
    ])

    return layout
