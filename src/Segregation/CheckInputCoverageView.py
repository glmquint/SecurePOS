import json
import os
import random
import plotly.graph_objects as go
import pandas as pd
from random import random
from src.Segregation.CheckInputCoverageModel import CheckInputCoverageModel


class CheckInputCoverageView:

    def __init__(self, model):
        self.__check_input_coverage_model: CheckInputCoverageModel = model

    def plot_check_input_coverage_view(self):

        pandas_dataset: pd.DataFrame = self.__check_input_coverage_model.get_prepared_session_df()

        # we rename attributes for better readability on the plot
        labels = ['MeanAbsoluteDifferencingTransactionTimestamps',
                  'MeanAbsoluteDifferencingTransactionAmount',
                  'MedianLongitude',
                  'MedianLatitude',
                  'MedianTargetIP',
                  'MedianDestIP']
        assert len(labels) == len(
            pandas_dataset.columns), f"cannot rename different number of columns: {len(labels)} instead of {len(pandas_dataset.columns)}"
        pandas_dataset.columns = labels

        fig = go.Figure()

        # for each row in the dataset, create a scatter plot
        for _, row in pandas_dataset.iterrows():
            fig.add_trace(
                go.Scatterpolar(
                    r=row.values.tolist(),
                    theta=pandas_dataset.columns.tolist(),
                    fill=None,
                    mode="markers"
                )
            )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=False,
            title="Coverage Report",
        )

        fig.write_image(
            f"{os.path.dirname(__file__)}/Data/Plot/PlotCheckInputCoverage.png")

    @staticmethod
    def get_simulated_check_input_coverage():
        value = random()
        if value < 0.1:
            return "no"
        else:
            return "ok"

    @staticmethod
    def get_check_input_coverage():
        with open(f'{os.path.dirname(__file__)}/Data/checkInputCoverageReport.json', 'r') as check_input_coverage_file:
            json_data = json.load(check_input_coverage_file)
            evaluation_check_input_coverage = json_data.get("evaluation")
            check_input_coverage_file.close()
            return evaluation_check_input_coverage
