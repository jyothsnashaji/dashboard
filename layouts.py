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


button_style={'position':'relative','border-radius':'50%','bottom':'30px','color':'white','padding':'14px 40px','background-color':'#4289f4','margin':'auto','display':'block'}

index_page=html.Div([
    html.Button(id="add", children="Add Router", n_clicks=0,style={**button_style,**{'top':'50px'}}),
    html.Button(id="view", children="View Routers", n_clicks=0,style={**button_style,**{'top':'50px'}})

],id='index')

def home_page():
    return html.Div([
                
                html.Div([
                    
                    dash_table.DataTable(id='table',columns=[{'name':'Choose a Router','id':'Router_id'}],
                                                    data=[{'Router_id':i.replace('_','.')} for i in get_list_of_routers()] ,
                                                    style_cell={'textAlign':'center'},style_as_list_view=True, 
                                                    style_table={'height':'100%','paddingTop':'20px','paddingBottom':'20px','width':'75%','margin-left':'auto', 'margin-right':'auto'},
                                                    
                )])
                
               
],id='main')


def router_dash_layout(router_id):
    global button_style
    
    return html.Div([
                
                       

                html.Div([
                html.Div([
                    dcc.Graph(id="g_sum"+router_id,figure=update_gaugemeter("cpu",router_id),
                    style={}),
                    
                    html.Button(id="reset"+router_id,n_clicks=0,children="Reset",
                                style=button_style)
                        
            
                ],style={'width':'50%','display':'inline-block'}),
                html.Div([
                    dcc.Graph(id="g_nw"+router_id,figure=update_gaugemeter("cpu",router_id)),
                    
                    html.Button(id="b_nw"+router_id,n_clicks=0,children="Details",
                                style=button_style)
                        
            
                ],style={'width':'50%','display':'inline-block'})]),
                html.Div([
                html.Div([
                    dcc.Graph(id="g_sw"+router_id,figure=update_gaugemeter("cpu",router_id)),
                    html.Button(id="b_sw"+router_id,n_clicks=0,children="Details",
                                style=button_style)
            
                ],style={'width':'50%','display':'inline-block'}),
                html.Div([
                    dcc.Graph(id="g_hw"+router_id,figure=update_gaugemeter("cpu",router_id)),
                    
                    html.Button(id="b_hw"+router_id,n_clicks=0,children="Details",
                                style=button_style)
            
                ],style={'width':'50%','display':'inline-block'})
                ])
            ],style={'position':'relative'})
        

def router_dash(router_id):
    return html.Div([
                dcc.Interval(id="update",n_intervals=0,interval=60000),
                dcc.Tabs(id='dash_tabs'+router_id,value='dash'+router_id,parent_className='custom-tabs_sub',className='custom-tabs-container_sub',children=[
                    dcc.Tab(label='Dashboard',value='dash'+router_id,className='custom-tab_sub',
                selected_className='custom-tab--selected_sub',id='dash'+router_id)]),
                
                html.Div(id='dash_contents'+router_id)
                ])
          
    
        
def update_gaugemeter(param,router_id):
    
    score=np.mean(np.array(list(map(int,get_col(param,router_id)))))
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
        'color':'#4289f4'

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
