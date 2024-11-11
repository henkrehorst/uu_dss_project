import os
from sqlalchemy import create_engine, Table, Column, Integer, Numeric, String, MetaData, inspect, UniqueConstraint


def migrate():
    engine = create_engine(os.getenv('DATABASE_URL'))
    table_name = 'travel_emissions'

    if not inspect(engine).has_table(table_name):
        metadata = MetaData()
        Table(table_name, metadata,
              Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
              Column('vehicle_type', String(length=30), nullable=False),
              # CO2 Emissions in grams/km
              Column('co2_emission', Numeric(10, 2), nullable=False),
              )
        metadata.create_all(engine)

        print('Table {} created'.format(table_name))
