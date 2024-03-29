import json
import os
import random
import plotly.graph_objects as go
import pandas as pd
from src.Segregation.CheckInputCoverageModel import CheckInputCoverageModel


class CheckInputCoverageView:
    """
    View class responsible for visualizing input coverage checks.

    Attributes:
    __check_input_coverage_model (CheckInputCoverageModel): An instance of the input coverage model.

    Methods:
    plot_check_input_coverage_view():
        Plots the input coverage using plotly based on the prepared session data.
    get_simulated_check_input_coverage() -> str:
        Returns a simulated input coverage status.
    get_check_input_coverage() -> str:
        Retrieves and returns the evaluation state of the input coverage check from a JSON file.
    """

    def __init__(self, model):
        """
        Initializes the CheckInputCoverageView with the given model.

        Parameters:
        model (CheckInputCoverageModel): An instance of the input coverage model.
        """
        self.__check_input_coverage_model: CheckInputCoverageModel = model

    def plot_check_input_coverage_view(self):
        """
        Plots the input coverage using plotly based on the prepared session data.
        """
        pandas_dataset: pd.DataFrame = self.__check_input_coverage_model.get_prepared_session_df()

        # Rename attributes for better readability on the plot
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

        # For each row in the dataset, create a scatter plot
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
    def get_simulated_check_input_coverage() -> str:
        """
        Returns a simulated input coverage status.

        Returns:
        str: "no" if the simulated value is less than 0.1, otherwise "ok".
        """
        value = random.random()
        if value < 0.1:
            return "no"
        else:
            return "ok"

    @staticmethod
    def get_check_input_coverage() -> str:
        """
        Retrieves and returns the evaluation state of the input coverage check from a JSON file.

        Returns:
        str: The evaluation state of the input coverage check.
        """
        with open(f'{os.path.dirname(__file__)}/Data/checkInputCoverageReport.json', 'r') as check_input_coverage_file:
            json_data = json.load(check_input_coverage_file)
            evaluation_check_input_coverage = json_data.get("evaluation")
            return evaluation_check_input_coverage
