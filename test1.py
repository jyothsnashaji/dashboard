import dash_bootstrap_components as dbc
import dash_html_components as html
import dash 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(
    [
        dbc.Alert("This is a primary alert", color="primary"),
        dbc.Alert("This is a secondary alert", color="secondary"),
        dbc.Alert("This is a success alert! Well done!", color="success"),
        dbc.Alert("This is a warning alert... be careful...", color="warning"),
        dbc.Alert("This is a danger alert. Scary!", color="danger"),
        dbc.Alert("This is an info alert. Good to know!", color="info"),
        dbc.Alert("This is a light alert", color="light"),
        dbc.Alert("This is a dark alert", color="dark"),
    ]
)

if __name__ == "__main__":
    app.run_server()