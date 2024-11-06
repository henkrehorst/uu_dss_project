import os
from sqlalchemy import create_engine, Table, Column, Integer, Numeric, String, MetaData, inspect, UniqueConstraint


def migrate():
    engine = create_engine(os.getenv('DATABASE_URL'))
    table_name = 'ns_train_tariffs'

    if not inspect(engine).has_table(table_name):
        metadata = MetaData()
        Table(table_name, metadata,
              Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
              Column('tariff_units', String(length=4), nullable=False),
              Column('year', Integer, nullable=False),
              Column('second_class_full_tariff', Numeric(10, 2), nullable=False),
              Column('second_class_20_discount_tariff', Numeric(10, 2), nullable=False),
              Column('second_class_40_discount_tariff', Numeric(10, 2), nullable=False),
              Column('second_class_full_tariff_ex_tax', Numeric(10, 2), nullable=False),
              # Ensure that the combination of tariff_units and year is unique
              UniqueConstraint('tariff_units', 'year', name='unique_tariff_units_year')
              )
        metadata.create_all(engine)

        print('Table {} created'.format(table_name))
