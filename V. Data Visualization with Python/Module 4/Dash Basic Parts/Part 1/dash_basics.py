from data_preparation import data_preparing

from dash import Dash, html, dcc

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1("Airline Dashboard", style={"textAlign": "center", "color": "#503D36", "font-size": 40}),
    html.P("Proportion of distance group (250 mile distance interval group) by flights.", style={"textAlign": "center", "color": "#F57241"}),
    dcc.Graph(figure=data_preparing())
])


if __name__ == '__main__':
    app.run()
