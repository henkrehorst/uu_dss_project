from dotenv import load_dotenv
from data.ns.import_ns_tariff import import_ns_tariffs_by_year
from data.ns.import_frequent_ns_rail_routes import import_frequent_rail_routes
from data.travel_emissions.import_travel_emissions import import_emissions_for_vehicles
from data.train_disruptions.import_train_disruptions import import_train_disruptions
from data.googlemaps.import_rail_route_car_comparison_data import import_rail_routes_car_times_by_google_maps
from data.car_costs.import_car_costs import import_car_costs

if "__main__" == __name__:
    print("Start data loading...")
    # Load env variables
    load_dotenv('.env')

    # import_ns_tariffs_by_year(2016)
    # import_ns_tariffs_by_year(2017)
    # import_ns_tariffs_by_year(2018)
    # import_ns_tariffs_by_year(2019)
    # import_ns_tariffs_by_year(2020)
    # import_ns_tariffs_by_year(2021)
    # import_ns_tariffs_by_year(2022)
    # import_ns_tariffs_by_year(2023)
    # import_ns_tariffs_by_year(2024)
    # import_frequent_rail_routes()
    # import_emissions_for_vehicles()
    # import_train_disruptions()
    import_rail_routes_car_times_by_google_maps()
    import_car_costs()

    print("Data loading finished!")
