from data_preparation import data_preparing

from dash import Dash, html, dcc

# Create a dash application
app = Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add description about the graph using HTML P (paragraph) component
# Finally, add graph component.
app.layout = html.Div(children=[
    html.H1("Airline Dashboard", style={"textAlign": "center", "color": "#503D36", "font-size": 40}),
    html.P("Proportion of distance group (250 mile distance interval group) by flights.", style={"textAlign": "center", "color": "#F57241"}),
    dcc.Graph(figure=data_preparing())
])


# Run the application
if __name__ == '__main__':
    app.run()
