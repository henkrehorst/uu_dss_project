from dotenv import load_dotenv
from migrations import create_ns_tariff_table_migration, \
    create_ns_frequent_rail_routes_table_migration, \
    create_travel_emissions_table_migration, \
    create_train_disruptions_table_migration, \
    create_rail_route_car_comparison_table_migration,\
    create_car_cost_table_migration

if __name__ == '__main__':
    print("Running migration...")
    # Load env variables
    load_dotenv('.env')

    # Run migrations scripts
    create_ns_tariff_table_migration.migrate()
    create_ns_frequent_rail_routes_table_migration.migrate()
    create_travel_emissions_table_migration.migrate()
    create_train_disruptions_table_migration.migrate()
    create_rail_route_car_comparison_table_migration.migrate()
    create_car_cost_table_migration.migrate()

    print("Migrations finished!")
