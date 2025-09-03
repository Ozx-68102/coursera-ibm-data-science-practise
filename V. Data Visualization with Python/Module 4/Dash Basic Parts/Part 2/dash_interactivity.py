import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

from data_preparation import data_preparing

DATA = None

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1("Airline Performance Dashboard", style={"textAlign": "center", "color": "#503D36", "font-size": 40}),
    html.Div(["Input Year: ",
              dcc.Input(id="input-year", value="2010", type="number", style={"height": "50px", "font-size": 35})],
             style={'font-size': 40}),
    html.Br(),
    html.Br(),
    html.Div(dcc.Graph(id="line-plot"))
])


@app.callback(Output(component_id="line-plot", component_property="figure"),
              Input(component_id="input-year", component_property="value"))
def get_graph(entered_year: int) -> go.Figure:
    global DATA
    if DATA is None:
        DATA = data_preparing()

    df = DATA[DATA.loc[:, "Year"] == int(entered_year)]

    line_data = df.groupby("Month")["ArrDelay"].mean().reset_index()
    fig = go.Figure(data=go.Scatter(x=line_data.loc[:, "Month"], y=line_data.loc[:, "ArrDelay"], mode="lines",
                                    marker={"color": "green"}))
    fig.update_layout(title="Month vs. Average Flight Delay Time", xaxis_title="Month", yaxis_title="ArrDelay")

    return fig


if __name__ == '__main__':
    DATA = data_preparing()
    app.run()
