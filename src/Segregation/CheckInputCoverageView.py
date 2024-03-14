import json
import random
import plotly.graph_objects as go
import pandas as pd
from random import random
from PreparedSession import *


class CheckInputCoverageView:

    def __init__(self, model):
        self.__checkInputCoverageModel = model

    def plotCheckInputCoverageView(self):

        PreparedSessionList = self.__checkInputCoverageModel.getPreparedSessionList()

        labels = ['MeanAbsoluteDifferencingTransactionTimestamps',
                  'MeanAbsoluteDifferencingTransactionAmount',
                  'MedianLongitude',
                  'MedianLatitude',
                  'MedianTargetIP',
                  'MedianDestIP']

        data = []
        for i in PreparedSessionList:
            row = [i.getMeanAbsoluteDifferencingTransactionTimestamps(), i.getMeanAbsoluteDifferencingTransactionAmount(),
                   i.getMedianLongitude(), i.getMedianLatitude(), i.getMedianTargetIP(), i.getMedianDestIP()]
            data.append(row)

        # Create a pandas DataFrame with the generated data and labels
        dataset = pd.DataFrame(data, columns=labels)

        # numeric_columns = dataset.columns[1:-1]
        numeric_columns = dataset.columns[0::]
        numeric_values_dataset = dataset[numeric_columns].values
        # print(numeric_values_dataset)

        pandas_dataset = pd.DataFrame(data=numeric_values_dataset, columns=labels)

        fig = go.Figure()

        for i in range(len(data)):
            fig.add_trace(
                go.Scatterpolar(
                    r=pandas_dataset.loc[i].values.tolist(),
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

    def getSimulatedCheckInputCoverage(self):
        value = random()
        if value < 0.1:
            return "no"
        else:
            return "ok"

    def getCheckInputCoverage(self):
        with open('Data/checkInputCoverageReport.json', 'r') as checkInputCoverageFile:
            jsonData = json.load(checkInputCoverageFile)
            evaluationCheckInputCoverage = jsonData.get("evaluation")
            checkInputCoverageFile.close()
            return evaluationCheckInputCoverage


