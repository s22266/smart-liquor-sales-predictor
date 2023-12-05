"""
This is a boilerplate pipeline 'data_preparation'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import preprocess_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_data,
                inputs={"data": "rawData", "columns_to_remove": "params:columns_to_remove", "records_to_remove": "params:records_with_null"},
                outputs="preProcessedData",
                name="preprocess_data",
            ),
        ]
    )
