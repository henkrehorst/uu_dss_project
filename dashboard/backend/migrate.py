from dotenv import load_dotenv
from migrations import sample_table_migration

if __name__ == '__main__':
    print("Running migration...")
    # Load env variables
    load_dotenv('.env')

    # Run migrations scripts
    sample_table_migration.migrate()

    print("Migrations finished!")
