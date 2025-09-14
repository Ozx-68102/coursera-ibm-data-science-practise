import os

import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Output, Input

dir_path = os.path.join(".", "data")
os.makedirs(dir_path, exist_ok=True)


def download_file_if_not_exists(u: str) -> str:
    filepath = os.path.join(dir_path, u.rsplit("/", 1)[-1])
    if os.path.exists(filepath):
        print(f"File has already existed.")
        return filepath

    import requests
    with requests.get(url=u, stream=True) as response:
        response.raise_for_status()

        total_size = int(response.headers.get("Content-Length", 0))
        chunk_size = 1024 ** 2
        download_size = 0

        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if not chunk:
                    continue

                file.write(chunk)
                download_size += len(chunk)

                if total_size > 0:
                    progress = (download_size / total_size) * 100
                    print(f"Downloading: {progress:.2f}% ({download_size} / {total_size} bytes)")

        print(f"Download complete.")
        return filepath


# import datasets
data_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
filename = download_file_if_not_exists(u=data_url)
data = pd.read_csv(filename)

# Create a year list from 1980 to 2023
year_list = [i for i in range(1980, 2024, 1)]

app = Dash(__name__)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            "textAlign": "center",
            "color": "#503D36",
            "font-size": 24
        }
    ),

    # Select report-type dropdown
    html.Label("Select Report Type", style={"font-size": 18, "margin-top": 20}),
    dcc.Dropdown(id="dropdown-statistics", options=[
        {"label": "Yearly Statistics", "value": "Yearly Statistics"},
        {"label": "Recession Period Statistics", "value": "Recession Period Statistics"}],
                 placeholder="Select a Report Type", value="Select Statistics",
                 style={
                     "width": "80%",
                     "padding": "3px",
                     "font-size": "20px",
                     "text-align-last": "center"
                 }),

    # Select year dropdown
    html.Label("Select Year", style={"font-size": 18, "margin-top": 20, "display": "block"}),
    dcc.Dropdown(id="dropdown-year", options=[{"label": i, "value": i} for i in year_list],
                 placeholder="Select Year", value="Select Year",
                 style={
                     "width": "80%",
                     "padding": "3px",
                     "font-size": "20px",
                     "text-align-last": "center"
                 }),

    # Division for output display
    html.Div([
        html.Div(id="output-container", className="chart-grid",
                 style={"display": "flex", "flexDirection": "column", "gap": "10px"})
    ])
])


# Callback 1: Update input container (enable/disable year dropdown)
@app.callback(
    Output(component_id="dropdown-year", component_property="disabled"),
    Input(component_id="dropdown-statistics", component_property="value")
)
def update_input_container(selected_statistics: str) -> bool:
    return False if selected_statistics == "Yearly Statistics" else True


# Callback 2: Update output container structure (preparation for graphs)
@app.callback(
    Output(component_id="output-container", component_property="children"),
    [
        Input(component_id="dropdown-statistics", component_property="value"),
        Input(component_id="dropdown-year", component_property="value")
    ]
)
def update_output_container(selected_statistics: str, selected_year: int | None) -> list[html.Div] | None:
    if selected_statistics == "Recession Period Statistics":
        recession_data = data.loc[data.loc[:, "Recession"] == 1]

        # Plot 1: Automobile sales fluctuate over Recession Period (year wise) using line chart
        yearly_recession_sales = recession_data.groupby("Year")["Automobile_Sales"].sum().reset_index()
        rec_plot1 = dcc.Graph(
            figure=px.line(yearly_recession_sales, x="Year", y="Automobile_Sales",
                           title="Automobile Sales Fluctuation Over Recession Period (Year-wise)",
                           template="plotly_white")
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        avg_sales = recession_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        rec_plot2 = dcc.Graph(
            figure=px.bar(avg_sales, x="Vehicle_Type", y="Automobile_Sales",
                          title="Average Vehicles Sold by Type During Recessions", template="plotly_white",
                          color="Vehicle_Type")
        )

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        total_ad = recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index()
        rec_plot3 = dcc.Graph(
            figure=px.pie(total_ad, values="Advertising_Expenditure", names="Vehicle_Type",
                          title="Total Advertising Expenditure Share by Vehicle Type (Recessions)",
                          template="plotly_white", hole=0.3)
        )

        # Plot 4: Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        unemployment_vs_sales = recession_data.groupby(["unemployment_rate", "Vehicle_Type"])[
            "Automobile_Sales"].mean().reset_index()
        rec_plot4 = dcc.Graph(
            figure=px.bar(unemployment_vs_sales, x="unemployment_rate", y="Automobile_Sales",
                          title="Effect of Unemployment Rate on Vehicle Type and Sales (Recessions)",
                          template="plotly_white", color="Vehicle_Type",
                          labels={"unemployment_rate": "Unemployment Rate (%)",
                                  "Automobile_Sales": "Average Automobile Sales"})
        )

        return [
            html.Div(className="chart-item", children=[html.Div(children=rec_plot1), html.Div(children=rec_plot2)],
                     style={"display": "flex"}),
            html.Div(className="chart-item", children=[html.Div(children=rec_plot3), html.Div(children=rec_plot4)],
                     style={"display": "flex"})
        ]
    elif selected_statistics == "Yearly Statistics" and selected_year is not None:
        yearly_data = data.loc[data.loc[:, "Year"] == selected_year]

        # Plot 1: Yearly Automobile sales using line chart for the whole period.
        yas = data.groupby("Year")["Automobile_Sales"].sum().reset_index()
        yearly_chart1 = dcc.Graph(
            figure=px.line(yas, x="Year", y="Automobile_Sales", title="Yearly Automobile Sales [1980-2023]",
                           template="plotly_white", labels={"Automobile_Sales": "Average Annual Sales"})
        )

        # Plot 2: Total Monthly Automobile sales using line chart.
        mas = data.groupby("Month")["Automobile_Sales"].sum().reset_index()
        yearly_chart2 = dcc.Graph(
            figure=px.line(mas, x="Month", y="Automobile_Sales", title="Total Monthly Automobile Sales",
                           template="plotly_white",
                           labels={"Month": "Month (1-12)", "Automobile_Sales": "Total Monthly Sales"})
        )

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        average_vehicle_data = yearly_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        yearly_chart3 = dcc.Graph(
            figure=px.bar(average_vehicle_data, x="Vehicle_Type", y="Automobile_Sales",
                          title=f"Average Vehicles Sold by Type in {selected_year}", template="plotly_white",
                          color="Vehicle_Type", labels={"Automobile_Sales": "Average Monthly Sales"})
        )

        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        yearly_ad = yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index()
        yearly_chart4 = dcc.Graph(
            figure=px.pie(yearly_ad, values="Advertising_Expenditure", names="Vehicle_Type",
                          title="Total Advertisement Expenditure for Each Vehicle", template="plotly_white", hole=0.3)
        )

        return [
            html.Div(className="chart-item",
                     children=[html.Div(children=yearly_chart1), html.Div(children=yearly_chart2)],
                     style={"display": "flex"}),
            html.Div(className="chart-item",
                     children=[html.Div(children=yearly_chart3), html.Div(children=yearly_chart4)],
                     style={"display": "flex"})
        ]

    return None


if __name__ == "__main__":
    app.run()
