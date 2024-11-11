import json
import os

from flask import Blueprint, abort
import pandas as pd
from sqlalchemy import create_engine

rail_routes_blueprint = Blueprint('rail_routes', __name__)


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


@rail_routes_blueprint.route('/rail_routes')
def rail_routes():
    # select all geojson data from the ns_frequent_rail_routes table
    engine = create_engine(os.getenv('DATABASE_URL'))

    rail_routes_geojson = pd.read_sql_query(f"SELECT geojson FROM ns_frequent_rail_routes", engine)
    return json.dumps(rail_routes_geojson['geojson'].apply(json.loads).apply(lambda x: x[0]).to_list())
