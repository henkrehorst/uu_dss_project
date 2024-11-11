from dotenv import load_dotenv
from migrations import sample_table_migration, create_ns_tariff_table_migration, \
    create_ns_frequent_rail_routes_table_migration, \
    create_travel_emissions_table_migration, \
    create_train_disruptions_table_migration, \
    create_rail_route_car_comparison_table_migration

if __name__ == '__main__':
    print("Running migration...")
    # Load env variables
    load_dotenv('.env')

    # Run migrations scripts
    sample_table_migration.migrate()
    create_ns_tariff_table_migration.migrate()
    create_ns_frequent_rail_routes_table_migration.migrate()
    create_travel_emissions_table_migration.migrate()
    create_train_disruptions_table_migration.migrate()
    create_rail_route_car_comparison_table_migration.migrate()

    print("Migrations finished!")
