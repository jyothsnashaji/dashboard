import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import datetime

app = dash.Dash()
app.layout = html.Div([
    html.Button(id='button', children='Generate Tabs', n_clicks=0),
   # html.Div(id='content'),
    dcc.Tabs(id='tabs',value='1',children=[dcc.Tab(label ='1',value='1'),
                                        dcc.Tab(label='2',value='2'),
                                        dcc.Tab(label='3',value='3',children=
                                            dcc.Tabs(
                                                children=[dcc.Tab(label='31'),dcc.Tab(id='test',label='32')]))])
    # Include a dcc component so that the JS and CSS assets are loaded
   
])
app.config['suppress_callback_exceptions'] = True
@app.callback(Output('test','label'),[Input('tabs','value')])
def print_val(val1):
    print(val1)
    return "test"
'''

@app.callback(Output('content', 'children'),
              [Input('button', 'n_clicks')])
def display_content(n_clicks):
    if n_clicks == 0:
        return ''
    now = datetime.datetime.now()
    return html.Div([
        dcc.Tabs(
            children=[
                dcc.Tab(label='Tab 1',value='tab-1'),
                dcc.Tab(label='Tab 2',value='tab-2'),
                dcc.Tab(label='Tab 3',value='tab-3')
                    
            ],
            value='tab-1',
            id='tabs'
        ),
        html.Div(
            id='tab-1',
            style={'display': 'block'},
            children='Tab 1 at {}'.format(now)
        ),
        html.Div(
            id='tab-2',
            style={'display': 'none'},
            children='Tab 2 at {}'.format(now)
        ),
        html.Div(
            id='tab-3',
            style={'display': 'none'},
            children='Tab 3 at {}'.format(now)
        )
    ])


def generate_display_tab(tab_id):
    def display_tab(value):
        if value == tab_id:
            return {'display': 'block'}
        else:
            return {'display': 'none'}
    return display_tab


for tab_id in ['tab-1', 'tab-2', 'tab-3']:
    app.callback(
        Output(tab_id, 'style'),
        [Input('tabs', 'value')]
    )(generate_display_tab(tab_id))

'''
if __name__ == '__main__':
    app.run_server(debug=True)
    '''