import dash_bootstrap_components as dbc
import dash_html_components as html
import dash 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(
    html.Iframe(src="https://www.google.com/maps/embed/v1/place?q=40.7127837,-74.0059413&amp;key=AIzaSyAGCnR9T4ANEX0q_wpvbqUZKjslDqkPjn8")
)

if __name__ == "__main__":
    app.run_server()