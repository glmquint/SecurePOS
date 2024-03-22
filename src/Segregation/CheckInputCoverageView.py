import json
import random
import plotly.graph_objects as go
import pandas as pd
from random import random

from src.DataObjects.Session import PreparedSession
from src.Segregation.CheckInputCoverageModel import CheckInputCoverageModel


class CheckInputCoverageView:

    def __init__(self, model):
        self.__checkInputCoverageModel : CheckInputCoverageModel = model

    def plot_check_input_coverage_view(self):

        pandas_dataset : pd.DataFrame = self.__checkInputCoverageModel.get_prepared_session_df()

        # we rename attributes for better readability on the plot
        labels = ['MeanAbsoluteDifferencingTransactionTimestamps',
                  'MeanAbsoluteDifferencingTransactionAmount',
                  'MedianLongitude',
                  'MedianLatitude',
                  'MedianTargetIP',
                  'MedianDestIP']
        assert len(labels) == len(pandas_dataset.columns), f"cannot rename different number of columns: {len(labels)} instead of {len(pandas_dataset.columns)}"
        pandas_dataset.columns = labels

        # FIXME: cleanup
        '''
        data = []
        for i in PreparedSessionList:
            row = [i.getMeanAbsoluteDifferencingTransactionTimestamps(), i.getMeanAbsoluteDifferencingTransactionAmount(),
                   i.getMedianLongitude(), i.getMedianLatitude(), i.getMedianTargetIP(), i.getMedianDestIP()]
            data.append(row)

        # Create a pandas DataFrame with the generated data and labels
        dataset = pd.DataFrame(data, columns=labels)


        dataset = pd.DataFrame([ps.to_json() for ps in preparedSessionPd], columns=preparedSessionPd[0].to_json().keys())
        dataset.drop(['label'], axis=1, inplace=True)

        numeric_columns = dataset.columns[0::]
        numeric_values_dataset = dataset[numeric_columns].values

        pandas_dataset = pd.DataFrame(data=numeric_values_dataset, columns=labels)
        '''

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

        fig.write_image("Data/Plot/PlotCheckInputCoverage.png")

    @staticmethod
    def get_simulated_check_input_coverage():
        value = random()
        if value < 0.1:
            return "no"
        else:
            return "ok"

    @staticmethod
    def get_check_input_coverage():
        with open('Data/checkInputCoverageReport.json', 'r') as checkInputCoverageFile:
            jsonData = json.load(checkInputCoverageFile)
            evaluationCheckInputCoverage = jsonData.get("evaluation")
            checkInputCoverageFile.close()
            return evaluationCheckInputCoverage


