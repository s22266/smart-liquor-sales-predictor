from pathlib import Path

import streamlit as st
import pandas as pd
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project


project_path = Path(__file__).resolve().parents[1]
bootstrap_project(Path(project_path))
with KedroSession.create(project_path=project_path) as session:
    key = "item_of_catalog"
    context = session.load_context()
    # kedro_connector = context.catalog.datasets.__dict__[key]
    # kedro_connector = context.catalog._get_datasets(key)


# Streamlit UI
st.title("Sales Prediction")

# File uploader for new data
uploaded_file = st.file_uploader("Upload CSV for Prediction", type=["csv"])

# Select prediction period
prediction_period = st.slider("Select Prediction Period (days)", min_value=1, max_value=365, value=30)

if uploaded_file is not None:

    dataframe = pd.read_csv(uploaded_file)
    context.catalog.save("predictionData", dataframe)

    session.run(pipeline_name="data_evaluation")

    st.write(dataframe)