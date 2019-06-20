from dash.dependencies import Input, Output,State
import pandas as pd
from app import app
import math

@app.callback(Output('router_id','children'),[Input('table','selected_rows'),Input('button','n_clicks')],[State('content','children')])
def get_router_id(selected_rows,n_clicks,layout):
    
    df=pd.read_csv('Routerdata.csv')
    df=df.sort_values('Router_id')
    temp=df['Router_id'].unique()
    return temp[selected_rows[0]]


#        @app.callback(Output('main','children'),[Input('table','selected_rows'),Input('button','n_clicks')],[State('main','children')])


        
  