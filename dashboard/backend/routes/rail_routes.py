import json
import os

from flask import Blueprint
import pandas as pd
from sqlalchemy import create_engine

rail_routes_blueprint = Blueprint('rail_routes', __name__)


@rail_routes_blueprint.route("/rail_routes/lines")
def get_rail_routes_lines():
    engine = create_engine(os.getenv('DATABASE_URL'))

    frequent_rail_routes = pd.read_sql_query(
        f"select id, name, from_station, to_station, color from ns_frequent_rail_routes", engine)

    return frequent_rail_routes.to_dict(orient='records')


@rail_routes_blueprint.route('/rail_routes')
def rail_routes():
    # select all geojson data from the ns_frequent_rail_routes table
    engine = create_engine(os.getenv('DATABASE_URL'))

    rail_routes_geojson = pd.read_sql_query(f"SELECT geojson FROM ns_frequent_rail_routes", engine)
    return json.dumps(rail_routes_geojson['geojson'].apply(json.loads).apply(lambda x: x[0]).to_list())
