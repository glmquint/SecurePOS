from src.Segregation.CheckDataBalancingModel import CheckDataBalancingModel
from src.DataObjects.Session import PreparedSession

import json
import os
from random import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')




class CheckDataBalanceView:
    """
        View class responsible for visualizing data balance checks.

        Attributes:
        __tolerance_parameter (float): The tolerance parameter used for data balancing.
        __check_data_balance_model (CheckDataBalancingModel): An instance of the data balancing
                                                            model.

        Methods:
        plot_check_data_balance():
            Plots the data balance using matplotlib based on the prepared session data.
        get_simulated_check_data_balance() -> str:
            Returns a simulated data balance status.
        get_check_data_balance() -> str:
            Retrieves and returns the evaluation state of the data balance check from a JSON file.
    """
    __tolerance_parameter = 0

    def __init__(self, tolerace_parameter, model: CheckDataBalancingModel):
        self.__tolerance_parameter = tolerace_parameter
        self.__check_data_balance_model: CheckDataBalancingModel = model

    def plot_check_data_balance(self):
        """
        Plots the data balance using matplotlib based on the prepared session data.
        """
        # retrive data from the model
        prepared_session_list: [
            PreparedSession] = self.__check_data_balance_model.get_prepared_session_list()

        labels = ["normal", "moderate", "high"]

        # count each label occurrence
        count_labels = dict(zip(labels, [0] * len(labels)))
        for prepared_session in prepared_session_list:
            if prepared_session.get_label() in count_labels:
                count_labels[prepared_session.get_label()] += 1

        # Set the width of the bars
        bar_width = 0.6

        # Set the positions of the bars on the x-axis
        bar_positions1 = np.arange(len(labels))
        bar_positions2 = [pos + bar_width for pos in bar_positions1]

        # normalize occurrences
        maximum = max(count_labels.values())
        minimum = min(count_labels.values())
        if maximum == 0:
            raise ValueError(
                "Maximum value is 0 in the count_labels dictionary")
        percentage_diff = (abs(maximum - minimum) /
                           (maximum + minimum) / 2) * 100

        string = ('Tolerance interal = ' + str(self.__tolerance_parameter)
                  + " | Difference detected = "
                  + str(round(percentage_diff, 2)))

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

        plt.savefig(
            f'{os.path.dirname(__file__)}/Data/Plot/PlotCheckDataBalancePlot.png')
        plt.close()

    @staticmethod
    def get_simulated_check_data_balance():
        value = random()
        if value < 0.1:
            return "no"
        return "ok"

    @staticmethod
    def get_check_data_balance():
        with (open(f'{os.path.dirname(__file__)}/Data/checkDataBalanceReport.json', 'r')
              as check_data_balance_file):
            json_data = json.load(check_data_balance_file)
            evaluation_check_data_balance = json_data.get("evaluation")
            check_data_balance_file.close()
            return evaluation_check_data_balance
