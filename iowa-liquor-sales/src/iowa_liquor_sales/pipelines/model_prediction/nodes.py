"""
This is a boilerplate pipeline 'model_prediction'
generated using Kedro 0.18.14
"""

from autogluon.tabular import TabularPredictor
import pandas as pd

def data_prediction_node(county_name, category_name, start_month, start_year, end_month, end_year, historic_df):
    """
    Performs predictions on the provided data using the supplied model.

    Args:
    county_name (str): Name of the county.
    category_name (str): Name of the category.
    start_month (int): Starting month.
    start_year (int): Starting year.
    end_month (int): Ending month.
    end_year (int): Ending year.

    Returns:
    pd.DataFrame: DataFrame with predicted values.
    """

    df = generate_dataframe(county_name, category_name, start_month, start_year, end_month, end_year)

    path = "./data/06_models/ag_models"

    predictor = TabularPredictor.load(path)

    # Conduct predictions
    predictions = predictor.predict(df)
    
    # Dodajemy kolumnę "predicted" do DataFrame
    df['predicted'] = predictions

    historic_df = get_historic_data(historic_df, county_name, category_name)

    return df, historic_df

def generate_dataframe(county_name, category_name, start_month, start_year, end_month, end_year):
    """
    Generates a DataFrame with 'Month', 'Year', 'County', and 'Category Name' columns.

    Args:
    county_name (str): The name of the county.
    category_name (str): The name of the category.
    start_month (int): The starting month.
    start_year (int): The starting year.
    end_month (int): The ending month.
    end_year (int): The ending year.

    Returns:
    pd.DataFrame: A DataFrame with generated data.
    """

    # Tworzenie listy z danymi miesięcy i lat
    months = []
    years = []
    current_month = start_month
    current_year = start_year

    while current_year < end_year or (current_year == end_year and current_month <= end_month):
        months.append(current_month)
        years.append(current_year)

        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1

    # Tworzenie DataFrame
    data = {
        'Month': months,
        'Year': years,
        'County': [county_name] * len(months),
        'Category Name': [category_name.upper()] * len(months)
    }

    df = pd.DataFrame(data)
    return df

def get_historic_data(processed_data, filter_value_for_county, filter_value_for_description):

    filter_value_for_county = filter_value_for_county.upper()
    filter_value_for_description = filter_value_for_description.upper()

    processed_data = processed_data[processed_data['County'].str.upper() == filter_value_for_county]
    processed_data = processed_data[processed_data['Category Name'].str.contains(filter_value_for_description, case=False)]

    return processed_data