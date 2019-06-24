import dash
from dash.dependencies import Input, Output,State
import dash_core_components as dcc
import dash_html_components as html
import datetime

app = dash.Dash()
app.layout = html.Div([
    html.Div(id='n_clicks_prev',children='0',style={'display':'none'}),
    
    dcc.Tabs(id='tabs',children=[dcc.Tab(children=
                                            html.Button(id='button', children='Generate Tabs', n_clicks=0)
                                                    
)               
    
                                ])
])
app.config['suppress_callback_exceptions'] = True

@app.callback(Output('tabs','children'),[Input('button','n_clicks')],[State('n_clicks_prev','children'),State('tabs','children')])
def gen_tab(n_clicks,n_clicks_prev,children):
    if (n_clicks>int(n_clicks_prev)):
        children.append(dcc.Tab(label=str(n_clicks),children=html.Div("Helo")))
    return children
     



@app.callback(Output('n_clicks_prev','children'),[Input('button','n_clicks')],[State('n_clicks_prev','children')])
def update_n_clicks(n_clicks,n_clicks_prev,):
    if (n_clicks>int(n_clicks_prev)):
        n_clicks_prev=str(n_clicks)
    return n_clicks_prev

if __name__ == '__main__':
    app.run_server(debug=True)