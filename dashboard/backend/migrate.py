from dotenv import load_dotenv
from migrations import sample_table_migration, create_ns_tariff_table_migration, \
    create_ns_frequent_rail_routes_table_migration

if __name__ == '__main__':
    print("Running migration...")
    # Load env variables
    load_dotenv('.env')

    # Run migrations scripts
    sample_table_migration.migrate()
    create_ns_tariff_table_migration.migrate()
    create_ns_frequent_rail_routes_table_migration.migrate()

    print("Migrations finished!")
