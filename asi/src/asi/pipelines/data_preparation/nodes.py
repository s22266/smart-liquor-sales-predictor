"""
This is a boilerplate pipeline 'data_preparation'
generated using Kedro 0.18.14
"""
from typing import List

import pandas as pd


def example_function(df: pd.DataFrame) -> pd.DataFrame:
    return df

def remove_columns(data: pd.DataFrame, columns_to_remove: List[str]) -> pd.DataFrame:
    return data.drop(columns=columns_to_remove, errors='ignore')

def drop_null_rows(data: pd.DataFrame, records_to_remove: List[str]) -> pd.DataFrame:
    return data.dropna(subset=records_to_remove)

def map_zipcode_to_common_county_and_fill(data: pd.DataFrame) -> pd.DataFrame:
    zipcode_to_county = data.dropna(subset=['county']).groupby('zipcode')['county'].agg(lambda x: x.value_counts().index[0]).to_dict()

    data['county'] = data.apply(lambda row: zipcode_to_county.get(row['zipcode'], row['county']) if pd.isnull(row['county']) else row['county'], axis=1)

    return data