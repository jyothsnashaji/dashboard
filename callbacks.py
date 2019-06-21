from dash.dependencies import Input, Output,State
import pandas as pd
from app import app
import math

@app.callback(Output('router_id','children'),[Input('button','n_clicks'),Input('table','selected_rows')])
def get_router_id(n_clicks,selected_rows):
    df=pd.read_csv('Routerdata.csv')
    df=df.sort_values('Router_id')
    temp=df['Router_id'].unique()
    return temp[selected_rows[0]]


#        @app.callback(Output('main','children'),[Input('table','selected_rows'),Input('button','n_clicks')],[State('main','children')])


        
  