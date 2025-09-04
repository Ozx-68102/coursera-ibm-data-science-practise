import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

from data_preparation import data_preparing

# set a constant to make sure just download it once
DATA = None

# Create a dash application
app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1("Airline Performance Dashboard", style={"textAlign": "center", "color": "#503D36", "font-size": 40}),
    html.Div(["Input Year: ",
              dcc.Input(id="input-year", value="2010", type="number", style={"height": "50px", "font-size": 35})],
             style={"font-size": 40}),
    html.Br(),
    html.Br(),
    html.Div(dcc.Graph(id="line-plot"))
])

# add callback decorator
#
# `Input()` function takes two parameters:
#
# component-id with the value input-year, which is the ID of the input dropdown.
# component_property being accessed is the value property, which represents the year entered by the user.
#
# `Output()` function takes two parameters:
#
# component-id with the value line-plot, which is the id of the output.
# component_property being modified is the figure property, which specifies the data and layout of the line plot.
@app.callback(Output(component_id="line-plot", component_property="figure"),
              Input(component_id="input-year", component_property="value"))

# Add computation to callback function and return graph
def get_graph(entered_year: int) -> go.Figure:
    global DATA
    if DATA is None:
        DATA = data_preparing()

    df = DATA[DATA.loc[:, "Year"] == int(entered_year)]

    # Group the data by Month and compute average over arrival delay time.
    line_data = df.groupby("Month")["ArrDelay"].mean().reset_index()
    fig = go.Figure(data=go.Scatter(x=line_data.loc[:, "Month"], y=line_data.loc[:, "ArrDelay"], mode="lines",
                                    marker={"color": "green"}))
    fig.update_layout(title="Month vs. Average Flight Delay Time", xaxis_title="Month", yaxis_title="ArrDelay")

    return fig

# Initial the constant and run the app
if __name__ == "__main__":
    DATA = data_preparing()
    app.run()
