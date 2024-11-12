import json
import os

from flask import Blueprint, abort
import pandas as pd
from sqlalchemy import create_engine

rail_routes_blueprint = Blueprint('rail_routes', __name__)


@rail_routes_blueprint.route('/rail_routes')
def rail_routes():
    # select all geojson data from the ns_frequent_rail_routes table
    engine = create_engine(os.getenv('DATABASE_URL'))

    rail_routes_geojson = pd.read_sql_query(f"SELECT geojson FROM ns_frequent_rail_routes", engine)
    return json.dumps(rail_routes_geojson['geojson'].apply(json.loads).apply(lambda x: x[0]).to_list())


@rail_routes_blueprint.route("/rail_routes/lines")
def get_rail_routes_lines():
    engine = create_engine(os.getenv('DATABASE_URL'))

    frequent_rail_routes = pd.read_sql_query(
        f"select id, name, from_station, to_station, color from ns_frequent_rail_routes", engine)

    return frequent_rail_routes.to_dict(orient='records')


@rail_routes_blueprint.route("/rail_routes/lines/<from_station>/<to_station>")
def get_rail_route_by_stations(from_station, to_station):
    engine = create_engine(os.getenv('DATABASE_URL'))

    rail_route = pd.read_sql_query(
        f"select * from ns_frequent_rail_routes where from_station = '{from_station}' and to_station = '{to_station}'",
        engine)

    if rail_route.shape[0] == 0:
        abort(404, description="No rail route found")

    # fix geojson format
    rail_route['geojson'] = rail_route['geojson'].apply(json.loads)

    return rail_route.to_dict(orient='records')[0]


@rail_routes_blueprint.route("/rail_routes/lines/<from_station>/<to_station>/duration_comparison")
def get_rail_route_duration_comparison_by_vehicle(from_station, to_station):
    engine = create_engine(os.getenv('DATABASE_URL'))

    time_comparisons = pd.read_sql_query(
        f"""select car.duration_in_minutes as car_time, ns.trip_duration as train_time from ns_frequent_rail_routes ns 
        join public.rail_route_car_comparison car on ns.to_station = car.to_station 
        and ns.from_station = car.from_station 
        where ns.from_station = '{from_station}' and ns.to_station = '{to_station}'""",
        engine)

    if time_comparisons.shape[0] == 0:
        abort(404, description="No rail route found")

    return [
        {
            "vehicle": "car",
            "travel time car": round(time_comparisons['car_time'][0], 1)
        },
        {
            "vehicle": "train",
            "travel time train": round(time_comparisons['train_time'][0], 1)
        },
        {
            "vehicle": "differences",
            "travel time differences": round(time_comparisons['car_time'][0] - time_comparisons['train_time'][0], 1)
        },
    ]


@rail_routes_blueprint.route("/rail_routes/lines/<from_station>/<to_station>/emissions")
def get_rail_route_emissions_comparison(from_station, to_station):
    engine = create_engine(os.getenv('DATABASE_URL'))

    route_distances = pd.read_sql_query(
        f"""
        select car.road_distance from rail_route_car_comparison car
        where car.from_station = '{from_station}' and car.to_station = '{to_station}'""",
        engine)

    if route_distances.shape[0] == 0:
        abort(404, description="No rail route found")

    travel_emissions = pd.read_sql_query("""select * from travel_emissions order by vehicle_type""", engine)
    travel_emissions_graph_data = []

    for index, row in travel_emissions.iterrows():
        travel_emissions_graph_data.append({
            "vehicle": row['vehicle_type'].replace("_", " "),
            "co2 emission " + row['vehicle_type'].replace("_", " "): round(
                (row['co2_emission'] * route_distances['road_distance'][0]), 1)
        })

    return travel_emissions_graph_data


@rail_routes_blueprint.route("/rail_routes/lines/<from_station>/<to_station>/disruptions")
def get_rail_route_disruptions(from_station, to_station):
    engine = create_engine(os.getenv('DATABASE_URL'))

    rail_route_name = pd.read_sql_query(
        f"select name from ns_frequent_rail_routes where from_station = '{from_station}' and to_station = '{to_station}'",
        engine)

    if rail_route_name.shape[0] == 0:
        abort(404, description="No rail route found")

    average_duration = pd.read_sql_query(
        f"""select year as x, avg(average_duration_minutes) as y from train_disruptions
                where rail_route Like '%{rail_route_name['name'][0].replace("–","-")}%' group by year""",
        engine)

    return [{
        "id": "disruptions",
        "color": "hsl(33, 70%, 50%)",
        "data": average_duration.to_dict()
    }]

