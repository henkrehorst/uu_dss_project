import os

from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, Numeric


def migrate():
    engine = create_engine(os.getenv('DATABASE_URL'))
    table_name = 'car_costs'

    if not inspect(engine).has_table(table_name):
        metadata = MetaData()
        Table(table_name, metadata,
              Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
              Column('period', Integer, nullable=False),
              Column('avg_cost', Numeric(10, 2), nullable=False),
              )
        metadata.create_all(engine)

        print('Table {} created'.format(table_name))
