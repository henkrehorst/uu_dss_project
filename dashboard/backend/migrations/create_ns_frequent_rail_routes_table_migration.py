import os
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, inspect, Numeric
from sqlalchemy.dialects.postgresql import JSONB


def migrate():
    engine = create_engine(os.getenv('DATABASE_URL'))
    table_name = 'ns_frequent_rail_routes'

    if not inspect(engine).has_table(table_name):
        metadata = MetaData()
        Table(table_name, metadata,
              Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
              Column('name', String(length=255), nullable=False),
              Column('from_station', String(length=3), nullable=False),
              Column('to_station', String(length=3), nullable=False),
              Column('from_coordinates', String(length=60), nullable=False),
              Column('to_coordinates', String(length=60), nullable=False),
              Column('color', String(length=7), nullable=False),
              Column('trip_duration', Numeric(10,2), nullable=False),
              Column('tariff_units', Integer, nullable=False),
              Column('geojson', JSONB, nullable=False)
              )
        metadata.create_all(engine)

        print('Table {} created'.format(table_name))
