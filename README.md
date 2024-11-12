# Team 08 - NS Tough Autumn Dashboard

### Running the app:
- Open a terminal or command prompt
- CD to root the directory of this codebase
- run ``docker compose up``. In some versions, you might need docker-compose up
- The Dashboard is available at http://localhost:8084

### Related links 
- Link to the Codebase: https://github.com/henkrehorst/uu_dss_project

### Datasets & Sources
- NS API Portal: several API's to retrieve data about stations, locations, prices, etc.
- NS Tariefeenheden Reports: CSV files, containing data that we scraped from PDF's
- CBS API: retrieving fuel prices for the last +- 10 years
- RDW API: data on fuel types and fuel consumption for every registered car
- Google Maps Directions API: retrieving data for routes on the road
- CE Delft API: retrieves data about car and train emissions

All of our data gets loaded into the database when running the Docker container. This loading is wrapped in a try-catch block, so that if some loading fails, a backup dataset is loaded into the database to ensure our model works.

### Data Collection and Preparation
We retrieve and process all of our data in the Jupyter Notebooks, that are stored in the directory dashboard/SeparateChartsForTesting. What all the files do is briefly explained here:
* EmissionComparison.ipynb
  * Retrieves the emission data for both train and cars from the CE Delft API. The data is transformed to floats, stored in a DataFrame and plotted in a nice chart.
* GemVertraging.ipynb<br>
  * Retrieves delays data from ? and loads it into DataFrames. The data is then filtered to only the routes that we have selected to show in our dashboard. The data only for those routes is plotted into a line chart.
* PriceComparison.ipynb<br>
  * As the price comparison is the most important aspect of our project, this is the most extensive notebook we created. It starts with retrieving the tariff units, or tariefeenheden in Dutch, for each of our defined routes from the database. With these tariff units, the ticket prices for all the routes are calculated. For calculating the car prices, we retrieve data from the CBS API (fuel prices), the RDW API (average consumption per car type) and the Google Maps API (the distances between stations, with latitude/longitude parameters as input that we retrieve from the database). Combining the fuel price, average consumption and distances, we can calculate the price for traveling a route by car.
* TimeComparison.ipynb<br>
  * The time comparison uses both the Google Maps API and the NS API, to retrieve the amount of time it takes to get from coordinate A (a given train station from our selection) to coordinate B (another train station) by either train or car. These are the pure travel times without any delays. The travel times are plotted against each other in a bar chart, and the time difference between the two options is also plotted.

### Converting Notebooks to the backend and dashboard
It was easy for us to divide the tasks of working out these KPI's into notebooks, where we can try things easily with our code. The code then just needs some slight adaptions to make it useable to plot things in the dashboard.

In the Notebooks, we perform basically four steps, and here, we explain how these are transformed into the realisation of the final code in the backend and the visualizations in the dashboard. <br>
* Step 1: Data retrieval. The retrieval of the data in the backend is the same as in the notebooks, by requesting the API's and using the static CSV files. 
* Step 2: Data cleaning. We do some data cleaning in the notebooks. In the backend, we migrate the data, and create tables for all of the cleaned data.
* Step 3: Doing some calculations. In app.py, we define routes that send our data to the frontend React app. For the calculations, we perform some SQL queries on our data to transform it into basically (x, y) value pairs, which allow for easy plotting, as plots contain x and y axes. These (x, y) pairs are sent to the frontend in JSON format.
* Step 4: Plotting the data. The data that is sent to the frontend is plotted by using Nivo, a set of data visualization components that are built on top of React. Nivo takes the JSON formatted data and nicely plots them.