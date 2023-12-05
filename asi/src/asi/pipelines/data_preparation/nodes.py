"""
This is a boilerplate pipeline 'data_preparation'
generated using Kedro 0.18.14
"""
from typing import List

import pandas as pd
import json
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import time

geolocator = Nominatim(user_agent="my_geocoding_app", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
# Dict
found_coordinates = {}

def example_function(df: pd.DataFrame) -> pd.DataFrame:
    return df

"""
This is the main function create for preprocessing raw data 
(all beloved function combined in sync way)
"""
def preprocess_data(data: pd.DataFrame, columns_to_remove: List[str], records_to_remove: List[str]) -> pd.DataFrame:

    df1 = remove_columns(data, columns_to_remove)
    df2 = drop_null_rows(df1, records_to_remove)
    df3 = modify_date_column(df2)
    df4 = map_store_location_on_store(df3)
    df5 = createCoordinatesColumns(df4)
    df6 = fullfill_store_location_with_geocode_function(df5)
    df7 = drop_null_rows(df6, ['latitude', 'longitude'])
    df8 = remove_columns(df7, ['store_location'])

    preProcessedData = pd.DataFrame(df8)
    return preProcessedData

def remove_columns(data: pd.DataFrame, columns_to_remove: List[str]) -> pd.DataFrame:
    return data.drop(columns=columns_to_remove, errors='ignore')

def drop_null_rows(data: pd.DataFrame, records_to_remove: List[str]) -> pd.DataFrame:
    return data.dropna(subset=records_to_remove)

def map_zipcode_to_common_county_and_fill(data: pd.DataFrame) -> pd.DataFrame:
    zipcode_to_county = data.dropna(subset=['county']).groupby('zipcode')['county'].agg(lambda x: x.value_counts().index[0]).to_dict()

    data['county'] = data.apply(lambda row: zipcode_to_county.get(row['zipcode'], row['county']) if pd.isnull(row['county']) else row['county'], axis=1)

    return data

def modify_date_column(data: pd.DataFrame) -> pd.DataFrame:
    data_copy = data.copy()
    data_copy['date'] = pd.to_datetime(data_copy['date'])
    data_copy['year'] = data_copy['date'].dt.year
    data_copy['month'] = data_copy['date'].dt.month
    data_copy['day'] = data_copy['date'].dt.day
    dataToDrop = data_copy
    dataToDrop.drop('date', axis=1, inplace=True)

    return dataToDrop

def map_store_location_on_store(data: pd.DataFrame) -> pd.DataFrame:
    dataToReturn = pd.DataFrame(data)
    store_to_location = dataToReturn.dropna(subset=['store_location']).groupby('store')['store_location'].agg(
        lambda x: x.value_counts().index[0]).to_dict()

    dataToReturn['store_location'] = dataToReturn.apply(
        lambda row: store_to_location.get(row['store'], row['store_location']) if pd.isnull(row['store_location']) else
        row['store_location'], axis=1)

    return dataToReturn

def process_store_location(location_str):
    try:
        location_dict = json.loads(location_str.replace("'", "\""))
        return location_dict['coordinates'][0], location_dict['coordinates'][1]
    except (json.JSONDecodeError, KeyError, AttributeError):
        return None, None

def createCoordinatesColumns(data: pd.DataFrame) -> pd.DataFrame:
    data['longitude'], data['latitude'] = zip(*data['store_location'].apply(process_store_location))
    return data


def geocode_and_fill_coordinates(row):
    time.sleep(3)
    address = row['address']
    city = row['city']

    if pd.notnull(address) and pd.notnull(city):
        if (address, city) in found_coordinates:
            return found_coordinates[(address, city)]
        try:
            location = geocode(f"{address}, {city}")
            if location:
                lat, lon = location.latitude, location.longitude
                found_coordinates[(address, city)] = (lat, lon)
                return lat, lon
        except Exception as e:
            print(f"Error while geocoding: {e}")

    return None, None
def fullfill_store_location_with_geocode_function(data: pd.DataFrame) -> pd.DataFrame:
    df = data[data['store_location'].isna()]
    unique_addresses = df['address'].unique()

    for address in unique_addresses:
        temp_df = df[df['address'] == address]
        if not temp_df.empty:
            geocode_and_fill_coordinates(temp_df.iloc[0])

    # Update 'latitude' and 'longitude' using dict 'found_coordinates'
    for index, row in data.iterrows():
        if (row['address'], row['city']) in found_coordinates:
            lat, lon = found_coordinates[(row['address'], row['city'])]
            data.at[index, 'latitude'] = lat
            data.at[index, 'longitude'] = lon

    dataToReturn = pd.DataFrame(data)

    return dataToReturn