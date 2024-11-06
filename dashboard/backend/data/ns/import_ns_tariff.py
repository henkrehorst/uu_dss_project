import os

import pandas as pd
from sqlalchemy import create_engine


def split_and_expand_row(df):
    # Extract the first row (labeled as "0 to 8")
    first_row = df[df["tariff_units"] == '0 t/m 8'].values[0]

    # Create 8 new rows, each with one value from the "0 to 8" row
    new_rows = pd.DataFrame([first_row] * 9, columns=df.columns)

    # Update the index of new rows to be from 0 to 8
    new_rows["tariff_units"] = range(0, 9)

    # Drop the original "0 to 8" row
    df = df.drop(df[df["tariff_units"] == '0 t/m 8'].index)

    # Concatenate the new rows at the top of the DataFrame
    new_frame = pd.concat([new_rows, df]).reset_index(drop=True)

    return new_frame


def import_ns_tariffs_by_year(year):
    engine = create_engine(os.getenv('DATABASE_URL'))
    table_name = 'ns_train_tariffs'

    # Check if ns tariffs for the year is already imported
    if pd.read_sql(f"SELECT COUNT(*) FROM {table_name} WHERE year = {year}", engine)['count'][0] > 0:
        print(f"NS tariffs for year {year} already imported")
        return

    tariffs_by_year = pd.read_csv(f"./data/ns/csv/treinprijzen{year}.csv", delimiter=",")

    # Clean and reformat csv data
    tariffs_by_year = split_and_expand_row(tariffs_by_year)
    tariffs_by_year = tariffs_by_year.replace('€', '', regex=True)
    tariffs_by_year = tariffs_by_year.replace(' ', '', regex=True)
    tariffs_by_year = tariffs_by_year.replace(',', '.', regex=True)
    tariffs_by_year.astype(float)
    tariffs_by_year['tariff_units'].astype(int)

    # Added year column to pandas frame
    tariffs_by_year['year'] = year

    # Import data to database
    tariffs_by_year.to_sql(table_name, engine, if_exists='append', index=False)

    print(f"NS tariffs for year {year} imported successfully")
