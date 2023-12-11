"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.14
"""
import importlib

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.model_selection import train_test_split
from typing import Dict, Tuple, Any, Optional
from sklearn.preprocessing import LabelEncoder, StandardScaler
from datetime import datetime
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """
        Processes the input DataFrame by selecting columns, removing outliers, encoding categorical variables,
        and scaling the data.

        Steps:
        - Select specific columns.
        - Remove outliers.
        - Drop unnecessary columns based on correlation analysis.
        - Add 'day_of_week', 'is_weekday', and 'season' columns based on date.
        - Encode categorical columns.
        - Scale the data using StandardScaler.

        Args:
            data: Input DataFrame after data preparation.

        Returns:
            Processed DataFrame.
        """
    # Select specific columns
    selected_columns = ['store', 'zipcode', 'vendor_no', 'itemno',
                        'state_bottle_cost', 'state_bottle_retail', 'sale_bottles',
                        'sale_dollars', 'sale_liters', 'sale_gallons']
    df1 = data[selected_columns]

    def outliers(df, ft):
        Q1 = df1[ft].quantile(0.25)
        Q3 = df1[ft].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        ls = df.index[ (df[ft] < lower_bound) | (df[ft] > upper_bound) ]

        return ls

    index_list = []
    for ft in selected_columns:
        index_list.extend(outliers(df1, ft))

    def remove(df, ls):
        ls = sorted(set(ls))
        df = df.drop(ls)
        return df

    data = remove(data, index_list)

    # Drop unnecessary columns
    data = data.drop(columns=['sale_gallons', 'state_bottle_retail'])

    # Add 'day_of_week', 'is_weekday', and 'season' columns
    def get_season(month):
        if month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        elif month in [9, 10, 11]:
            return 'Autumn'
        else:
            return 'Winter'

    def get_weekday_info(year, month, day):
        date = datetime(year, month, day)
        return date.weekday(), date.weekday() < 5

    if 'year' in data.columns and 'month' in data.columns and 'day' in data.columns:
        data['day_of_week'], data['is_weekday'] = zip(*data.apply(lambda row: get_weekday_info(row['year'], row['month'], row['day']), axis=1))
        data['season'] = data['month'].apply(get_season)
    else:
        print("Warning: Columns 'year', 'month', or 'day' not found in data.")

    # Encode categorical columns
    label_encoder = LabelEncoder()
    columns_to_encode = ['invoice_line_no', 'name', 'address', 'city', 'county', 'category_name',
                         'vendor_name', 'im_desc', 'is_weekday', 'season']

    for col in columns_to_encode:
        data[col] = label_encoder.fit_transform(data[col])

    # Scale the data
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    data = pd.DataFrame(data_scaled, columns=data.columns, index=data.index)

    return data


def train_test_split_data(data: pd.DataFrame, parameters: Dict) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Splits the data into training and testing sets.

    Args:
        data: DataFrame containing the data to be split.
        params: Dictionary of parameters including target, test_size, random_state, etc.

    Returns:
        A Tuple containing the DataFrames: X_train, X_test, y_train, y_test.
    """

    target = parameters['target']
    test_size = parameters['test_size']
    random_state = parameters['random_state']

    X = data.drop(target, axis=1)
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    return X_train, X_test, y_train, y_test

def train_model(X_train: pd.DataFrame, y_train: pd.Series, model_options: Dict[str, Any]) -> Tuple[BaseEstimator, Dict[str, Any]]:
    """

    Args:
        X_train:
        y_train:
        model_options:

    Returns:

    """
    modelModule = model_options['module']
    modelClass = model_options['class']
    modelArgs = model_options['kwargs']

    regressor_class = getattr(importlib.import_module(modelModule), modelClass)
    regressor_instance = regressor_class(**modelArgs)

    # Fit model
    regressor_instance.fit(X_train, y_train)

    flat_model_params = {**{"model_type": modelClass}, **modelArgs}

    return regressor_instance, flat_model_params

def evaluate_model(model_and_params: Tuple[BaseEstimator, Dict[str, Any], Optional[LabelEncoder]], X_test: pd.DataFrame, y_test: pd.DataFrame) -> pd.DataFrame:
    """

    Args:


    Returns:

    """
    model, _ = model_and_params

    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    results = pd.DataFrame({
        "MSE": [mse],
        "MAE": [mae],
        "R2_Score": [r2]
    })

    return results
