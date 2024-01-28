"""
This is a boilerplate pipeline 'model_prediction'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline
from kedro.pipeline.node import node
from .nodes import data_prediction_node


data_prediction_node = node(
    data_prediction_node,
    inputs={"county_name": "params:county_name", "category_name": "params:category_name", "start_month": "params:start_month", "start_year": "params:start_year", "end_month": "params:end_month", "end_year": "params:end_year"},
    outputs="predicted_data",
    name="data_prediction_node"
)

def create_pipeline(**kwargs):
    return Pipeline(
        [
            data_prediction_node,
        ],
        tags=["predict"]
    )