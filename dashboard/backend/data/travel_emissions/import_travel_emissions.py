import os

import requests
import pandas as pd
from sqlalchemy import create_engine


def import_emissions_for_vehicles():
    url_train = "https://tools.ce.nl/stream/api/data?advanced=false&last_emission_calculation_method=3&year=2&vehicle_category=91&vehicle_technology=2&distance_type=1&emission_calculation_method=3&emission=energy_consumption&emission=co2_eq_incl_infra"
    url_cars = "https://tools.ce.nl/stream/api/data?advanced=false&last_emission_calculation_method=3&year=2&vehicle_category=1&vehicle_technology=7&vehicle_technology=35&vehicle_technology=50&distance_type=1&emission_calculation_method=3&emission=co2_eq_incl_infra"

    emissions_data = list()

    # Fetching data from the CE STREAM API for the train
    response_train = requests.get(url_train)
    if response_train.status_code == 200:
        data_train = response_train.json()
        co2_train = float(data_train["items"][0]["co2_eq_incl_infra"].replace(",", "."))
        emissions_data.append({"vehicle_type": "train", "co2_emission": co2_train})
    else:
        print("Error fetching train data:", response_train.status_code)

    # Fetching data from the CE STREAM API for cars
    response_cars = requests.get(url_cars)
    if response_cars.status_code == 200:
        data_cars = response_cars.json()
        co2_car_gasoline = float(data_cars["items"][0]["co2_eq_incl_infra"].replace(",", "."))
        co2_car_diesel = float(data_cars["items"][1]["co2_eq_incl_infra"].replace(",", "."))
        co2_car_electric = float(data_cars["items"][2]["co2_eq_incl_infra"].replace(",", "."))
        emissions_data.append({"vehicle_type": "car_gasoline", "co2_emission": co2_car_gasoline})
        emissions_data.append({"vehicle_type": "car_diesel", "co2_emission": co2_car_diesel})
        emissions_data.append({"vehicle_type": "car_electric", "co2_emission": co2_car_electric})

        # convert emissions_data to a pandas DataFrame
        df = pd.DataFrame(emissions_data)

        # save to database
        engine = create_engine(os.getenv('DATABASE_URL'))
        df.to_sql("travel_emissions", con=engine, if_exists="replace")

        # print success message
        print("Emissions data successfully imported into database!")

    else:
        print("Error fetching car data:", response_cars.status_code)
