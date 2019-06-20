import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
from plotly import tools
import math



def router_main(router_id):
   
    
    layout=html.Div([
                html.Div([
                html.Div([
                    dcc.Graph(id="g_sum",figure=update_gaugemeter("Summary",router_id)),
                    html.Button(id="reset",n_clicks=0,children="Reset",
                                style={'border-radius':'12px','margin':'auto','display':'block','color':'white','padding':'14px 40px','background-color':'#4289f4'})
            
                ],style={'width':'50%','display':'inline-block'}),
                html.Div([
                    dcc.Graph(id="g_nw",figure=update_gaugemeter("Network Health",router_id)),
                    html.Button(id="b_nw",n_clicks=0,children="Details",formAction="router_sub("+str(router_id)+")",
                                style={'border-radius':'12px','margin':'auto','display':'block','color':'white','padding':'14px 40px','background-color':'#4289f4'})
            
                ],style={'width':'50%','display':'inline-block'})]),
                html.Div([
                html.Div([
                    dcc.Graph(id="g_sw",figure=update_gaugemeter("Software Health",router_id)),
                    html.Button(id="b_sw",n_clicks=0,children="Details",
                                style={'border-radius':'12px','margin':'auto','display':'block','color':'white','padding':'14px 40px','background-color':'#4289f4'})
            
                ],style={'width':'50%','display':'inline-block'}),
                html.Div([
                    dcc.Graph(id="g_hw",figure=update_gaugemeter("Hardware Health",router_id)),
                    html.Button(id="b_hw",n_clicks=0,children="Details",
                                style={'border-radius':'12px','margin':'auto','display':'block','color':'white','padding':'14px 40px','background-color':'#4289f4'})
            
                ],style={'width':'50%','display':'inline-block'})])

               
        ],style={'position':'relative'})
    return layout

def update_gaugemeter(param,router_id):
    df=pd.read_csv('Routerdata.csv')
    df=df[df['Router_id']==router_id]
    score=df[param].mean()
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
            'text': 'Score = '+str(score),
            'font':{'size':'20px','color':'#4289f4'},
            'showarrow': False,
            'align':'center'
        }
    ]
    }   


    fig = {"data": [base_chart, meter_chart_1],
       "layout": layout}
    return fig


def router_sub(router_id):
    df=pd.read_csv('Routerdata.csv')

    df=df[df['Router_id']==router_id]

    trace1=go.Scatter(x=df['Time'],y=df['Summary'],name='Summary')
    trace2=go.Scatter(x=df['Time'],y=df['Network Health'],name='Network Health')
    trace3=go.Scatter(x=df['Time'],y=df['Software Health'],name='Software Health')
    trace4=go.Scatter(x=df['Time'],y=df['Hardware Health'],name='Hardware Health')

    fig = tools.make_subplots(rows=2, cols=2, subplot_titles=('Summary','Network Health','Software Health','Hardware Health'))

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 2, 1)
    fig.append_trace(trace4, 2, 2)



    fig['layout']['yaxis1'].update(title='Summary')
    fig['layout']['yaxis2'].update(title='Network Health')
    fig['layout']['yaxis3'].update(title='Software Health')
    fig['layout']['yaxis4'].update(title='Hardware Health')

    layout=html.Div([

            html.Div([
                dcc.Graph(id='graph',figure=fig)
            ])
        
            
    ])

    return layout

