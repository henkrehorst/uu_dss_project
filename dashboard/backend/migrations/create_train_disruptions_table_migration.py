import os
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, inspect, Numeric


def migrate():
    engine = create_engine(os.getenv('DATABASE_URL'))
    table_name = 'train_disruptions'

    if not inspect(engine).has_table(table_name):
        metadata = MetaData()
        Table(table_name, metadata,
              Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
              Column('rdt_station_codes', String(length=100), nullable=False),
              Column('year', Integer, nullable=False),
              Column('average_duration_minutes', Numeric(10, 2), default=0, nullable=False),
              )
        metadata.create_all(engine)

        print('Table {} created'.format(table_name))
