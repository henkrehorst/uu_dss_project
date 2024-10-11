import pandas as pd
import plotly.express as px
from flask import Flask, render_template_string, render_template
from flask_cors import CORS
from sqlalchemy import create_engine, text, inspect, Table
import requests
import json
import numpy as np

# Load the csv file into the db
def _load_data_to_db():
    engine = create_engine("postgresql://student:infomdss@db_dashboard_project:5432/dashboard")

    with engine.connect() as conn:
        result = conn.execute(text("DROP TABLE IF EXISTS population CASCADE;"))

    population_df = pd.read_csv("../data/world_population.csv", delimiter=";")
    population_df.to_sql("population", engine, if_exists="replace", index=True)

# Fetch the hardcoded population table from the database
def _fetch_data_from_db():
    engine = create_engine("postgresql://student:infomdss@db_dashboard_project:5432/dashboard")
    population_table = pd.read_sql_table('population', engine, index_col='index')

    return population_table

# Generate the interactive plot for in your HTML file
def generate_population_graph():
    # Get the table from the database, returns a dataframe of the table
    population_df = _fetch_data_from_db()
    population_df['YearIncrease'] = population_df['YearIncrease'].str.replace(',','.').astype(float)

    world_data = population_df[population_df['Region'] == 'WORLD']
    netherlands_data = population_df[population_df['Region'] == 'Netherlands']

    # Combine the data for World and Netherlands into a single DataFrame
    combined_data = pd.concat([world_data, netherlands_data])

    # Create a bar chart using Plotly for the combined data
    fig = px.bar(combined_data, x='Year', y='YearIncrease', color='Region',
                title='Yearly Increase in World and Netherlands Population',
                barmode='group')  # Set the barmode to 'group' for side-by-side bars

    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    return plot_html


# Load the data into the database
# You will do this asynchronously as a cronjob in the background of your application
# Or you fetch the data from different sources when the page is visited or how you like to fetch your data
# Notice that the method _load_data_to_db() now just reads a preloaded .csv file
# You will have to fetch external files, or call API's to fill your database
_load_data_to_db()

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    # As soon as the page is loaded, the data is retrieved from the db and the graph is created
    # And is put in the HTML div
    return render_template('index.html', plot_html=generate_population_graph())


@app.route('/rail_routes')
def rail_routes():


    # Primary Key from NS API
    primary_key = "0c97e49d1a0e4a10bb2313d4bb697472"

    # Placeholder for the URL
    url = "https://gateway.apiportal.ns.nl/Spoorkaart-API/api/v1/spoorkaart"

    # Headers as defined in NS API documentation
    headers = {
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": primary_key
    }
    # Send GET request
    try:
        # Returns JSON file with nearest train station(s) of the put in lat/long
        response = requests.get(url, headers=headers)
        # Parse JSON content
        stations_data = response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found

    def random_color_generator():
        color = np.random.randint(0, 256, size=3)
        return tuple(color)

    # Cleaning the data so it becomes more readable and removes uneccesary information
    def clean_station_data(data):
        cleaned_data = []
        # Loop over all results in the retrieved data to select only necessary attributes
        for route in data['payload']['features']:
            route['style'] = {'color': 'rgb{0}'.format(random_color_generator())}
            cleaned_data.append(route)

        return cleaned_data

    cleaned_stations_data = clean_station_data(stations_data)

    return json.dumps(cleaned_stations_data)


if __name__ == '__main__':
    app.run(debug=True)