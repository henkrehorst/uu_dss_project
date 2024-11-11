from dotenv import load_dotenv
from data.ns.import_ns_tariff import import_ns_tariffs_by_year
from data.ns.import_frequent_ns_rail_routes import import_frequent_rail_routes

if "__main__" == __name__:
    print("Start data loading...")
    # Load env variables
    load_dotenv('.env')

    import_ns_tariffs_by_year(2021)
    import_ns_tariffs_by_year(2022)
    import_ns_tariffs_by_year(2023)
    import_ns_tariffs_by_year(2024)
    import_frequent_rail_routes()

    print("Data loading finished!")
