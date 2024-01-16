"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import process_data, train_test_split_data, train_model, evaluate_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=process_data,
                inputs={"data": "preProcessedData"},
                outputs="processedData",
                name="process_data",
            ),
            node(
                func=train_test_split_data,
                inputs={"data": "processedData", "parameters": "params:model_options"},
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="train_test_split_data",
            ),
            node(
                func=train_model,
                inputs={"X_train": "X_train", "y_train": "y_train", "model_options": "params:decision_tree_regressor"},
                outputs="decision_tree_regressor",
                name="train_model_decision_tree_regressor",
            ),
            node(
                func=evaluate_model,
                inputs=["decision_tree_regressor", "X_test", "y_test"],
                outputs="decision_tree_regressor_evaluation_results",
                name="evaluate_model_decision_tree_regressor",
            ),
        ]
    )