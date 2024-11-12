import json
import os
from flask import abort, Blueprint
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.stats import t
from sqlalchemy import create_engine

price_comparison_blueprint = Blueprint('price_comparison', __name__)


@price_comparison_blueprint.route("/price_comparison/<from_station>/<to_station>")
def price_comparison(from_station, to_station):
    engine = create_engine(os.getenv('DATABASE_URL'))
    car_costs = pd.read_sql_query('SELECT * FROM car_costs where cast("Perioden" as int) > 2015', engine)
    # convert to key value pair
    road_cost = (car_costs['yearAvg'] / 100) * float(get_road_distance(from_station, to_station))
    car_costs = car_costs.set_index('Perioden')['yearAvg']

    # ROUTE COSTS CAR
    ## Prepare the data
    years_road = np.array(car_costs.index.values).reshape(-1, 1)  # Reshape for scikit-learn

    # Create and fit the model
    linear_model_road = LinearRegression()
    linear_model_road.fit(years_road, road_cost)

    # Predict future years (e.g., 2024, 2025)
    future_years_road = np.array([2023, 2024, 2025, 2026, 2027, 2028]).reshape(-1, 1)
    future_road_cost = linear_model_road.predict(future_years_road)

    # Error margin calculations
    road_cost_pred = linear_model_road.predict(years_road)
    road_error_margin = np.sqrt(np.sum((road_cost - road_cost_pred) ** 2) / (len(years_road) - 2))  # Standard error
    road_t_value = t.ppf(0.975, df=len(years_road) - 2)  # t-value for 95% confidence interval
    road_ci = road_t_value * road_error_margin  # Confidence interval

    # ROUTE COSTS TRAIN
    # Prepare the data
    trainCosts = get_train_costs(from_station, to_station)
    years_train = np.array(trainCosts['year']).reshape(-1, 1)  # Reshape for scikit-learn
    train_cost = trainCosts['tariff']

    # Create and fit the model
    linear_model_train = LinearRegression()
    linear_model_train.fit(years_train, train_cost)

    # Predict future years (e.g., 2024, 2025)
    future_years_train = np.array([2024, 2025, 2026, 2027, 2028]).reshape(-1, 1)
    future_train_cost = linear_model_train.predict(future_years_train)

    # Error margin calculations for train
    train_cost_pred = linear_model_train.predict(years_train)
    train_error_margin = np.sqrt(np.sum((train_cost - train_cost_pred) ** 2) / (len(years_train) - 2))  # Standard error
    train_t_value = t.ppf(0.975, df=len(years_train) - 2)  # t-value for 95% confidence interval
    train_ci = train_t_value * train_error_margin  # Confidence interval

    return json.dumps([
        {"id": "future road", "data": combine_year_costs(future_years_road.astype(int).flatten(), future_road_cost)},
        {"id": "future train", "data": combine_year_costs(future_years_train.astype(int).flatten(), future_train_cost)},
        {"id": "road prices", "data": combine_year_costs(years_road.astype(int).flatten(), road_cost)},
        {"id": "train prices", "data": combine_year_costs(trainCosts['year'].astype(int), trainCosts['tariff'])}
    ], cls=NpEncoder)


def get_road_distance(from_station, to_station):
    # get enegine
    engine = create_engine(os.getenv('DATABASE_URL'))

    # get the distance with pandas
    road_distance = pd.read_sql_query(
        f"SELECT road_distance FROM rail_route_car_comparison WHERE from_station = '{from_station}' AND to_station = '{to_station}'",
        engine)

    if road_distance.shape[0] == 0:
        abort(404, description='No road distance found for this route')

    return road_distance['road_distance'][0]


def get_train_costs(from_station, to_station):
    # get enegine
    engine = create_engine(os.getenv('DATABASE_URL'))

    # get the distance with pandas
    train_tariffs = pd.read_sql_query(
        f"""select year, second_class_full_tariff Tariff from ns_train_tariffs
                where cast(tariff_units as int) = (
                select tariff_units from ns_frequent_rail_routes 
                n where n.to_station =  '{to_station}' and n.from_station = '{from_station}')""",
        engine)

    if train_tariffs.shape[0] == 0:
        abort(404, description='No tariffs found for this route')

    return train_tariffs


def combine_year_costs(years, costs):
    return [{'x': year, 'y': cost} for year, cost in zip(years, costs)]


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
