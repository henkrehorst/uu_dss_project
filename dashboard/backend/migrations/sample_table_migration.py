import os

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, inspect


def migrate():
    engine = create_engine(os.getenv('DATABASE_URL'))
    table_name = 'sample'

    if not inspect(engine).has_table(table_name):
        metadata = MetaData()
        Table(table_name, metadata,
              Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
              Column('name', String(length=200), nullable=False))
        metadata.create_all(engine)

        print('Table {} created'.format(table_name))
