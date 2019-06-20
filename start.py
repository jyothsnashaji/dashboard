import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
from dash.dependencies import Input,Output,State
from dashmain import router_main,router_sub
app=dash.Dash()
app.config['suppress_callback_exceptions']=True
df=pd.read_csv('Routerdata.csv')
df=df.sort_values('Router_id')
app.layout= html.Div([
                html.Div([
                    html.H1(children="ROUTERS",style={"textAlign":'center','paddingTop':'30px','font':'Comic Sans MS Header','color':'#4289f4'})]),
                html.Div([
                    dash_table.DataTable(id='table',columns=[{'name':'Router_id','id':'Router_id'}],
                                                    data=[{'Router_id':i} for i in df['Router_id'].unique()],
                                                    style_cell={'textAlign':'center'},
                                                    row_selectable='single',
                                                    selected_rows=[0]

                )],style={'textAlign':'center','background':'#e8e9ff','height':'100%'}),
                html.Div([
                    html.Button(id='button',n_clicks=0,children='View Stats',style={'margin':'auto','display':'block'})
                ],style={'paddingTop':'100px','margin':'auto'})
               
],style={'background':'#e8e9ff','height':'100%'},id='main')



@app.callback(Output('main','children'),[Input('table','selected_rows'),Input('button','n_clicks')],[State('main','children')])
def update_page(selected_rows,n_clicks,layout):
    if(n_clicks):
        temp=df['Router_id'].unique()
        sel_id=temp[selected_rows[0]]
        
        #dfr=df[df['Router_id']==sel_id]
  
        layout=html.Div([
                    html.Div([html.H1(children='Router '+str(sel_id),
                style={"textAlign":'center','paddingTop':'30px','font':'Comic Sans MS Header','color':'#4289f4'})]),
                router_main(sel_id)])
    return layout
    



if __name__ == "__main__":
    app.run_server()
