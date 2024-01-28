"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.14
"""
from kedro.pipeline import Pipeline, node
from .nodes import (
    filter_data_from_2017,
    remove_records_with_missing_values,
    group_and_sum_sales,
    remove_categories_with_missing_days,
    aggregate_by_month_year,
    remove_outliers,
    create_year_and_month_columns
)

# Tworzenie węzłów dla funkcji
filter_data_from_2017_node = node(
    filter_data_from_2017,
    inputs="imported_data_iowa_liquer",
    outputs="filtered_data",
    name="filter_data_from_2017_node"
)

remove_records_with_missing_values_node = node(
    remove_records_with_missing_values,
    inputs="filtered_data",
    outputs="cleaned_data",
    name="remove_records_with_missing_values_node"
)

group_and_sum_sales_node = node(
    group_and_sum_sales,
    inputs="cleaned_data",
    outputs="grouped_sales",
    name="group_and_sum_sales_node"
)

remove_categories_with_missing_days_node = node(
    remove_categories_with_missing_days,
    inputs="grouped_sales",
    outputs="data_without_missing_categories",
    name="remove_categories_with_missing_days_node"
)

aggregate_by_month_year_node = node(
    aggregate_by_month_year,
    inputs="data_without_missing_categories",
    outputs="monthly_aggregated_data",
    name="aggregate_by_month_year_node"
)

remove_outliers_node = node(
    remove_outliers,
    inputs="monthly_aggregated_data",
    outputs="data_without_outliers",
    name="remove_outliers_node"
)

create_year_and_month_columns_node = node(
    create_year_and_month_columns,
    inputs="data_without_outliers",
    outputs="final_data",
    name="create_year_and_month_columns_node"
)

def create_pipeline(**kwargs):
    return Pipeline(
        [
            filter_data_from_2017_node,
            remove_records_with_missing_values_node,
            group_and_sum_sales_node,
            remove_categories_with_missing_days_node,
            aggregate_by_month_year_node,
            remove_outliers_node,
            create_year_and_month_columns_node,
        ]
    )
