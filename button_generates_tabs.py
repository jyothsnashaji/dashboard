import dash
from dash.dependencies import Input, Output,State
import dash_core_components as dcc
import dash_html_components as html
import datetime

app = dash.Dash()
app.layout = html.Div([
    html.Button(id='button', children='Generate Tabs', n_clicks=0),
    dcc.Tabs(id='tabs',children=[dcc.Tab(children=html.Div("Index"))])
    
])
app.config['suppress_callback_exceptions'] = True

@app.callback(Output('tabs','children'),[Input('button','n_clicks')],[State('tabs','children')])
def gen_tab(n_clicks,children):
    print(children)
    children.append(dcc.Tab(label=str(n_clicks),children=html.Div("Helo")))
    print(children)
    return children

if __name__ == '__main__':
    app.run_server(debug=True)