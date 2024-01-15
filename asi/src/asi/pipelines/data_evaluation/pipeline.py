"""
This is a boilerplate pipeline 'data_evaluation'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import make_prediction
from ..data_preparation.nodes import preprocess_data
from ..data_science.nodes import process_data

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_data,
                inputs={"data": "csvInputData", "columns_to_remove": "params:columns_to_remove","records_to_remove": "params:records_with_null"},
                outputs="preProcessedPredictionData",
                name="pre_process_data_prediction_node",
            ),
            node(
                func=process_data,
                inputs={"data": "preProcessedPredictionData"},
                outputs="processedPredictionData",
                name="process_data_prediction_node",
            ),
            node(
                func=make_prediction,
                inputs=["decision_tree_regressor", "processedPredictionData"],
                outputs="predictionData",
                name="prediction_node",
            ),
        ]
    )
