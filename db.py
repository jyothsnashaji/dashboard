import pandas as pd

df=pd.read_csv('Routerdata.csv')
df=df.sort_values('Router_id')

def get_col(param,router_id):
    global df
    df=df[df['Router_id']==router_id]
    return df[param]

def get_list_of_routers():
    global df
    return df['Router_id'].unique()


def get_network_col():
    return 'Network Health'

def get_hardware_col():
    return 'Hardware Health'

def get_software_col():
    return 'Software Health'




def get_router_id(row):
    df=pd.read_csv('Routerdata.csv')
    df=df.sort_values('Router_id')
    temp=df['Router_id'].unique()
    return temp[row]