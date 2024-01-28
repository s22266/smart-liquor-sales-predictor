"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline
from kedro.pipeline.node import node
from .nodes import train_model_node


train_model_node = node(
    train_model_node,
    inputs="final_data",
    outputs="best_model",
    name="train_model_node"
)

def create_pipeline(**kwargs):
    return Pipeline(
        [
            train_model_node,
        ],
        tags=["model_training_pipeline"]
    )
