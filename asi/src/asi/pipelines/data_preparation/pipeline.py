"""
This is a boilerplate pipeline 'data_preparation'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import remove_columns, drop_null_rows, map_zipcode_to_common_county_and_fill


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=remove_columns,
                inputs={"data": "rawData", "columns_to_remove": "params:columns_to_remove"},
                outputs="basicData",
                name="deletedColumns",
            ),
            node(
                func=drop_null_rows,
                inputs={"data": "basicData", "records_to_remove": "params:records_with_null"},
                outputs="preCleanedData",
                name="droppedNull",
            ),
            node(
                func=map_zipcode_to_common_county_and_fill,
                inputs={"data": "preCleanedData"},
                outputs="countyFullfilledData",
                name="map_zipcode_to_common_county_and_fill",
            ),
        ]
    )
