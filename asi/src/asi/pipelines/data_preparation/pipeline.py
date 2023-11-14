"""
This is a boilerplate pipeline 'data_preparation'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import example_function


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=example_function,
                inputs=["iowa_liquor_sales_subset"],
                outputs="cleaned_data",
                name="example_node",
            ),
        ]
    )
