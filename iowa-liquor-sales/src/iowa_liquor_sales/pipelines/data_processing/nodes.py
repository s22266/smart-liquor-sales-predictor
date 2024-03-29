"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.14
"""
from kedro.pipeline import node
import pandas as pd
from pandas.tseries.offsets import MonthEnd

def filter_data_from_2017(df_start):
    """
        Filters the DataFrame to include only data from 2017 onwards.

        Args:
            df_start (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The filtered DataFrame with data from 2017 onwards.
    """

    # Column mapping dictionary
    column_mapping = {
        'county': 'County',
        'category_name': 'Category Name',
        'sale_dollars': 'Sale (Dollars)',
        'date': 'Date'
    }

    # Rename columns based on the mapping
    df_start = df_start.rename(columns=lambda x: column_mapping[x] if x in column_mapping else x)

    features = ['Date', 'County', 'Category Name']
    target_column = 'Sale (Dollars)'

    # Select required columns and convert the 'Date' column to datetime
    df = df_start[features + [target_column]]
    df['Date'] = pd.to_datetime(df['Date'])

    # Filter rows where the year is 2017 or later
    df = df[df['Date'].dt.year >= 2017]

    return df

def remove_records_with_missing_values(df):
    """
    Remove rows with missing values from the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with rows containing missing values removed.
    """
    # Remove rows with missing values
    df = df.dropna()

    return df

def group_and_sum_sales(df):
    """
    Group the DataFrame by specified features and sum the 'Sale (Dollars)' column.

    Args:
        df (pd.DataFrame): The input DataFrame.
    Returns:
        pd.DataFrame: The grouped DataFrame with the 'Sale (Dollars)' column summed.
    """
    features = ['Date', 'County', 'Category Name']

    # Group by specified features and sum the 'Sale (Dollars)' column
    df = df.groupby(features)['Sale (Dollars)'].sum().reset_index()

    return df

def remove_categories_with_missing_days(df):
    """
    Remove categories within each county where there are missing days in the last two months.

    Args:
        df (pd.DataFrame): The input DataFrame with a 'Date' column.

    Returns:
        pd.DataFrame: The DataFrame with categories removed where missing days are present.
    """
    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Define date range for the last two months
    end_date = df['Date'].max()
    start_date = (end_date - MonthEnd(2))

    # Filter data for the last two months
    df_recent = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Function to check for missing days
    def has_missing_days(group):
        expected_days = pd.date_range(start=start_date, end=end_date, freq='D')
        actual_days = group['Date'].dt.date.unique()
        return not expected_days.isin(actual_days).all()

    # Apply the function to groups and select those with missing days
    groups_with_missing_days = df_recent.groupby(['County', 'Category Name']).filter(has_missing_days)

    # Remove groups with missing days from the original DataFrame
    df = df[~df.index.isin(groups_with_missing_days.index)]

    return df

def aggregate_by_month_year(df):
    """
    Aggregate data by month and year.

    Args:
        df (pd.DataFrame): The input DataFrame with a 'Date' column.

    Returns:
        pd.DataFrame: The aggregated DataFrame with sales summed by month, county, and category.
    """
    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Extract month and year
    df['Month_Year'] = df['Date'].dt.to_period('M')

    # Group data and sum 'Sale (Dollars)'
    df = df.groupby(['Month_Year', 'County', 'Category Name'])['Sale (Dollars)'].sum().reset_index()

    return df

def remove_outliers(df):
    """
    Remove outliers from a specified column in the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
    Returns:
        pd.DataFrame: The DataFrame with outliers removed.
    """

    column_name = 'Sale (Dollars)'

    # Step 1 and 2: Calculate Q1, Q3, and IQR for the specified column
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1

    # Step 3: Identify outliers
    outliers = (df[column_name] < (Q1 - 1.5 * IQR)) | (df[column_name] > (Q3 + 1.5 * IQR))

    # Step 4: Replace outliers with the median of the column
    median = df[column_name].median()
    df.loc[outliers, column_name] = median

    return df


def create_year_and_month_columns(df):
    """
    Create 'Year' and 'Month' columns based on the 'Month_Year' column.

    Args:
        df (pd.DataFrame): The input DataFrame with a 'Month_Year' column.

    Returns:
        pd.DataFrame: The DataFrame with 'Year' and 'Month' columns added and 'Month_Year' column removed.
    """
    # Convert 'Month_Year' back to datetime format
    df['Month_Year'] = pd.to_datetime(df['Month_Year'].astype(str))

    # Add 'Year' and 'Month' columns
    df['Year'] = df['Month_Year'].dt.year
    df['Month'] = df['Month_Year'].dt.month

    # Drop the 'Month_Year' column
    df.drop('Month_Year', axis=1, inplace=True)

    return df

def alcohol_description_parser(df):
    """
    Transforms values in the 'alcohol_description' column to one of the specified keywords if they match any of the
    specified character strings. Removes rows that do not match any keyword. Additionally, aggregates the data to sum
    up the quantities of the same alcohol types.

    Parameters:
        df (pd.DataFrame): The input DataFrame with the 'Category Name' column.

    Returns:
        pd.DataFrame: The processed DataFrame with 'alcohol_description' values replaced, cleaned, and aggregated.
    """
    
    keywords = ['RUM', 'VODKA', 'TEQUILA', 'WHISKIES', 'SCHNAPPS']

    def transform_description(description):
        for keyword in keywords:
            if keyword in description.upper():
                return keyword
        return None

    # Create a copy of the DataFrame to avoid modifying the original
    df = df.copy()

    # Apply the transformation to the 'Category Name' column
    df['Category Name'] = df['Category Name'].apply(transform_description)

    # Remove rows where the transformed 'Category Name' is None (i.e., no keyword match)
    df = df.dropna()

    # Column name for sales data
    target_column = 'Sale (Dollars)'

    # Group by the transformed 'Category Name' and other relevant columns, and sum the sales data
    df_aggregated = df.groupby(['Category Name', 'Month', 'Year', 'County'], as_index=False)[target_column].sum()

    return df_aggregated
