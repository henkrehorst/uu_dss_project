import os
from sqlalchemy import create_engine, Table, Column, Integer, Numeric, String, MetaData, inspect


def migrate():
    engine = create_engine(os.getenv('DATABASE_URL'))
    table_name = 'rail_route_car_comparison'

    if not inspect(engine).has_table(table_name):
        metadata = MetaData()
        Table(table_name, metadata,
              Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
              Column('rail_route_name', String(length=255), nullable=False),
              Column('from_station', String(length=3), nullable=False),
              Column('to_station', String(length=3), nullable=False),
              Column('duration_in_minutes', Numeric(2,10), nullable=False),
              Column('road_distance', Numeric(2,10), nullable=False),
              )
        metadata.create_all(engine)

        print('Table {} created'.format(table_name))
