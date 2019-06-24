from dash.dependencies import Input, Output,State
import pandas as pd
from app import app
import math





def get_router_id(selected_rows):
    df=pd.read_csv('Routerdata.csv')
    df=df.sort_values('Router_id')
    temp=df['Router_id'].unique()
    return temp[selected_rows[0]]
    

    
  