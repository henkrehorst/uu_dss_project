import pandas as pd
from sqlalchemy import create_engine
import os


def import_train_disruptions():
    # Load all CSV files for the years 2017 to 2023
    file_paths = ['disruptions-2017.csv',
                  'disruptions-2018.csv',
                  'disruptions-2019.csv',
                  'disruptions-2020.csv',
                  'disruptions-2021.csv',
                  'disruptions-2022.csv',
                  'disruptions-2023.csv'
                  ]

    dataframes = [pd.read_csv(fr"./data/train_disruptions/csv/{file}") for file in file_paths]

    # Concatenate all dataframes into a single dataframe
    data = pd.concat(dataframes, ignore_index=True)

    # Extract the year from the 'start_time' column and add it as a new column
    data['year'] = pd.to_datetime(data['start_time']).dt.year

    # Group by 'Traject' (the column 'rdt_lines') and 'year', then calculate the average delay per line
    average_delay_per_line = data.groupby(['rdt_station_codes', 'year'])['duration_minutes'].mean().reset_index()

    # Rename columns for clarity
    average_delay_per_line.columns = ['rdt_station_codes', 'year', 'average_duration_minutes']

    # save train disruptions to database
    engine = create_engine(os.getenv('DATABASE_URL'))
    average_delay_per_line.to_sql('train_disruptions', engine, if_exists='replace', index=False)

    print("Train disruptions imported successfully")
