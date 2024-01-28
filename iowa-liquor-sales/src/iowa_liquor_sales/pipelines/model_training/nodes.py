"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.18.14
"""

import pandas as pd
from autogluon.tabular import TabularPredictor

def train_model_node(df: pd.DataFrame):
    time_limit = 12
    label_column="Sale (Dollars)"
    df[label_column] = df[label_column].astype(float)

    predictor = TabularPredictor(label=label_column, path="./data/06_models/ag_models").fit(df, time_limit=time_limit)
    leaderboard = predictor.leaderboard(silent=True)
    best_model = leaderboard.iloc[0]['model']  # Pobranie najlepszego modelu
    return best_model