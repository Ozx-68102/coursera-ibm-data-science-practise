import os

import pandas as pd
from dash import html, dcc, Input, Output, Dash
from plotly import express as px

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


# Read the wildfire data into pandas dataframe
data_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv"
print("=" * 20)
filename = download_file_if_not_exists(u=data_url)
print("=" * 20)
df = pd.read_csv(filename)

# Extract year and month from the date column
datetime = pd.to_datetime(df.loc[:, "Date"]).dt
df.loc[:, "Year"] = datetime.year
df.loc[:, "Month"] = datetime.month_name() # used for the names of the months

# Create App
app = Dash(__name__)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Layout Section of Dash
# Task 1: Add the Title to the Dashboard
app.layout = html.Div(children=[
    html.H1("Australia Wildfire Dashboard", style={"textAlign": "center", "color": "#503D36", "font-size": 26}),

    # Task 2: Add the radio items and a dropdown right below the first inner division
    html.Div([
        # First inner division for adding dropdown helper text for Selected Drive wheels
        html.Div([
            html.H2("Select Region:", style={"margin-right": "2em"}),

            # Radio items to select the region
            # dcc.RadioItems(["NSW", "QL", "SA", "TA", "VI", "WA"], "NSW", id="region", inline=True)]),
            dcc.RadioItems([
                {"label": "New South Wales", "value": "NSW"},
                {"label": "Northern Territory", "value": "NT"},
                {"label": "Queensland", "value": "QL"},
                {"label": "South Australia", "value": "SA"},
                {"label": "Tasmania","value": "TA"},
                {"label": "Victoria","value": "VI"},
                {"label": "Western Australia","value": "WA"}
            ],"NSW", id="region",inline=True)
        ]),

        #Dropdown to select year
        html.Div([
            html.H2("Select Year:", style={"margin-right": "2em"}),
            dcc.Dropdown(df.Year.unique(), value = 2005,id="year")
        ]),

        # Task 3: Add two empty divisions for output inside the next inner division.
        # Second Inner division for adding 2 inner divisions for 2 output graphs
        html.Div([
            html.Div([], id="plot1"),
            html.Div([], id="plot2")
        ], style={"display": "flex"})
    ])
])

# Task 4: Add the Output and input components inside the app.callback decorator.
# Place to add @app.callback Decorator
@app.callback(
    [
        Output(component_id="plot1", component_property="children"),
        Output(component_id="plot2", component_property="children")
    ],
    [
        Input(component_id="region", component_property="value"),
        Input(component_id="year", component_property="value")
    ]
)

# Task 5: Add the callback function.
# Place to define the callback function.
def reg_year_display(region: str, year: int) -> list[dcc.Graph]:
    # data
    region_data = df.loc[df["Region"] == region]
    year_data = region_data.loc[region_data["Year"] == year]

    # Plot 1 - Monthly Average Estimated Fire Area
    est_data = year_data.groupby("Month")["Estimated_fire_area"].mean().reset_index()
    fig1 = px.pie(est_data, values="Estimated_fire_area", names="Month", title=f"{region} : Monthly Average Estimated Fire Area in year {year}")

    # Plot 2 - Monthly Average Count of Pixels for Presumed Vegetation Fires
    veg_data = year_data.groupby("Month")["Count"].mean().reset_index()
    fig2 = px.bar(veg_data, x="Month", y="Count", title=f"{region} : Average Count of Pixels for Presumed Vegetation Fires in year {year}")

    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]


if __name__ == "__main__":
    app.run()
