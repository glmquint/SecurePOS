import json
import random
import plotly.graph_objects as go
# from plotly import graph_objs as go
import pandas as pd
import numpy as np
from random import random
from PreparedSession import *


class CheckInputCoverageView:

    def plotCheckinputCoverageView(self, PreparedSessionList):

        labels = ['MeanAbsoluteDifferencingTransactionTimestamps',
                  'MeanAbsoluteDifferencingTransactionAmount',
                  'MedianLongitude',
                  'MedianLatitude',
                  'MedianTargetIP',
                  'MedianDestIP']

        data = []
        for i in PreparedSessionList:
            row = [i.MeanAbsoluteDifferencingTransactionTimestamps, i.MeanAbsoluteDifferencingTransactionAmount,
                   i.MedianLongitude, i.MedianLatitude, i.MedianTargetIP, i.MedianDestIP]
            data.append(row)

        # Create a pandas DataFrame with the generated data and labels
        dataset = pd.DataFrame(data, columns=labels)

        # numeric_columns = dataset.columns[1:-1]
        numeric_columns = dataset.columns[0::]
        numeric_values_dataset = dataset[numeric_columns].values
        # print(numeric_values_dataset)

        pandas_dataset = pd.DataFrame(data=numeric_values_dataset, columns=labels)

        fig = go.Figure()

        for i in range(3):
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

        fig.write_image("Data/PlotCheckInputCoverage.png")

    def getSimulatedCheckInputCoverage(self):
        value = random()
        if value < 0.2:
            return "no"
        else:
            return "ok"

    def getCheckInputCoverage(self):
        with open('Data/checkInputCoverageReport.json', 'r') as checkInputCoverageFile:
            jsonData = json.load(checkInputCoverageFile)
            evaluationCheckInputCoverage = jsonData.get("evaluation")
            checkInputCoverageFile.close()
            return evaluationCheckInputCoverage


def test():
    c = CheckInputCoverageView()
    p1 = []
    for i in range(0, 20):
        p1.append(PreparedSession([random(), random(), random(), random(), random(), random(), "High"]))

    p2 = []
    for i in range(0, 15):
        p2.append(PreparedSession([random(), random(), random(), random(), random(), random(), "High"]))

    p3 = []
    for i in range(0, 18):
        p3.append(PreparedSession([random(), random(), random(), random(), random(), random(), "High"]))

    c.plotCheckinputCoverageView(p1 + p2 + p3)

