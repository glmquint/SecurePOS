import json
import math
from random import random
import matplotlib.pyplot as plt
import numpy as np
from PreparedSession import *


class CheckDataBalanceView:
    toleraceParameter = 0

    def __init__(self, toleraceParameter):
        self.toleraceParameter = toleraceParameter

    def plotCheckDataBalance(self, PreparedSessionList):

        labels = ['Low', 'Medium', 'High']

        values = [0, 0, 0]

        for i in PreparedSessionList:
            match i.label:
                case "Low":
                    values[0] += 1
                case "Medium":
                    values[1] += 1
                case "High":
                    values[2] += 1
                case _:
                    continue

        # Set the width of the bars
        bar_width = 0.6

        # Set the positions of the bars on the x-axis
        bar_positions1 = np.arange(len(labels))
        bar_positions2 = [pos + bar_width for pos in bar_positions1]

        maximim = max(values)
        minimum = min(values)

        percentage_diff = (abs(maximim - minimum) / (maximim + minimum) / 2) * 100

        string = 'Tolerance interal = '+str(self.toleraceParameter)+" | Difference detected = " + str(round(percentage_diff,2))
        plt.text(1.5, 23.5, string,
                 horizontalalignment='center',
                 verticalalignment='top')

        plt.bar(bar_positions2, values, width=bar_width)

        plt.axhline(y=maximim, linewidth=1, color='k')
        plt.axhline(y=minimum, linewidth=1, color='k')

        # Add title and labels
        plt.title('Data Balance')
        plt.xlabel('Labels')
        plt.ylabel('Values')

        # Set x-axis tick positions and labels
        plt.xticks([pos + bar_width for pos in bar_positions1], labels)

        # plt.savefig('Data/PlotCheckDataBalancePlot.png')
        plt.show()

    def getSimulatedCheckDataBalance(self):
        value = random()
        if value < 0.1:
            return "no"
        else:
            return "ok"

    def getCheckDataBalance(self):
        with open('Data/checkDataBalanceReport.json', 'r') as checkDataBalanceFile:
            jsonData = json.load(checkDataBalanceFile)
            evaluationCheckDataBalance = jsonData.get("evaluation")
            checkDataBalanceFile.close()
            return evaluationCheckDataBalance


def test():
    c = CheckDataBalanceView(5)
    p1 = []
    for i in range(0, 20):
        p1.append(PreparedSession([0, 0, 0, 0, 0, 0, "High"]))

    p2 = []
    for i in range(0, 15):
        p2.append(PreparedSession([0, 0, 0, 0, 0, 0, "Medium"]))

    p3 = []
    for i in range(0, 18):
        p3.append(PreparedSession([0, 0, 0, 0, 0, 0, "Low"]))

    c.plotCheckDataBalance(p1 + p2 + p3)


test()
