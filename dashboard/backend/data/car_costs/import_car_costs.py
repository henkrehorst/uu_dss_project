import os

import pandas as pd
from sodapy import Socrata
import requests
from sqlalchemy import create_engine


def import_car_costs():
    # create engine
    engine = create_engine(os.getenv('DATABASE_URL'))

    full_prices = get_full_prices()

    # insert data into table
    full_prices.to_sql('car_costs', engine, if_exists='replace', index=True)

    print('Car cost successfully imported!')


def get_average_full_usage():
    client = Socrata("opendata.rdw.nl", None)

    results = client.get("8ys7-d773",
                         select="avg(brandstofverbruik_gecombineerd::number), count(brandstofverbruik_gecombineerd), brandstof_omschrijving",
                         where="brandstofverbruik_gecombineerd IS NOT NULL AND brandstofverbruik_gecombineerd != '0.00'",
                         group='brandstof_omschrijving, brandstofverbruik_gecombineerd',
                         order="brandstofverbruik_gecombineerd", limit=20000000)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)

    #renmae columns
    results_df = results_df.rename(columns={'avg_brandstofverbruik_gecombineerd_number': 'brandstofverbruik_gecombineerd'})
    results_df = results_df.rename(columns={'count_brandstofverbruik_gecombineerd': 'brandstofverbruik_gecombineerd_count'})

    # Convert fuel usage column values from string to float
    results_df['brandstofverbruik_gecombineerd'] = results_df['brandstofverbruik_gecombineerd'].astype(float)
    results_df['brandstofverbruik_gecombineerd_count'] = results_df['brandstofverbruik_gecombineerd_count'].astype(int)

    average_usage = results_df.groupby('brandstof_omschrijving').agg(
        average_fuel_usage=('brandstofverbruik_gecombineerd', 'mean'),
        number_of_cars=('brandstofverbruik_gecombineerd_count', 'sum')
    ).reset_index().sort_values(by=['number_of_cars'], ascending=False)

    return average_usage[average_usage['brandstof_omschrijving'].isin(['Benzine', 'Diesel', 'LPG'])]


def get_full_prices():
    # Url for the fuel prices API
    url = "https://opendata.cbs.nl/ODataApi/odata/81567NED/Motorbrandstof"

    try:
        # Fetch data from the API
        response = requests.get(url)
        response.raise_for_status()  # Raises an error if the request failed

        # Parse the response JSON data
        data = response.json()

        # The data we want is inside the "value" key
        records = data.get("value", [])

        # Convert data to a pandas DataFrame for easier manipulation
        fuelNames = pd.DataFrame(records)

    except requests.exceptions.RequestException as e:
        print("Error retrieving data:", e)

    # Drop unnecessary columns
    fuelNames = fuelNames.drop(['Description', 'CategoryGroupID'], axis=1)

    # Modify the title column to the first word
    fuelNames['Title'] = fuelNames['Title'].str.split().str[0]

    # Url for the fuel prices API
    url = "https://opendata.cbs.nl/ODataApi/odata/81567NED/TypedDataSet?$filter=substringof('JJ', Perioden)"

    try:
        # Fetch data from the API
        response = requests.get(url)
        response.raise_for_status()  # Raises an error if the request failed

        # Parse the response JSON data
        data = response.json()

        # The data we want is inside the "value" key
        records = data.get("value", [])

        # Convert data to a pandas DataFrame for easier manipulation
        fuelPrices = pd.DataFrame(records)

    except requests.exceptions.RequestException as e:
        print("Error retrieving data:", e)

    # The "Perioden" column is in a string format of year+quarter with year spanning the first 4 digits,
    # let's separate year
    fuelPrices['Perioden'] = fuelPrices['Perioden'].str[:4]

    fuelPrices = fuelPrices.drop(['PompprijsSnelwegBemandStation_2', 'PompprijsNietSnelwegBemandStation_3',
                                  'PompprijsNietSnelwegOnbemandStation_4'], axis=1)

    fuelPrices = fuelPrices.merge(fuelNames, left_on='Motorbrandstof', right_on='Key', how='left')

    # Drop the 'Key' column since we don't need it anymore
    fuelPrices = fuelPrices.drop(columns=['Motorbrandstof', 'Key']).rename(columns={'Title': 'FuelName'})

    # for our comparison, we are only interested in the years from 2019
    # fuelPrices = fuelPrices[fuelPrices['Perioden'].astype(int) >= 2019]

    # sort for readability
    fuelPrices = fuelPrices.sort_values(by=['Perioden'], ascending=True).reset_index(drop=True)

    # drop redundant columns
    fuelPrices = fuelPrices.drop(['ID'], axis=1)

    ConventionalFuelUsage = get_average_full_usage()

    # Drop all caps, including first character
    ConventionalFuelUsage['brandstof_omschrijving'] = ConventionalFuelUsage['brandstof_omschrijving'].str.lower()
    # Bring back uppercase to only the first character
    ConventionalFuelUsage['brandstof_omschrijving'] = ConventionalFuelUsage['brandstof_omschrijving'].str.capitalize()

    # Merge fuelPrices with conventionalFuelUsage on the fuel type column
    merged_df = pd.merge(
        fuelPrices,
        ConventionalFuelUsage,
        left_on="FuelName",
        right_on="brandstof_omschrijving",
        how="left"
    )

    # Calculate the price per 100 km for each row
    merged_df["price_per_100km"] = merged_df["GemiddeldePompprijs_1"] * merged_df["average_fuel_usage"]

    # Select the relevant columns for the result
    result_df = merged_df[
        ["Perioden", "FuelName", "GemiddeldePompprijs_1", "average_fuel_usage", "price_per_100km", "number_of_cars"]]

    # Ensure ConventionalFuelUsage is a separate copy
    result_df = result_df.copy()

    # Perform the vectorized calculation
    result_df['product'] = (
            result_df['price_per_100km'] * result_df['number_of_cars']
    )

    TotalSampleCars = ConventionalFuelUsage['number_of_cars'].sum()

    summedDf = result_df.groupby('Perioden').sum()

    summedDf = summedDf.copy()

    summedDf['yearAvg'] = (
            summedDf['product'] / TotalSampleCars
    )

    # drop redundant columns
    summedDf = summedDf.drop(
        ['FuelName', 'GemiddeldePompprijs_1', 'average_fuel_usage', 'price_per_100km', 'number_of_cars', 'product'],
        axis=1)

    return summedDf