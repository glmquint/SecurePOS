import json
from random import random
import matplotlib.pyplot as plt
import numpy as np

from src.DataObjects.Session import PreparedSession
from src.Segregation.CheckDataBalancingModel import CheckDataBalancingModel


class CheckDataBalanceView:
    __tolerance_parameter = 0

    def __init__(self, toleraceParameter, model : CheckDataBalancingModel):
        self.__tolerance_parameter = toleraceParameter
        self.__check_data_balance_model : CheckDataBalancingModel = model

    def plot_check_data_balance(self):

        # retrive data from the model
        preparedSessionList : [PreparedSession] = self.__check_data_balance_model.get_prepared_session_list()

        labels = ["normal", "moderate", "high"]

        # count each label occurrence
        count_labels = dict(zip(labels, [0]*len(labels)))
        for prepared_session in preparedSessionList:
            if prepared_session.getLabel() in count_labels:
                count_labels[prepared_session.getLabel()] += 1

        # Set the width of the bars
        bar_width = 0.6

        # Set the positions of the bars on the x-axis
        bar_positions1 = np.arange(len(labels))
        bar_positions2 = [pos + bar_width for pos in bar_positions1]

        # normalize occurrences
        maximum = max(count_labels.values())
        minimum = min(count_labels.values())
        if maximum == 0:
            raise ValueError("Maximum value is 0 in the count_labels dictionary")
        percentage_diff = (abs(maximum - minimum) / (maximum + minimum) / 2) * 100

        string = 'Tolerance interal = ' + str(self.__tolerance_parameter) + " | Difference detected = " + str(
            round(percentage_diff, 2))

        plt.bar(bar_positions2, list(count_labels.values()), width=bar_width)

        plt.axhline(y=maximum, linewidth=1, color='k')
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

    @staticmethod
    def get_simulated_check_data_balance():
        value = random()
        if value < 0.1:
            return "no"
        else:
            return "ok"

    @staticmethod
    def get_check_data_balance():
        with open('Data/checkDataBalanceReport.json', 'r') as checkDataBalanceFile:
            jsonData = json.load(checkDataBalanceFile)
            evaluationCheckDataBalance = jsonData.get("evaluation")
            checkDataBalanceFile.close()
            return evaluationCheckDataBalance
