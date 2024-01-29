"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.18.14
"""

import pandas as pd
from autogluon.tabular import TabularPredictor

def train_model(df: pd.DataFrame):
    """
        Trains a machine learning model using the provided DataFrame and returns the best model.

        Args:
            df (pd.DataFrame): The DataFrame containing the training data.

        Returns:
            str: The name of the best performing model.
    """
    # Set the time limit for the training process
    time_limit = 600
    # Define the label (target) column
    label_column="Sale (Dollars)"
    # Ensure the label column is of float type
    df[label_column] = df[label_column].astype(float)

    # Initialize and fit the TabularPredictor
    # The path specifies where the trained models will be saved
    predictor = TabularPredictor(label=label_column, path="./data/06_models/ag_models").fit(df, time_limit=time_limit)

    # Retrieve and display the leaderboard of models trained by the TabularPredictor
    leaderboard = predictor.leaderboard(silent=True)

    # Select the best model based on the leaderboard
    best_model = leaderboard.iloc[0]['model']

    # Print detailed information about the best model
    print(predictor.info()['model_info'][best_model])

    # Return the name of the best model
    return best_model