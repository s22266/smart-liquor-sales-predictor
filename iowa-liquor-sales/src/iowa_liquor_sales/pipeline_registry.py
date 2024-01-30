"""Project pipelines."""
from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()
    print(pipelines)
    pipelines["create_model"] = sum([pipelines['data_processing'], pipelines['model_training']])
    pipelines["__default__"] = sum([pipelines['data_processing'], pipelines['model_training']])
    return pipelines
