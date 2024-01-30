"""
This is a boilerplate pipeline 'data_evaluation'
generated using Kedro 0.18.14
"""

import pandas as pd


def make_prediction(model, data: pd.DataFrame) -> pd.DataFrame:
    predictions = model.predict(data)
    return pd.DataFrame(predictions, columns=['prediction'])
