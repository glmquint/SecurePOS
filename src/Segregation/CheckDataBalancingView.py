import json
import math
from random import random
import matplotlib.pyplot as plt
import numpy as np
from PreparedSession import *


class CheckDataBalanceView:
    __toleranceParameter = 0

    def __init__(self, toleraceParameter, model):
        self.__toleranceParameter = toleraceParameter
        self.__checkDataBalanceModel = model

    def plotCheckDataBalance(self):

        PreparedSessionList = self.__checkDataBalanceModel.getPreparedSessionList()

        labels = ['Low', 'Medium', 'High']

        values = [0, 0, 0]

        for i in PreparedSessionList:
            match i.getLabel():
                case "low":
                    values[0] += 1
                case "medium":
                    values[1] += 1
                case "high":
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

        string = 'Tolerance interal = ' + str(self.__toleranceParameter) + " | Difference detected = " + str(
            round(percentage_diff, 2))

        plt.bar(bar_positions2, values, width=bar_width)

        plt.axhline(y=maximim, linewidth=1, color='k')
        plt.axhline(y=minimum, linewidth=1, color='k')

        # Add title and labels
        plt.title('Data Balance')
        plt.xlabel('Labels')
        plt.ylabel('Values')

        # Set x-axis tick positions and labels
        plt.xticks([pos + bar_width for pos in bar_positions1], labels)

        plt.text(0.5, 1.10, string,
                 horizontalalignment='center', transform=plt.gca().transAxes)

        plt.savefig('Data/Plot/PlotCheckDataBalancePlot.png')

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
